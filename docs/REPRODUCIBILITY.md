# Reproduction details

## 1. Inspect the fixed release

`python experiments/scripts/validate_release.py` checks the released data against `SHA256SUMS`, reconstructs the split in memory, checks group completeness and verifies recorded difficulty counts. It does not require a GPU, model or API.

`python experiments/scripts/reproduce_artifacts.py` writes the reconstructed split to `experiments/generated/reconstructed/` and regenerates aggregate tables under `results/reproduced/`. It uses the existing saved evaluation results and does not recompute embeddings.

## 2. Construct new data (optional)

The workflow aligns QA identifiers with event dates/indices, with BM25 answer-based source matching as a fallback. Generation receives the query, reference answer and positive document. The verifier receives the source, answer and candidate.

| Configuration | Value |
| --- | --- |
| Generation / verification model identifier | `deepseek-v4-flash` |
| Heavy embedding identifier | `qwen/qwen3-embedding-8b` |
| Light embedding model | `BAAI/bge-large-zh-v1.5` |
| Similarity weights | Heavy 0.7; light 0.3 |
| Generator temperature by API attempt | 0.9, 0.6, 0.3 |
| Verifier temperature | 0.3 |
| Generation / verification output limits | 1,536 / 1,024 tokens |
| API attempt limit | 3 |
| Generation attempt limit per target | 5 |
| Inner screening turns per attempt | 2 |
| Worker threads | 5 |
| Global retained similarity range | [0.50, 0.95) |

API identifiers are provider configuration strings, not model snapshots distributed by this repository. Regeneration depends on access to those endpoints and stochastic model responses. Changing an endpoint or model produces a new construction run.

### Screening routes

1. Reject scores outside the global range and failed answer-anchor checks.
2. Route using **requested difficulty**, not observed difficulty.
3. Easy targets pass on the rule outcome. Medium targets use rules when answer anchors are available.
4. Medium targets without anchors and all Hard targets require similarity ≥0.60, a true factual-change judgment and retention score ≥80.
5. Prefer candidates meeting the target interval. Otherwise retain a usable candidate within the search budget and assign its observed difficulty.

The verifier prompt's terminology-retention guidance (>90%) and acceptance score threshold (≥80) are different quantities. Rule-route retention scores are control defaults. The final dataset does not store retention scores or free-text verifier feedback. The controller passes its own screening summary and similarity direction to revision calls.

Prompts are embedded in `pipeline.py`: `DIFFICULTY_GENERATE_HINTS`, `DIFFICULTY_REFINE_HINTS`, `VerifierAgent.VERIFIER_PROMPT` and the `AdversarialAttacker` prompt constants. Original prompt strings are preserved in the public release.

### Local configuration

`.env` supports simple `KEY=value` lines and optional matching quotes around an entire value. Process environment variables override the file. The loader does not perform shell expansion or execute commands. `.env.example` contains empty credential fields; the generation entry point reports missing variable **names**, never their values.

The Qwen evaluator reads `EMBEDDING_API_KEY` and `EMBEDDING_BASE_URL`; specify its model identifier with `--model`. Keep regenerated outputs and checkpoints separate from the immutable released files.

## 3. Train and evaluate

Use the commands in the root README. Reported training settings: three epochs, max sequence length 512, microbatch eight, accumulation four, learning rate 2e-5, weight decay 0.01, gradient clipping 1, warmup 10%, cosine scheduling and no mixed precision. AdamW and the scheduler are recreated each epoch. Sampling uses observed difficulty with ratios 0.6/0.3/0.1, 0.2/0.6/0.2 and 0.1/0.3/0.6.

| Epoch | Sampled records | Records in complete training batches |
| --- | ---: | ---: |
| 1 | 5,251 | 5,248 |
| 2 | 5,472 | 5,472 |
| 3 | 7,848 | 7,848 |

Accumulation produces an optimizer batch of 32 examples; each contrastive loss call still sees a microbatch of eight. The original shuffled loader does not remove semantically equivalent positives across questions.

The final checkpoint is `<output_dir>/final`. No independent validation-based epoch selection is implemented. The evaluator normalizes embeddings, uses cosine similarity and ranks the positive first in an exact tie. FDR counts only strict positive wins. For this release, P@1 equals Recall@1, MRR@10 = (1 + P@1)/2, and Recall@5 = 1.

## 4. Environment and available evidence

`requirements.txt` declares functional dependency ranges for installation, not the original experiment's frozen environment. Save `python -m pip freeze` alongside future runs to record their versions. The original archive supplied code, datasets and aggregate reports but no environment lockfile or checkpoints.

Release validation covers data integrity, split reconstruction, table reconstruction, Python syntax, configuration behavior and evaluator metric logic using synthetic scores. Training and live API inference have not been rerun during repository preparation.
