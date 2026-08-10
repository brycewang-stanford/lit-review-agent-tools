# Semantic Scholar (S2 Graph API)

~200M papers with the best free **citation graph** — citations, references, influential
citation counts, AI-generated TLDRs, and paper recommendations. Base URL
`https://api.semanticscholar.org/graph/v1`.

Used by `fetch_papers.py` (search). Its ranking is the most "semantic" of the free
indexes, which is why it is in the default source set.

## Auth & limits — read this first

The keyless pool is **shared across every anonymous client on the internet and is
routinely exhausted**. In this repo's recorded runs, keyless `/paper/search` returned
HTTP 429 on both attempts while single-paper lookups succeeded. Treat 429 as normal,
not as a bug: retry once, then continue without this source.

`S2_API_KEY` (free, request form on their site) goes in the `x-api-key` **header**,
not the query string.

## Endpoints

```
GET /paper/search?query=…&limit=20&fields=…       relevance search
GET /paper/search/bulk?query=…                    up to 1000/page, no relevance ranking
GET /paper/{id}?fields=…                          DOI:… | PMID:… | PMCID:… | ARXIV:… | CorpusId:… | 40-hex
GET /paper/{id}/citations?fields=…                who cites this
GET /paper/{id}/references?fields=…               what this cites
GET /paper/{id}/recommendations
GET /author/search?query=… | /author/{id}/papers
POST /paper/batch  {"ids":[…]}                    up to 500 ids in one call
```

`fields` is mandatory in practice — omit it and you get bare ids. Useful set:

```
title,abstract,year,authors,venue,citationCount,influentialCitationCount,
externalIds,openAccessPdf,isOpenAccess,url,tldr,fieldsOfStudy,publicationTypes
```

`year=2020-` filters a range; `openAccessPdf` gives a direct PDF URL when one exists.

## Response shape

```json
{"total":1234,"data":[{"paperId":"649def34…","title":"…","abstract":"…","year":2021,
 "venue":"BMJ","citationCount":9781,"influentialCitationCount":812,
 "externalIds":{"DOI":"10.1136/bmj.n160","PubMed":"33781993","ArXiv":null},
 "openAccessPdf":{"url":"…","status":"GOLD"},"tldr":{"text":"…"}}]}
```

`abstract` is often `null` even when the paper has one — S2 cannot redistribute every
publisher's text. Fall back to OpenAlex or Europe PMC for the abstract; that fallback
is exactly what `fetch_papers.py`'s merge step does.

## Good and bad at

Good: citation graph in both directions, `influentialCitationCount` (a better signal
than raw counts for "what actually mattered"), TLDRs, recommendations, batch lookup.
Bad: availability without a key, abstract coverage, non-English work.
