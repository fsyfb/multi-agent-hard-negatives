# Public release preparation

This package reorganizes the authors' supplied experimental materials for repository upload. No new experimental results are introduced.

## Preserved

- Five source/data files copied byte-for-byte: event text, QA JSON, full constructed triples and two fixed splits.
- Three original aggregate evaluation JSON files copied byte-for-byte, including their original model labels.
- Generation/verification prompt strings, similarity thresholds, selection logic, sampling schedule and metric formulas.
- English manuscript figure assets.

## Packaging changes

- Replaced hardcoded generation and embedding credentials and service URLs with environment variables.
- Added `.env.example`, a standard-library environment loader and missing-configuration checks.
- Removed the original helper that extracted and printed credentials from `pipeline.py`; evaluation now reads local environment variables directly.
- Added generation CLI options for input/output files; new candidates default to `experiments/generated/` rather than overwriting the released dataset.
- Changed training defaults to `train_split.json` and full precision to match the reported run. Both remain explicit CLI options.
- Changed the loss import to the public `from sentence_transformers import losses` interface.
- Added English documentation, data validation, immutable-file checksums and a reconstruction entry point.
- Translated generated summary-table headings to English; numeric results are unchanged.
- Adjusted the plotting helper to create its output directory and skip unavailable training-history plots.

## Excluded files

Model weights, the large remote embedding cache, redundant JSONL copies, duplicated result archives, private configuration values and unfilled manuscript drafts are excluded. Source texts and dataset identifiers remain intact for traceability.

## Verification boundary

Data and table reconstruction are checked without downloading a model. Synthetic-score tests check ranking ties and margin calculations. No new training, API calls or model-based evaluation were performed during this release preparation.
