# 02 — Cut screening effort by 94% with ASReview

**Stage:** screen · **No API key, fully local** · **Verified 2026-07-27**

Title/abstract screening is the bottleneck of a systematic review: thousands of
records, most irrelevant. ASReview ranks them with active learning so the
relevant ones surface early — you stop when you stop finding them.

This is the catalogue's biggest claim, so it was measured against a **published
review's own labelled data** (the SYNERGY benchmark), not a synthetic set.

## Run it

```bash
pip install asreview
asreview simulate "synergy:van_de_Schoot_2018" \
  --n-prior-included 1 --n-prior-excluded 1 --seed 42 --output sim.asreview
```

`simulate` replays a completed review: it knows the real include/exclude labels
and reports how much screening you *could* have skipped.

## Actual result

Corpus: **4,544 records, 38 genuinely relevant.**

| Recall | Records screened | Share of corpus |
|---|---|---|
| 50% | 58 | 1.3% |
| 80% | 97 | 2.1% |
| 90% | 185 | 4.1% |
| 95% | 214 | 4.7% |
| **100%** | **248** | **5.5%** |

`Loss: 0.012 · NDCG: 0.722`

Every relevant paper was found after reading 248 abstracts instead of 4,544 —
**94.5% of the screening avoided**, with no loss of recall on this dataset.

## Reading this honestly

- This is **one** dataset. Recall curves vary with how distinctive the relevant
  papers are; a review whose includes look like its excludes will do worse.
- The 100% figure is knowable only *because* the labels already exist. In a live
  review you cannot see recall, so you need a stopping rule — ASReview's own
  guidance is to stop after a run of consecutive irrelevant records.
- Priors matter: this used 1 known-relevant and 1 known-irrelevant record to
  seed the model. With no priors, early ranking is much weaker.

## Feeding it your own corpus

[Recipe 01](../01-screening-corpus/) emits a compatible CSV:

```bash
asreview lab            # opens the browser UI, import corpus.csv, screen interactively
```

Simulation needs a labelled column; interactive screening does not.
