# arXiv

2.4M+ preprints in physics, maths, CS, quantitative biology, statistics, economics —
and, uniquely in this set, **every record has a free PDF**. No key.
Base URL `http://export.arxiv.org/api/query`.

Used by `fetch_papers.py` (search), `fetch_arxiv.py` (search + download) and
`resolve_oa.py` (last-resort PDF for anything with an arXiv id).

## Limits

One request per **3 seconds**, `max_results` ≤ 2000 per call (use `start` to page, and
stay under ~30k results per query). arXiv publishes and enforces this; exceeding it
gets your IP throttled. Bulk downloading of PDFs is against their terms — for whole-corpus
work they publish an S3 bucket instead.

## Query

```
GET /api/query?search_query=all:transformer&start=0&max_results=20&sortBy=relevance
```

| Prefix | Field |
|---|---|
| `all:` | everything |
| `ti:` `abs:` `au:` | title, abstract, author |
| `cat:` | category, e.g. `cat:cs.CL`, `cat:stat.ME` |
| `id_list=2103.15348` | fetch specific ids instead of searching |

Boolean `AND` / `OR` / `ANDNOT`, quotes for phrases, parentheses for grouping — all
must be URL-encoded. `sortBy`: `relevance` · `submittedDate` · `lastUpdatedDate`.

**There is no date filter.** The legacy API cannot express "since 2023"; either sort by
`submittedDate` and take the head, or over-fetch and filter client-side (what
`fetch_papers.py --from-year` does).

## Response — Atom XML, not JSON

```xml
<entry>
  <id>http://arxiv.org/abs/2103.15348v2</id>
  <published>2021-03-29T…</published><updated>…</updated>
  <title>…</title><summary>…</summary>
  <author><name>…</name></author>
  <arxiv:doi>10.1145/…</arxiv:doi>
  <arxiv:journal_ref>ACL 2021</arxiv:journal_ref>
  <arxiv:primary_category term="cs.CL"/>
  <link title="pdf" href="http://arxiv.org/pdf/2103.15348v2"/>
</entry>
```

Namespaces: `{"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}`.
`title` and `summary` arrive with hard line wrapping — collapse whitespace or every
title in your manifest carries newlines. The id ends in a **version suffix** (`v2`);
`https://arxiv.org/pdf/{id}` works with or without it.

`arxiv:doi` is present only once the preprint is published — most entries have none,
which is why arXiv records dedupe by title rather than DOI in `fetch_papers.py`, and
why `--dedup-titles` exists to fold the preprint into its published twin.

## Good and bad at

Good: guaranteed full text, fast, keyless, strong CS/physics/ML coverage, category
filters that actually work.
Bad: no peer review (a hit is not evidence), no date filter, no citation counts, and
nothing biomedical or social-scientific worth relying on.
