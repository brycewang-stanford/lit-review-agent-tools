# Recipes — workflows that were actually run

Every catalogue tells you a tool exists. Almost none tell you what happens when
you run it. These recipes were **executed end to end on this machine**, and the
numbers below are the output of those runs, not estimates.

**Rule for this directory: nothing ships unrun.** If a workflow could not be
executed here, it is listed under [Not verified](#not-verified) with the reason —
never written up from documentation.

Every recipe below needs **no API key and no paid service**.

| # | Recipe | Stage | Runtime | Verified |
|---|---|---|---|---|
| [01](01-screening-corpus/) | Build a deduplicated screening corpus from OpenAlex | search | 18 s | 2026-07-27 |
| [02](02-active-learning-screening/) | Cut screening by 94% with ASReview active learning | screen | ~30 s | 2026-07-27 |
| [03](03-verify-citations/) | Catch invented and retracted citations | cite-check | ~2 s/citation | 2026-07-27 |
| [04](04-pdf-to-markdown/) | Turn a paper into structured Markdown with docling | extract | 78 s / 29 pp | 2026-07-27 |

They chain: **01 → 02** (corpus to screener) and **04 → 03** (references out of a
PDF into the verifier). Both chains were run, and both surfaced problems that
only appear when you actually run them — see each recipe.

## Headline results

- **ASReview found all 38 relevant papers after screening 248 of 4,544 records
  (5.5%)** on a published systematic review's own data. 95% recall came at 214
  records. That is the single most load-bearing claim in this whole catalogue,
  and it holds up.
- **OpenAlex returned 597 usable records with abstracts in 18 seconds**, 91% with
  a direct open-access PDF link — no key, no institutional access.
- **The citation checker caught a retracted paper and an invented one** in a
  4-item test set. It also *falsely confirmed* a real citation until that bug was
  fixed; see recipe 03, which is the most useful thing in this directory.
- **docling converted a 29-page paper in 78 seconds on CPU**, reconstructing 7
  tables including the search-strategy table a systematic review actually needs.

## What running them actually taught us

Things that are invisible until you try:

1. **Open access does not mean downloadable.** 91% of corpus records advertised a
   PDF link. The first candidate (BMJ) served an HTML block page with a `.pdf`
   URL; it took 4 attempts to get a real PDF. Any pipeline that assumes
   `oa_url` → PDF will silently ingest HTML.
2. **PDF extraction corrupts DOIs.** Of 10 DOIs pulled from a converted reference
   list, 2 were unresolvable — one had a trailing `)`, and
   `10.1007/s40593013-0012-6` had lost a hyphen across a line break. Always
   validate extracted DOIs before treating a citation as missing.
3. **Title matching cannot confirm a citation.** "Attention Is All You Need"
   resolves in Crossref to a *different* 2025 paper, "Is Attention All You
   Need?", at 100% token overlap. Only a DOI confirms.
4. **"pip install" hides real costs.** docling pulls torch and downloads ~26 MB
   of OCR weights on first run. Budget the disk and the first-run latency.

## Not verified

These need an LLM API key or a paid search backend, which this environment does
not have. They are deliberately **not** written up:

| Tool | Blocker |
|---|---|
| PaperQA2 | Needs an LLM API key for embeddings and answers |
| STORM / Co-STORM | Needs an LLM key plus a search backend |
| GPT Researcher | Needs an LLM key plus a search API |
| AI-Scientist / AutoResearchClaw | Needs an LLM key, and runs experiments |
| Semantic Scholar API at volume | Returns HTTP 429 without a key |

If you have run any of these, a recipe following the same format — commands,
real output, runtime, and where it breaks — is the most valuable contribution
you can make to this repo. See [contributing.md](../contributing.md).

## Environment these were run in

macOS (Darwin 25.5.0, Apple silicon), Python 3.13.5, no GPU, home broadband.
`pyalex 0.21`, `asreview 3.0.8`, `docling 2.115.0`. Runtimes on a GPU box, or
behind an institutional proxy, will differ.
