# RESEARCH STORY

1. **Original intuition**: Information scarcity might systematically alter the semantic representation of a claim.
2. **Representation-space density as evidence-sufficiency signal**: We hypothesized that claims lacking evidence would fall into sparse, low-density regions of an embedding space when compared to a manifold of well-supported facts.
3. **E0 controlled benchmark**: We tested this strictly on a frozen FEVER-derived dataset.
4. **Modest FEVER association**: The density signal yielded an AUROC of 0.5463, showing a statistically significant but modest capability to identify missing evidence.
5. **Cross-construction challenge**: We questioned if this signal actually captured evidence insufficiency or merely structural artifacts of the FEVER benchmark.
6. **AVeriTeC naturalistic evaluation**: We evaluated the same density metric on AVeriTeC, mapping its "Not Enough Evidence" class to our target.
7. **Direction reversal**: The signal severely inverted (AUROC 0.2754), indicating that insufficient claims were *closer* to the supported manifold than refuted claims.
8. **Post-hoc diagnostics**: Bounded, read-only analysis isolated the effect to reference-manifold geometry and class-composition rather than a genuine knowledge-gap measurement.
9. **Construction dependence**: The signal is highly dependent on how evidence insufficiency is constructed and aggregated in the evaluation dataset.
10. **Need for construction-aware validation**: Interpreting embedding-space metrics requires rigorous, cross-construction validation to disentangle true functional signals from geometric and stylistic artifacts.
