import asyncio
from typing import List, Dict, Any
from .data_adapters.base import BenchmarkInstance
from app.services.algo.engine import CoreResearchEngine
from app.services.claim_service import ClaimService
from app.models.claim import NormalizedClaim

class ExperimentRunner:
    def __init__(self, core_engine: CoreResearchEngine, claim_service: ClaimService):
        self.core_engine = core_engine
        self.claim_service = claim_service

    async def run_benchmark(self, instances: List[BenchmarkInstance]) -> List[Dict[str, Any]]:
        """
        Runs the CoreResearchEngine against a batch of benchmark instances.
        Bypasses live retrieval to ensure reproducible, frozen-data benchmarking.
        """
        results = []
        
        for instance in instances:
            # 1. Normalize the benchmark claim (required for the engine)
            normalized_claim = await self.claim_service.normalize_claim(instance.claim)
            
            # 2. Run the core algorithmic signals (Density, Uncertainty, NLI)
            # using the frozen evidence provided by the benchmark adapter.
            signal = await self.core_engine.compute_signals(
                claim=normalized_claim,
                evidence_list=instance.evidence
            )
            
            # 3. Record results for metric computation
            results.append({
                "claim_id": instance.claim.id,
                "dataset": instance.dataset_name,
                "true_is_insufficient": instance.is_insufficient,
                "true_family": instance.true_construction_family.value if instance.true_construction_family else None,
                # The raw composite score we want to evaluate for AUROC
                "predicted_insufficiency_score": signal.insufficiency_signal, 
                "predicted_density": signal.representation_density,
                "predicted_uncertainty": signal.uncertainty,
                "predicted_contradiction": signal.contradiction_level
            })
            
        return results
