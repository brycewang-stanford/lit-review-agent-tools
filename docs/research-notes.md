# Literature Review Skills & Tools on GitHub — Landscape Review

*Compiled July 2026. Star counts are approximate and change over time.*

## TL;DR

The single most popular repo for **literature-review skills/tools** is
**[academic-research-skills](https://github.com/Imbad0202/academic-research-skills)** (~39.4k★)
— a suite of **Claude Code skills** that runs a full `research → write → review → revise → finalize`
pipeline with human-in-the-loop integrity gates. It far outranks every other lit-review-specific
project. The rest of the ecosystem splits into three camps: **autonomous research agents**
(GPT Researcher, PaperQA), **systematic-review screening tools** (ASReview, prismAId), and
**curated "awesome" lists**.

---

## 1. The clear #1: academic-research-skills

| | |
|---|---|
| **Repo** | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) |
| **Stars** | ~39.4k |
| **License** | CC-BY-NC 4.0 |
| **What it is** | A suite of Claude Code skills for the whole academic research lifecycle |

**How it works** — 4 Claude Code skills orchestrated as a 10-stage pipeline:

1. **Deep Research** (13-agent research team, 8 modes)
2. **Academic Paper** (12-agent writing pipeline, 11 modes)
3. **Academic Paper Reviewer** (7-agent multi-perspective peer review)
4. **Academic Pipeline** (10-stage orchestrator with integrity gates)

**Literature-review–specific capabilities** (in the Deep Research skill):
- **Full mode** — comprehensive literature mapping, verified against the Semantic Scholar API
- **Systematic-review mode** — PRISMA-compliant structured reviews
- **Lit-review mode** — thematic literature synthesis
- **Three-way-scan mode** — WHY / HOW / WHAT paper triage
- **Fact-check mode** — verification against cited sources
- Cross-index triangulation across **Semantic Scholar + OpenAlex + Crossref**, plus contamination
  detection and optional cross-model verification

**Design philosophy:** *"AI is your copilot, not the pilot."* Every stage needs user confirmation;
integrity gates (stages 2.5 & 4.5) run a 7-mode blocking checklist to surface — rather than hide —
verification failures.

**Install:** `/plugin install academic-research-skills` (Claude Code v3.7.0+).
**Cost:** roughly $4–6 per 15k-word paper.

> There's also a Codex-native sibling, [academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) (~7k★).

---

## 2. Autonomous research agents

| Repo | Stars | What it does |
|---|---|---|
| [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) | ~27k | Autonomous agent that runs deep research on any topic and produces a cited report. General-purpose, not academic-only. |
| [Future-House/paper-qa](https://github.com/Future-House/paper-qa) | ~8.8k | High-accuracy RAG for answering questions from scientific papers **with citations**. PaperQA2 claims superhuman literature-search accuracy. |
| [a554b554/AutoSurveyGPT](https://github.com/a554b554/AutoSurveyGPT) | small | Auto-generates a literature survey by finding & ranking Google Scholar papers with GPT. |

---

## 3. Systematic-review & screening tools

| Repo | Stars | What it does |
|---|---|---|
| [asreview/asreview](https://github.com/asreview/asreview) | ~0.9k | Active-learning tool for systematic-review screening; interactively ranks papers to cut screening time. Well-established in the academic community. |
| [Open-and-Sustainable/prismAId](https://github.com/Open-and-Sustainable/prismAId) | — | Generative-AI toolkit for protocol-based systematic reviews; no-code, replicable screening & extraction. |
| ReviewAid / Abstrackr | — | Open-source full-text screening & data-extraction assistants for systematic reviews. |

---

## 4. Curated "awesome" lists (great starting points)

- [evidencesynthesis-tools/awesome-evidence-synthesis](https://github.com/evidencesynthesis-tools/awesome-evidence-synthesis) — open-source tools for systematic reviews, meta-analysis & evidence synthesis
- [0x11c11e/awesome-ai-research-tools](https://github.com/0x11c11e/awesome-ai-research-tools) — AI tools for lit reviews, citation management, data analysis
- [handsome-rich/Awesome-Auto-Research-Tools](https://github.com/handsome-rich/Awesome-Auto-Research-Tools) — automated literature search, paper reading, experiment management
- GitHub topics: [`literature-review`](https://github.com/topics/literature-review), [`systematic-reviews`](https://github.com/topics/systematic-reviews)

---

## 5. Honorable mentions (Claude Code / MCP ecosystem)

| Repo | Stars | Note |
|---|---|---|
| [ScienceClaw](https://github.com/beita6969/ScienceClaw) | ~0.9k | Self-evolving AI research colleague, 285 skills, "zero hallucination" claim |
| [cookjohn/zotero-mcp](https://github.com/cookjohn/zotero-mcp) | ~1k | MCP server exposing Zotero for AI-driven literature retrieval & metadata |
| [OpenLAIR/dr-claw](https://github.com/OpenLAIR/dr-claw) | ~1k | "Research IDE" with many AI-assistant personas |
| [federicodeponte/opendraft](https://github.com/federicodeponte/opendraft) | ~0.3k | 19-agent open-source academic-paper writer |

---

## How to choose

- **You use Claude Code and want an end-to-end research→paper workflow** → **academic-research-skills** (the clear leader, and relevant to this project's environment).
- **You want a general autonomous "research this topic" agent** → **GPT Researcher**.
- **You need grounded Q&A over a corpus of PDFs with citations** → **PaperQA / PaperQA2**.
- **You're doing a rigorous PRISMA systematic review (screening thousands of abstracts)** → **ASReview** or **prismAId**.
- **You just want to browse the field** → start from the **awesome-* lists** above.

---

### Sources
- [github.com/topics/literature-review](https://github.com/topics/literature-review) (sorted by stars)
- [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)
- [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher)
- [Future-House/paper-qa](https://github.com/Future-House/paper-qa)
- [asreview/asreview](https://github.com/asreview/asreview)
- [Open-and-Sustainable/prismAId](https://github.com/Open-and-Sustainable/prismAId)
- [evidencesynthesis-tools/awesome-evidence-synthesis](https://github.com/evidencesynthesis-tools/awesome-evidence-synthesis)
