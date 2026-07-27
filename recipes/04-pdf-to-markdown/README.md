# 04 — Turn a paper into structured Markdown with docling

**Stage:** extract · **No API key, runs locally** · **Verified 2026-07-27**

Everything downstream — RAG, extraction, citation checking — needs the PDF as
clean structured text. docling does it locally with no key.

## Run it

```bash
pip install docling
```
```python
from docling.document_converter import DocumentConverter
res = DocumentConverter().convert("paper.pdf")
open("paper.md", "w").write(res.document.export_to_markdown())
```

## Actual result

A 29-page open-access systematic review (893 KB PDF):

| | |
|---|---|
| Import time (first call) | 38 s |
| Conversion | **78 s for 29 pages**, CPU only |
| Markdown out | 111,483 characters |
| Tables reconstructed | 7 |
| Figures detected | 4 |

Headings came out in document order: `REVIEW ARTICLE → Abstract → Introduction →
AI in education (AIEd) → Method → Search strategy`.

## Quality where it matters

The **search-strategy table survived as a real Markdown table** — the boolean
query blocks, intact:

```
| Topic                   | Search terms                                        |
|-------------------------|-----------------------------------------------------|
| Artificial intelligence | ' artificial intelligence ' OR ' machine intelligence ' OR … |
```

For a systematic review that table *is* the reproducibility record, and most
naive PDF-to-text loses it entirely. The reference list also survived with DOIs
intact enough to feed [recipe 03](../03-verify-citations/).

## Costs the README doesn't mention

- **torch is a dependency.** `pip install docling` pulled torch 2.13, torchvision
  and transformers. This is not a small install.
- **~26 MB of OCR weights download on first run** (RapidOCR PP-OCRv4), from
  ModelScope and Hugging Face. First conversion on an air-gapped box will fail
  unless you pre-seed the cache.
- **78 s for 29 pages on CPU** is fine for a handful of papers and painful for a
  thousand. Budget GPU or batch time at corpus scale.

## Getting the PDF in the first place

Harder than expected. From [recipe 01](../01-screening-corpus/), 91% of records
advertised an open-access PDF link, but the first candidate (a BMJ URL ending in
`.pdf`) returned a 5 KB HTML block page. It took **4 candidates** to get a real
PDF. Check the `%PDF-` magic bytes before handing anything to a converter:

```python
open(path, "rb").read(5) == b"%PDF-"
```
