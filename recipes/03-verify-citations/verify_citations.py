#!/usr/bin/env python3
"""Check that cited works actually exist — no API key required.

LLM-drafted related-work sections invent plausible references. This resolves
each citation against Crossref and OpenAlex, reports the canonical metadata,
and flags anything it cannot find or that has been retracted.

Usage:
    python3 verify_citations.py citations.txt

Input: one citation per line. A DOI, or a title, or free-form text containing
either. Lines starting with # are ignored.

Only DOI lookups yield CONFIRMED. Title lookups return the closest match in
Crossref, which is not always the work you meant, so they are reported as
TITLE MATCH for a human to accept or reject.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "lit-review-agent-tools/1.0 (mailto:lit-review-agent-tools@example.com)"
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
# Crossref marks retractions and corrections through update-to relations.
RETRACTION_TYPES = {"retraction", "withdrawal", "removal"}


def get(url: str) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return None


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def similar(a: str, b: str) -> float:
    """Token overlap — enough to tell 'same paper' from 'plausible invention'."""
    ta, tb = set(norm(a).split()), set(norm(b).split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta), len(tb))


def by_doi(doi: str) -> dict | None:
    d = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    return d.get("message") if d else None


def by_title(title: str) -> tuple[dict | None, float]:
    d = get(
        "https://api.crossref.org/works?rows=5&select=DOI,title,author,issued,"
        "container-title,is-referenced-by-count,update-to&query.bibliographic="
        + urllib.parse.quote(title)
    )
    best, best_score = None, 0.0
    for item in ((d or {}).get("message") or {}).get("items", []):
        cand = (item.get("title") or [""])[0]
        s = similar(title, cand)
        if s > best_score:
            best, best_score = item, s
    return best, best_score


def openalex_retracted(doi: str) -> bool | None:
    d = get("https://api.openalex.org/works/https://doi.org/" + urllib.parse.quote(doi))
    return None if d is None else bool(d.get("is_retracted"))


def describe(m: dict) -> str:
    title = (m.get("title") or [""])[0]
    year = ""
    for k in ("issued", "published-print", "published-online"):
        parts = (m.get(k) or {}).get("date-parts") or [[]]
        if parts and parts[0]:
            year = str(parts[0][0])
            break
    authors = m.get("author") or []
    who = authors[0].get("family", "?") if authors else "?"
    if len(authors) > 1:
        who += " et al."
    venue = (m.get("container-title") or [""])[0]
    return f"{who} ({year}) {title[:72]}{'…' if len(title) > 72 else ''} — {venue[:40]}"


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    lines = [
        ln.strip()
        for ln in open(sys.argv[1], encoding="utf-8")
        if ln.strip() and not ln.startswith("#")
    ]

    verdicts = {"confirmed": 0, "title-only": 0, "not-found": 0, "mismatch": 0, "retracted": 0}
    for raw in lines:
        doi_m = DOI_RE.search(raw)
        meta, score, how = None, 1.0, "doi"
        if doi_m:
            meta = by_doi(doi_m.group(0).rstrip(".,;"))
        if meta is None:
            how = "title"
            meta, score = by_title(raw)

        if meta is None:
            verdicts["not-found"] += 1
            print(f"✗ NOT FOUND   {raw[:82]}")
            continue

        doi = meta.get("DOI", "")
        retracted = openalex_retracted(doi) if doi else None
        updates = {(u.get("type") or "").lower() for u in (meta.get("update-to") or [])}
        if retracted or (updates & RETRACTION_TYPES):
            verdicts["retracted"] += 1
            print(f"⚠ RETRACTED   {describe(meta)}\n              https://doi.org/{doi}")
        elif how == "title" and score < 0.75:
            verdicts["mismatch"] += 1
            print(f"? WEAK MATCH  {raw[:60]}")
            print(f"              closest: {describe(meta)} (overlap {score:.0%})")
        elif how == "title":
            # A title search returns the *closest* work, not necessarily the one
            # meant: "Attention Is All You Need" resolves to a 2025 paper called
            # "Is Attention All You Need?". Never call that confirmed — surface
            # what was matched and make a human agree.
            verdicts["title-only"] += 1
            print(f"~ TITLE MATCH {describe(meta)}  (overlap {score:.0%})")
            print(f"              https://doi.org/{doi}  — verify this is the work you meant")
        else:
            verdicts["confirmed"] += 1
            print(f"✓ CONFIRMED   {describe(meta)}")
            print(f"              https://doi.org/{doi}")
        time.sleep(0.3)

    print("\n" + "  ".join(f"{k}={v}" for k, v in verdicts.items()))
    return 1 if (verdicts["not-found"] or verdicts["retracted"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
