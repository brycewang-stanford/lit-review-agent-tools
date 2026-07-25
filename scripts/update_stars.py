#!/usr/bin/env python3
"""Refresh the Stars column in README.md / README.en.md from the GitHub API.

For every table row whose first cell links to a github.com/owner/repo and whose
second cell already looks like a star value (e.g. `~39.5k`, `~44`, `954`), fetch
the current star count and rewrite that cell. Cells that are `—`, `niche`,
`小众`, `(list)` etc. are left untouched.

Env:
  GITHUB_TOKEN  optional; raises the API rate limit from 60 to 5000 req/h.
"""
from __future__ import annotations

import os
import re
import sys
import time
import urllib.error
import urllib.request

FILES = ["README.md", "README.en.md"]

REPO_RE = re.compile(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")
# A cell we're willing to overwrite: optional ~, digits, optional .digits, optional k
STAR_CELL_RE = re.compile(r"^~?\d[\d.]*k?$")

TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()


def fmt(n: int) -> str:
    if n >= 100:
        return f"~{n / 1000:.1f}k"
    return f"~{n}"


def clean_repo(slug: str) -> str:
    # strip common trailing junk from markdown link targets
    return slug.rstrip("/").removesuffix(".git")


def get_stars(repo: str) -> int | None:
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "lit-review-star-bot"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                import json

                return json.load(resp).get("stargazers_count")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"  ! {repo}: 404 (renamed/deleted?) — skipping", file=sys.stderr)
                return None
            if e.code in (403, 429):
                # rate limited; back off
                wait = 20 * (attempt + 1)
                print(f"  … rate limited on {repo}, sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            print(f"  ! {repo}: HTTP {e.code}", file=sys.stderr)
            return None
        except (urllib.error.URLError, TimeoutError) as e:
            time.sleep(5)
    return None


def process(path: str, cache: dict[str, int | None]) -> int:
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    changed = 0
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        # split the markdown row into cells (drop leading/trailing empties)
        raw = line.rstrip("\n")
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        first, second = cells[0], cells[1]
        # separator row like |---|---|
        if set(second) <= {"-", ":"}:
            continue
        if not STAR_CELL_RE.match(second):
            continue
        m = REPO_RE.search(first)
        if not m:
            continue
        repo = clean_repo(m.group(1))
        if repo not in cache:
            cache[repo] = get_stars(repo)
            time.sleep(0.2)
        stars = cache[repo]
        if stars is None:
            continue
        new_val = fmt(stars)
        if new_val == second:
            continue
        # replace only the second column's text, preserving spacing/structure
        # rebuild the row from cells to stay robust
        cells[1] = new_val
        lines[i] = "| " + " | ".join(cells) + " |\n"
        print(f"  {repo}: {second} -> {new_val}")
        changed += 1

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    return changed


def main() -> int:
    cache: dict[str, int | None] = {}
    total = 0
    for path in FILES:
        if not os.path.exists(path):
            continue
        print(f"Updating {path} …")
        total += process(path, cache)
    print(f"Done. {total} cell(s) updated across {len(FILES)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
