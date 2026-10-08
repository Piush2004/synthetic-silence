# EXPERIMENT LINEAGE

1. **E0** -> Established FEVER baseline and methodology.
2. **E1 Protocol** -> Defined rigorous rules for testing cross-construction generalization.
3. **AVeriTeC Preflight** -> Acquired and audited AVeriTeC data without testing.
4. **AVeriTeC Adapter** -> Integrated QA-structured evidence into uniform claim format.
5. **E1 Population** -> Split train/dev/test with strict leakage quarantine.
6. **DEV Threshold** -> Youden's J threshold calibrated strictly on DEV.
7. **Frozen TEST** -> The 500-instance locked evaluation set.
8. **E1 Execution** -> Immutable inference pipeline evaluating TEST.
9. **Post-Hoc Diagnostics** -> Read-only attribution of inverted AUROC.
10. **Final Interpretation** -> Documented construction-specific fragility of the density signal.
