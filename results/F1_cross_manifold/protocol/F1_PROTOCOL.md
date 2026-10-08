# F1_PROTOCOL.md

## Research Question
Does B3's behavior change primarily because the construction changes, because the reference manifold changes, or because both change simultaneously?

## Conditions
- C: AVeriTeC TEST -> FEVER manifold
- D: FEVER TEST -> AVeriTeC manifold

## Details
- Embedding: all-MiniLM-L6-v2
- Algorithm: B3 (kNN Density + LedoitWolf Mahalanobis distance)
- Score direction: Higher value = lower density = greater insufficiency
- Primary Metric: AUROC
