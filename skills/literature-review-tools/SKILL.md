---
name: literature-review-tools
description: >-
  Recommend open-source AI tools, agents, Claude Code / Codex skills, and MCP
  servers for any stage of a literature review — searching, reading, extracting,
  synthesizing, screening, citation-checking, and paper writing. Use when the
  user asks "what tool should I use to..." for research/lit-review work, wants to
  automate a survey or related-work section, needs PDF→Markdown extraction for
  LLMs, is running a PRISMA / systematic review, wants to wire papers into
  Claude/Cursor via MCP, or asks to chat with a Zotero library. Curated catalog
  of 70+ vetted projects, organized by use case. 支持中英文（也用于「文献综述工具选型」）。
---

# Literature Review Tools — Selection Guide

A curated, use-case-organized catalog of the strongest **open-source** AI tools for
literature review: end-to-end research agents, deep-research / auto-survey generators,
autonomous "idea→paper" systems, citation-backed RAG over PDFs, PRISMA screening,
MCP servers, Zotero/Obsidian integrations, PDF→structured extraction, citation
graphs, and paper-writing / peer-review assistants.

Full source of truth (README, always current star counts): <https://github.com/brycewang-stanford/lit-review-agent-tools>

## How to use this skill

1. Identify **which stage** of the lit-review workflow the user is on (search → read → extract → synthesize → screen → cite-check → write/review).
2. Match it to a category below and recommend the **⭐ editor's pick first**, then 1–2 alternatives.
3. For anything beyond the top pick — full star counts, every project in a category, or a category not summarized here — read [`reference/catalog.md`](reference/catalog.md). Do **not** guess project names or URLs; pull them from the catalog.
4. Give a one-line "why this one" tied to the user's constraint (Claude Code vs. standalone, open vs. commercial, privacy/local, medical, etc.).

## ⚡ 30-second picker

```text
Use Claude Code, want end-to-end research→paper ──────────▶ academic-research-skills ⭐
Want AI to research a topic → cited report ───────────────▶ GPT Researcher / STORM
Want fully autonomous "idea → submittable paper" ────────▶ AI-Scientist-v2 / AutoResearchClaw
Citation-backed Q&A over a pile of PDFs ──────────────────▶ PaperQA2
Rigorous PRISMA review (thousands of abstracts) ─────────▶ ASReview / prismAId
Clean Markdown from PDFs to feed an LLM ─────────────────▶ MinerU / Docling / marker
Lit capabilities inside Claude / Cursor (MCP) ───────────▶ paper-search-mcp / zotero-mcp
Chat with your library inside Zotero ────────────────────▶ zotero-gpt / PapersGPT
Pre-submission AI peer review ───────────────────────────▶ open_reviewer / ai-peer-review
```

## Categories (top pick per category)

| Category | Editor's pick ⭐ | When |
|---|---|---|
| All-in-one research agents & skills | **academic-research-skills** | Claude Code user wanting research→write→review→revise, with integrity/citation gates |
| Deep research & auto-survey | **STORM** / **gpt-researcher** | Topic → cited survey / report / related-work |
| Autonomous science (idea→paper) | **AI-Scientist(-v2)** / **AutoResearchClaw** | Fully automated discovery: lit + hypotheses + experiments + writing |
| Literature Q&A / RAG | **paper-qa (PaperQA2)** | Citation-backed answers over a PDF corpus |
| Systematic review & screening | **ASReview** | Active-learning screening of thousands of abstracts (PRISMA) |
| MCP servers | **zotero-mcp** / **arxiv-mcp-server** | Wire papers into Claude / Cursor / Cline |
| Zotero / Obsidian integration | **zotero-gpt** | Chat with your library inside your reference manager |
| PDF → structured extraction | **MinerU** / **docling** / **marker** | Turn PDFs into clean Markdown/JSON for LLMs |
| Citation graphs & API clients | **scholarly** / **pyalex** | Citation-network analysis; scripting academic DBs |
| Writing & peer-review assistants | **open_reviewer** / **ai-peer-review** | Draft, polish, and pre-submission review |
| Awesome lists | **Awesome-Auto-Research-Tools** | Browse the whole landscape |

## Decision table (map need → recommendation)

| User's need | Recommend |
|---|---|
| Claude Code, end-to-end research→paper | **academic-research-skills** (most complete, #1 in space) |
| Generic "research this topic for me" agent | **GPT Researcher** / **STORM** |
| Wiki/survey-style long-form with citations | **STORM / Co-STORM** |
| Fully autonomous "idea → submittable paper" | **AI-Scientist-v2** / **AutoResearchClaw** |
| Cited Q&A over many PDFs | **PaperQA / PaperQA2** |
| Rigorous PRISMA systematic review | **ASReview** or **prismAId** |
| PDF → clean Markdown for an LLM | **MinerU / Docling / marker** |
| Lit capabilities in an MCP client | **paper-search-mcp / zotero-mcp** |
| Chat with library inside Zotero | **zotero-gpt / PapersGPT** |
| AI pre-review before submission | **open_reviewer / ai-peer-review** |
| Just want to browse the landscape | The **Awesome lists** section |

## Notes & caveats

- **Open-source is prioritized.** Commercial/closed tools (Elicit, Consensus, Scite, SciSpace, Research Rabbit, Connected Papers) are listed for reference only — see the catalog's commercial section.
- **Star counts drift.** The catalog's numbers are periodic GitHub-API snapshots — treat as rough popularity signals, not exact. For live numbers, point the user at the repo.
- **Match the constraint, not just the task.** Privacy/local → `local-deep-research`; medical → `medsci-skills` / `paperai`; Codex instead of Claude → `academic-research-skills-codex`.

Full catalog with every project, star count, and one-line description: [`reference/catalog.md`](reference/catalog.md).
