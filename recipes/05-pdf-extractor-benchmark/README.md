# 05 — Head-to-head: MinerU vs marker vs docling

**Stage:** extract · **No API key** · **Run 2026-07-27**

The three most-starred PDF extractors in this catalogue (MinerU 75.8k★, docling
63.8k★, marker 37.9k★) all claim "PDF → clean Markdown for LLMs". They are not
interchangeable. This runs all three over the same two papers, in **isolated
virtualenvs**, on the same machine.

## Result

Two open-access papers, 43 pages total. CPU only, Apple silicon, no GPU.

| | docling | MinerU | marker |
|---|---|---|---|
| **Total time** | **34.4 s** | 230.9 s | 692.3 s |
| paper 1 (27 pp) | 23.6 s | 198.0 s | 272.1 s |
| paper 2 (16 pp) | 10.8 s | 32.9 s | 420.2 s |
| **DOIs recovered from references** | 88 | 89 | **111** |
| — of those, resolvable in Crossref | 92% | 93% | 92% |
| Tables (tool's own count, paper 1) | 7 | — | 7 |
| Output size, paper 1 | 111 KB | 106 KB | 120 KB |
| Install size | 1.3 GB | 1.4 GB | 1.2 GB |
| Worked on first try? | **yes** | no | no |

## The trade-off nobody advertises

**docling is ~20× faster than marker. marker recovers 26% more DOIs.**

That is not a tie-breaker you can ignore, because which one matters depends on
what you are doing:

- **Screening or RAG over a corpus** — you want throughput, and body text is
  what gets embedded. Take docling.
- **Citation chasing / snowballing / reference auditing** — the reference list
  *is* the deliverable, and 23 extra recovered DOIs per paper compounds fast.
  marker's slower, OCR-backed pass earns its cost.

All three land at ~92% DOI resolvability, so the differences are in *recall* of
references, not in accuracy of what they do extract.

> **Read the DOI numbers carefully.** Paper 2's references barely use DOIs at
> all (0–3 recovered by any tool), so the recall difference rests mostly on
> paper 1. n=2 is enough to disprove "they're interchangeable"; it is not enough
> to rank them definitively.

## Setup friction — the part the READMEs omit

Only **docling** ran on the first attempt. The other two each needed a fix that
no README mentions:

**marker** failed twice before producing output:

1. `RuntimeError: A worker process died while extracting paper1.pdf` — its
   `pdftext` dependency crashes under macOS multiprocessing. Fix:
   ```python
   PdfConverter(artifact_dict=create_model_dict(), config={"pdftext_workers": 1})
   ```
2. Then: `SpawnError: llama-server binary not found`. marker's current surya
   backend needs a **non-Python system binary**:
   ```bash
   brew install llama.cpp
   ```
   A `pip install marker-pdf` alone will not get you a working install.

**MinerU** — two separate problems, one of which was ours:

1. The `mineru` CLI reported `Failed to query task status for task#1: 404 Not
   Found` and wrote an empty output directory. The Python API worked.
2. Calling that API from a `python - <<'EOF'` heredoc crashed with
   `BrokenProcessPool` / `FileNotFoundError: '<stdin>'`. That was **our** bug,
   not MinerU's: it uses multiprocessing spawn, so the entry point must be a
   real file guarded by `if __name__ == "__main__":`. Corrected, it ran fine.

**Do not install them into the same environment.** MinerU pins `transformers`
down to 4.57.6; marker's surya wants ≥5.12.1. pip installs both and warns, and
you are left with one of them silently running against the wrong version. Each
tool here got its own venv — which is also why the install column reads 1.2–1.4
GB *each*, not shared.

## Reproduce it

```bash
for t in docling marker mineru; do python3 -m venv venv-$t; done
./venv-docling/bin/pip install docling
./venv-marker/bin/pip install marker-pdf && brew install llama.cpp
./venv-mineru/bin/pip install "mineru[core]"

./venv-docling/bin/python run_docling.py paper1.pdf out-docling.md
./venv-marker/bin/python  run_marker.py  paper1.pdf out-marker.md
./venv-mineru/bin/python  run_mineru.py  paper1.pdf mineru-out
```

The three runner scripts are in this directory. DOI recall is measured by
regexing `10.\d{4,9}/...` out of each Markdown output and resolving every hit
against the Crossref API.

## Honest limits

- **n = 2 papers**, both open-access journal PDFs with born-digital text. Scanned
  documents, heavy formula content and CJK text would likely reorder these results
  — MinerU in particular advertises formula and multilingual handling this
  benchmark never exercises.
- **CPU only.** All three support GPU, and MinerU and marker are the ones that
  would benefit most. On a GPU box the speed gap almost certainly narrows.
- **One platform.** Both marker failures were macOS multiprocessing issues that
  may not occur on Linux.
- Versions: `docling 2.115.0`, `marker-pdf` + `llama.cpp 10090`, `mineru 3.4.4`,
  Python 3.13.5.

If you run this on Linux or with a GPU, a PR correcting these numbers is very
welcome.
