# EVIDENCE LEDGER

| Claim | Evidence | Status | Artifact |
|---|---|---|---|
| E0 B3 AUROC = 0.5463 | FEVER TEST execution | ESTABLISHED | exp_E0_baseline_offline_6998cbb1/metrics.json |
| E1 B3 AUROC = 0.3545 | AVeriTeC TEST execution | ESTABLISHED | E1_execution/statistical_analysis.json |
| E1 retrieved_insufficient AUROC = 0.2754 | AVeriTeC TEST construction analysis | ESTABLISHED | E1_execution/construction_analysis.json |
| E1 threshold was DEV-derived | Threshold locked prior to TEST access | ESTABLISHED | E1_execution/E1_THRESHOLD_LOCK.json |
| TEST tuning occurred | Frozen protocol strictly separated TEST | NOT OBSERVED | E1_execution/E1_EXECUTION_FREEZE.json |
| E0 remained unchanged | Cryptographic hash identical | ESTABLISHED | E1_post_analysis/E1_FROZEN_RESULT.json |
| E1 leakage was clean | Quarantined 6 matching claims | ESTABLISHED | data/processed/e1_population/manifest.json |
| B3 generalizes across constructions | AUROC inverted from 0.5463 to 0.3545 | NOT ESTABLISHED | E1_execution/statistical_analysis.json |
| B3 is construction-dependent | Extreme AUROC inversion (0.2754) | SUPPORTED | E1_post_analysis/hypothesis_assessment.json |
| B3 is intrinsically an implausibility detector | Requires isolating stylistic artifacts | NOT ESTABLISHED | E1_post_analysis/hypothesis_assessment.json |
| Stylistic confounding caused inversion | Requires instance-level extraction | NOT TESTABLE | E1_post_analysis/hypothesis_assessment.json |
| Domain shift contributes | AVeriTeC geometries likely differ from FEVER | PARTIALLY SUPPORTED | E1_post_analysis/hypothesis_assessment.json |
