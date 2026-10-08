import numpy as np
from typing import List
from app.models.claim import NormalizedClaim
from app.models.schemas import Evidence, InsufficiencySignal
from app.services.algo.embeddings import EmbeddingService
from app.services.algo.density import DensityEstimator
from app.services.algo.uncertainty import SimilarityDistributionEntropy
from app.services.algo.nli import LLMNLIAdapter

class CoreResearchEngine:
    def __init__(
        self, 
        embedding_service: EmbeddingService,
        density_estimator: DensityEstimator,
        uncertainty_module: SimilarityDistributionEntropy,
        nli_service: LLMNLIAdapter
    ):
        self.embedder = embedding_service
        self.density = density_estimator
        self.uncertainty = uncertainty_module
        self.nli = nli_service

    async def compute_signals(
        self, 
        claim: NormalizedClaim, 
        evidence_list: List[Evidence]
    ) -> InsufficiencySignal:
        
        # 1. Semantic Representation
        claim_emb = self.embedder.get_embeddings([claim.normalized_text])
        evidence_texts = [ev.text for ev in evidence_list]
        evidence_embs = self.embedder.get_embeddings(evidence_texts)
        
        # 2. Density / Neighborhood
        density_scores = self.density.compute_density_signal(claim_emb) 
        avg_density = float(np.mean(density_scores)) if len(density_scores) > 0 else None # Changed from 1.0 to None
        
        # 3. Uncertainty (Similarity Entropy)
        uncertainty_score = self.uncertainty.compute_uncertainty(claim_emb, evidence_embs)
        
        # 4. Entailment & Contradiction
        entailment, contradiction = await self.nli.verify_entailment(claim.normalized_text, evidence_texts)
        
        # Assemble the uncalibrated Insufficiency Signal
        signal = InsufficiencySignal(
            evidence_coverage=1.0 if len(evidence_list) > 0 else 0.0,
            semantic_support=entailment, 
            retrieval_confidence=max(0.0, 1.0 - avg_density) if avg_density is not None else None,
            contradiction_level=contradiction,
            temporal_coverage=None, # Stub for temporal module
            representation_density=avg_density, 
            uncertainty=uncertainty_score,
            insufficiency_signal=None, # Explicitly None until calibrated
            construction_family_estimate=None,
            calibration_status="NOT_CALIBRATED"
        )
        
        return signal
