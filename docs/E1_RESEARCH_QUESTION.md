# E1 Research Question

## Core Objective
**Does claim-space density retain discriminative information when the construction of evidence insufficiency changes?**

More formally: Does the representation-density signal (kNN semantic distance from known-supported knowledge) generalize across distinct constructions of insufficient evidence, or is the E0 signal strictly an artifact of the FEVER `NOT ENOUGH INFO` construction and the `SUPPORTS`-derived reference manifold?

## Hypothesis
Evidence insufficiency may manifest through measurable changes in semantic representation density and neighborhood structure, but the usefulness of density-based signals may depend on how insufficiency is constructed within the specific dataset or environment.

**Important Negative Constraint:**
This hypothesis does *not* assert that "density detects knowledge voids."

## Context from E0
E0 evaluated the pipeline under `FROZEN_EVIDENCE_MODE` using the FEVER dataset. It established a measurable but weak continuous-score AUROC of 0.5463 for B3 (kNN Density). 
However, E0 relied on:
1. A reference manifold consisting entirely of FEVER `SUPPORTS` claims.
2. A definition of insufficiency derived exclusively from FEVER's `NOT ENOUGH INFO` class, which heavily relies on artificial claim mutation (e.g., entity swapping, clause deletion).

E1 asks whether B3 survives when we alter the construction mechanism of the claim and the semantics of "insufficient evidence" (e.g., using AVeriTeC, or evaluating out-of-distribution real-world information scarcity).

## Failure Conditions as Valid Results
- **Outcome A**: Density generalizes across constructions.
- **Outcome B**: Density works only for some constructions (e.g., artificial mutations but not real-world scarcity).
- **Outcome C**: Density works on FEVER but fails entirely elsewhere.
- **Outcome D**: Density does not outperform evidence-based baselines under live retrieval.
- **Outcome E**: Density signal reverses direction across constructions.
- **Outcome F**: Results are inconclusive due to insufficient data.

All are scientifically valid. Methodological optimization to force Outcome A is explicitly prohibited.
