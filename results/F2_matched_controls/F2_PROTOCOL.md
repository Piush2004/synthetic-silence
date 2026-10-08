# F2_PROTOCOL.md
## Target Construction
AVeriTeC: retrieved_insufficient

## Candidate Control Classes
AVeriTeC: Supported (rare_valid)

## Matching Variables
- claim_length_chars
- claim_length_words
- lexical_diversity

## Matching Algorithm
1:1 Nearest-Neighbor Mahalanobis matching on standardized features without replacement.

## Caliper
0.5 standard deviations (Mahalanobis distance <= 0.5)

## Missing Value Handling
Claims with 0 words are excluded.

## Primary Metric
AUROC
