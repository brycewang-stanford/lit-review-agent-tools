# 03 — Catch invented and retracted citations

**Stage:** cite-check · **No API key** · **Verified 2026-07-27**

LLM-drafted related-work sections invent references that look right. Separately,
real papers get retracted and keep being cited for years. This resolves each
citation against Crossref and OpenAlex and reports what it actually found.

## Run it

```bash
python3 verify_citations.py citations.txt
```

One citation per line — a DOI, a title, or free text containing either.

## Actual output

```
✓ CONFIRMED   Jumper et al. (2021) Highly accurate protein structure prediction with AlphaFold — Nature
              https://doi.org/10.1038/s41586-021-03819-2
~ TITLE MATCH Mineault (2025) Is Attention All You Need? — From Human Attention to Computational At  (overlap 100%)
              https://doi.org/10.1007/978-3-031-84300-6_13  — verify this is the work you meant
⚠ RETRACTED   Wakefield et al. (1998) RETRACTED: Ileal-lymphoid-nodular hyperplasia, non-specific colitis, and… — The Lancet
              https://doi.org/10.1016/s0140-6736(97)11096-0
? WEAK MATCH  Deep Contrastive Meta-Learning for Systematic Review Screeni
              closest: ? (2020) Review for "Diagnostic test accuracy of the Nursing Delirium Screening S… — (overlap 38%)

confirmed=1  title-only=1  not-found=0  mismatch=1  retracted=1
```

It correctly flagged the Wakefield MMR paper as retracted, and the invented
citation matched nothing above 38% overlap.

## The bug this recipe exists to document

The first run reported **`✓ CONFIRMED`** for *Attention Is All You Need* —
pointing at `10.1007/978-3-031-84300-6_13`, which is a **different 2025 paper**
called *Is Attention All You Need?*. Every token of the query appears in the
candidate title, so overlap scored 100%.

A citation checker that confidently confirms the wrong paper is worse than none:
it launders an error into a verification. The script now **never** returns
CONFIRMED from a title lookup. Titles yield `~ TITLE MATCH`, always printed with
the matched work so a human accepts or rejects it. Only a DOI confirms.

The general lesson, which applies to every "citation integrity" feature in this
catalogue: **string similarity is not identity.** If a tool claims to verify
citations, check whether it resolves identifiers or just matches text.

## Verdicts

| Verdict | Meaning |
|---|---|
| `✓ CONFIRMED` | DOI resolved in Crossref. Trustworthy. |
| `~ TITLE MATCH` | Closest Crossref hit for a title. **Needs a human.** |
| `? WEAK MATCH` | Best candidate below 75% overlap. Probably invented. |
| `✗ NOT FOUND` | Nothing resolved. Invented, or too mangled to resolve. |
| `⚠ RETRACTED` | Flagged retracted by OpenAlex or Crossref `update-to`. |

Exit code is non-zero if anything was not-found or retracted, so it drops into
CI over a manuscript's bibliography.

## Chaining from a PDF

[Recipe 04](../04-pdf-to-markdown/) converts a paper, from which 88 DOIs were
recovered by regex. Feeding the first 10 in gave `confirmed=7, not-found=1,
mismatch=2` — and both failures were **extraction** artefacts, not bad
citations: a trailing `)`, and `10.1007/s40593013-0012-6` missing a hyphen lost
across a PDF line break. Validate extracted DOIs before accusing an author.
