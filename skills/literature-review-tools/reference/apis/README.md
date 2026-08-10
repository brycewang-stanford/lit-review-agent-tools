# Scholarly APIs — route the question to the right index

The rest of this skill installs tools. This directory does the opposite: it lets you
answer a literature question **with one HTTP call and nothing installed**, and it
documents the exact endpoints the bundled `fetch_papers.py` / `resolve_oa.py` scripts
use, so you can debug or extend them.

Reach for this when the user wants *a specific paper, a DOI resolved, an author's
output, an OA PDF, or a citation graph* — a venv is overkill for that. Reach for the
launcher when the user wants a corpus, a screening run, or an extraction pipeline.

> Layout modelled on the excellent [`paper-lookup`](https://github.com/K-Dense-AI) skill
> by K-Dense Inc. The endpoints, quirks and failure modes here were re-verified against
> live APIs on 2026-08-10 and annotated with what this repo's scripts actually hit.

## Pick a database

| The user wants… | Query this | Then |
|---|---|---|
| Papers on a topic, any field | OpenAlex | Semantic Scholar for citation context |
| Papers on a biomedical topic | PubMed | Europe PMC for the full text |
| Full text of a biomedical paper | Europe PMC (OA subset) | Unpaywall for non-biomed |
| Physics / maths / CS preprints | arXiv | Semantic Scholar for the published version |
| Biology / health preprints | Europe PMC (`SRC:PPR`) | bioRxiv/medRxiv APIs *by DOI or date only* |
| One paper by DOI | Crossref | OpenAlex for citations, Unpaywall for the PDF |
| An open-access PDF for a DOI | Unpaywall → OpenAlex → Europe PMC | `resolve_oa.py` already chains these |
| Who cites whom | Semantic Scholar | OpenAlex `referenced_works` |
| An author's publications | OpenAlex | Semantic Scholar author endpoint |
| Journal / funder / license metadata | Crossref | OpenAlex `sources` |
| PMID ↔ PMCID ↔ DOI | NCBI ID Converter | Europe PMC search |

**One query, several indexes.** Relevance ranking differs enough between these APIs
that the same query returns largely disjoint top-10s — in the run recorded in
[`recipes/06-multi-source-search`](../../../../recipes/06-multi-source-search/), six
sources returned 50 hits of which only 3 were duplicates. If coverage matters, do not
trust one index; run `fetch_papers.py` and let it merge them.

## Identifier formats

| Identifier | Shape | Example | Understood by |
|---|---|---|---|
| DOI | `10.xxxx/…` | `10.1136/bmj.n160` | everything |
| PMID | digits | `33781993` | PubMed, Europe PMC, S2 (`PMID:`) |
| PMCID | `PMC` + digits | `PMC8005925` | Europe PMC, PMC |
| arXiv id | `YYMM.NNNNN` | `2103.15348` | arXiv, S2 (`ARXIV:`), OpenAlex |
| OpenAlex id | `W` + digits | `W2741809807` | OpenAlex |
| S2 id | 40-char hex | `649def34f8be…` | Semantic Scholar |
| ORCID | `0000-…-…-…` | `0000-0001-6187-6610` | OpenAlex, Crossref |

Cross-lookup prefixes: OpenAlex takes `/works/doi:10.…` and `/works/pmid:…`;
Semantic Scholar takes `DOI:…`, `PMID:…`, `PMCID:…`, `ARXIV:…`.
A DOI that 404s in one index is usually alive in another — try before concluding it is fake.

## Keys: what is actually needed

Everything below works with **no key**. Keys only buy rate limit.

| API | Env var | Without it |
|---|---|---|
| OpenAlex | `OPENALEX_API_KEY` / `OPENALEX_MAILTO` | works; shared pool |
| Crossref | `CROSSREF_MAILTO` | works at ~5 req/s; `mailto` doubles it |
| Semantic Scholar | `S2_API_KEY` | **frequently HTTP 429** — the shared pool is often exhausted |
| NCBI (PubMed) | `NCBI_API_KEY`, `NCBI_EMAIL` | 3 req/s instead of 10 |
| Unpaywall | `UNPAYWALL_EMAIL` | **skipped entirely** — the API requires an email |
| Europe PMC | — | no key exists |
| arXiv | — | no key; 1 request / 3 s |
| CORE | `CORE_API_KEY` | skipped; registration required |

Read keys from the environment, then from `~/.lit-review-tools/.env`
(`litrun.py env --set KEY=VALUE`). Never invent an email for Unpaywall — ask the user.

## Per-API references

| API | File | Used by |
|---|---|---|
| OpenAlex | [`openalex.md`](openalex.md) | `fetch_papers.py`, `resolve_oa.py`, `fetch_openalex.py` |
| Crossref | [`crossref.md`](crossref.md) | `fetch_papers.py`, recipe 03 (citation verification) |
| Semantic Scholar | [`semantic-scholar.md`](semantic-scholar.md) | `fetch_papers.py` |
| PubMed / PMC (NCBI) | [`pubmed-pmc.md`](pubmed-pmc.md) | `fetch_papers.py`, `fetch_pubmed.py` |
| Europe PMC | [`europepmc.md`](europepmc.md) | `fetch_papers.py`, `resolve_oa.py` |
| arXiv | [`arxiv.md`](arxiv.md) | `fetch_papers.py`, `fetch_arxiv.py` |
| Unpaywall, CORE, bioRxiv/medRxiv | [`open-access.md`](open-access.md) | `resolve_oa.py` |

## Calling them

Claude Code: `WebFetch`, or `curl` via Bash when you need the raw bytes or a POST.
Always send a `User-Agent` that identifies you; several of these APIs throttle
anonymous clients harder. If you get 429, wait ~3 s and retry **once**, then move on
to another source rather than hammering.

## Reporting back

State which APIs you queried and which returned nothing — a silent omission reads as
"no such paper exists", which is a much stronger claim than "OpenAlex had no match".
Quote DOIs verbatim, and if a DOI failed to resolve anywhere, say so rather than
paraphrasing it into a plausible-looking citation.
