# CLAIM-AUDIT MATRIX

| Claim | Evidence source | Experiment | Metric | Direct observation? | Interpretation? | Alternative explanations? | Confidence/status | Allowed wording | Forbidden wording |
|---|---|---|---|---|---|---|---|---|---|
| "B3 failed to generalize." | AUROC comparison | E0 vs E1 | AUROC | Yes | No | Domain shift | SUPPORTED | "The signal did not demonstrate cross-construction generalization." | "The method is universally invalid." |
| "B3 acts as an implausibility detector." | retrieved_insufficient AUROC=0.2754 | E1 | AUROC vs opposing class | No | Yes | Class-composition | SUPPORTED INTERPRETATION | "The class-conditional geometry is consistent with B3 capturing proximity to the reference manifold." | "B3 measures implausibility." |
| "Stylistic confounding drove the result." | Hypothesis H4 | E1 | N/A | No | Yes | N/A | NOT TESTABLE | "Stylistic artifacts remain a possible confound." | "Stylistic confounding caused the inversion." |
| "Density does not measure evidence sufficiency." | E1 AUROC | E1 | AUROC | Yes | No | N/A | ESTABLISHED FOR EVALUATED CONSTRUCTIONS | "In this setting, density failed to consistently measure evidence sufficiency." | "Density cannot measure evidence sufficiency." |
