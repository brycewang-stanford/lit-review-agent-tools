# Roadmap — from "a list you read once" to "a dataset you use weekly"

> **TL;DR（中文）** 目前仓库是一份手工维护的静态清单：66 个工具、11 个分类、**4 份**需要同步手改的副本。
> 下一阶段的核心不是「再加 30 个工具」，而是把它变成**一份可编程的数据集 + 若干消费界面**：
> 单一数据源（`data/tools.yaml`）→ 自动渲染所有 Markdown → 自动抓取活跃度/许可证信号 → 可搜索站点 / Skill / MCP。
> 加工具从「改 4 个文件」变成「加 1 段 YAML」，清单从「读一次」变成「每周回来看」。

**Owner:** @brycewang-stanford · **Written:** 2026-07-27 · **Phase 1 shipped 2026-07-27**

---

## 1. Where the repo actually is today

| Dimension | State |
|---|---|
| Content | 66 open-source tools + 5 commercial references, 11 use-case categories, bilingual (zh/en) |
| Surfaces | `README.md`, `README.en.md`, `AWESOME.md`, `skills/literature-review-tools/` (4 hand-synced copies) |
| Automation | `scripts/update_stars.py` (weekly star refresh), `awesome-lint` on `AWESOME.md`, markdown link check on both READMEs |
| Assets | SVG banner + 1280×640 social preview, issue/PR templates, CC0 license, CoC |
| Distribution | awesome.re submission kit drafted, zh + en promo copy drafted, none published yet |

**What's genuinely strong:** the curation and taxonomy. The "30-second picker" and decision table are the differentiator — most awesome-lists are undifferentiated link dumps.

**What caps it:** everything below the curation is manual and static.

1. **Four sources of truth.** Verified today: README.md / README.en.md / catalog.md carry 68 repo links each, `AWESOME.md` carries 67. They agree *right now*, but only because they were written in one sitting. Every future contribution is a 4-file edit — drift is a matter of time, not risk.
2. **One signal only (stars).** Stars measure past hype, not whether a tool still works. There is no *last commit*, *archived*, *license*, or *language* signal — exactly the fields a researcher needs before adopting something.
3. **Silent decay.** `scripts/update_stars.py:54` swallows 404s (renamed/deleted repos) and moves on. A dead entry can sit in the list indefinitely with a stale star count and nobody is told.
4. **Claimed counts drift from real counts.** The badge and tagline say `70+`; the actual figure is 66. Small, but this list's stated pitch is "信息真实".
5. **No reason to return.** A static README is a one-visit artifact. There is no changelog, no feed, no "what changed this month".
6. **No consumable dataset.** Other people's tooling can't ingest a Markdown table. A JSON/YAML dataset is what gets forked, embedded, and cited.

## 2. Thesis

> Stop treating the README as the product. Treat **the dataset** as the product, and render every surface from it.

Three pillars, in dependency order:

```
 P1  Data layer        data/tools.yaml → generates all Markdown surfaces
      ↓
 P2  Trust signals     freshness · archived · license · health report
      ↓
 P3  Surfaces          searchable site · skill · MCP · monthly changelog
      ↓
 P4  Editorial depth   verified recipes, stage matrix  ← the actual moat
      ↓
 P5  Distribution      awesome.re, HN/Reddit/知乎, tool-of-the-month
```

---

## Phase 1 — Single source of truth ✅ *shipped 2026-07-27*

**Goal:** adding a tool is one YAML block plus `make build`. Drift becomes impossible, not unlikely.

> **Delivered.** `data/tools.yaml` (67 entries) + `data/categories.yaml` now generate
> `README.md`, `README.en.md`, `AWESOME.md`, and `data/tools.json`. The migration was
> verified byte-faithful: regenerated output matched the previous files exactly, apart
> from the marker comments and the tool count, which was corrected from the claimed
> `70+` to the actual `66`. `scripts/update_stars.py` now writes to the data layer
> instead of rewriting Markdown cells, so the weekly bot and the drift gate agree.
> Remaining item from this phase: wiring the skill catalog (§3.2), still blocked on §6.

### 1.1 Schema — `data/tools.yaml`

```yaml
- id: paper-qa
  name: paper-qa
  repo: Future-House/paper-qa          # canonical; drives all API lookups
  category: paper-qa-rag
  stage: [read, extract, synthesize]   # search|read|extract|synthesize|screen|cite-check|write|review
  editor_pick: true
  added: 2026-07-25
  desc_en: High-accuracy RAG over scientific papers; every answer carries citations.
  desc_zh: 高精度科学文献 RAG，回答必带引用；PaperQA2 号称检索达超人水平。
  install: "pip install paper-qa"      # optional
  # ── machine-written below this line; never hand-edit ──
  stars: 8900
  pushed_at: 2026-07-20
  archived: false
  license: Apache-2.0
  language: Python
```

Categories live in `data/categories.yaml` (id, emoji, zh/en title, zh/en intro blurb) so ordering and headings are data too.

### 1.2 Generator — `scripts/build.py`

Renders, between `<!-- BEGIN GENERATED:<section> -->` / `<!-- END GENERATED -->` markers, so hand-written prose (the intro, the 30-second picker, the decision table) stays hand-written:

- `README.md` — zh tables
- `README.en.md` — en tables
- `AWESOME.md` — `- [Name](url) - Description.` bullets, period-terminated, awesome-lint clean
- `data/tools.json` — published machine-readable artifact
- `skills/literature-review-tools/reference/catalog.md` — **coordinate before wiring; `skills/` is being edited by another agent this session** (see §6)

### 1.3 Validator — `scripts/validate.py`

Fails CI on: duplicate `id`/`repo`, unknown `category`/`stage`, missing bilingual description, `desc_*` over ~120 chars, description not ending in `.` (awesome-lint requirement), malformed `repo` slug.

### 1.4 Drift gate — CI

```yaml
- run: python3 scripts/validate.py
- run: python3 scripts/build.py
- run: git diff --exit-code   # generated files must already be committed
```

### 1.5 Migration

One-off `scripts/migrate_readme_to_yaml.py` parses the existing tables into `tools.yaml`; then diff regenerated output against current files to prove the migration is byte-faithful before deleting the parser.

**Acceptance criteria**

- [x] `make build` regenerates all surfaces; `git diff` is empty on a clean tree
- [x] A new tool can be added in a single YAML block, with CI proving all four surfaces updated
- [x] `CONTRIBUTING.md` rewritten: "edit both READMEs" → "edit `data/tools.yaml`"
- [x] Tool count in badge/tagline generated from the data, not typed

**Not shipped from the proposed schema:** the `stage` and `install` fields. Nothing
consumes them until the Phase 3 site and the Phase 4 stage matrix exist, and
back-filling 66 entries with guessed workflow stages would be curation-by-assertion.
Add them alongside the consumer that needs them.

**Effort:** ~1 focused day. **Impact:** unblocks every later phase.

---

## Phase 2 — Trust and freshness signals

**Goal:** the list answers "is this still alive, and can I legally use it?" — which stars never answer.

### 2.1 `scripts/update_stars.py` → `scripts/refresh_metadata.py`

One `GET /repos/{owner}/{repo}` already returns everything needed. Capture `stargazers_count`, `pushed_at`, `archived`, `license.spdx_id`, `language`, and write them back into `tools.yaml` instead of rewriting Markdown cells with a regex.

### 2.2 Stop swallowing failures

Today a 404 prints to stderr inside a weekly Action nobody reads. Instead:

- 404 → follow the GitHub redirect to detect renames; if genuinely gone, mark `status: dead`
- `archived: true` → mark `status: archived`
- Any status change → the workflow opens/updates a single tracking issue **"Health report: N entries need attention"**

### 2.3 Render the signals

Add a **Health** column: 🟢 active (pushed <90d) · 🟡 slowing (<1y) · 🔴 stale (>1y) · 🗄️ archived. Add license to the table (researchers care — the current #1 pick is CC-BY-**NC**, which materially restricts commercial use and is worth surfacing on the list, not buried in `docs/research-notes.md`).

### 2.4 Auto-generated `HEALTH.md`

Full metadata dump: every tool with stars, last push, license, status. Costs nothing to generate and is the kind of page that gets linked to.

**Acceptance criteria**

- [ ] Weekly Action refreshes YAML metadata and regenerates all surfaces in one commit
- [ ] A renamed or archived upstream repo produces a tracking issue within a week
- [ ] Every table row shows health + license

**Effort:** ~half a day on top of Phase 1. **Impact:** turns a link list into a maintained reference.

---

## Phase 3 — Surfaces people actually return to

### 3.1 Searchable site (GitHub Pages)

Single `docs/index.html` + `data/tools.json`, no build step, no framework: instant client-side filter by category / stage / language / license / health, free-text search, dark mode, deep-linkable filters (`?stage=screen`). Reuse the existing banner and social-preview art so branding carries over.

This is what makes the project shareable *as a product* rather than as a README screenshot.

### 3.2 Keep the Claude skill generated, not copied

`skills/literature-review-tools/reference/catalog.md` becomes a build output. The hand-written routing logic in `SKILL.md` stays hand-written. **Blocked on coordination — see §6.**

### 3.3 Dataset as a public artifact

Publish `data/tools.json` and document its schema in `docs/DATA.md`. Explicitly invite reuse. Datasets get forked and cited; tables get screenshotted.

### 3.4 Monthly changelog

`CHANGELOG.md`, generated from `added`/`status` changes: *"July: +6 tools, 2 archived, MinerU crossed 75k."* This is the single cheapest mechanism for repeat visits.

**Effort:** ~1 day (site is the bulk). **Impact:** the difference between 1 visit and 12.

---

## Phase 4 — Editorial depth (the real moat)

Anyone can clone a link list in an afternoon. Nobody can clone verified hands-on experience.

> ⚠️ **Overlap:** a `skills/literature-review-tools/recipes/recipes.json` is being authored in parallel. Decide one home before writing more: either recipes are *skill data* (stay under `skills/`, and the repo-facing `recipes/*.md` are generated from that JSON) or they are *repo content* (live at root, and the skill consumes them). Do not maintain both by hand.

- **`recipes/` — 5–8 end-to-end, actually-run workflows.** e.g. *"200 PDFs → MinerU → PaperQA2 index → cited answers"*, *"topic → STORM outline → citation check against OpenAlex"*, *"3,000 abstracts → ASReview active-learning screen → PRISMA flow diagram"*. Each with commands, runtime, cost, and a note on where it breaks. Screenshot or transcript required — no recipe ships unrun.
- **Stage × Tool matrix.** One grid: rows = the 8 workflow stages, columns = top tools, cells = ✅ / ⚠️ / ❌. Makes coverage gaps visible at a glance and is inherently screenshot-shaped.
- **Honest head-to-heads.** Same task through 3 tools, documented outcome. Even one such comparison outranks another 20 catalog entries in value.
- **Deepen the ⭐ picks.** Each editor's pick gets a short "why this, when not this" paragraph. Curation with a stated opinion is the product.

**Effort:** ongoing, ~1 recipe/week. **Impact:** highest long-term; this is what gets cited rather than merely starred.

---

## Phase 5 — Distribution

Assets are already drafted (`docs/promo-zhihu.md`, `docs/promo-en.md`, `docs/awesome-re-submission.md`) but unpublished.

1. **awesome.re** — the submission doc correctly concludes the list is too new. Revisit after ~4 weeks of commit/PR history. Resolve the flagged `CONTRIBUTING.md` vs `contributing.md` casing question before submitting.
2. **Repo hygiene for discovery** — topics (`awesome`, `literature-review`, `ai-agents`, `claude-skills`, `mcp`, `systematic-review`), `CITATION.cff` (a research-tool list *should* be citable), enable Discussions.
3. **Publish the drafted posts** — 知乎/公众号 first (the zh README is the stronger asset), then HN/Reddit once the site from Phase 3 exists. Lead with the site or the stage matrix, not the raw README.
4. **Tool of the month** — one short writeup, cross-posted. Sustains attention between big pushes.

---

## 6. Coordination and risks

| Risk | Mitigation |
|---|---|
| **Concurrent edits to `skills/`** — another agent owns that tree this session | Phases 1–2 touch only `data/`, `scripts/`, `.github/`, root Markdown. Do **not** wire `catalog.md` into `build.py` until that work lands and is merged. |
| Generated files clobbering hand-written prose | Marker-delimited generated regions only; prose outside markers is never touched by `build.py` |
| Star-refresh bot spamming commits | Batch to one weekly commit; skip commits where only star noise changed under a threshold |
| Over-automating descriptions | Descriptions stay hand-written. Automation covers metadata only — the curation *is* the value |
| Migration corrupting the catalog | Byte-diff regenerated output against current files before deleting the migration script |

---

## 7. Sequencing

| # | Work | Effort | Impact | Blocks |
|---|---|---|---|---|
| ~~1~~ | ~~`data/tools.yaml` + `build.py` + drift-gate CI~~ | ✅ done | 🔥🔥🔥 | — |
| 2 | `refresh_metadata.py`, health/license signals, `HEALTH.md` | 0.5d | 🔥🔥🔥 | needs 1 |
| 3 | GitHub Pages searchable site + `tools.json` | 1d | 🔥🔥 | needs 1 |
| 4 | Skill catalog generated from SSOT | 0.5h | 🔥 | needs 1 + skills-agent merge |
| 5 | `recipes/` — first 3 verified workflows | 3× half-day | 🔥🔥🔥 | none |
| 6 | Stage × Tool matrix | 2h | 🔥🔥 | needs 1 |
| 7 | `CHANGELOG.md` generation | 2h | 🔥 | needs 1+2 |
| 8 | Repo hygiene: topics, `CITATION.cff`, Discussions | 30m | 🔥 | none |
| 9 | Publish 知乎 post; awesome.re after ~4 weeks | — | 🔥🔥 | needs 3 |

### Next three commits

1. ~~`feat(data): introduce data/tools.yaml as single source of truth`~~ ✅
2. ~~`feat(ci): generate all Markdown surfaces from tools.yaml and gate on drift`~~ ✅
3. `feat(data): capture freshness, archived state, and license from the GitHub API` ← next

---

## 8. What success looks like in 90 days

- Adding a tool is a one-block YAML PR; no surface can silently drift
- Every entry shows how alive it is and under what license — refreshed weekly, with dead entries flagged automatically
- A searchable site is the thing people share, and `tools.json` is the thing people fork
- 5+ verified end-to-end recipes exist that no competing list has
- The list is on awesome.re, and there is a monthly reason to come back
