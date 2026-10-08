# FOLLOW-UP EXPERIMENTS

These experiments are scientifically motivated by the E1 failure attribution but ARE NOT EXECUTED during this freeze.

1. **F1 — Cross-manifold evaluation**: Evaluate AVeriTeC claims using the frozen FEVER manifold and FEVER claims using an authorized AVeriTeC manifold. Purpose: separate construction effects from reference-distribution effects.
2. **F2 — Matched negative controls**: Construct matched pairs controlling claim length, entities, topic, and lexical complexity. Purpose: test whether B3 responds strictly to superficial structure.
3. **F3 — Evidence-conditioned density**: Compare claim-only representation against claim + evidence representation. Purpose: test whether density actually incorporates evidentiary information.
4. **F5 — True NLI baseline**: Implement a genuine pretrained NLI baseline. Purpose: compare density against an established verification signal.
5. **F6 — Learned classifier**: Train a supervised combination of density signals. Purpose: determine whether supervised combinations outperform individual density signals.
6. **F4 — Temporal evaluation**: Test the approved temporal pre/post-cutoff condition. Purpose: evaluate whether temporal novelty contributes independently.
