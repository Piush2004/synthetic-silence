# F2 Matched Negative Controls

## 1. Research Question
Does claim-space density (B3) distinguish the intended insufficiency condition from an appropriately matched control population, or does its apparent discrimination largely disappear when structural characteristics are controlled?

## 2. Motivation
E1 observed a severe AUROC inversion (0.2754) for the `retrieved_insufficient` construction. F2 isolates whether observable structural traits (length, lexical diversity) confound this signal.

## 3. Frozen Dependencies
- E1 TEST predictions & labels
- AVeriTeC reference manifold
- B3 density algorithm (all-MiniLM-L6-v2 + Mahalanobis)

## 4. Candidate Control Population
Target: `retrieved_insufficient`
Control Candidate: `rare_valid` (Supported)

## 5. Matching Variables
1. Claim Length (characters)
2. Claim Length (words)
3. Lexical Diversity (unique words / total words)

## 6. Matching Method
1:1 Nearest-Neighbor matching using Euclidean distance on standardized features, with a 0.5 standard deviation caliper, performed strictly without B3 visibility.

## 7. Matching Protocol
Pre-registered and locked in `F2_PROTOCOL.md` prior to executing B3.

## 8. Balance Diagnostics
- Pre-match SMDs: [np.float64(0.05708402531636755), np.float64(0.1608318358262692), np.float64(0.2653470704557221)]
- Post-match SMDs: [np.float64(0.01351929807687365), np.float64(0.0166847460861545), np.float64(0.008150397630806666)]
Balance substantially improved across all features.

## 9. Leakage Audit
CLEAN. Matching constructed on isolated non-B3 variables within the disjoint test split.

## 10. B3 Results
Matched B3 AUROC: 0.3353

## 11. Comparison with E1
| Analysis | Population | AUROC | AUPRC | 95% CI | Status |
|---|---|---|---|---|---|
| E1 | Original retrieved_insufficient | 0.2754 | — | — | FROZEN |
| F2 | Matched controls | 0.3353 | 0.4035 | [0.2007, 0.4804] | F2 |
| Chance | Reference | 0.5000 | — | — | Reference |

## 12. Statistical Analysis
Bootstrap intervals were constructed over the matched paired dataset (1,000 iterations).

## 13. Interpretation
The signal remained inverted after structural matching, suggesting the inversion is not fully explained by these observable characteristics.

## 14. Alternative Explanations
If inverted, reference-manifold geometry or uncaptured semantic domains could explain the persisting bias. If chance, the original signal was a purely structural artifact.

## 15. Limitations
Matching variables are coarse. Finer semantic nuances (e.g. specific entity prevalence) were not matched.

## 16. Scientific Conclusion
Observable structural matching does not resolve the original inversion, providing evidence that B3 is responsive to deeper geometric or semantic properties independent of length/lexical diversity.
