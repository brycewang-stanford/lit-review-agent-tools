# PubMed & PMC (NCBI E-utilities)

37M+ biomedical citations with MeSH indexing, plus the PMC full-text archive. The
MeSH vocabulary is the reason PubMed still beats general indexes for clinical
questions: it is human-curated subject indexing, not string matching.
Base URL `https://eutils.ncbi.nlm.nih.gov/entrez/eutils`.

Used by `fetch_papers.py` and `fetch_pubmed.py`.

## Auth & limits

3 req/s anonymous, 10 with `NCBI_API_KEY` (`&api_key=…`). Add `&email=` and `&tool=`
so NCBI can contact you instead of blocking you. Sleep ~0.34 s between calls when
keyless — `fetch_papers.py` does.

## The two-step dance

```
GET /esearch.fcgi?db=pubmed&term=…&retmax=20&retmode=json&sort=relevance   → PMIDs
GET /efetch.fcgi?db=pubmed&id=1,2,3&retmode=xml                            → full records
GET /esummary.fcgi?db=pubmed&id=…&retmode=json                             → light metadata
GET /elink.fcgi?dbfrom=pubmed&db=pmc&id=…                                  → PMID → PMCID
GET /efetch.fcgi?db=pmc&id=PMC8005925&retmode=xml                          → JATS full text
```

`esummary` returns JSON but no abstract. **`efetch` with `retmode=xml` is the only way
to get abstracts**, and it returns XML even though the rest of E-utilities speaks JSON.

Query syntax is the same as the PubMed website:

```
("systematic review"[Publication Type]) AND (machine learning[Title/Abstract])
AND ("2022"[Date - Publication] : "3000"[Date - Publication])
covid-19[MeSH Terms] AND humans[MeSH Terms] AND english[Language]
```

Date filtering via parameters: `&datetype=pdat&mindate=2022&maxdate=3000`.

## Parsing the XML

Fields worth pulling from each `PubmedArticle`:

| XPath | Field |
|---|---|
| `.//PMID` | PMID |
| `.//ArticleTitle` | title — **may contain inline `<i>`/`<sub>`**, so use `itertext()`, not `.text` |
| `.//AbstractText` | abstract, often **several elements** with `Label="METHODS"` etc. — join them |
| `./PubmedData/ArticleIdList/ArticleId[@IdType='doi']` | DOI — **scope it exactly like this** |
| `.//PubDate/Year` or `.//PubDate/MedlineDate` | year (MedlineDate is free text like `2023 Jan-Feb`) |
| `.//Author/ForeName` + `LastName` | authors |
| `.//Journal/Title` | venue |
| `.//PublicationType` | `Retracted Publication`, `Retraction of Publication` live here |

Taking only `AbstractText[0]` silently truncates every structured abstract to its
Background section — a classic quiet data-loss bug.

The DOI path is the sharper trap. A `PubmedArticle` embeds the article's **entire
reference list**, and every reference carries its own `<ArticleId IdType="doi">`. A
`.//ArticleId` sweep therefore returns a *cited* paper's DOI — in one recorded run,
a stroke-imaging review came back carrying an ICPSR **dataset** DOI from its own
bibliography. The record looks perfect and points at the wrong object. Scope the
lookup to `./PubmedData/ArticleIdList`, and fall back to
`.//Article/ELocationID[@EIdType='doi']`. Written up in
[`recipes/06`](../../../../recipes/06-multi-source-search/).

## ID conversion

The old `/pmc/utils/idconv/v1.0/` path now 301-redirects; the live endpoint is

```
GET https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids=10.1136/bmj.n160&format=json
→ {"records":[{"doi":"10.1136/bmj.n160","pmcid":"PMC8005925","pmid":33781993}]}
```

Follow redirects (`curl -L`) or you will parse an HTML 301 page as JSON.

## Good and bad at

Good: MeSH-indexed retrieval, publication-type filters (RCT, meta-analysis, retraction),
clinical coverage, and PMC full text for the OA subset.
Bad: anything non-biomedical, and PDFs — PubMed exposes almost none. For full text
prefer Europe PMC (same corpus, one JSON call, no XML dance).
