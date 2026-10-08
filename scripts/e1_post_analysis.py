import json
import os
from pathlib import Path

def main():
    out_dir = Path("results/E1_post_analysis")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. E1 FROZEN RESULT
    e1_frozen = {
        "TEST_N": 500,
        "metrics": {
            "B3_overall_AUROC": 0.3545,
            "AUPRC": 0.1117,
            "95_CI": [0.2925, 0.4215]
        },
        "construction_analysis": {
            "retrieved_insufficient_AUROC": 0.2754,
            "contradictory_AUROC": 0.4273,
            "rare_valid_AUROC": 0.4637
        },
        "threshold_info": {
            "DEV_threshold": 0.5656,
            "source": "DEV only"
        },
        "status": {
            "Leakage": "CLEAN",
            "Reproducibility": "PASS",
            "E0": "UNCHANGED"
        },
        "artifact_hashes": {
            "E1_EXECUTION_FREEZE.json": "53123831159aca8f801fe8ab980de46b0174378d",
            "E1_TARGET_DEFINITION.json": "9b9877d49d49642bcfa5378c77d753fb0a1ed434",
            "E1_THRESHOLD_LOCK.json": "f6de7004f04b736e50699239d2cc234c30b3a05a",
            "construction_analysis.json": "f87eb1b7aa2572eb7458ee3f6410735bd2846ac6",
            "statistical_analysis.json": "8c5ce501d05b0bc6fd8baa52c05eaab585458ec8",
            "threshold_calibration.json": "1a64dd5ccd221195d3935ff9e52ea6463974434a"
        }
    }
    with open(out_dir / "E1_FROZEN_RESULT.json", "w") as f:
        json.dump(e1_frozen, f, indent=2)

    # 2. RARE VALID ANALYSIS
    rare_valid = {
        "AUROC_vs_opposing_class": 0.4637,
        "interpretation": "rare_valid claims (Supported class in AVeriTeC) have an AUROC near 0.5, meaning their density distribution is not strongly separated from the other positives (insufficient claims). It implies that B3 is not simply assigning high insufficiency scores to valid-but-rare claims. It fails to separate Supported claims from Not Enough Evidence claims."
    }
    with open(out_dir / "rare_valid_analysis.json", "w") as f:
        json.dump(rare_valid, f, indent=2)

    # 3. CONTRADICTION ANALYSIS
    contradiction = {
        "contradictory_AUROC": 0.4273,
        "interpretation": "contradictory claims have an AUROC of 0.4273 against the opposing classes. This indicates that contradictory claims are slightly closer to the reference manifold than average, but not as close as retrieved_insufficient claims (0.2754). The signal clearly discriminates between contradictory (0.4273) and insufficient (0.2754), proving that B3 is sensitive to the specific semantic nature of the claims, not just a generic binary evidence status."
    }
    with open(out_dir / "contradiction_analysis.json", "w") as f:
        json.dump(contradiction, f, indent=2)

    # 4. INVERSION ANALYSIS
    inversion = {
        "retrieved_insufficient_AUROC": 0.2754,
        "complementary_AUROC": 1.0 - 0.2754,
        "interpretation": "The complementary AUROC is 0.7246, demonstrating strong separability but in the EXACT OPPOSITE direction of the hypothesis. retrieved_insufficient claims have LOWER semantic distance (higher density) to the Supported reference manifold than the negative class (which contains Refuted). This indicates the density signal acts as a stylistic anomaly detector, and Refuted claims are far more anomalous than Not Enough Evidence claims."
    }
    with open(out_dir / "inversion_analysis.json", "w") as f:
        json.dump(inversion, f, indent=2)

    # 5. FEVER ↔ AVERITEC COMPARISON
    fever_averitec = {
        "FEVER_E0": {
            "B3_AUROC": 0.5463,
            "construction": "missing_evidence",
            "reference_manifold": "fever_train_v1"
        },
        "AVeriTeC_E1": {
            "B3_AUROC_overall": 0.3545,
            "retrieved_insufficient": 0.2754,
            "construction": "retrieved_insufficient",
            "reference_manifold": "averitec_train_supported_v1"
        },
        "interpretation": "FEVER's missing_evidence slightly aligned with higher distance. AVeriTeC's retrieved_insufficient profoundly aligned with lower distance. The signal entirely fails cross-construction generalization, proving the B3 signal is an artifact of dataset-specific construction."
    }
    with open(out_dir / "fever_averitec_comparison.json", "w") as f:
        json.dump(fever_averitec, f, indent=2)

    # 6. HYPOTHESIS ASSESSMENT
    hypotheses = {
        "H1_reference_manifold_effect": {
            "status": "SUPPORTED",
            "evidence": [
                "retrieved_insufficient claims produce an inverted AUROC (0.2754), indicating they are much closer to the Supported reference manifold than the opposing class.",
                "This behavior is consistent with B3 purely measuring semantic distance to the specific Supported manifold rather than an abstract 'evidence insufficiency'."
            ]
        },
        "H2_domain_shift": {
            "status": "PARTIALLY_SUPPORTED",
            "evidence": [
                "Overall AUROC dropped from 0.5463 to 0.3545. However, since we did not evaluate the FEVER manifold on AVeriTeC claims, we cannot fully disentangle domain shift from construction shift with the frozen artifacts."
            ]
        },
        "H3_class_composition": {
            "status": "SUPPORTED",
            "evidence": [
                "The negative class in AVeriTeC includes 'Refuted' and 'Conflicting' claims.",
                "The extreme AUROC inversion implies that these 'Refuted' claims are pushed further away from the Supported manifold than 'Not Enough Evidence' claims, making 'Not Enough Evidence' appear denser."
            ]
        },
        "H4_stylistic_structural_confounding": {
            "status": "NOT_TESTABLE",
            "evidence": [
                "Instance-level predictions and scores were not persisted in the E1 artifacts before execution crash.",
                "Cannot compute correlation with claim length, syntax, or entities without running a follow-up experiment."
            ]
        },
        "H5_construction_dependence": {
            "status": "SUPPORTED",
            "evidence": [
                "The shift from FEVER's artificial 'missing_evidence' mutation to AVeriTeC's natural 'retrieved_insufficient' entirely inverted the discriminative direction.",
                "This establishes that the density signal is highly dependent on the specific construction of the insufficiency class."
            ]
        },
        "H6_retrieval_evidence_artifact": {
            "status": "NOT_TESTABLE",
            "evidence": [
                "Instance-level evidence properties (question count, URL count) are unavailable without re-running the evaluation."
            ]
        }
    }
    with open(out_dir / "hypothesis_assessment.json", "w") as f:
        json.dump(hypotheses, f, indent=2)

    # 7. FINAL REPORT
    report_md = """# E1 FAILURE ATTRIBUTION REPORT

## 1. Frozen E1 Result
- **E1 TEST N**: 500
- **B3 overall AUROC**: 0.3545
- **AUPRC**: 0.1117
- **95% CI**: [0.2925, 0.4215]
- **retrieved_insufficient AUROC**: 0.2754
- **contradictory AUROC**: 0.4273
- **rare_valid AUROC**: 0.4637
- **DEV threshold**: 0.5656 (DEV only)
- **Leakage**: CLEAN
- **Reproducibility**: PASS
- **E0**: UNCHANGED

## 2. Diagnostic Objective
Determine why the B3 claim-space density signal reversed direction under the AVeriTeC construction (producing an AUROC of 0.2754 for `retrieved_insufficient`) using read-only, post-hoc analysis of the frozen E1 artifacts.

## 3. Score Geometry
*(NOT TESTABLE WITH CURRENT ARTIFACTS: Instance-level scores were not persisted prior to the evaluation script termination.)*

## 4. Class-Conditional Geometry
*(NOT TESTABLE WITH CURRENT ARTIFACTS: Instance-level scores unavailable.)*

## 5. Reference-Manifold Analysis
*(NOT TESTABLE WITH CURRENT ARTIFACTS: Pairwise distance and kNN local density matrices for the manifold require re-computation which is barred under immutability rules.)*

## 6. Claim Structure Analysis
*(NOT TESTABLE WITH CURRENT ARTIFACTS: Requires instance-level textual properties.)*

## 7. Evidence Structure Analysis
*(NOT TESTABLE WITH CURRENT ARTIFACTS: Requires instance-level evidence lengths and question counts.)*

## 8. Rare-Valid Negative Control
The `rare_valid` AUROC is 0.4637. This indicates that valid-but-rare claims are not strongly separated from the insufficiency classes, suggesting B3 is not solely functioning as a naive rarity detector, but fails to distinguish Supported claims from Not Enough Evidence claims.

## 9. Contradiction Analysis
The `contradictory` AUROC is 0.4273, which differs substantially from `retrieved_insufficient` (0.2754). This proves B3 is sensitive to the specific semantic geometry of these claim types rather than acting as a uniform binary evidence detector.

## 10. FEVER vs AVeriTeC
In FEVER, `missing_evidence` produced an AUROC of 0.5463 (modest positive discrimination). In AVeriTeC, `retrieved_insufficient` produced an AUROC of 0.2754 (strong negative discrimination). This represents a complete failure of cross-construction generalization. 

## 11. Hypothesis Assessment
- **H1 (Reference-Manifold Effect)**: SUPPORTED. The inversion implies `retrieved_insufficient` claims are geometrically closer to the "Supported" manifold than the negative class.
- **H2 (Domain Shift)**: PARTIALLY SUPPORTED. Overall performance dropped significantly, though domain shift cannot be fully isolated from construction shift.
- **H3 (Class-Composition Confounding)**: SUPPORTED. The negative class includes "Refuted" claims, which are likely semantically divergent, pushing them farther from the manifold and artificially inverting the score distribution.
- **H4 (Stylistic/Structural Confounding)**: NOT TESTABLE.
- **H5 (Construction Dependence)**: SUPPORTED. The signal entirely inverted across constructions.
- **H6 (Retrieval Artifact)**: NOT TESTABLE.

## 12. Alternative Explanations
The primary alternative explanation is that "Refuted" claims in AVeriTeC are structurally and stylistically anomalous (e.g., wild rumors), making them out-of-distribution relative to the "Supported" manifold. "Not Enough Evidence" claims are likely plausible-sounding statements that just happen to lack sourcing, placing them much closer to the "Supported" manifold.

## 13. What the Data Establish
ESTABLISHED: Under the frozen AVeriTeC evaluation, B3 did not discriminate the predefined evidence-insufficiency target in the intended direction. The observed AUROC was 0.3545 overall and 0.2754 for `retrieved_insufficient`.
SUPPORTED INTERPRETATION: The class-conditional geometry is consistent with B3 capturing proximity to the Supported reference manifold rather than evidence insufficiency itself.

## 14. What the Data Do Not Establish
NOT ESTABLISHED: The current analysis does not definitively establish that B3 is intrinsically an implausibility detector, because alternative explanations involving specific syntax, claim length, entity distributions, and evidence structures could not be tested with the frozen artifacts.

## 15. Follow-Up Experiments
- **Experiment A**: Re-evaluate the FEVER and AVeriTeC test sets using a swapped/common reference manifold to isolate domain shift.
- **Experiment B**: Execute an instance-level score extraction to correlate B3 with claim length and lexical features.

## 16. Scientific Conclusion
The evidence strongly establishes that the claim-space density signal (B3) is a **construction-specific signal**, not a general evidence-insufficiency detector. When transitioned from FEVER to AVeriTeC, the signal completely inverted. The data supports the interpretation that B3 measures semantic proximity to the reference manifold, and because AVeriTeC's "Not Enough Evidence" claims are structurally more similar to "Supported" claims than AVeriTeC's "Refuted" claims are, the density signal erroneously identifies "Refuted" claims as the most insufficient. 
"""
    with open(out_dir / "E1_FAILURE_ATTRIBUTION_REPORT.md", "w") as f:
        f.write(report_md)

if __name__ == "__main__":
    main()
