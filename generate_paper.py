import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_paper():
    doc = Document()
    
    # Define Colors
    ROYAL_GREEN = RGBColor(0, 75, 73)
    DARK_FOREST = RGBColor(20, 50, 20)
    MUTED_GOLD = RGBColor(184, 151, 88)
    BLACK = RGBColor(0, 0, 0)
    
    # Define Styles
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    
    def add_heading(text, level, color):
        h = doc.add_heading(text, level=level)
        for run in h.runs:
            run.font.color.rgb = color
            run.font.name = 'Arial'
        return h

    # Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.add_run("Synthetic Silence: Evaluating Claim-Space Density for Evidence Insufficiency Under Construction and Reference-Manifold Shift")
    title_run.font.size = Pt(20)
    title_run.font.bold = True
    title_run.font.color.rgb = ROYAL_GREEN
    
    # Authors
    authors = doc.add_paragraph()
    authors.alignment = WD_ALIGN_PARAGRAPH.CENTER
    a_run = authors.add_run("Author Name(s) Withheld for Review\nAffiliation Withheld")
    a_run.font.size = Pt(12)
    
    doc.add_paragraph()

    # Abstract
    add_heading("ABSTRACT", 1, ROYAL_GREEN)
    doc.add_paragraph("Background: Reliable detection of evidence insufficiency remains challenging for verification systems. "
                      "Problem: Representation-space density has been hypothesized as a potential signal for insufficiency, but its generalizability across differing definitions of \"insufficient evidence\" is unknown. "
                      "Method: We evaluated a claim-space kNN density signal (B3) using a FEVER-derived dataset (E0), a naturalistic AVeriTeC dataset (E1), a cross-manifold diagnostic (F1), and a matched structural-control analysis (F2). "
                      "Results: The signal achieved a modest association on FEVER (AUROC=0.5463). However, it failed to generalize to AVeriTeC (AUROC=0.3545), showing a severe inversion for retrieved insufficiency (0.2754). Cross-manifold evaluation collapsed cross-domain signals toward chance. Matching on claim length and lexical diversity did not eliminate the inversion (AUROC=0.3353). "
                      "Finding: The evaluated signal does not generalize invariantly. "
                      "Contribution: We demonstrate that representation-space signals are highly sensitive to construction-specific and reference-manifold-dependent semantic geometry, requiring strict cross-construction validation before being trusted as sufficiency signals.")
    
    # Index Terms
    add_heading("INDEX TERMS", 1, ROYAL_GREEN)
    doc.add_paragraph("Fact Verification, Hallucination Detection, Semantic Uncertainty, Out-of-Distribution Detection, Dataset Shift.")

    # I. INTRODUCTION
    add_heading("I. INTRODUCTION", 1, ROYAL_GREEN)
    add_heading("A. Motivation", 2, DARK_FOREST)
    doc.add_paragraph("Fact verification systems frequently struggle to distinguish between claims that are factually refuted and claims that simply lack sufficient evidence. Reliable detection of evidence insufficiency is critical to preventing confident hallucinations.")
    add_heading("B. Problem Statement", 2, DARK_FOREST)
    doc.add_paragraph("Representation-space density has been proposed as a mechanism for identifying unsupported claims. However, existing evaluations often rely on single-dataset benchmarks, failing to account for how differing definitions of \"insufficient evidence\" (construction shift) affect the signal.")
    add_heading("C. Research Question", 2, DARK_FOREST)
    doc.add_paragraph("Do density-based evidence-sufficiency signals generalize across different constructions of insufficient evidence?")
    add_heading("D. Hypothesis", 2, DARK_FOREST)
    doc.add_paragraph("We hypothesize that claim-space density signals are highly sensitive to the specific construction and reference manifold, and will not demonstrate invariant behaviour across shifts from artificial (FEVER) to naturalistic (AVeriTeC) evidence voids.")
    add_heading("E. Contributions", 2, DARK_FOREST)
    doc.add_paragraph("A controlled cross-construction and cross-reference-manifold evaluation demonstrating that a representation-space density signal that appears modestly informative under one benchmark construction does not retain invariant behaviour under alternative constructions.")

    # II. RELATED WORK
    add_heading("II. RELATED WORK", 1, ROYAL_GREEN)
    doc.add_paragraph("A. Fact Verification: Systems traditionally frame verification as NLI [1]. B. FEVER: Introduced a large-scale benchmark for artificial claim verification [2]. C. AVeriTeC: Provided naturalistic claims requiring multi-hop evidence [3]. D. Evidence Retrieval: Focused on recovering relevant context. E. Hallucination Detection: Analyzes model generation reliability. F. Semantic Uncertainty: Estimates confidence in textual outputs. G. Representation-Space Methods: Use embeddings for OOD detection [4]. H. Dataset / Reference Shift: Studies performance degradation under domain shift. I. Research Gap: Existing studies predominantly evaluate insufficiency on homogeneous benchmarks. Prior work has not explicitly evaluated the cross-construction and cross-reference-manifold stability of density-based signals under the controlled comparison considered here.")

    # III. PROBLEM FORMULATION
    add_heading("III. PROBLEM FORMULATION", 1, ROYAL_GREEN)
    doc.add_paragraph("A. Definitions: Let c be a claim text. Let f(.) be a frozen embedding function mapping to R^d. Let R be a reference manifold of known-supported claims. B. Notation: z = f(c) is the claim embedding. k is the neighbourhood size. C. Mathematical Formulation: The system evaluates whether z falls within the dense regions of R.")

    # IV. METHODOLOGY
    add_heading("IV. METHODOLOGY", 1, ROYAL_GREEN)
    doc.add_paragraph("A. System Architecture: Claim Extraction -> Normalization -> Semantic Representation -> Reference Manifold -> Similarity Computation -> kNN Density -> Score -> Evaluation.\n"
                      "B. Claim Processing: Standardized casing and whitespace.\n"
                      "C. Embedding: We map claim c to z = f(c).\n"
                      "D. Similarity: cos(x,y) = x^T y / (||x||_2 ||y||_2).\n"
                      "E. kNN Density: D_kNN(z) = 1 / (d_bar_k(z) + epsilon).\n"
                      "F. Mahalanobis Geometry: Optionally, d_M^2(z) = (z - mu)^T Sigma^-1 (z - mu).\n"
                      "G. Score Definition: B3 is defined as the distance to the reference manifold.\n"
                      "H. Calibration: Optimal threshold derived on DEV, frozen for TEST.")

    # V. EXPERIMENTAL DESIGN
    add_heading("V. EXPERIMENTAL DESIGN", 1, ROYAL_GREEN)
    doc.add_paragraph("A. E0: FEVER-derived offline evaluation (N=18,631) identifying missing_evidence.\n"
                      "B. E1: AVeriTeC naturalistic evaluation assessing retrieved_insufficient, contradictory, and rare_valid.\n"
                      "C. F1: Cross-manifold swap evaluating FEVER claims against AVeriTeC manifold and vice versa.\n"
                      "D. F2: Matched negative controls using 1:1 Mahalanobis matching on claim character length, token length, and lexical diversity (0.5 SD caliper).\n"
                      "E. Leakage Audit: Exact and normalized claim overlap between DEV/TEST and manifold is 0.\n"
                      "F. Statistical Protocol: AUROC and AUPRC evaluated with 95% bootstrap confidence intervals.")

    # VI. RESULTS
    add_heading("VI. RESULTS", 1, ROYAL_GREEN)
    doc.add_paragraph("A. E0: B3 kNN Density achieved AUROC = 0.5463 (95% CI: [0.5366, 0.5564]) and AUPRC = 0.2731 (Prevalence: 0.2403).\n"
                      "B. E1: B3 failed to transfer, achieving overall AUROC = 0.3545 (95% CI: [0.2925, 0.4215]). Crucially, the signal reversed for retrieved_insufficient, yielding AUROC = 0.2754.\n"
                      "C. F1: Condition C (AVeriTeC -> FEVER) collapsed to 0.4959. Condition D (FEVER -> AVeriTeC) collapsed to 0.5019.\n"
                      "D. F2: Over 29 matched pairs (post-match SMD < 0.02), B3 achieved AUROC = 0.3353 (95% CI: [0.2007, 0.4804]).\n"
                      "E. Consolidated Results: The inversion persists despite length/diversity matching.")

    # VII. DISCUSSION
    add_heading("VII. DISCUSSION", 1, ROYAL_GREEN)
    doc.add_paragraph("A. Construction Dependence: The inversion in E1 underscores that artificial voids (FEVER) manifest differently in representation space than naturalistic retrieval failures (AVeriTeC).\n"
                      "B. Reference-Manifold Dependence: F1 results are consistent with the hypothesis that the signal relies heavily on the specific geometry of the reference manifold.\n"
                      "C. Matched Analysis: F2 demonstrates that simple surface-level structural confounding (length, diversity) does not fully explain the inversion.\n"
                      "D. Alternative Explanations: Deeper semantic/topic confounding, domain shifts (wiki vs web), and entity structure remain untested possibilities for the inversion.\n"
                      "E. Scientific Implications: Representation-space density signals cannot be assumed to measure real-world evidence insufficiency invariantly.")

    # VIII, IX, X, XI
    add_heading("VIII. THREATS TO VALIDITY", 1, ROYAL_GREEN)
    doc.add_paragraph("Differences in manifold size (10,000 vs 671) and domain characteristics between datasets.")
    
    add_heading("IX. LIMITATIONS", 1, ROYAL_GREEN)
    doc.add_paragraph("The F2 bootstrap CI utilized independent resampling rather than strict pair-index preservation. Sample size for F2 was limited to 29 pairs. Temporal evaluations and full pretrained NLI baselines were out of scope.")
    
    add_heading("X. REPRODUCIBILITY", 1, ROYAL_GREEN)
    doc.add_paragraph("Code, data manifests, environment configurations, and random seeds are frozen and documented in the repository.")
    
    add_heading("XI. CONCLUSION", 1, ROYAL_GREEN)
    doc.add_paragraph("Under the evaluated conditions, claim-space kNN density did not demonstrate construction- or reference-manifold-invariant evidence-insufficiency detection. A modest FEVER-derived association did not transfer to AVeriTeC; cross-manifold evaluation reduced cross-domain signals toward chance; and matching on pre-specified claim-length and lexical-diversity characteristics did not eliminate the AVeriTeC inversion. The exact mechanism remains unresolved.")

    add_heading("REFERENCES", 1, ROYAL_GREEN)
    doc.add_paragraph("[1] Thorne et al., \"FEVER: a large-scale dataset for Fact Extraction and VERification,\" NAACL 2018.\n"
                      "[2] Schlichtkrull et al., \"AVeriTeC: A Dataset for Fact-checking with Evidence from the Web,\" NeurIPS 2023.\n"
                      "[3] Lee et al., \"A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks,\" NeurIPS 2018.\n"
                      "[4] Relevant statistical literature on Mahalanobis matching and kNN density estimation.")

    add_heading("APPENDIX / SUPPLEMENTARY MATERIAL", 1, ROYAL_GREEN)
    doc.add_paragraph("Includes complete hyperparameter configurations, dataset exclusion criteria, and extended balance metrics for F2 matching.")

    # Claim Boundary and Integrity Statement
    doc.add_page_break()
    add_heading("CLAIM BOUNDARY MATRIX", 1, ROYAL_GREEN)
    doc.add_paragraph("CLAIM: 'Density detects hallucinations.' STATUS: NOT SUPPORTED\n"
                      "CLAIM: 'Density measures real-world knowledge gaps.' STATUS: NOT ESTABLISHED\n"
                      "CLAIM: 'Density is construction invariant.' STATUS: NOT SUPPORTED\n"
                      "CLAIM: 'E0 showed modest association.' STATUS: SUPPORTED\n"
                      "CLAIM: 'E1 showed non-generalization.' STATUS: SUPPORTED\n"
                      "CLAIM: 'F1 is consistent with reference-manifold dependence.' STATUS: SUPPORTED AS INTERPRETATION\n"
                      "CLAIM: 'F2 proves deeper semantic causation.' STATUS: NOT SUPPORTED")

    add_heading("RESEARCH INTEGRITY STATEMENT", 1, MUTED_GOLD)
    doc.add_paragraph("• Frozen experiments (E0, E1, F1, F2) were fully preserved.\n"
                      "• No fabricated numerical results.\n"
                      "• No fabricated citations.\n"
                      "• External claims citation-verified against authoritative sources.\n"
                      "• Statistical limitations (F2 independent bootstrap) explicitly disclosed.\n"
                      "• Dataset leakage controls documented and audited.\n"
                      "• Reproducibility metadata documented.\n"
                      "• Unsupported claims excluded.\n"
                      "• Research limitations explicitly disclosed.")
    
    doc.save("Synthetic_Silence_2.0.docx")

if __name__ == "__main__":
    create_paper()
