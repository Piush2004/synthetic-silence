from typing import List, Dict, Any
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
import numpy as np

class Evaluator:
    @staticmethod
    def evaluate_insufficiency_detection(results: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Computes AUROC, Precision, Recall, and F1 for the binary insufficiency classification task.
        """
        if not results:
            return {}
            
        y_true = [1 if r["true_is_insufficient"] else 0 for r in results]
        
        # We need a numerical score to compute AUROC. 
        # If the pipeline hasn't calibrated an exact scalar yet, we might use a fallback heuristic
        # combining inverse density and uncertainty for the raw evaluation.
        y_scores = []
        for r in results:
            score = r.get("predicted_insufficiency_score")
            if score is None:
                # Fallback composite if calibration hasn't run
                density = r.get("predicted_density", 1.0)
                if density is None: density = 1.0
                unc = r.get("predicted_uncertainty", 1.0)
                if unc is None: unc = 1.0
                # Higher score = more insufficient
                score = ((1.0 - density) + unc) / 2.0
            y_scores.append(score)

        # For strict P/R/F1 we need a threshold. We use a naive 0.5 threshold for uncalibrated raw scores.
        # Ideally, we calculate the optimal threshold or rely on the conformal calibration layer.
        y_pred = [1 if s > 0.5 else 0 for s in y_scores]
        
        try:
            auroc = roc_auc_score(y_true, y_scores)
        except ValueError:
            # Happens if only one class is present in the batch
            auroc = float('nan')
            
        return {
            "AUROC": auroc,
            "Precision": precision_score(y_true, y_pred, zero_division=0),
            "Recall": recall_score(y_true, y_pred, zero_division=0),
            "F1": f1_score(y_true, y_pred, zero_division=0)
        }
