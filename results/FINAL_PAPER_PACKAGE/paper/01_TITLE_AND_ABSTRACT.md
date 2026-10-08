# Synthetic Silence: Evaluating the Construction and Reference-Manifold Dependence of Representation-Space Evidence Sufficiency Signals

## Abstract
**Background:** Reliable detection of evidence insufficiency remains challenging for verification systems.
**Problem:** Representation-space density has been hypothesized as a potential signal for insufficiency, but its generalizability across differing definitions of "insufficient evidence" is unknown.
**Method:** We evaluated a claim-space kNN density signal (B3) using a FEVER-derived dataset (E0), a naturalistic AVeriTeC dataset (E1), a cross-manifold diagnostic (F1), and a matched structural-control analysis (F2).
**Results:** The signal achieved a modest association on FEVER (AUROC=0.5463). However, it failed to generalize to AVeriTeC (AUROC=0.3545), showing a severe inversion for retrieved insufficiency (0.2754). Cross-manifold evaluation collapsed cross-domain signals toward chance. Matching on claim length and lexical diversity did not eliminate the inversion (AUROC=0.3353).
**Finding:** The evaluated signal does not generalize invariantly. 
**Contribution:** We demonstrate that representation-space signals are highly sensitive to construction-specific and reference-manifold-dependent semantic geometry, requiring cross-construction validation.
**Limitation:** The exact mechanism of the residual inversion remains unresolved.
