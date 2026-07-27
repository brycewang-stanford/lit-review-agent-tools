#!/usr/bin/env python3
"""Render every Markdown surface from data/tools.yaml + data/categories.yaml.

Generated content is written between HTML-comment markers:

    <!-- BEGIN GENERATED:<region> -->
    ...
    <!-- END GENERATED:<region> -->

Everything outside those markers is hand-written prose and is never touched.

Surfaces:
  README.md      zh tables          regions: badge, tagline, toc, categories
  README.en.md   en tables          regions: badge, tagline, toc, categories
  AWESOME.md     awesome-lint bullets   regions: toc, categories
  data/tools.json  machine-readable dataset (whole file is generated)

Usage:
  python3 scripts/build.py           # write files
  python3 scripts/build.py --check   # exit 1 if anything would change
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

# The freshness thresholds are owned by the script that applies them; importing
# rather than restating them keeps the rendered legend honest if they change.
from refresh_metadata import ACTIVE_DAYS, SLOWING_DAYS

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

MARKER_BEGIN = "<!-- BEGIN GENERATED:{} -->"
MARKER_END = "<!-- END GENERATED:{} -->"


# ── helpers ──────────────────────────────────────────────────────────────────


def fmt_stars(n: int) -> str:
    """Render a star count.

    Thousands are abbreviated and marked approximate; anything under 1k is shown
    exactly, because rounding those to one decimal collapsed genuinely different
    repos (146, 122 and 131 all rendered as "~0.1k").
    """
    return f"~{n / 1000:.1f}k" if n >= 1000 else str(n)


def star_cell(tool: dict, lang: str) -> str:
    if tool.get("stars") is not None:
        return fmt_stars(tool["stars"])
    label = tool.get("stars_label") or {}
    return label.get(lang, "—")


# Freshness, as computed by scripts/refresh_metadata.py. build.py only renders
# the stored value — deriving it from today's date here would make generated
# files change on their own and break the CI drift gate.
STATUS_ICON = {
    "active": "🟢",
    "slowing": "🟡",
    "stale": "🔴",
    "archived": "🗄️",
    "unreachable": "❔",
    "unknown": "❔",
}
STATUS_WORD = {
    "active": ("活跃", "active"),
    "slowing": ("放缓", "slowing"),
    "stale": ("停滞", "stale"),
    "archived": ("已归档", "archived"),
    "unreachable": ("无法访问", "unreachable"),
    "unknown": ("未知", "unknown"),
}


def health_cell(tool: dict) -> str:
    return STATUS_ICON.get(tool.get("status", "unknown"), "❔")


def license_cell(tool: dict) -> str:
    lic = tool.get("license")
    return "—" if not lic or lic == "unknown" else lic


def surfaces(tool: dict) -> list[str]:
    return tool.get("surfaces", ["readme", "awesome"])


def load() -> tuple[list[dict], list[dict], dict]:
    cats = yaml.safe_load((DATA / "categories.yaml").read_text(encoding="utf-8"))
    tools = yaml.safe_load((DATA / "tools.yaml").read_text(encoding="utf-8"))
    meta_path = DATA / "meta.yaml"
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    return cats, tools, meta or {}


def by_category(tools: list[dict], cats: list[dict], surface: str) -> dict[str, list[dict]]:
    out = {c["id"]: [] for c in cats}
    for t in tools:
        if surface in surfaces(t):
            out[t["category"]].append(t)
    return out


# ── renderers ────────────────────────────────────────────────────────────────


def render_readme_categories(cats, grouped, lang: str) -> str:
    blocks = []
    for cat in cats:
        rows = grouped[cat["id"]]
        if not rows:
            continue
        out = [
            f"## {cat[f'title_{lang}']}",
            "",
            f"> {cat[f'intro_{lang}']}",
            "",
            cat[f"header_{lang}"],
            cat["separator"],
        ]
        for t in rows:
            name = f"[{t['name']}](https://github.com/{t['repo']})"
            if t.get("editor_pick"):
                name = f"⭐ {name}"
            out.append(
                f"| {name} | {star_cell(t, lang)} | {health_cell(t)} "
                f"| {license_cell(t)} | {t[f'desc_{lang}']} |"
            )
        blocks.append("\n".join(out))
    return "\n\n---\n\n".join(blocks)


def render_readme_toc(cats, grouped, lang: str) -> str:
    return "\n".join(
        f"- [{c[f'title_{lang}']}]({c[f'anchor_{lang}']})" for c in cats if grouped[c["id"]]
    )


def render_awesome_categories(cats, grouped) -> str:
    blocks = []
    for cat in cats:
        rows = grouped[cat["id"]]
        if not rows:
            continue
        out = [f"## {cat['title_awesome']}", ""]
        for t in rows:
            name = t.get("name_awesome", t["name"])
            out.append(f"- [{name}](https://github.com/{t['repo']}) - {t['desc_awesome']}")
        blocks.append("\n".join(out))
    return "\n\n".join(blocks)


def render_awesome_toc(cats, grouped) -> str:
    def anchor(title: str) -> str:
        return "#" + title.lower().replace(" ", "-")

    return "\n".join(
        f"- [{c['title_awesome']}]({anchor(c['title_awesome'])})" for c in cats if grouped[c["id"]]
    )


def render_health(cats, tools, meta) -> str:
    """A full metadata dump: what the README's emoji column can't show."""
    by_id = {c["id"]: c for c in cats}
    tally: dict[str, int] = {}
    for t in tools:
        s = t.get("status", "unknown")
        tally[s] = tally.get(s, 0) + 1

    order = ["active", "slowing", "stale", "archived", "unreachable", "unknown"]
    lines = [
        "# Health report",
        "",
        "> Generated by `scripts/build.py` from `data/tools.yaml`. Do not edit by hand.",
        "",
        f"**{len(tools)} entries** · last refreshed from the GitHub API on "
        f"**{meta.get('refreshed_at', 'unknown')}**",
        "",
        "| Status | Meaning | Count |",
        "|---|---|---|",
    ]
    meanings = {
        "active": f"pushed within {ACTIVE_DAYS} days",
        "slowing": f"pushed within {SLOWING_DAYS} days",
        "stale": f"no push in over {SLOWING_DAYS} days",
        "archived": "archived by its owner",
        "unreachable": "API lookup failed — needs a human",
        "unknown": "no data yet",
    }
    for s in order:
        if s in tally:
            lines.append(f"| {STATUS_ICON[s]} {STATUS_WORD[s][1]} | {meanings[s]} | {tally[s]} |")

    lines += [
        "",
        "Freshness is a proxy, not a verdict: a stable, finished tool can sit",
        "untouched for a year and still work perfectly. Treat 🔴 as *check before",
        "you depend on it*, not *broken*.",
        "",
    ]

    for cat in cats:
        rows = [t for t in tools if t["category"] == cat["id"]]
        if not rows:
            continue
        lines += [
            f"## {by_id[cat['id']]['title_en']}",
            "",
            "| Project | Stars | Last push | Status | License | Language |",
            "|---|---|---|---|---|---|",
        ]
        for t in sorted(rows, key=lambda x: -(x.get("stars") or 0)):
            stars = f"{t['stars']:,}" if t.get("stars") is not None else "—"
            status = t.get("status", "unknown")
            lines.append(
                f"| [{t['name']}](https://github.com/{t['repo']}) "
                f"| {stars} | {t.get('pushed_at') or '—'} "
                f"| {STATUS_ICON.get(status, '❔')} {STATUS_WORD.get(status, ('', status))[1]} "
                f"| {license_cell(t)} | {t.get('language') or '—'} |"
            )
        lines.append("")

    return "\n".join(lines)


def render_json(cats, tools) -> str:
    payload = {
        "$schema": "https://github.com/brycewang-stanford/lit-review-agent-tools/blob/main/docs/DATA.md",
        "generated_by": "scripts/build.py",
        "categories": [
            {"id": c["id"], "title_zh": c["title_zh"], "title_en": c["title_en"]} for c in cats
        ],
        "tools": [
            {
                "name": t["name"],
                "repo": t["repo"],
                "url": f"https://github.com/{t['repo']}",
                "category": t["category"],
                "editor_pick": bool(t.get("editor_pick")),
                "stars": t.get("stars"),
                # PyYAML turns a bare `2026-07-20` into a date object.
                "pushed_at": str(t["pushed_at"]) if t.get("pushed_at") else None,
                "status": t.get("status"),
                "archived": t.get("archived"),
                "license": t.get("license"),
                "language": t.get("language"),
                "description_en": t.get("desc_en") or t.get("desc_awesome"),
                "description_zh": t.get("desc_zh"),
            }
            for t in tools
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


# ── marker splicing ──────────────────────────────────────────────────────────


def splice(text: str, region: str, body: str, path: Path) -> str:
    begin, end = MARKER_BEGIN.format(region), MARKER_END.format(region)
    i, j = text.find(begin), text.find(end)
    if i == -1 or j == -1:
        sys.exit(f"error: {path.name} is missing the '{region}' generated markers")
    if j < i:
        sys.exit(f"error: {path.name} has '{region}' markers in the wrong order")
    return text[: i + len(begin)] + "\n" + body + "\n" + text[j:]


# ── main ─────────────────────────────────────────────────────────────────────


def build() -> dict[Path, str]:
    cats, tools, meta = load()
    readme_grouped = by_category(tools, cats, "readme")
    awesome_grouped = by_category(tools, cats, "awesome")
    n_tools = sum(len(v) for v in readme_grouped.values())

    out: dict[Path, str] = {}

    for path, lang, badge, tagline in (
        (
            ROOT / "README.md",
            "zh",
            f"![Tools](https://img.shields.io/badge/tools-{n_tools}-blue)",
            f"<em>收录 <b>{n_tools}</b> 个用于文献综述的开源项目，按使用场景分类 · 每季度更新 · 欢迎 PR</em>",
        ),
        (
            ROOT / "README.en.md",
            "en",
            f"![Tools](https://img.shields.io/badge/tools-{n_tools}-blue)",
            f"<em><b>{n_tools}</b> open-source projects for literature review, "
            "organized by use case · updated quarterly · PRs welcome</em>",
        ),
    ):
        text = path.read_text(encoding="utf-8")
        text = splice(text, "badge", badge, path)
        text = splice(text, "tagline", tagline, path)
        text = splice(text, "toc", render_readme_toc(cats, readme_grouped, lang), path)
        text = splice(
            text, "categories", render_readme_categories(cats, readme_grouped, lang), path
        )
        out[path] = text

    aw_path = ROOT / "AWESOME.md"
    aw = aw_path.read_text(encoding="utf-8")
    aw = splice(aw, "toc", render_awesome_toc(cats, awesome_grouped), aw_path)
    aw = splice(aw, "categories", render_awesome_categories(cats, awesome_grouped), aw_path)
    out[aw_path] = aw

    out[ROOT / "HEALTH.md"] = render_health(cats, tools, meta)
    out[DATA / "tools.json"] = render_json(cats, tools)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if any file would change")
    args = ap.parse_args()

    rendered = build()
    stale = []
    for path, content in rendered.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        stale.append(path)
        if not args.check:
            path.write_text(content, encoding="utf-8")

    rel = [str(p.relative_to(ROOT)) for p in stale]
    if args.check:
        if stale:
            print("Generated files are out of date:", file=sys.stderr)
            for r in rel:
                print(f"  {r}", file=sys.stderr)
            print("\nRun `make build` and commit the result.", file=sys.stderr)
            return 1
        print(f"All {len(rendered)} generated files are up to date.")
        return 0

    print(f"Wrote {len(stale)}/{len(rendered)} file(s)" + (": " + ", ".join(rel) if rel else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
