#!/usr/bin/env python3
"""resolve_oa — turn DOIs into legally downloadable full text.

A search gives you metadata; a citation-backed answer needs the actual paper.
This walks an escalating chain of open-access resolvers per DOI and stops at
the first one that yields a file:

  1. Unpaywall        best OA location   (needs an email — free, no key)
  2. OpenAlex         best_oa_location / oa_url        (keyless)
  3. Europe PMC       OA full-text XML → plain text    (keyless, biomed)
  4. arXiv            preprint PDF when the record has an arXiv id
  5. CORE             OA aggregator      (only if CORE_API_KEY is set)

Standard library only. Nothing here bypasses a paywall: a DOI nothing can open is
reported as `closed` and skipped — or as `not-in-crossref` when Crossref has never
heard of it, which means either an invented citation or a DOI registered elsewhere
(DataCite datasets, some preprint servers). Either way, do not cite it unchecked.

Input is DOIs on the command line, a text file of DOIs, or the results.json /
manifest.json that fetch_papers.py wrote.

Usage:
  resolve_oa.py --from-json ./papers/results.json --outdir ./papers --email you@example.com
  resolve_oa.py --doi 10.7717/peerj.4375 --doi 10.1038/nature12373 --outdir ./papers
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

UA = "litrun-resolve-oa/1.0 (+https://github.com/brycewang-stanford/lit-review-agent-tools)"


def _get(url, params=None, timeout=60, retries=1):
    if params:
        url = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < retries:
                time.sleep(3)
                continue
            raise RuntimeError(f"HTTP {e.code}") from e
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
                continue
            raise RuntimeError(f"{type(e).__name__}: {e}") from e


def _get_json(url, params=None, timeout=60):
    return json.loads(_get(url, params, timeout).decode("utf-8", "replace"))


def norm_doi(doi):
    doi = (doi or "").strip().lower()
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", doi).rstrip(".")


def safe_name(s, maxlen=90):
    return (re.sub(r"[^\w\-]+", "_", s or "").strip("_")[:maxlen]) or "paper"


def is_pdf(blob):
    return blob[:5] == b"%PDF-"


def jats_to_text(xml_bytes):
    """Flatten PMC's JATS XML into title + abstract + body, dropping the
    bibliographic front matter that makes a naive itertext() dump unreadable."""
    root = ET.fromstring(xml_bytes)
    chunks = []
    title = root.find(".//article-title")
    if title is not None:
        chunks.append("".join(title.itertext()).strip())
    for tag in ("abstract", "body"):
        for el in root.findall(f".//{tag}"):
            chunks.append(" ".join("".join(el.itertext()).split()))
    return "\n\n".join(c for c in chunks if c)


# ------------------------------------------------------------------ resolvers
# Each returns (kind, bytes_or_text, source_url) or None.


def via_unpaywall(doi, email):
    if not email:
        return None
    d = _get_json(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}", {"email": email})
    if not d.get("is_oa"):
        return None
    loc = d.get("best_oa_location") or {}
    url = loc.get("url_for_pdf") or loc.get("url")
    if not url:
        return None
    blob = _get(url, timeout=90)
    return ("pdf", blob, url) if is_pdf(blob) else None


def via_openalex(doi):
    w = _get_json(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}")
    loc = w.get("best_oa_location") or {}
    url = loc.get("pdf_url") or (w.get("open_access") or {}).get("oa_url")
    ids = w.get("ids") or {}
    if not url:
        # An arXiv landing page in `ids` is still a downloadable preprint.
        return ("arxiv-id", ids.get("arxiv") or "", "") if ids.get("arxiv") else None
    blob = _get(url, timeout=90)
    return ("pdf", blob, url) if is_pdf(blob) else None


def via_europepmc(doi):
    params = {"query": f'DOI:"{doi}"', "format": "json", "pageSize": 1, "resultType": "core"}
    res = _get_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params)
    hits = res.get("resultList", {}).get("result", [])
    if not hits:
        return None
    h = hits[0]
    pmcid = h.get("pmcid")
    if pmcid and h.get("isOpenAccess") == "Y":
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
        try:
            text = jats_to_text(_get(url, timeout=90))
            if len(text) > 2000:  # a stub isn't full text
                return ("txt", text.encode("utf-8"), url)
        except Exception:
            pass
    for u in ((h.get("fullTextUrlList") or {}).get("fullTextUrl") or []):
        if u.get("documentStyle") == "pdf" and u.get("availabilityCode") in ("OA", "F"):
            try:
                blob = _get(u["url"], timeout=90)
                if is_pdf(blob):
                    return ("pdf", blob, u["url"])
            except Exception:
                continue
    return None


def via_arxiv(arxiv_id):
    aid = (arxiv_id or "").rsplit("/", 1)[-1]
    if not aid:
        return None
    url = f"https://arxiv.org/pdf/{aid}"
    blob = _get(url, timeout=90)
    return ("pdf", blob, url) if is_pdf(blob) else None


def doi_registered(doi):
    """Does this DOI exist at all? Asked only when nothing resolved, so that a
    fabricated citation is reported as `not-in-crossref` rather than as `closed` —
    'behind a paywall' and 'no such record' are very different answers."""
    try:
        _get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}", timeout=30, retries=0)
        return True
    except RuntimeError as e:
        return False if "HTTP 404" in str(e) else None  # None = could not tell


def via_core(doi, key):
    if not key:
        return None
    body = json.dumps({"q": f'doi:"{doi}"', "limit": 1}).encode()
    req = urllib.request.Request(
        "https://api.core.ac.uk/v3/search/works",
        data=body,
        headers={"User-Agent": UA, "Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.loads(r.read().decode("utf-8", "replace"))
    for w in res.get("results", []):
        url = w.get("downloadUrl")
        if url:
            try:
                blob = _get(url, timeout=90)
                if is_pdf(blob):
                    return ("pdf", blob, url)
            except Exception:
                continue
    return None


# ------------------------------------------------------------------ input


def load_targets(args):
    """→ [{doi, title, arxiv_id, pdf_url}] from whichever input was given."""
    targets = []
    for d in args.doi or []:
        targets.append({"doi": norm_doi(d), "title": "", "arxiv_id": "", "pdf_url": ""})
    if args.from_json:
        data = json.loads(Path(args.from_json).read_text())
        rows = data.get("results", data) if isinstance(data, dict) else data
        for r in rows:
            if not isinstance(r, dict):
                continue
            aid = r.get("id", "") if r.get("source") == "arxiv" else ""
            targets.append({"doi": norm_doi(r.get("doi")), "title": r.get("title", ""),
                            "arxiv_id": aid, "pdf_url": r.get("pdf_url", "")})
    if args.from_file:
        for line in Path(args.from_file).read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                targets.append({"doi": norm_doi(line), "title": "", "arxiv_id": "", "pdf_url": ""})
    # Keep records that carry *some* handle, deduplicated.
    seen, out = set(), []
    for t in targets:
        k = t["doi"] or t["arxiv_id"] or t["pdf_url"]
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(t)
    return out


def main():
    p = argparse.ArgumentParser(prog="resolve_oa.py", description=__doc__.split("\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--doi", action="append", help="a DOI (repeatable)")
    p.add_argument("--from-json", dest="from_json", help="results.json/manifest.json from fetch_papers.py")
    p.add_argument("--from-file", dest="from_file", help="text file, one DOI per line")
    p.add_argument("--outdir", required=True)
    p.add_argument("--email", default=os.environ.get("UNPAYWALL_EMAIL") or os.environ.get("NCBI_EMAIL", ""),
                   help="contact email — required by Unpaywall (else that step is skipped)")
    p.add_argument("--max", type=int, default=0, help="stop after N DOIs (0 = all)")
    p.add_argument("--skip-existing", action="store_true", help="don't re-download files already in --outdir")
    args = p.parse_args()

    if not (args.doi or args.from_json or args.from_file):
        sys.exit("resolve_oa: give --doi, --from-json or --from-file.")

    targets = load_targets(args)
    if args.max:
        targets = targets[:args.max]
    if not targets:
        sys.exit("resolve_oa: no usable DOIs in the input.")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    core_key = os.environ.get("CORE_API_KEY", "")
    if not args.email:
        print("resolve_oa: no --email/UNPAYWALL_EMAIL — skipping Unpaywall, "
              "the rest of the chain still runs keyless.", file=sys.stderr)

    report, counts = [], {"pdf": 0, "txt": 0, "closed": 0, "not-in-crossref": 0, "error": 0, "skipped": 0}
    for i, t in enumerate(targets, 1):
        doi, label = t["doi"], (t["title"] or t["doi"] or t["arxiv_id"])[:60]
        stem = safe_name(doi.replace("/", "_") or t["arxiv_id"])
        print(f"[{i}/{len(targets)}] {label}", file=sys.stderr)

        existing = list(outdir.glob(f"{stem}.*"))
        if args.skip_existing and existing:
            counts["skipped"] += 1
            report.append({"doi": doi, "status": "skipped", "file": existing[0].name})
            print("   · already present", file=sys.stderr)
            continue

        chain = []
        if doi:
            chain += [("unpaywall", lambda: via_unpaywall(doi, args.email)),
                      ("openalex", lambda: via_openalex(doi)),
                      ("europepmc", lambda: via_europepmc(doi))]
        if t["arxiv_id"]:
            chain.append(("arxiv", lambda: via_arxiv(t["arxiv_id"])))
        if t["pdf_url"]:
            chain.append(("search-hit", lambda: (lambda b: ("pdf", b, t["pdf_url"]) if is_pdf(b) else None)(
                _get(t["pdf_url"], timeout=90))))
        if doi and core_key:
            chain.append(("core", lambda: via_core(doi, core_key)))

        got, errs = None, []
        for name, fn in chain:
            try:
                res = fn()
            except Exception as e:
                errs.append(f"{name}: {e}")
                continue
            if res is None:
                continue
            kind, payload, url = res
            if kind == "arxiv-id":  # OpenAlex handed us a preprint id instead of a file
                try:
                    res2 = via_arxiv(payload)
                except Exception as e:
                    errs.append(f"arxiv: {e}")
                    continue
                if not res2:
                    continue
                kind, payload, url = res2
                name = "openalex→arxiv"
            got = (name, kind, payload, url)
            break

        if not got:
            if not doi:
                status = "error"
            else:
                status = "closed" if doi_registered(doi) is not False else "not-in-crossref"
            counts[status] += 1
            report.append({"doi": doi, "title": t["title"], "status": status, "tried": errs})
            why = "DOI is not registered with Crossref" if status == "not-in-crossref" else "no open copy found"
            print(f"   ✗ {why}{' (' + '; '.join(errs[:2]) + ')' if errs else ''}", file=sys.stderr)
            continue

        name, kind, payload, url = got
        dest = outdir / f"{stem}.{'pdf' if kind == 'pdf' else 'txt'}"
        dest.write_bytes(payload)
        counts[kind] += 1
        report.append({"doi": doi, "title": t["title"], "status": kind, "via": name,
                       "url": url, "file": dest.name, "bytes": len(payload)})
        print(f"   ✓ {kind} via {name}  ({len(payload)//1024} KB)", file=sys.stderr)
        time.sleep(0.3)

    out = {"resolved": counts, "total": len(targets), "items": report}
    (outdir / "oa_report.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    hit = counts["pdf"] + counts["txt"]
    print(f"\nresolve_oa: {hit}/{len(targets)} open ({counts['pdf']} PDF, {counts['txt']} full-text XML→txt), "
          f"{counts['closed']} closed, {counts['not-in-crossref']} DOI(s) unknown to Crossref, "
          f"{counts['error']} errored, {counts['skipped']} skipped", file=sys.stderr)
    print(f"  files + oa_report.json in {outdir}", file=sys.stderr)
    if hit == 0:
        sys.exit("resolve_oa: nothing was openly available — the corpus is unchanged.")


if __name__ == "__main__":
    main()
