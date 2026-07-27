#!/usr/bin/env python3
"""Build a deduplicated, screening-ready corpus from OpenAlex — no API key.

Usage:
    pip install pyalex
    python3 build_corpus.py "large language models for systematic review" --max 400

Writes corpus.csv with the columns ASReview expects (title, abstract, doi, ...).
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter

import pyalex
from pyalex import Works

# OpenAlex asks for an email to put you in the polite pool: faster, and they can
# contact you instead of silently blocking. Any real address works.
pyalex.config.email = "lit-review-agent-tools@example.com"
pyalex.config.max_retries = 3


def abstract_of(work: dict) -> str:
    """OpenAlex ships abstracts as an inverted index, not text."""
    idx = work.get("abstract_inverted_index")
    if not idx:
        return ""
    positions: list[tuple[int, str]] = []
    for word, spots in idx.items():
        positions.extend((p, word) for p in spots)
    return " ".join(w for _, w in sorted(positions))


def norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--max", type=int, default=400)
    ap.add_argument("--from-year", type=int, default=2019)
    ap.add_argument("--out", default="corpus.csv")
    a = ap.parse_args()

    pager = (
        Works()
        .search(a.query)
        .filter(from_publication_date=f"{a.from_year}-01-01", has_abstract=True)
        .paginate(per_page=200, n_max=a.max)
    )

    seen_doi: set[str] = set()
    seen_title: set[str] = set()
    rows: list[dict] = []
    dupes = Counter()

    for page in pager:
        for w in page:
            doi = (w.get("doi") or "").lower().replace("https://doi.org/", "")
            nt = norm_title(w.get("title"))
            if doi and doi in seen_doi:
                dupes["doi"] += 1
                continue
            if nt and nt in seen_title:
                dupes["title"] += 1
                continue
            if doi:
                seen_doi.add(doi)
            if nt:
                seen_title.add(nt)
            rows.append(
                {
                    "title": w.get("title") or "",
                    "abstract": abstract_of(w),
                    "doi": doi,
                    "year": w.get("publication_year") or "",
                    "venue": ((w.get("primary_location") or {}).get("source") or {}).get(
                        "display_name", ""
                    ),
                    "cited_by": w.get("cited_by_count", 0),
                    "openalex_id": w.get("id", ""),
                    "oa_url": (w.get("best_oa_location") or {}).get("pdf_url", "") or "",
                }
            )

    if not rows:
        print("No results — try a broader query.", file=sys.stderr)
        return 1

    with open(a.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    oa = sum(1 for r in rows if r["oa_url"])
    print(f"query      : {a.query!r} (from {a.from_year})")
    print(f"kept       : {len(rows)} records -> {a.out}")
    print(f"dropped    : {dupes['doi']} duplicate DOIs, {dupes['title']} duplicate titles")
    print(f"open access: {oa} have a direct PDF link ({oa / len(rows):.0%})")
    print(f"years      : {min(r['year'] for r in rows)}–{max(r['year'] for r in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
