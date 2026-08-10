# OpenAlex

Broadest of the free indexes: ~250M works across every field, with authors,
institutions, sources, topics, citation counts and OA locations. No key required.
Base URL `https://api.openalex.org`.

Used by `fetch_papers.py` (search), `resolve_oa.py` (step 2 of the OA chain) and
`fetch_openalex.py`.

## Auth & limits

- Keyless works. `?api_key=…` (`OPENALEX_API_KEY`) or the legacy polite pool
  `?mailto=you@example.com` (`OPENALEX_MAILTO`) raise the limit.
- 100 req/s ceiling. Single-entity lookups by id/DOI are unmetered; list and search
  queries draw on a daily free allowance.

## Endpoints

```
GET /works/{id}                     W2741809807 | doi:10.1136/bmj.n160 | pmid:33781993
GET /works?search=…&per_page=25     full-text search over title+abstract+fulltext
GET /works?filter=…                 comma-separated field:value, all ANDed
GET /authors?search= | /sources?search= | /institutions?search= | /topics/{id}
```

Useful parameters:

| Param | Notes |
|---|---|
| `search` | boolean `AND`/`OR`/`NOT` (uppercase), `"phrase"~5`, `wildcar*`, `fuzzy~1` |
| `search.semantic` | embedding search, beta — 1 req/s, ≤50 results |
| `filter` | `from_publication_date:2023-01-01`, `publication_year:2024`, `type:article`, `is_oa:true`, `cited_by_count:>100`, `authorships.author.id:A…`, `institutions.country_code:us`, `doi:…`. Operators `>` `<` `!` `\|` |
| `sort` | `cited_by_count:desc`, `publication_date:desc`, `relevance_score:desc` |
| `select` | trim the response — works on both list and single-entity endpoints |
| `group_by` | aggregate counts, e.g. `group_by=publication_year` for a topic's trend line |
| `cursor=*` | deep pagination past 10,000; follow `meta.next_cursor` until null |

## Response shape (fields worth reading)

```json
{"id":"https://openalex.org/W2741809807","doi":"https://doi.org/10.7717/peerj.4375",
 "display_name":"…","publication_year":2018,"type":"article","is_retracted":false,
 "cited_by_count":1169,
 "open_access":{"is_oa":true,"oa_status":"gold","oa_url":"…"},
 "best_oa_location":{"pdf_url":"…","license":"cc-by","version":"publishedVersion"},
 "primary_location":{"source":{"display_name":"PeerJ","issn_l":"2167-8359"}},
 "authorships":[{"author":{"id":"…","display_name":"…"},"institutions":[…]}],
 "abstract_inverted_index":{"Despite":[0],"growing":[1]},
 "referenced_works":["https://openalex.org/W…"],
 "ids":{"doi":"…","pmid":"…","arxiv":"…"}}
```

Two gotchas that bite every time:

- **`title` does not exist** on the work object — the field is `display_name`.
- **Abstracts are inverted indexes**, `{word: [positions]}`. Rebuild by placing each
  word at each position and joining in index order (`_inverted()` in `fetch_papers.py`).
- `is_retracted` is a free retraction check — cheaper than a dedicated service, and
  worth reading before you cite anything (see recipe 03).

## What it is good and bad at

Good: coverage, OA links, citation counts, institution/author disambiguation, trend
aggregation via `group_by`.
Bad: relevance ranking is weaker than Semantic Scholar's for conceptual queries, and
`open_access.oa_url` is often a **landing page, not a PDF** — always check the bytes
start with `%PDF-` before saving one (`resolve_oa.py` does).
