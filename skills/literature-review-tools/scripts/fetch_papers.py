#!/usr/bin/env python3
"""fetch_papers — one keyless search across six scholarly APIs, deduplicated.

Queries any combination of OpenAlex, Crossref, Semantic Scholar, PubMed,
Europe PMC and arXiv, merges the hits into one normalised record list
(deduplicated by DOI, then by normalised title), and writes:

  <outdir>/results.json   normalised records + per-source errors
  <outdir>/<key>.txt      title + abstract per record   (--save abstracts, default)
  <outdir>/manifest.json  appended, same shape the other bundled fetchers write

Standard library only — no pip install, no API key. Keys are used if present
(S2_API_KEY, NCBI_API_KEY, OPENALEX_API_KEY/OPENALEX_MAILTO, CROSSREF_MAILTO)
and simply raise rate limits.

Usage:
  fetch_papers.py --query "retrieval augmented generation" --max 20 --outdir ./papers
  fetch_papers.py --query "CRISPR off-target" --sources pubmed,europepmc --from-year 2022 \
                  --outdir ./papers --pdfs
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

UA = "litrun-fetch-papers/1.0 (+https://github.com/brycewang-stanford/lit-review-agent-tools)"
SOURCES = ["openalex", "crossref", "semanticscholar", "pubmed", "europepmc", "arxiv"]


# ------------------------------------------------------------------ http


def _get(url, params=None, headers=None, timeout=60, retries=1):
    """GET a URL, returning raw bytes. Retries once on 429/5xx."""
    if params:
        url = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"
    hdrs = {"User-Agent": UA, "Accept": "*/*"}
    hdrs.update(headers or {})
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(3)
                continue
            raise RuntimeError(f"HTTP {e.code} for {url.split('?')[0]}") from e
        except Exception as e:  # timeouts, DNS, TLS
            if attempt < retries:
                time.sleep(2)
                continue
            raise RuntimeError(f"{type(e).__name__}: {e}") from e


def _get_json(url, params=None, headers=None, timeout=60):
    return json.loads(_get(url, params, headers, timeout).decode("utf-8", "replace"))


# ------------------------------------------------------------------ shaping


def norm_doi(doi):
    if not doi:
        return ""
    doi = doi.strip().lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    return doi.rstrip(".")


def norm_title(title):
    return re.sub(r"[^a-z0-9]+", "", (title or "").lower())[:120]


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def record(source, **kw):
    """Every source funnels into this one shape."""
    r = {
        "source": source, "sources": [source], "id": "", "doi": "", "title": "",
        "abstract": "", "year": None, "authors": [], "venue": "", "cited_by": None,
        "is_oa": None, "pdf_url": "", "url": "",
    }
    r.update({k: v for k, v in kw.items() if v not in (None, "", [])})
    r["doi"] = norm_doi(r["doi"])
    return r


# ------------------------------------------------------------------ sources


def s_openalex(query, limit, from_year):
    params = {"search": query, "per_page": min(limit, 200)}
    filters = []
    if from_year:
        filters.append(f"from_publication_date:{from_year}-01-01")
    if filters:
        params["filter"] = ",".join(filters)
    if os.environ.get("OPENALEX_API_KEY"):
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    elif os.environ.get("OPENALEX_MAILTO"):
        params["mailto"] = os.environ["OPENALEX_MAILTO"]
    data = _get_json("https://api.openalex.org/works", params)
    out = []
    for w in data.get("results", [])[:limit]:
        loc = w.get("best_oa_location") or w.get("primary_location") or {}
        out.append(record(
            "openalex",
            id=(w.get("id") or "").rsplit("/", 1)[-1],
            doi=w.get("doi") or "",
            title=w.get("display_name") or "",
            abstract=_inverted(w.get("abstract_inverted_index")),
            year=w.get("publication_year"),
            authors=[a.get("author", {}).get("display_name") for a in w.get("authorships", [])[:20]],
            venue=((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
            cited_by=w.get("cited_by_count"),
            is_oa=(w.get("open_access") or {}).get("is_oa"),
            pdf_url=loc.get("pdf_url") or "",
            url=w.get("id") or "",
        ))
    return out


def _inverted(inv):
    """OpenAlex ships abstracts as {word: [positions]}."""
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def s_crossref(query, limit, from_year):
    params = {"query.bibliographic": query, "rows": min(limit, 100)}
    if from_year:
        params["filter"] = f"from-pub-date:{from_year}-01-01"
    mail = os.environ.get("CROSSREF_MAILTO") or os.environ.get("UNPAYWALL_EMAIL")
    if mail:
        params["mailto"] = mail  # polite pool: double the rate limit
    data = _get_json("https://api.crossref.org/works", params)
    out = []
    for w in data.get("message", {}).get("items", [])[:limit]:
        parts = (w.get("issued") or {}).get("date-parts") or [[None]]
        pdf = ""
        for link in w.get("link") or []:
            if link.get("content-type") == "application/pdf":
                pdf = link.get("URL", "")
                break
        out.append(record(
            "crossref",
            id=w.get("DOI", ""),
            doi=w.get("DOI", ""),
            title=(w.get("title") or [""])[0],
            abstract=strip_tags(w.get("abstract")),
            year=parts[0][0] if parts and parts[0] else None,
            authors=[" ".join(filter(None, [a.get("given"), a.get("family")]))
                     for a in (w.get("author") or [])[:20]],
            venue=(w.get("container-title") or [""])[0],
            cited_by=w.get("is-referenced-by-count"),
            pdf_url=pdf,
            url=w.get("URL", ""),
        ))
    return out


def s_semanticscholar(query, limit, from_year):
    fields = "title,abstract,year,authors,venue,citationCount,externalIds,openAccessPdf,url,isOpenAccess"
    params = {"query": query, "limit": min(limit, 100), "fields": fields}
    if from_year:
        params["year"] = f"{from_year}-"
    headers = {}
    if os.environ.get("S2_API_KEY"):
        headers["x-api-key"] = os.environ["S2_API_KEY"]
    data = _get_json("https://api.semanticscholar.org/graph/v1/paper/search", params, headers)
    out = []
    for w in data.get("data", [])[:limit]:
        ext = w.get("externalIds") or {}
        out.append(record(
            "semanticscholar",
            id=w.get("paperId", ""),
            doi=ext.get("DOI", ""),
            title=w.get("title") or "",
            abstract=w.get("abstract") or "",
            year=w.get("year"),
            authors=[a.get("name") for a in (w.get("authors") or [])[:20]],
            venue=w.get("venue") or "",
            cited_by=w.get("citationCount"),
            is_oa=w.get("isOpenAccess"),
            pdf_url=(w.get("openAccessPdf") or {}).get("url", ""),
            url=w.get("url") or "",
        ))
    return out


def s_pubmed(query, limit, from_year):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    common = {}
    if os.environ.get("NCBI_API_KEY"):
        common["api_key"] = os.environ["NCBI_API_KEY"]
    if os.environ.get("NCBI_EMAIL"):
        common["email"] = os.environ["NCBI_EMAIL"]
    params = dict(common, db="pubmed", term=query, retmax=min(limit, 100), retmode="json", sort="relevance")
    if from_year:
        params["mindate"], params["maxdate"], params["datetype"] = f"{from_year}", "3000", "pdat"
    ids = _get_json(f"{base}/esearch.fcgi", params).get("esearchresult", {}).get("idlist", [])
    if not ids:
        return []
    time.sleep(0.34)  # NCBI: 3 req/s without a key
    xml = _get(f"{base}/efetch.fcgi", dict(common, db="pubmed", id=",".join(ids), retmode="xml"))
    root = ET.fromstring(xml)
    out = []
    for art in root.findall(".//PubmedArticle"):
        pmid = art.findtext(".//PMID") or ""
        # Scope the DOI hunt to the article's own id list. A PubmedArticle embeds
        # its whole reference list, each entry carrying its own <ArticleId
        # IdType="doi">, so a `.//ArticleId` sweep silently returns a *cited*
        # paper's DOI — see recipes/06 for the record this corrupted.
        doi = ""
        for aid in art.findall("./PubmedData/ArticleIdList/ArticleId"):
            if aid.get("IdType") == "doi":
                doi = aid.text or ""
                break
        if not doi:
            for el in art.findall(".//Article/ELocationID"):
                if el.get("EIdType") == "doi":
                    doi = el.text or ""
                    break
        abstract = " ".join(" ".join(t.itertext()) for t in art.findall(".//AbstractText")).strip()
        year = art.findtext(".//PubDate/Year") or art.findtext(".//PubDate/MedlineDate") or ""
        title_el = art.find(".//ArticleTitle")  # may carry inline <i>/<sub> markup
        out.append(record(
            "pubmed",
            id=pmid, doi=doi,
            title=re.sub(r"\s+", " ", "".join(title_el.itertext())).strip() if title_el is not None else "",
            abstract=abstract,
            year=int(year[:4]) if year[:4].isdigit() else None,
            authors=[" ".join(filter(None, [a.findtext("ForeName"), a.findtext("LastName")]))
                     for a in art.findall(".//Author")[:20]],
            venue=art.findtext(".//Journal/Title") or "",
            url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
        ))
    return out


def s_europepmc(query, limit, from_year):
    q = query
    if from_year:
        q = f"({query}) AND (FIRST_PDATE:[{from_year}-01-01 TO 3000-01-01])"
    params = {"query": q, "format": "json", "pageSize": min(limit, 100), "resultType": "core"}
    data = _get_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params)
    out = []
    for w in data.get("resultList", {}).get("result", [])[:limit]:
        pdf = ""
        for u in ((w.get("fullTextUrlList") or {}).get("fullTextUrl") or []):
            if u.get("documentStyle") == "pdf":
                pdf = u.get("url", "")
                break
        out.append(record(
            "europepmc",
            id=w.get("id", ""), doi=w.get("doi", ""),
            title=w.get("title") or "",
            abstract=strip_tags(w.get("abstractText")),
            year=int(w["pubYear"]) if str(w.get("pubYear", "")).isdigit() else None,
            authors=[a.get("fullName") for a in ((w.get("authorList") or {}).get("author") or [])[:20]],
            venue=(w.get("journalInfo") or {}).get("journal", {}).get("title") or w.get("bookOrReportDetails", {}).get("publisher", ""),
            cited_by=w.get("citedByCount"),
            is_oa=w.get("isOpenAccess") == "Y",
            pdf_url=pdf,
            url=f"https://europepmc.org/article/{w.get('source','MED')}/{w.get('id','')}",
        ))
    return out


def s_arxiv(query, limit, from_year):
    # arXiv has no server-side date filter on the legacy API; sort by relevance
    # and drop anything older than --from-year client-side.
    params = {"search_query": f"all:{query}", "start": 0,
              "max_results": min(limit * 2 if from_year else limit, 100),
              "sortBy": "relevance"}
    xml = _get("http://export.arxiv.org/api/query", params)
    ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    out = []
    for e in ET.fromstring(xml).findall("a:entry", ns):
        published = e.findtext("a:published", "", ns)
        year = int(published[:4]) if published[:4].isdigit() else None
        if from_year and year and year < int(from_year):
            continue
        aid = (e.findtext("a:id", "", ns) or "").rsplit("/", 1)[-1]
        out.append(record(
            "arxiv",
            id=aid,
            doi=e.findtext("arxiv:doi", "", ns),
            title=re.sub(r"\s+", " ", e.findtext("a:title", "", ns)).strip(),
            abstract=re.sub(r"\s+", " ", e.findtext("a:summary", "", ns)).strip(),
            year=year,
            authors=[a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)[:20]],
            venue=e.findtext("arxiv:journal_ref", "", ns) or "arXiv",
            is_oa=True,
            pdf_url=f"https://arxiv.org/pdf/{aid}" if aid else "",
            url=e.findtext("a:id", "", ns),
        ))
        if len(out) >= limit:
            break
    return out


FETCHERS = {
    "openalex": s_openalex, "crossref": s_crossref, "semanticscholar": s_semanticscholar,
    "pubmed": s_pubmed, "europepmc": s_europepmc, "arxiv": s_arxiv,
}


# ------------------------------------------------------------------ merge


def merge(records):
    """Deduplicate on DOI first, then on normalised title. First hit wins;
    later hits only fill in fields the winner left empty."""
    by_key, order = {}, []
    for r in records:
        key = r["doi"] or f"t:{norm_title(r['title'])}"
        if not key or key == "t:":
            continue
        if key not in by_key:
            by_key[key] = r
            order.append(key)
            continue
        cur = by_key[key]
        if r["source"] not in cur["sources"]:
            cur["sources"].append(r["source"])
        for f in ("doi", "abstract", "title", "venue", "pdf_url", "url"):
            if not cur.get(f) and r.get(f):
                cur[f] = r[f]
        for f in ("year", "cited_by", "is_oa"):
            if cur.get(f) in (None, "") and r.get(f) is not None:
                cur[f] = r[f]
        if len(r.get("authors") or []) > len(cur.get("authors") or []):
            cur["authors"] = r["authors"]
    return [by_key[k] for k in order]


def collapse_titles(records):
    """Second pass: fold records that share a title but carry different DOIs —
    i.e. a preprint and its published version. Keeps the one with the DOI that
    looks published (non-preprint prefix), else the first seen."""
    PREPRINT = ("10.48550", "10.1101", "10.21203", "10.31234", "10.31219", "10.26434")
    by_title, order = {}, []
    for r in records:
        k = norm_title(r["title"])
        if not k:
            order.append(id(r))
            by_title[id(r)] = r
            continue
        if k not in by_title:
            by_title[k] = r
            order.append(k)
            continue
        cur = by_title[k]

        def rank(rec):  # published DOI > preprint DOI > no DOI at all
            if not rec["doi"]:
                return 0
            return 1 if rec["doi"].startswith(PREPRINT) else 2

        keep, drop = cur, r
        if rank(r) > rank(cur):
            keep, drop = r, cur
            by_title[k] = r
        for s in drop["sources"]:
            if s not in keep["sources"]:
                keep["sources"].append(s)
        keep.setdefault("also_doi", [])
        if drop["doi"] and drop["doi"] != keep["doi"]:
            keep["also_doi"].append(drop["doi"])
        if not keep["abstract"] and drop["abstract"]:
            keep["abstract"] = drop["abstract"]
        if not keep["pdf_url"] and drop["pdf_url"]:
            keep["pdf_url"] = drop["pdf_url"]
    return [by_title[k] for k in order]


def safe_name(s, maxlen=70):
    return (re.sub(r"[^\w\- ]+", "", s or "").strip().replace(" ", "_")[:maxlen]) or "paper"


def key_for(r):
    return safe_name(f"{r['source']}_{(r['doi'] or r['id']).replace('/', '_')}_{r['title']}", 90)


def download(url, dest):
    data = _get(url, timeout=90)
    if not data:
        raise RuntimeError("empty response")
    dest.write_bytes(data)


def merge_manifest(outdir, entries):
    path = outdir / "manifest.json"
    existing = []
    if path.exists():
        try:
            existing = json.loads(path.read_text())
        except Exception:
            existing = []
    existing.extend(entries)
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(prog="fetch_papers.py", description=__doc__.split("\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--query", required=True)
    p.add_argument("--sources", default="openalex,crossref,semanticscholar",
                   help=f"comma-separated subset of: {', '.join(SOURCES)} (default: openalex,crossref,semanticscholar)")
    p.add_argument("--max", type=int, default=20, help="results per source before dedup")
    p.add_argument("--from-year", dest="from_year", help="drop anything published before this year")
    p.add_argument("--outdir", required=True)
    p.add_argument("--save", choices=["abstracts", "none"], default="abstracts",
                   help="write one .txt per record for PaperQA2/grep (default) or metadata only")
    p.add_argument("--pdfs", action="store_true", help="also download any PDF the search already exposed")
    p.add_argument("--open-access-only", action="store_true", dest="oa_only")
    p.add_argument("--dedup-titles", action="store_true", dest="dedup_titles",
                   help="also fold same-title records with different DOIs (preprint + published)")
    args = p.parse_args()

    picked = [s.strip() for s in args.sources.split(",") if s.strip()]
    unknown = [s for s in picked if s not in FETCHERS]
    if unknown:
        sys.exit(f"fetch_papers: unknown source(s): {', '.join(unknown)}. Known: {', '.join(SOURCES)}")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    raw, errors, per_source = [], {}, {}
    for s in picked:
        print(f"→ {s}: searching {args.query!r} (max {args.max})", file=sys.stderr)
        try:
            hits = FETCHERS[s](args.query, args.max, args.from_year)
            per_source[s] = len(hits)
            raw.extend(hits)
            print(f"  ✓ {s}: {len(hits)} hit(s)", file=sys.stderr)
        except Exception as e:
            errors[s] = str(e)
            per_source[s] = 0
            print(f"  ! {s} failed: {e} — continuing with the other sources", file=sys.stderr)
        time.sleep(0.5)

    merged = merge(raw)
    if args.dedup_titles:
        before = len(merged)
        merged = collapse_titles(merged)
        print(f"  · title pass folded {before - len(merged)} preprint/published pair(s)", file=sys.stderr)
    if args.oa_only:
        merged = [r for r in merged if r.get("is_oa") or r.get("pdf_url")]

    manifest = []
    for r in merged:
        r["key"] = key_for(r)
        fname = ""
        if args.pdfs and r.get("pdf_url"):
            try:
                dest = outdir / f"{r['key']}.pdf"
                download(r["pdf_url"], dest)
                fname, r["file_kind"] = dest.name, "pdf"
            except Exception as e:
                print(f"  ! PDF failed for {r['key'][:40]}: {e}", file=sys.stderr)
        if not fname and args.save == "abstracts":
            dest = outdir / f"{r['key']}.txt"
            body = [r["title"], ""]
            if r["authors"]:
                body.append(", ".join(a for a in r["authors"] if a))
            if r["venue"] or r["year"]:
                body.append(f"{r['venue']} ({r['year']})".strip())
            if r["doi"]:
                body.append(f"doi:{r['doi']}")
            body += ["", r["abstract"] or "(no abstract available from this source)"]
            dest.write_text("\n".join(body) + "\n", encoding="utf-8")
            fname, r["file_kind"] = dest.name, "txt"
        r["file"] = fname
        if fname:
            manifest.append({
                "title": r["title"], "year": r["year"], "authors": r["authors"],
                "doi": r["doi"], "file": fname, "kind": r.get("file_kind"),
                "url": r["url"], "sources": r["sources"],
            })

    if manifest:
        merge_manifest(outdir, manifest)
    results = {
        "query": args.query, "sources": picked, "from_year": args.from_year,
        "raw_hits": len(raw), "unique": len(merged), "per_source": per_source,
        "errors": errors, "results": merged,
    }
    (outdir / "results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    dupes = len(raw) - len(merged)
    multi = sum(1 for r in merged if len(r["sources"]) > 1)
    with_doi = sum(1 for r in merged if r["doi"])
    print(f"\nfetch_papers: {len(raw)} raw → {len(merged)} unique "
          f"({dupes} duplicate(s) merged, {multi} found by >1 source, {with_doi} with a DOI)", file=sys.stderr)
    print(f"  results.json + {len(manifest)} file(s) in {outdir}", file=sys.stderr)
    if errors:
        print(f"  failed source(s): {', '.join(errors)}", file=sys.stderr)
    if not merged:
        sys.exit("fetch_papers: no results — try fewer/other --sources or a broader query.")


if __name__ == "__main__":
    main()
