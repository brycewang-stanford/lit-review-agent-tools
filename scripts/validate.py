#!/usr/bin/env python3
"""Validate data/tools.yaml and data/categories.yaml before anything is rendered.

Catches the mistakes a contributor is actually likely to make: a typo'd
category, a duplicate entry, a missing translation, or a description that
awesome-lint would reject downstream.

Usage:
  python3 scripts/validate.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VALID_SURFACES = {"readme", "awesome"}
# Kept generous: these are the descriptions rendered into table cells.
MAX_DESC = 400
MAX_DESC_AWESOME = 160

CAT_REQUIRED = [
    "id",
    "title_zh",
    "title_en",
    "title_awesome",
    "anchor_zh",
    "anchor_en",
    "intro_zh",
    "intro_en",
    "header_zh",
    "header_en",
    "separator",
]


def main() -> int:
    errors: list[str] = []

    def err(msg: str) -> None:
        errors.append(msg)

    cats = yaml.safe_load((DATA / "categories.yaml").read_text(encoding="utf-8"))
    tools = yaml.safe_load((DATA / "tools.yaml").read_text(encoding="utf-8"))

    # ── categories ───────────────────────────────────────────────────────────
    cat_ids: set[str] = set()
    for i, c in enumerate(cats):
        where = f"categories.yaml[{i}]"
        for field in CAT_REQUIRED:
            if not c.get(field):
                err(f"{where}: missing '{field}'")
        cid = c.get("id")
        if cid in cat_ids:
            err(f"{where}: duplicate category id '{cid}'")
        cat_ids.add(cid)

    # ── tools ────────────────────────────────────────────────────────────────
    seen_repo: dict[str, str] = {}
    seen_name: dict[str, str] = {}
    for i, t in enumerate(tools):
        name = t.get("name", f"<entry {i}>")
        where = f"tools.yaml[{i}] ({name})"

        if not t.get("name"):
            err(f"{where}: missing 'name'")
        repo = t.get("repo")
        if not repo:
            err(f"{where}: missing 'repo'")
        elif not REPO_RE.match(repo):
            err(f"{where}: 'repo' must be owner/name, got {repo!r}")
        elif repo.lower() in seen_repo:
            err(f"{where}: duplicate repo, already listed as {seen_repo[repo.lower()]}")
        else:
            seen_repo[repo.lower()] = name

        if name in seen_name:
            err(f"{where}: duplicate name (also {seen_name[name]})")
        seen_name[name] = where

        cat = t.get("category")
        if cat not in cat_ids:
            err(f"{where}: unknown category {cat!r} (valid: {', '.join(sorted(cat_ids))})")

        surfaces = t.get("surfaces", ["readme", "awesome"])
        if not isinstance(surfaces, list) or not surfaces:
            err(f"{where}: 'surfaces' must be a non-empty list")
        elif set(surfaces) - VALID_SURFACES:
            err(f"{where}: unknown surface(s) {sorted(set(surfaces) - VALID_SURFACES)}")
        else:
            if "readme" in surfaces:
                for field in ("desc_zh", "desc_en"):
                    if not t.get(field):
                        err(f"{where}: rendered in README but missing '{field}'")
                    elif len(t[field]) > MAX_DESC:
                        err(f"{where}: '{field}' is {len(t[field])} chars (max {MAX_DESC})")
            if "awesome" in surfaces:
                d = t.get("desc_awesome")
                if not d:
                    err(f"{where}: rendered in AWESOME.md but missing 'desc_awesome'")
                else:
                    if not d.endswith("."):
                        err(f"{where}: 'desc_awesome' must end with a period (awesome-lint)")
                    if d[:1].islower():
                        err(f"{where}: 'desc_awesome' must start with a capital (awesome-lint)")
                    if len(d) > MAX_DESC_AWESOME:
                        err(
                            f"{where}: 'desc_awesome' is {len(d)} chars "
                            f"(max {MAX_DESC_AWESOME}; awesome-lint prefers short)"
                        )

        stars = t.get("stars")
        if stars is None:
            # Only the README tables render a Stars column, so a label is only
            # needed there; AWESOME.md entries may legitimately carry no count.
            if not t.get("stars_label"):
                if "readme" in surfaces:
                    err(f"{where}: 'stars' is null so a 'stars_label' {{zh, en}} is required")
            else:
                missing = {"zh", "en"} - set(t["stars_label"])
                if missing:
                    err(f"{where}: 'stars_label' missing {sorted(missing)}")
        elif not isinstance(stars, int) or stars < 0:
            err(f"{where}: 'stars' must be a non-negative integer, got {stars!r}")

        added = t.get("added")
        if added is not None and not DATE_RE.match(str(added)):
            err(f"{where}: 'added' must be YYYY-MM-DD, got {added!r}")

    if errors:
        print(f"{len(errors)} validation error(s):\n", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1

    n_readme = sum(1 for t in tools if "readme" in t.get("surfaces", ["readme", "awesome"]))
    print(
        f"OK — {len(tools)} entries across {len(cats)} categories "
        f"({n_readme} rendered in the READMEs)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
