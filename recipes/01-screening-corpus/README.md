# 01 — Build a deduplicated screening corpus from OpenAlex

**Stage:** search · **No API key** · **Verified 2026-07-27, 18 seconds**

The first real task in a review is turning a question into a de-duplicated set of
candidate records with abstracts. OpenAlex covers ~240M works, is fully open, and
needs no key.

## Run it

```bash
pip install pyalex
python3 build_corpus.py "large language models for systematic review screening" --max 600
```

## Actual output

```
query      : 'large language models for systematic review screening' (from 2019)
kept       : 597 records -> corpus.csv
dropped    : 0 duplicate DOIs, 3 duplicate titles
open access: 546 have a direct PDF link (91%)
years      : 2019–2026
```

18 seconds wall clock, including pagination.

## What the script handles that a naive query doesn't

- **Abstracts arrive inverted.** OpenAlex ships `abstract_inverted_index`
  (`{word: [positions]}`), not text. The script reconstructs reading order.
  Miss this and every abstract is empty.
- **Two-key deduplication.** DOI first, then normalised title, because
  preprint/publisher pairs often share a title and not a DOI. Here that caught 3
  title duplicates that DOI matching alone would have kept.
- **`has_abstract=true` filter.** A screening corpus without abstracts is
  unscreenable; better to exclude those records than to discover it later.
- **Polite pool.** Setting `pyalex.config.email` gets faster service and means
  OpenAlex contacts you rather than silently rate-limiting.

## Output shape

`corpus.csv` with `title, abstract, doi, year, venue, cited_by, openalex_id,
oa_url` — the columns ASReview expects, so [recipe 02](../02-active-learning-screening/)
takes this file directly.

## Caveat found while running

91% of records advertised an `oa_url`, but those URLs do not reliably serve a
PDF — see [recipe 04](../04-pdf-to-markdown/), where the first candidate returned
an HTML block page from a `.pdf` address. Validate the magic bytes before you
trust a download.
