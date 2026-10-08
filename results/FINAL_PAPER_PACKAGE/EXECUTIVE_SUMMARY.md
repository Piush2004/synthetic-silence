# Executive Summary
**Problem**: Existing verification systems struggle to detect evidence insufficiency reliably. 
**Research Question**: Do representation-space density signals for evidence insufficiency generalize across different constructions?
**Method**: Evaluated kNN claim-space density (B3) on FEVER (E0), AVeriTeC (E1), cross-manifold setups (F1), and structural matched controls (F2).
**Main Finding**: The modest signal observed in FEVER (AUROC=0.5463) inverted on AVeriTeC (0.3545 overall; 0.2754 for insufficiency). Cross-manifold evaluation reduced signals toward chance. Structural matching did not eliminate the inversion (0.3353).
**Contribution**: Provides evidence for construction and reference-manifold dependence of apparent density signals, underscoring the necessity of cross-construction evaluation.
**Limitations**: Disentanglement limited by domain gaps, differing manifold sizes, matched sample size (29 pairs), and independent bootstrap limitation.
**Future Work**: Temporal conditions, evidence-conditioned representations, and true NLI baselines.
