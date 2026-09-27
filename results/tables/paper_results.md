# Reported evaluation results

| Model | Recall@1 | Recall@5 | MRR@10 | FDR | Avg Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| BGE | 0.8422 | 1.0000 | 0.9211 | 0.8422 | 0.0586 |
| Qwen-8B | 0.8410 | 1.0000 | 0.9205 | 0.8410 | 0.0639 |
| BGE-Align | 0.9947 | 1.0000 | 0.9973 | 0.9947 | 0.6044 |

## Results by observed difficulty

### BGE

| Difficulty | Records | Recall@1 | Recall@5 | MRR@10 | FDR | Avg Margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Easy | 497 | 0.9014 | 1.0000 | 0.9507 | 0.9014 | 0.1123 |
| Hard | 954 | 0.8029 | 1.0000 | 0.9015 | 0.8029 | 0.0273 |
| Medium | 247 | 0.8745 | 1.0000 | 0.9372 | 0.8745 | 0.0714 |

### Qwen-8B

| Difficulty | Records | Recall@1 | Recall@5 | MRR@10 | FDR | Avg Margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Easy | 497 | 0.9014 | 1.0000 | 0.9507 | 0.9014 | 0.1239 |
| Hard | 954 | 0.8040 | 1.0000 | 0.9020 | 0.8040 | 0.0287 |
| Medium | 247 | 0.8623 | 1.0000 | 0.9312 | 0.8623 | 0.0789 |

### BGE-Align

| Difficulty | Records | Recall@1 | Recall@5 | MRR@10 | FDR | Avg Margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Easy | 497 | 0.9940 | 1.0000 | 0.9970 | 0.9940 | 0.7124 |
| Hard | 954 | 0.9937 | 1.0000 | 0.9969 | 0.9937 | 0.5331 |
| Medium | 247 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6622 |

## FDR by recorded task category

### BGE

| Recorded task category | Records | FDR |
| --- | ---: | ---: |
| Factual | 228 | 0.9035 |
| Reasoning | 516 | 0.7946 |
| Spatial | 75 | 0.8133 |
| Temporal | 783 | 0.8595 |
| Temporal_Spatial | 96 | 0.8333 |

### Qwen-8B

| Recorded task category | Records | FDR |
| --- | ---: | ---: |
| Factual | 228 | 0.8816 |
| Reasoning | 516 | 0.7791 |
| Spatial | 75 | 0.7733 |
| Temporal | 783 | 0.8659 |
| Temporal_Spatial | 96 | 0.9271 |

### BGE-Align

| Recorded task category | Records | FDR |
| --- | ---: | ---: |
| Factual | 228 | 0.9912 |
| Reasoning | 516 | 0.9961 |
| Spatial | 75 | 1.0000 |
| Temporal | 783 | 0.9936 |
| Temporal_Spatial | 96 | 1.0000 |
