# The dataset

This list is generated from data, and that data is published for you to reuse.

- **[`data/tools.yaml`](../data/tools.yaml)** — the single source of truth. Hand-edited.
- **[`data/categories.yaml`](../data/categories.yaml)** — category headings, intros, and anchors.
- **[`data/tools.json`](../data/tools.json)** — generated, machine-readable export. **Use this one.**
- **[`data/meta.yaml`](../data/meta.yaml)** — when the metadata was last refreshed.
- **[`HEALTH.md`](../HEALTH.md)** — generated per-tool report: stars, last push, status, license, language.
- **[`CHANGELOG.md`](../CHANGELOG.md)** — generated: what was added when, plus the watch list.
- **`docs/index.html`** — generated searchable site; the catalogue is embedded in the page,
  so it is one file with no runtime fetch and works opened straight off disk.

Everything else — the tables in `README.md` and `README.en.md`, the bullets in
`AWESOME.md` — is rendered from these files by [`scripts/build.py`](../scripts/build.py).
CI fails if the rendered files and the data disagree, so the JSON is never stale
relative to what you read in the README.

## Using `tools.json`

```bash
curl -sL https://raw.githubusercontent.com/brycewang-stanford/lit-review-agent-tools/main/data/tools.json
```

```json
{
  "categories": [
    { "id": "paper-qa-rag", "title_zh": "📚 文献问答与 RAG", "title_en": "📚 Paper Q&A and RAG" }
  ],
  "tools": [
    {
      "name": "paper-qa",
      "repo": "Future-House/paper-qa",
      "url": "https://github.com/Future-House/paper-qa",
      "category": "paper-qa-rag",
      "editor_pick": true,
      "stars": 8943,
      "pushed_at": "2026-07-20",
      "status": "active",
      "archived": false,
      "license": "Apache-2.0",
      "language": "Python",
      "description_en": "FutureHouse; high-accuracy RAG for scientific papers …",
      "description_zh": "FutureHouse 出品，高精度科学文献 RAG …"
    }
  ]
}
```

| Field | Type | Notes |
|---|---|---|
| `name` | string | Display name |
| `repo` | string | `owner/repo`; the canonical identifier |
| `url` | string | Derived from `repo` |
| `category` | string | Joins to `categories[].id` |
| `editor_pick` | bool | Rendered as ⭐ in the READMEs |
| `stars` | int \| null | GitHub API snapshot, refreshed weekly. `null` where a curated label is used instead |
| `pushed_at` | string \| null | `YYYY-MM-DD` of the last push |
| `status` | string | `active` (pushed ≤90d) · `slowing` (≤365d) · `stale` · `archived` · `unreachable` |
| `archived` | bool | Archived by its owner |
| `license` | string | SPDX id where GitHub detects one. `none` = no license file at all, i.e. all rights reserved. `custom` = bespoke terms, read them. Values GitHub reports as `NOASSERTION` are hand-verified from the repo's LICENSE file and are never overwritten by the refresher |
| `language` | string | Primary language per GitHub |
| `description_en` | string | Falls back to the AWESOME.md description for entries not in the READMEs |
| `description_zh` | string \| null | Absent for entries that only appear in `AWESOME.md` |

Star counts and freshness are weekly snapshots, not live values. `status` is
computed at refresh time rather than at render time, so the generated files stay
a pure function of the data and don't silently change as days pass. Everything is [CC0](../LICENSE); no attribution required, though a
link back is appreciated.

## Editing the data

See [CONTRIBUTING.md](../CONTRIBUTING.md). In short: edit `data/tools.yaml`,
run `make build`, commit the result.

## Fields in `tools.yaml` not exported to JSON

`desc_awesome`, `name_awesome`, `stars_label`, `surfaces`, and `added` control
rendering rather than describing the tool. `surfaces` defaults to
`[readme, awesome]`; narrowing it (e.g. `[awesome]`) keeps an entry out of the
README tables while still listing it in the awesome.re edition.
