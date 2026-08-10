# 06 — Six indexes, one corpus, zero keys

**Stage:** search · **No API key, no install** · **Run 2026-08-10**

Everyone searches one database. This runs six — OpenAlex, Crossref, Semantic
Scholar, PubMed, Europe PMC, arXiv — over the same query, merges the results by
DOI, and then tries to fetch the actual papers through the open-access chain.
Both scripts are **standard library only**: `python3 script.py`, nothing installed.

Query: `large language models for systematic review automation`, 10 hits per source.

## Result

| | |
|---|---|
| Sources queried | 6 (**5 answered**, Semantic Scholar returned HTTP 429) |
| Raw hits | 50 |
| Unique papers after dedup | **47** |
| Papers found by more than one source | **1** |
| With a DOI / with an abstract | 39 / 40 |
| Search time | **15 s** |
| Full texts recovered, no keys | **33 of 47 (70%)** — 27 PDFs + 6 OA full-text XML |
| Resolution time | 3 min 46 s (dominated by downloading 42 MB) |
| Cost | none — no key, no venv, no account |

## The finding: six indexes barely overlap

**Of 47 unique papers, exactly one was returned by more than one source.**

| Source | Hits | Contributed to the unique set |
|---|---|---|
| OpenAlex | 10 | 10 |
| PubMed | 10 | 10 |
| arXiv | 10 | 10 |
| Europe PMC | 10 | 9 |
| Crossref | 10 | 8 |
| Semantic Scholar | 0 | — (rate-limited out) |
| **Total** | 50 | **47** |

These are not six views of one ranked list. They are six different literatures.
Searching only OpenAlex on this query would have surfaced 10 of the 47 papers a
six-source search finds — and the missing 37 are not junk: the PubMed and Europe
PMC hits are the clinical-screening papers, the arXiv hits are the method papers.

Two consequences worth taking seriously:

- **"I searched the literature" via one API is a much weaker claim than it sounds.**
  Recall, not precision, is the binding constraint in a review.
- Deduplication has to be real. Three of the 50 raw hits were duplicates: one
  shared DOI, and **two preprint/published pairs that only `--dedup-titles`
  catches**, because the arXiv preprint and the journal version carry different
  DOIs and would otherwise both enter the corpus as separate "evidence".

## Then: 33 of 47 papers, legally, with no credentials

`resolve_oa.py` walks an escalating chain per DOI and stops at the first hit.

| Resolver | Recovered | Note |
|---|---|---|
| Unpaywall | — | **skipped**: the API requires an email; none was supplied |
| OpenAlex | 16 | keyless; its `oa_url` is often a landing page, so bytes are checked |
| arXiv | 10 | anything carrying an arXiv id |
| Europe PMC | 7 | OA full-text XML → plain text, biomedical only |
| CORE | — | skipped: needs `CORE_API_KEY` |
| **Closed** | **14** | reported as closed in `oa_report.json`, not silently dropped |
| **Unknown to Crossref** | **0** | a DOI nothing can resolve *and* Crossref never registered |

Supplying `UNPAYWALL_EMAIL` (free) and `CORE_API_KEY` (free) would only raise this.
70% is the **floor**, achieved with no account of any kind.

Nothing here bypasses a paywall. The 14 closed papers stay closed; the report
names them so a human can decide about interlibrary loan.

The `closed` / `not-in-crossref` split matters more than it looks: "paywalled" and
"this DOI was never registered" are the same symptom with opposite meanings, and only
the second one means somebody invented a citation.

## What running it taught us

1. **Semantic Scholar's keyless pool is effectively unavailable.** It returned 429
   on every search attempt across three runs, while single-paper lookups on the same
   host succeeded. Its ranking is the best of the six for conceptual queries, so
   `S2_API_KEY` (free) is the single highest-value key here — but the pipeline must
   treat a dead source as normal, not fatal. Ours logs it in `results.json` and
   continues.
2. **Europe PMC's relevance ranking is aggressively recent.** All 9 of its
   contributions were published in 2026. It is the right tool for "what landed this
   year" and the wrong one for "what is the foundational work" — pair it with
   OpenAlex, which surfaced the older, more-cited papers on the same query.
3. **An open-access flag is not a file.** OpenAlex's `oa_url` frequently points at a
   publisher landing page. Checking `Content-Type` is not enough either — publishers
   serve HTML block pages as `application/pdf`. The only reliable test is the magic
   bytes `%PDF-`, which is why `is_pdf()` exists.
4. **Europe PMC full text needs structure-aware extraction.** A naive
   `itertext()` over the JATS XML prepends journal codes, PMC ids and licence
   boilerplate before the title. Pulling `article-title` + `abstract` + `body`
   turned an unreadable dump into clean prose.
5. **The `not-in-crossref` check caught our own bug, on this very run.** The first
   pass reported one DOI that Crossref had never registered:
   `10.3886/icpsr38464.v5`, attached to a stroke-imaging review. That DOI is real —
   it is an **ICPSR dataset** in DataCite, not the paper. Cause: a PubMed record
   embeds its entire reference list, each reference carrying its own
   `<ArticleId IdType="doi">`, so an XPath sweep of `.//ArticleId` returns *a cited
   paper's* DOI instead of the article's. Scoping the lookup to
   `./PubmedData/ArticleIdList` fixed it, and the corrected run resolves **two more
   full texts** (33 vs 31) with **zero** unregistered DOIs. A pipeline that had
   silently mismatched titles to DOIs would have produced citations that look
   perfect and point at the wrong object.
6. **The corpus is 42 MB for 33 papers.** Plan disk for real reviews, and use
   `--skip-existing` when re-running.

## Reproduce it

```bash
cd skills/literature-review-tools

python3 scripts/fetch_papers.py \
  --query "large language models for systematic review automation" \
  --sources openalex,crossref,semanticscholar,pubmed,europepmc,arxiv \
  --max 10 --dedup-titles --outdir ./corpus

python3 scripts/resolve_oa.py --from-json ./corpus/results.json --outdir ./corpus
```

Or as one launcher workflow:

```bash
python3 scripts/litrun.py workflow run topic-to-fulltext \
  --query "large language models for systematic review automation" --max 10
```

Add `--email you@example.com` to `resolve_oa.py` to enable the Unpaywall step.
Append `topic-to-fulltext-review` instead to send the resulting full texts
straight into PaperQA2 (that step needs `OPENAI_API_KEY`).

## Honest limits

- **One query, one machine, one day.** The disjointness result is stark enough to
  be structural, but n=1 query. A biomedical query would tilt further toward
  PubMed/Europe PMC; a pure-ML query toward arXiv.
- **Relevance was not judged.** These are counts, not quality. Six indexes finding
  different papers does not prove the extra 37 are all worth reading — some
  Europe PMC hits are peer-review records rather than studies.
- **`--max 10` is small.** Overlap would grow with deeper result sets; the point is
  that the *top* of each ranking, which is what anybody actually reads, barely
  intersects.
- **Timings are network-bound** and will vary with location and API load.

## Files

Both scripts live in the skill, not here, because they are part of the shipped
tooling: [`skills/literature-review-tools/scripts/fetch_papers.py`](../../skills/literature-review-tools/scripts/fetch_papers.py)
and [`resolve_oa.py`](../../skills/literature-review-tools/scripts/resolve_oa.py).
Per-API endpoint notes and failure modes:
[`skills/literature-review-tools/reference/apis/`](../../skills/literature-review-tools/reference/apis/).
