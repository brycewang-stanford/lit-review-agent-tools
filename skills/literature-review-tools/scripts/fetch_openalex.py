#!/usr/bin/env python3
"""fetch_openalex — search OpenAlex and save papers into a folder.

Downloads the open-access PDF when one is available, otherwise writes a
`<id>.txt` with the title + reconstructed abstract (PaperQA2 reads text too).
Writes a merged manifest.json. Uses the free OpenAlex API (no key needed for
light use; set OPENALEX_API_KEY / --mailto for higher limits + the polite pool).

Usage:
  fetch_openalex.py --query "retrieval augmented generation" --max 10 --outdir ./papers
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("fetch_openalex: 'requests' not installed. Run: litrun.py install openalex-fetch")

API = "https://api.openalex.org/works"
_UA = {"User-Agent": "litrun-fetch-openalex/1.0 (+https://github.com/brycewang-stanford/lit-review-agent-tools)"}


def safe_name(s, maxlen=80):
    s = re.sub(r"[^\w\- ]+", "", s).strip().replace(" ", "_")
    return s[:maxlen] or "work"


def reconstruct_abstract(inv):
    """OpenAlex stores abstracts as an inverted index {word: [positions]}."""
    if not inv:
        return ""
    pos = {}
    for word, positions in inv.items():
        for p in positions:
            pos[p] = word
    return " ".join(pos[i] for i in sorted(pos))


def download(url, dest):
    with requests.get(url, headers=_UA, stream=True, timeout=60, allow_redirects=True) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1 << 15):
                if chunk:
                    f.write(chunk)


def main():
    p = argparse.ArgumentParser(prog="fetch_openalex.py")
    p.add_argument("--query", required=True)
    p.add_argument("--max", type=int, default=10)
    p.add_argument("--outdir", required=True)
    p.add_argument("--mailto", default=os.environ.get("OPENALEX_MAILTO", ""))
    args = p.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    params = {"search": args.query, "per_page": min(args.max, 200)}
    if args.mailto:
        params["mailto"] = args.mailto
    key = os.environ.get("OPENALEX_API_KEY")
    if key:
        params["api_key"] = key

    print(f"fetch_openalex: searching OpenAlex for {args.query!r} (max {args.max})", file=sys.stderr)
    try:
        resp = requests.get(API, params=params, headers=_UA, timeout=60)
        resp.raise_for_status()
        works = resp.json().get("results", [])[:args.max]
    except Exception as e:
        sys.exit(f"fetch_openalex: search failed: {e}")

    manifest, saved = [], 0
    for w in works:
        oid = (w.get("id") or "").rsplit("/", 1)[-1] or "work"
        title = w.get("display_name") or w.get("title") or oid
        oa = w.get("best_oa_location") or w.get("primary_location") or {}
        pdf_url = oa.get("pdf_url") or (w.get("open_access") or {}).get("oa_url")
        kind = None
        if pdf_url:
            try:
                dest = outdir / f"{oid}_{safe_name(title)}.pdf"
                download(pdf_url, dest)
                kind = "pdf"
            except Exception as e:
                print(f"  ! {oid} PDF failed ({e}); saving abstract instead", file=sys.stderr)
        if kind is None:
            abstract = reconstruct_abstract(w.get("abstract_inverted_index"))
            dest = outdir / f"{oid}_{safe_name(title)}.txt"
            dest.write_text(f"{title}\n\n{abstract}\n", encoding="utf-8")
            kind = "txt"
        saved += 1
        print(f"  ✓ {oid} [{kind}]  {title[:65]}", file=sys.stderr)
        manifest.append({
            "openalex_id": oid,
            "title": title,
            "year": w.get("publication_year"),
            "authors": [a.get("author", {}).get("display_name") for a in w.get("authorships", [])],
            "file": dest.name,
            "kind": kind,
            "url": w.get("id"),
        })

    _merge_manifest(outdir, manifest)
    print(f"fetch_openalex: saved {saved}/{len(works)} item(s) to {outdir}.", file=sys.stderr)
    if saved == 0:
        sys.exit("fetch_openalex: nothing saved.")


def _merge_manifest(outdir, entries):
    """Append to an existing manifest.json so multi-source workflows accumulate."""
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
