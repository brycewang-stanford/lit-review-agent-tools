# Getting the actual file: Unpaywall, CORE, bioRxiv/medRxiv

Metadata tells you a paper exists. These APIs tell you whether you may read it.
`resolve_oa.py` chains them; this file documents each one and the order, so you can
debug a DOI that "should" be open.

## The chain, and why this order

```
1. Unpaywall    every publisher, every field — but needs an email
2. OpenAlex     same underlying OA data, keyless, sometimes a landing page not a PDF
3. Europe PMC   biomedical OA full text as XML — no PDF needed
4. arXiv        anything with an arXiv id, guaranteed PDF
5. CORE         repository aggregator, catches institutional copies — needs a key
```

Highest precision first, widest net last. Recorded result on a 47-paper multi-source
corpus with **no keys at all** (Unpaywall and CORE skipped): 33/47 resolved — 16 via
OpenAlex, 10 via arXiv, 7 via Europe PMC. See
[`recipes/06-multi-source-search`](../../../../recipes/06-multi-source-search/).

**Nothing here bypasses a paywall.** A closed paper stays closed and is reported as
`closed` in `oa_report.json`. Do not route around that with Sci-Hub or scraped mirrors:
it is unlawful in most jurisdictions and gets institutions blocked. Interlibrary loan
and author-request are the legitimate paths, and both need a human.

## Unpaywall

```
GET https://api.unpaywall.org/v2/{doi}?email=you@example.com
```

- The `email` parameter is **mandatory** — without it you get HTTP 422, not a warning.
  Never invent one; ask the user, or run without this step (`resolve_oa.py` does).
- 100k calls/day. Batch downloads are offered as a data dump instead.
- Read `is_oa`, then `best_oa_location.url_for_pdf` (may be null when only a landing
  page exists), `oa_status` (`gold`/`green`/`hybrid`/`bronze`/`closed`), and
  `.version` — `submittedVersion` means you got the preprint, not the paper of record.
  Quote page numbers from a `publishedVersion` only.

## CORE

```
POST https://api.core.ac.uk/v3/search/works
Authorization: Bearer $CORE_API_KEY      body: {"q":"doi:\"10.…\"","limit":1}
```

37M+ full texts harvested from institutional and subject repositories — the best
source for green OA copies that Unpaywall's publisher-centric view misses, and for
theses. Requires free registration; without `CORE_API_KEY` this step is skipped.
Use `downloadUrl` from a result, and verify the bytes really are a PDF.

## bioRxiv / medRxiv

```
GET https://api.biorxiv.org/details/biorxiv/10.1101/2020.01.30.927871
GET https://api.biorxiv.org/details/medrxiv/2023-01-01/2023-01-31/0     paged by date
GET https://api.biorxiv.org/pubs/biorxiv/{doi}                          published version
```

**There is no keyword search.** These APIs only browse by DOI or by date window; the
`collection` array comes back with `title`, `authors`, `date`, `category`, `jatsxml`.
To search preprints by topic, use Europe PMC's `SRC:PPR` filter (see
[`europepmc.md`](europepmc.md)) or OpenAlex `type:preprint` — then come back here for
the version history, or to `/pubs/` to find out whether the preprint was ever published.

That last check is the one people skip: citing a preprint whose published version
contradicts it is a real and common failure of automated reviews.

## Verifying what you downloaded

- A PDF starts with the bytes `%PDF-`. Publishers serve HTML "access denied" pages with
  HTTP 200 and `Content-Type: application/pdf` often enough that content-type is not
  evidence — check the magic bytes (`is_pdf()` in `resolve_oa.py`).
- Europe PMC full text under ~2 KB is a stub record, not an article.
- A DOI that resolves nowhere is two different findings. `resolve_oa.py` asks Crossref
  before giving up: `closed` means the paper exists behind a paywall; `not-in-crossref`
  means no Crossref record exists at all — an invented citation, a typo, or a DOI from
  another registry (DataCite datasets, some preprint servers). Never report the second
  as the first.
- Record the resolver that produced each file. When a citation later looks wrong, the
  first question is always "was that the published version or the preprint?", and
  `oa_report.json` answers it.
