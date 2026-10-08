# Scientific Regression Suite

This suite establishes controlled synthetic bounds (Cases A-I) to verify that the research engine's qualitative behaviors align with the scientific definitions of each construction family.

**IMPORTANT:** These are regression tests designed to prove the pipeline correctly processes known bounds. They do **NOT** constitute benchmark performance or validate the overarching research hypothesis.

## Synthetic Cases
- **Case A (Strongly Supported):** High NLI, low contradiction, high density.
- **Case B (No Evidence):** Zero coverage, max uncertainty, None density. Pipeline must explicitly mark as `missing_evidence`, not arbitrary contradiction.
- **Case C (Irrelevant Evidence):** Low density, high similarity entropy.
- **Case D (Contradictory Evidence):** High contradiction level; contradiction does not equal absence.
- **Case E (Temporally Stale):** Low temporal coverage for novel claims.
- **Case F (Rare but Valid):** Low density but HIGH semantic support (differentiates knowledge voids from valid long-tail facts).
- **Case G (Retrieval Failure):** Pipeline preserves explicit `FAILED`/`TIMEOUT` state.
- **Case H (Ambiguous Claim):** Moderate contradiction/neutrality.
- **Case I (Post-Cutoff Emerging):** High temporal coverage without automatic hallucination flagging.
