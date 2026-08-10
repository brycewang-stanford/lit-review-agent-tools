# Claude Skill — `literature-review-tools`

This repo's curated catalog is also packaged as an installable **[Claude Agent Skill](https://docs.claude.com/en/docs/claude-code/skills)** — and it does three things:

- **Look up** — ask *"find recent papers on X"*, *"get me the PDF for this DOI"*, or *"does this citation exist?"* and it searches six scholarly APIs and fetches the open-access full text. **No install, no API key** — this is the cheap default.
- **Recommend** — ask *"what should I use to turn PDFs into Markdown for an LLM?"* and it routes you to the best open-source pick with a one-line rationale.
- **Run** — ask *"use MinerU to convert this PDF"* or *"ask PaperQA2 about these papers"* and Claude drives the bundled launcher to install the tool in an isolated venv and run it — no manual pip wrangling.

```text
skills/
└── literature-review-tools/
    ├── SKILL.md              # routing (look up / recommend) + launcher instructions (run)
    ├── recipes/
    │   ├── recipes.json      # machine-readable manifest of runnable tools
    │   └── workflows.json    # named multi-step pipelines
    ├── scripts/
    │   ├── litrun.py         # launcher: install/run/configure tools by id
    │   ├── fetch_papers.py   # 6-API search, deduplicated — stdlib only, no key
    │   ├── resolve_oa.py     # DOI → open-access full text — stdlib only, no key
    │   └── fetch_*.py        # single-source fetchers (arXiv / OpenAlex / PubMed)
    └── reference/
        ├── catalog.md        # full 70+ tool catalog (progressive disclosure)
        └── apis/             # per-API endpoints, quirks and failure modes
```

## Search without installing anything

Two bundled scripts use **only the Python standard library** — no venv, no pip, no key:

```bash
# six indexes at once (OpenAlex, Crossref, Semantic Scholar, PubMed, Europe PMC, arXiv)
python3 scripts/fetch_papers.py --query "active learning for screening" \
    --sources openalex,crossref,semanticscholar,pubmed,europepmc,arxiv \
    --max 15 --dedup-titles --outdir ./corpus

# then turn those DOIs into full text you may legally read
python3 scripts/resolve_oa.py --from-json ./corpus/results.json --outdir ./corpus
```

Measured in [recipes/06](../recipes/06-multi-source-search/): 50 raw hits → **47 unique
papers in 15 s**, of which only one was found by more than one source, and **33 came
back as legal full text with no API key at all**. Closed papers are reported as closed
in `oa_report.json` — nothing here routes around a paywall.

`reference/apis/` documents each API's endpoints and the failure modes that waste an
hour (Crossref's `select` 400 on single-DOI lookups, OpenAlex's inverted-index
abstracts, Semantic Scholar's exhausted keyless pool, PubMed's multi-part abstracts).

## The launcher (`litrun.py`)

Dependency-free (stdlib only). Installs each tool into its own venv under
`~/.lit-review-tools/` (prefers [`uv`](https://docs.astral.sh/uv/), falls back to
`python -m venv`), and reads API keys from one shared `~/.lit-review-tools/.env`.

```bash
scripts/litrun.py list                 # what can be run
scripts/litrun.py doctor               # toolchain + which API keys are set
scripts/litrun.py info mineru          # a tool's install/run details
scripts/litrun.py env --set OPENAI_API_KEY=sk-...
scripts/litrun.py run mineru -- -p paper.pdf -o ./out -b pipeline
scripts/litrun.py run paper-qa -- ask "What methods does this corpus use?"
scripts/litrun.py mcp arxiv-mcp-server # prints MCP config to register in Claude/Cursor
scripts/litrun.py ui gpt-researcher    # clone & launch the full web UI (:8000)

# chained pipelines
scripts/litrun.py workflow list
scripts/litrun.py workflow run topic-to-review \
  --query "cat:cs.CL retrieval augmented generation" --max 8 \
  --question "What evaluation benchmarks recur?" --dry-run   # preview, then drop --dry-run
```

Runnable tools today: **papers-fetch · oa-resolve** (six-API search and open-access
retrieval, zero install), **MinerU · marker · docling** (PDF→Markdown), **PaperQA2**
(cited Q&A), **ASReview** (PRISMA screening), **arxiv-fetch · openalex-fetch ·
pubmed-fetch** (single-source fetchers), **GPT Researcher · STORM** (deep
research), **scholarly · pyalex** (API clients), and the **arxiv / paper-search /
zotero** MCP servers.

Built-in workflows: `pdf-to-markdown`, `pdf-corpus-qa`, `pdf-md-then-qa`,
`topic-to-pdfs`, `topic-to-review` (arXiv → cited answer), `topic-to-review-multi`
(arXiv **+** OpenAlex → cited answer), `topic-to-related-work` (retrieve →
PaperQA2 drafts a cited related-work paragraph), `topic-to-corpus` (six sources →
deduplicated corpus, keyless), `topic-to-fulltext` (→ open-access full text,
keyless), and `topic-to-fulltext-review` (→ PaperQA2 over the full texts rather
than the abstracts). The 70+ catalog stays browse-only; more recipes/workflows are
easy to add to `recipes/`.

## Install

**As a plugin (recommended)** — the repo doubles as a Claude Code plugin marketplace:

```text
/plugin marketplace add brycewang-stanford/lit-review-agent-tools
/plugin install lit-review-agent-tools@lit-review-marketplace
```

That pulls in the skill *and* the launcher scripts in one step.

**Copy the skill folder** (Claude Code personal skills live in `~/.claude/skills/`):

```bash
git clone https://github.com/brycewang-stanford/lit-review-agent-tools
cp -r lit-review-agent-tools/skills/literature-review-tools ~/.claude/skills/
```

Restart Claude Code (or run `/doctor`) and the skill auto-loads. Claude invokes it
whenever your request matches literature-review tool selection — no manual trigger needed.

**Project-scoped:** copy the same folder into `.claude/skills/` inside any project.

**Other Agent-SDK / MCP hosts:** point your skills loader at
`skills/literature-review-tools/SKILL.md`.

## How it works

- **`SKILL.md`** carries the YAML frontmatter (`name`, `description`) Claude uses to
  decide *when* to activate, plus the lightweight routing logic (pickers + decision tables).
- **`reference/catalog.md`** holds the full catalog and is only read when Claude needs
  the complete list, exact star counts, or a category not summarized in `SKILL.md` —
  classic progressive disclosure so the base context stays small.
- **`reference/apis/`** is the same idea for retrieval: `SKILL.md` says *which* index
  to query, and the per-API page is read only when a call actually has to be made or
  debugged.

Star counts are periodic GitHub-API snapshots; the repo README is the live source of truth.
