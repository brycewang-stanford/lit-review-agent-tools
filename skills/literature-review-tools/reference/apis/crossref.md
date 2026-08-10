# Crossref

The DOI registration agency's own metadata: ~160M records. This is the authority on
"does this DOI exist and what is it", plus journal, funder, license and reference-list
metadata. No key. Base URL `https://api.crossref.org`.

Used by `fetch_papers.py` (search) and by recipe 03, which verifies citations against it.

## Auth & limits

- Public pool ~5 req/s. Adding `?mailto=you@example.com` (`CROSSREF_MAILTO`) puts you
  in the **polite pool** with roughly double the allowance and human contact if you
  misbehave. A descriptive `User-Agent` matters here more than on other APIs.

## Endpoints

```
GET /works/{doi}                          one record — the canonical DOI check
GET /works?query.bibliographic=…&rows=20  search (whole-reference matching)
GET /works?query.title=…&query.author=…   fielded search
GET /journals/{issn}/works                everything in a journal
GET /members/{id}/works | /funders/{id}/works
```

| Param | Notes |
|---|---|
| `query.bibliographic` | best field for "here is a reference string, find it" |
| `filter` | `from-pub-date:2023-01-01`, `type:journal-article`, `has-abstract:true`, `is-update:true` (retraction/correction notices), `license.url:…` |
| `select` | trims the response — **list endpoints only** |
| `rows` / `offset` | ≤1000 rows; use `cursor=*` beyond 10k |
| `sort` / `order` | `relevance`, `published`, `is-referenced-by-count` |

## The 400 that wastes an hour

`select` is accepted on `/works?…` but **rejected on `/works/{doi}`**:

```
GET /works?query=prisma&rows=1&select=DOI,title   → 200
GET /works/10.1136/bmj.n160?select=DOI            → 400
```

If a single-DOI lookup 400s, drop `select` before concluding the DOI is bad.

## Response shape

```json
{"status":"ok","message":{"DOI":"10.1136/bmj.n160","title":["PRISMA 2020 …"],
 "container-title":["BMJ"],"issued":{"date-parts":[[2021,3,29]]},
 "author":[{"given":"Matthew J","family":"Page","ORCID":"…"}],
 "is-referenced-by-count":9781,"type":"journal-article",
 "abstract":"<jats:p>…</jats:p>","reference":[{"DOI":"…","unstructured":"…"}],
 "link":[{"URL":"…","content-type":"application/pdf"}],
 "update-to":[{"type":"retraction","DOI":"…"}]}
```

- `title` and `container-title` are **arrays**; take `[0]`.
- `abstract` is JATS XML when present at all (many publishers deposit none) — strip tags.
- `reference` gives you the paper's own bibliography, which is how you walk citations
  backwards without Semantic Scholar.
- `update-to` / `filter=is-update:true` surfaces retraction and correction notices.

## Good and bad at

Good: DOI truth, reference strings → records, funder/license metadata, retraction notices.
Bad: topical relevance search (it matches strings, not meaning), abstract coverage,
and it has no notion of open-access location — pair it with Unpaywall or OpenAlex.
