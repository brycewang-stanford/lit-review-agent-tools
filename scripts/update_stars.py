#!/usr/bin/env python3
"""Refresh the `stars:` values in data/tools.yaml from the GitHub API.

This writes to the data layer only. Run `scripts/build.py` afterwards (or just
`make stars`) to push the new numbers into the rendered Markdown surfaces.

Entries whose `stars` is null keep their curated `stars_label` (e.g. 小众 /
niche) and are skipped — that label is an editorial judgement, not a number.

The file is edited as text rather than round-tripped through a YAML dumper so
that comments, ordering, and quoting survive untouched.

Env:
  GITHUB_TOKEN  optional; raises the API rate limit from 60 to 5000 req/h.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "data" / "tools.yaml"

TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()

ENTRY_SPLIT = re.compile(r"^(?=- name:)", re.M)
REPO_RE = re.compile(r"^  repo:\s*(\S+)\s*$", re.M)
STARS_RE = re.compile(r"^  stars:\s*(.+?)\s*$", re.M)


def fetch(repo: str) -> tuple[int | None, str | None]:
    """Return (stars, error). Follows renames; reports anything unresolvable."""
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "lit-review-star-bot"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.load(resp)
            stars = data.get("stargazers_count")
            actual = data.get("full_name")
            if actual and actual.lower() != repo.lower():
                return stars, f"renamed upstream to {actual}"
            if data.get("archived"):
                return stars, "archived upstream"
            return stars, None
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, "404 — repo deleted, renamed, or made private"
            if e.code in (403, 429):
                wait = 20 * (attempt + 1)
                print(f"  … rate limited on {repo}, sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            return None, f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError):
            time.sleep(5)
    return None, "gave up after retries"


def main() -> int:
    text = TOOLS.read_text(encoding="utf-8")
    parts = ENTRY_SPLIT.split(text)

    changed = 0
    problems: list[str] = []

    for i, part in enumerate(parts):
        rm = REPO_RE.search(part)
        sm = STARS_RE.search(part)
        if not rm or not sm:
            continue
        repo, current = rm.group(1), sm.group(1)
        if current == "null":
            continue  # curated label; leave it alone

        stars, problem = fetch(repo)
        time.sleep(0.2)
        if problem:
            problems.append(f"{repo}: {problem}")
        if stars is None:
            continue
        if str(stars) == current:
            continue
        parts[i] = part[: sm.start(1)] + str(stars) + part[sm.end(1) :]
        print(f"  {repo}: {current} -> {stars}")
        changed += 1

    if changed:
        TOOLS.write_text("".join(parts), encoding="utf-8")

    print(f"Done. {changed} star count(s) updated in data/tools.yaml.")
    if problems:
        # Surfaced loudly: a silent 404 is how a dead entry lives forever.
        print(f"\n{len(problems)} entr(ies) need attention:", file=sys.stderr)
        for p in problems:
            print(f"  ! {p}", file=sys.stderr)
    print("Now run `python3 scripts/build.py` to re-render the Markdown surfaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
