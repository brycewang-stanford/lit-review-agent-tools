#!/usr/bin/env python3
"""fetch_pubmed — search PubMed and save each article's title + abstract as text.

PubMed rarely exposes downloadable PDFs (full text lives behind publishers /
PMC), so this saves `<pmid>.txt` files (title + abstract) that PaperQA2 can
ingest, plus a merged manifest.json. Uses NCBI E-utilities (no key needed for
light use; set NCBI_API_KEY / --email to raise the rate limit).

Usage:
  fetch_pubmed.py --query "CRISPR off-target detection" --max 10 --outdir ./papers
"""
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("fetch_pubmed: 'requests' not installed. Run: litrun.py install pubmed-fetch")

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
_UA = {"User-Agent": "litrun-fetch-pubmed/1.0 (+https://github.com/brycewang-stanford/lit-review-agent-tools)"}


def safe_name(s, maxlen=80):
    s = re.sub(r"[^\w\- ]+", "", s).strip().replace(" ", "_")
    return s[:maxlen] or "article"


def _common_params():
    p = {}
    if os.environ.get("NCBI_API_KEY"):
        p["api_key"] = os.environ["NCBI_API_KEY"]
    return p


def main():
    p = argparse.ArgumentParser(prog="fetch_pubmed.py")
    p.add_argument("--query", required=True)
    p.add_argument("--max", type=int, default=10)
    p.add_argument("--outdir", required=True)
    p.add_argument("--email", default=os.environ.get("NCBI_EMAIL", ""))
    args = p.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    common = _common_params()
    if args.email:
        common["email"] = args.email

    print(f"fetch_pubmed: searching PubMed for {args.query!r} (max {args.max})", file=sys.stderr)
    try:
        es = requests.get(f"{EUTILS}/esearch.fcgi", headers=_UA, timeout=60, params={
            "db": "pubmed", "term": args.query, "retmax": args.max, "retmode": "json", **common})
        es.raise_for_status()
        ids = es.json().get("esearchresult", {}).get("idlist", [])
    except Exception as e:
        sys.exit(f"fetch_pubmed: search failed: {e}")

    if not ids:
        sys.exit("fetch_pubmed: no results for that query.")

    try:
        ef = requests.get(f"{EUTILS}/efetch.fcgi", headers=_UA, timeout=90, params={
            "db": "pubmed", "id": ",".join(ids), "rettype": "abstract", "retmode": "xml", **common})
        ef.raise_for_status()
        root = ET.fromstring(ef.content)
    except Exception as e:
        sys.exit(f"fetch_pubmed: fetch failed: {e}")

    manifest, saved = [], 0
    for art in root.findall(".//PubmedArticle"):
        pmid = (art.findtext(".//PMID") or "").strip() or "unknown"
        title = (art.findtext(".//ArticleTitle") or "").strip() or pmid
        # AbstractText may be split into labeled sections.
        parts = []
        for node in art.findall(".//Abstract/AbstractText"):
            label = node.get("Label")
            text = "".join(node.itertext()).strip()
            parts.append(f"{label}: {text}" if label else text)
        abstract = "\n".join(parts)
        authors = []
        for a in art.findall(".//Author"):
            ln, fn = a.findtext("LastName"), a.findtext("ForeName")
            if ln:
                authors.append(f"{fn} {ln}".strip() if fn else ln)
        dest = outdir / f"pmid{pmid}_{safe_name(title)}.txt"
        dest.write_text(f"{title}\n\n{abstract}\n", encoding="utf-8")
        saved += 1
        print(f"  ✓ {pmid}  {title[:65]}", file=sys.stderr)
        manifest.append({
            "pmid": pmid, "title": title, "authors": authors,
            "file": dest.name, "kind": "txt",
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        })

    _merge_manifest(outdir, manifest)
    print(f"fetch_pubmed: saved {saved} abstract(s) to {outdir}.", file=sys.stderr)
    if saved == 0:
        sys.exit("fetch_pubmed: nothing saved.")


def _merge_manifest(outdir, entries):
    path = outdir / "manifest.json"
    existing = []
    if path.exists():
        try:
            existing = json.loads(path.read_text())
        except Exception:
            existing = []
    existing.extend(entries)
    path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
