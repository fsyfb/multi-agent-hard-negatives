# Data card

## Provenance and scope

The release contains Chinese event records, the NHMil_QA question–answer benchmark, generated negative documents, and fixed training/evaluation splits. Source benchmark: Shuyang Feng and Haiping Yang, *Construction and empirical evaluation of a retrieval-augmented generation benchmark based on South China Sea news updates* (English rendering of the Chinese title), 2026. [Original publication record](https://link.cnki.net/urlid/61.1167.g3.20260728.1418.010).

Event coverage is October 2018–February 2025. The 3,882 source QA pairs comprise 1,295 factual, 1,294 synthesis and 1,293 reasoning questions. The construction pipeline retains 3,775 identifiers with all three requested difficulty records. The release preserves original texts, identifiers, labels, scores and file contents; it does not replace countries or places in the actual data.

## Files and encoding

All files use UTF-8. `NHMil_QA.txt` is a JSON array despite its `.txt` suffix. `NHMil_event.txt` is plain event text. The three `.json` datasets are JSON arrays. Duplicate JSONL exports are omitted; `split_dataset.py --jsonl` can export JSONL splits if needed.

The full constructed dataset includes both train and evaluation records. Use **train_split.json** for training and **eval_split.json** for evaluation.

## Record schema

| Field | Type | Meaning |
| --- | --- | --- |
| `query` | string | Original question |
| `pos` | array of strings | Positive source text; one element in this release |
| `neg` | array of strings | Constructed candidate text; one element in this release |
| `metadata` | object | Construction, difficulty and screening information |

| Metadata field | Meaning |
| --- | --- |
| `original_id` | QA identifier and split-grouping key |
| `attack_strategy` | Original strategy name; refers to candidate generation or local fallback |
| `affected_axis` | Task category assigned before generation |
| `similarity_score` | Weighted positive–candidate similarity, rounded to four decimals |
| `sim_gap` | One minus similarity, rounded to four decimals |
| `adversarial_turns` | Selected candidate's inner screening turn, not total calls or attempts |
| `verifier_is_contradictory` | Passing flag populated by a rule-only route or model verification |
| `difficulty` | Requested target: `Easy`, `Medium`, or `Hard` |
| `actual_difficulty` | Observed similarity interval used for training and grouped evaluation |
| `difficulty_matched` | Agreement between requested and observed difficulty |
| `quality_status` | Selection outcome, including `target_hit` and `out_of_range_kept` |
| `answer_anchor_changed` | Surface anchor-check flag |
| `answer_anchor_status` | Reason returned by the anchor check |
| `changed_answer_anchors` | Up to five answer spans absent from the candidate |

The public code retains legacy field/class names for compatibility. In the manuscript, “candidate generation agent” and “rewriting task” refer to the corresponding components.

## Difficulty and task groupings

Observed difficulty uses the **unrounded** weighted score: Easy [0.50, 0.75), Medium [0.75, 0.85), Hard [0.85, 0.95). A saved score rounded to an interval boundary should not be used to overwrite its saved label.

| Group | Full dataset | Evaluation split |
| --- | ---: | ---: |
| Easy | 3,276 | 497 |
| Medium | 1,719 | 247 |
| Hard | 6,330 | 954 |

There are 8,042 target hits (71.01%) and 3,283 retained target misses. Each requested target occurs 3,775 times. Recorded task categories map to the manuscript as follows:

- `Factual`: entity group.
- `Reasoning`: relation group (including synthesis questions routed to this category).
- `Temporal`: temporal group.
- `Spatial` and `Temporal_Spatial`: geographical/spatiotemporal group.

Task labels describe allocation categories; a candidate may change more than one condition. The validation script reports the exact category strings present in the files.

## Split and evaluation unit

Splitting groups all three target records by `original_id`, sorts identifiers, shuffles them with seed 42, and reserves approximately 15% of the identifiers for evaluation. Train/evaluation identifier overlap is zero. Of 566 evaluation questions, 546 share a positive document with training. The experiment therefore evaluates unseen questions within a shared corpus.

Each of the 1,698 evaluation triples is ranked separately against its own positive and negative documents. There is no full-corpus retrieval index in this evaluation. The three records from a question are related observations, not independent questions.

## Label interpretation

A missing answer span indicates a surface change, not necessarily loss of semantic answer support. For rule-only routes, the stored verification flag is a default pass; for other routes it reflects a model judgment. The released labels contain residual errors, including candidates that change background information while preserving evidence for an inference. Appendix C of the manuscript discusses concrete records. Negative documents are synthetic training material and should not be treated as factual event reports.

The release contains final retained metadata and aggregate ranking reports. Full rejected-candidate histories, the original manual inspection forms and trained checkpoints are not included.
