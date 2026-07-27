#!/usr/bin/env python3
"""Refresh per-repo metadata in data/tools.yaml from the GitHub API.

One `GET /repos/{owner}/{repo}` gives everything the list needs: stars, last
push, archived flag, license, and language. All of it is written back into the
data layer; run `scripts/build.py` afterwards (or just `make refresh`) to
re-render the Markdown surfaces.

Why `status` is computed *here* and not in build.py
---------------------------------------------------
Freshness depends on the current date. If build.py derived it, the generated
files would change on their own as days passed and the CI drift gate would fail
without anyone touching the data. So this script — which commits its output —
owns every clock-dependent value, and build.py stays a pure function of the data.

Entries whose `stars` is null keep their curated `stars_label` (e.g. 小众 /
niche); their other metadata is still refreshed.

The file is edited as text rather than round-tripped through a YAML dumper so
that comments, ordering, and quoting survive untouched.

Env:
  GITHUB_TOKEN  optional; raises the API rate limit from 60 to 5000 req/h.

Exit codes:
  0  refreshed (possibly with warnings)
  1  a hard failure (network, auth, unreadable data)
"""
from __future__ import annotations

import datetime as dt
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
META = ROOT / "data" / "meta.yaml"

TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()

ENTRY_SPLIT = re.compile(r"^(?=- name:)", re.M)
REPO_RE = re.compile(r"^  repo:\s*(\S+)\s*$", re.M)

# Freshness thresholds, in days since the last push.
ACTIVE_DAYS = 90
SLOWING_DAYS = 365

# Fields this script owns. Any of them present in an entry get overwritten;
# absent ones get appended after the last machine-owned field (or after `repo`).
MANAGED = ("stars", "pushed_at", "archived", "license", "language", "status")


def classify(pushed_at: str | None, archived: bool, today: dt.date) -> str:
    if archived:
        return "archived"
    if not pushed_at:
        return "unknown"
    age = (today - dt.date.fromisoformat(pushed_at)).days
    if age <= ACTIVE_DAYS:
        return "active"
    if age <= SLOWING_DAYS:
        return "slowing"
    return "stale"


def fetch(repo: str) -> tuple[dict | None, str | None]:
    """Return (metadata, problem). `problem` is a human-readable warning."""
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "lit-review-metadata-bot"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, "404 — deleted, renamed, or made private"
            if e.code in (403, 429):
                wait = 20 * (attempt + 1)
                print(f"  … rate limited on {repo}, sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            return None, f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError):
            time.sleep(5)
            continue

        lic = (data.get("license") or {}).get("spdx_id") or "NOASSERTION"
        meta = {
            "stars": data.get("stargazers_count"),
            "pushed_at": (data.get("pushed_at") or "")[:10] or None,
            "archived": bool(data.get("archived")),
            "license": "unknown" if lic in ("NOASSERTION", "NONE") else lic,
            "language": data.get("language") or "unknown",
        }
        problem = None
        actual = data.get("full_name")
        if actual and actual.lower() != repo.lower():
            problem = f"renamed upstream to {actual}"
        elif meta["archived"]:
            problem = "archived upstream"
        return meta, problem
    return None, "gave up after retries"


def set_field(block: str, key: str, value: str) -> str:
    """Set `  key: value` in a YAML entry block, inserting if absent."""
    pat = re.compile(rf"^  {key}:.*$", re.M)
    if pat.search(block):
        return pat.sub(f"  {key}: {value}", block, count=1)
    # insert after the last managed field already present, else after `repo:`
    anchor = None
    for k in MANAGED:
        m = re.search(rf"^  {k}:.*$", block, re.M)
        if m:
            anchor = m
    if anchor is None:
        anchor = re.search(r"^  repo:.*$", block, re.M)
    if anchor is None:  # pragma: no cover - validate.py rejects this first
        return block
    return block[: anchor.end()] + f"\n  {key}: {value}" + block[anchor.end() :]


def main() -> int:
    today = dt.date.today()
    try:
        text = TOOLS.read_text(encoding="utf-8")
    except OSError as e:
        print(f"error: cannot read {TOOLS}: {e}", file=sys.stderr)
        return 1

    parts = ENTRY_SPLIT.split(text)
    changed = 0
    problems: list[str] = []
    counts: dict[str, int] = {}

    for i, part in enumerate(parts):
        rm = REPO_RE.search(part)
        if not rm:
            continue
        repo = rm.group(1)
        meta, problem = fetch(repo)
        time.sleep(0.15)
        if problem:
            problems.append(f"{repo}: {problem}")
        if meta is None:
            # Can't reach it — record that, rather than silently leaving stale data.
            counts["unreachable"] = counts.get("unreachable", 0) + 1
            new = set_field(part, "status", "unreachable")
            if new != part:
                parts[i], changed = new, changed + 1
            continue

        status = classify(meta["pushed_at"], meta["archived"], today)
        counts[status] = counts.get(status, 0) + 1

        before = part
        # `stars: null` means a curated label is in use; don't clobber it.
        if not re.search(r"^  stars:\s*null\s*$", part, re.M) and meta["stars"] is not None:
            part = set_field(part, "stars", str(meta["stars"]))
        part = set_field(part, "pushed_at", meta["pushed_at"] or "null")
        part = set_field(part, "archived", "true" if meta["archived"] else "false")
        # GitHub reports NOASSERTION for any license it can't machine-detect, which
        # includes real, restrictive ones (CC-BY-NC in a plain LICENSE file, say).
        # So an unknown from the API never overwrites a value a human verified.
        existing = re.search(r"^  license:\s*(\S+)\s*$", part, re.M)
        if meta["license"] != "unknown" or not existing or existing.group(1) == "unknown":
            part = set_field(part, "license", meta["license"])
        part = set_field(part, "language", meta["language"])
        part = set_field(part, "status", status)
        if part != before:
            changed += 1
        parts[i] = part

    if changed:
        TOOLS.write_text("".join(parts), encoding="utf-8")

    META.write_text(
        "# Written by scripts/refresh_metadata.py. Do not hand-edit.\n"
        "# Keeps every clock-dependent value out of scripts/build.py so that\n"
        "# generated files stay a pure function of the data.\n"
        f"refreshed_at: {today.isoformat()}\n",
        encoding="utf-8",
    )

    summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    print(f"Done. {changed} entr(ies) updated. Status: {summary or 'none'}")

    # Written unconditionally (empty when clean) so the workflow can decide
    # whether to open a tracking issue without parsing log output.
    out = os.environ.get("WARNINGS_FILE")
    if out:
        Path(out).write_text("\n".join(problems) + ("\n" if problems else ""), encoding="utf-8")

    if problems:
        # Surfaced loudly: a silent 404 is how a dead entry lives forever.
        print(f"\n{len(problems)} entr(ies) need attention:", file=sys.stderr)
        for p in problems:
            print(f"  ! {p}", file=sys.stderr)
    print("Now run `python3 scripts/build.py` to re-render the Markdown surfaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
