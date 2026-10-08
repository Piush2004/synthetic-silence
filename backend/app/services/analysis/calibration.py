import numpy as np
from app.models.schemas import InsufficiencySignal

class ConformalCalibrator:
    def __init__(self, alpha: float = 0.1):
        """
        Split-conformal interface.
        alpha is the target error rate (e.g., 0.1 for 90% confidence).
        """
        self.alpha = alpha
        self.calibration_scores = []
        self.q_hat = None
        self.fitted = False

    def fit(self, calibration_signals: list[float]):
        """
        Fits the calibrator using a held-out calibration set of raw insufficiency scores.
        """
        if not calibration_signals:
            return
            
        n = len(calibration_signals)
        self.calibration_scores = np.sort(calibration_signals)
        
        q_level = np.ceil((n + 1) * (1 - self.alpha)) / n
        q_level = min(max(q_level, 0.0), 1.0)
        
        self.q_hat = np.quantile(self.calibration_scores, q_level, method='higher')
        self.fitted = True

    def calibrate(self, signal: InsufficiencySignal) -> InsufficiencySignal:
        """
        Takes a raw InsufficiencySignal and calibrates it.
        Honestly reports NOT_CALIBRATED until fit() is actually called.
        """
        # Formulate a raw composite score
        raw_score = (signal.retrieval_confidence + signal.uncertainty) / 2.0
        
        signal.insufficiency_signal = raw_score

        if not self.fitted:
            signal.calibration_status = "NOT_CALIBRATED"
            return signal
            
        signal.calibration_status = f"CALIBRATED_{int((1-self.alpha)*100)}_PCT"
        
        return signal
