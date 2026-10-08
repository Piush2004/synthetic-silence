# SyntheticSilence2.0

**Project Purpose:** Investigating whether representation-space density serves as a reliable, construction-invariant signal for evidence insufficiency.
**Research Question:** Do density-based evidence-sufficiency signals generalize across different constructions?
**Final Findings:** No. Under evaluated conditions, kNN density demonstrated significant construction and reference-manifold dependence. The modest signal on FEVER (AUROC=0.5463) inverted on AVeriTeC (AUROC=0.2754), and cross-manifold evaluation collapsed the signal to chance. 
**Reproducibility:** See `results/FINAL_PAPER_PACKAGE/reproducibility/`.
**Limitations:** Domain gaps, differing manifold sizes, limited matched samples, lack of temporal/NLI baselines.
**Future Work:** Temporal conditions, full NLI baselines, and richer structural control populations.
