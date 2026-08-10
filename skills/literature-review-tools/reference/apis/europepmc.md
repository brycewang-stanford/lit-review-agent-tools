# Europe PMC

The most underrated API in this set. It indexes PubMed **plus** preprints, patents,
agricultural and theses records, answers in JSON (no XML dance), needs no key, and
serves open-access **full text** from one endpoint.
Base URL `https://www.ebi.ac.uk/europepmc/webservices/rest`.

Used by `fetch_papers.py` (search) and `resolve_oa.py` (OA full-text step).

## Endpoints

```
GET /search?query=…&format=json&pageSize=25&resultType=core
GET /search?query=…&cursorMark=*                 deep pagination (follow nextCursorMark)
GET /{PMCID}/fullTextXML                         OA full text as JATS
GET /{source}/{id}/textMinedTerms | /citations | /references
```

`resultType`: `idlist` (ids only) · `lite` (default, no abstract) · `core`
(**abstract, author list, journal, full-text URLs — what you almost always want**).

## Query language

| Want | Query |
|---|---|
| Preprints only | `(machine learning) AND SRC:PPR` — 4,642 hits for that example |
| Open access only | `… AND OPEN_ACCESS:Y` |
| Has full text in PMC | `… AND HAS_FT:Y` |
| Date range | `… AND (FIRST_PDATE:[2022-01-01 TO 3000-01-01])` |
| By DOI | `DOI:"10.1136/bmj.n160"` |
| Fielded | `TITLE:"…"`, `AUTH:"Page MJ"`, `JOURNAL:"BMJ"`, `MESH:"Neoplasms"` |

`SRC:PPR` is the practical answer to "search preprints by keyword" — bioRxiv and
medRxiv's own APIs cannot do it (see [`open-access.md`](open-access.md)).

## Response shape

```json
{"hitCount":4642,"nextCursorMark":"…",
 "resultList":{"result":[{"id":"33781993","source":"MED","pmid":"33781993",
   "pmcid":"PMC8005925","doi":"10.1136/bmj.n160","title":"…","abstractText":"…",
   "authorList":{"author":[{"fullName":"Page MJ"}]},
   "journalInfo":{"journal":{"title":"BMJ"}},"pubYear":"2021",
   "isOpenAccess":"Y","citedByCount":9781,
   "fullTextUrlList":{"fullTextUrl":[{"documentStyle":"pdf","availabilityCode":"OA","url":"…"}]}}]}}
```

`isOpenAccess` is the string `"Y"`/`"N"`, not a boolean. `source` tells you the
sub-corpus: `MED` (PubMed), `PPR` (preprint), `PMC`, `PAT`, `AGR`, `CTX`.
`abstractText` may carry inline HTML — strip tags.

## Full text

```
GET /PMC8005925/fullTextXML
```

Returns JATS for the **OA subset only** (`isOpenAccess:"Y"`); otherwise 404. Flattening
the whole document with a naive `itertext()` prepends a pile of bibliographic tokens —
extract `article-title` + `abstract` + `body` instead, which is what `jats_to_text()`
in `resolve_oa.py` does. A 200 response under ~2 KB is a stub, not an article.

## Good and bad at

Good: one keyless JSON call for metadata *and* full text; preprint keyword search;
citation counts; the widest biomedical net available without credentials.
Bad: coverage outside life sciences; relevance ranking skews recent, so pair it with
OpenAlex when you want the classic papers in a field.
