from typing import List, Tuple
from app.models.claim import ExtractedClaim
from app.models.schemas import InsufficiencySignal
from app.services.claim_service import ClaimService
from app.services.retrieval_service import OpenAlexRetrievalService
from app.services.ranking_service import EvidenceRankingService
from app.services.algo.engine import CoreResearchEngine
from app.services.analysis.temporal import TemporalAnalysisService
from app.services.analysis.calibration import ConformalCalibrator
from app.services.analysis.explanation import ExplanationService

class ResearchPipeline:
    def __init__(
        self,
        claim_service: ClaimService,
        retrieval_service: OpenAlexRetrievalService,
        ranking_service: EvidenceRankingService,
        core_engine: CoreResearchEngine,
        temporal_service: TemporalAnalysisService,
        calibrator: ConformalCalibrator,
        explanation_service: ExplanationService
    ):
        self.claim_service = claim_service
        self.retrieval = retrieval_service
        self.ranking = ranking_service
        self.core = core_engine
        self.temporal = temporal_service
        self.calibrator = calibrator
        self.explanation = explanation_service

    async def run(self, source_text: str) -> List[Tuple[ExtractedClaim, InsufficiencySignal, str]]:
        """
        Executes the full pipeline:
        1. Extract & Normalize Claims
        2. Retrieve & Rank Evidence
        3. Core Algorithm (Density, Uncertainty, NLI)
        4. Temporal Analysis
        5. Calibration
        6. Explanation Generation
        """
        results = []
        
        # 1. Extraction
        extracted_claims = await self.claim_service.extract_claims(source_text)
        
        for claim in extracted_claims:
            # Normalization
            normalized = await self.claim_service.normalize_claim(claim)
            
            # 2. Retrieval
            raw_evidence = await self.retrieval.retrieve_evidence(normalized)
            ranked_evidence = await self.ranking.filter_and_rank(raw_evidence)
            
            # 3. Core Compute
            signal = await self.core.compute_signals(normalized, ranked_evidence)
            
            # 4. Temporal Analysis
            temporal_coverage = self.temporal.compute_temporal_coverage(ranked_evidence)
            signal.temporal_coverage = temporal_coverage
            
            # 5. Classification Heuristic (Baseline Prototype)
            # This is a temporary placeholder heuristic, NOT a learned model.
            # Arbitrary weights/thresholds are used here strictly for architectural wiring.
            if self.temporal.extract_temporal_feature_ratio(temporal_coverage):
                signal.construction_family_estimate = "temporal_novelty"
            elif signal.contradiction_level > 0.7:
                signal.construction_family_estimate = "contradictory"
            elif signal.evidence_coverage == 0.0:
                signal.construction_family_estimate = "missing_evidence"
            else:
                signal.construction_family_estimate = "ambiguous_claim"
                
            # 6. Calibration
            calibrated_signal = self.calibrator.calibrate(signal)
            
            # 7. Explanation
            explanation_text = await self.explanation.generate_explanation(calibrated_signal, claim.original_text)
            
            results.append((claim, calibrated_signal, explanation_text))
            
        return results
