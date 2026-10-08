from pydantic import BaseModel
from app.models.schemas import InsufficiencySignal
from app.services.llm_provider import LLMProvider

class ExplanationOutput(BaseModel):
    explanation: str

class ExplanationService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def generate_explanation(self, signal: InsufficiencySignal, claim_text: str) -> str:
        """
        Generates a natural-language explanation of the score breakdown.
        """
        prompt = (
            f"You are an analytical engine explaining why a claim lacks sufficient evidence.\n"
            f"Claim: '{claim_text}'\n\n"
            f"Signal Breakdown:\n"
            f"- Evidence Coverage: {signal.evidence_coverage:.2f}\n"
            f"- Semantic Support (NLI Entailment): {signal.semantic_support:.2f}\n"
            f"- Contradiction Level: {signal.contradiction_level:.2f}\n"
            f"- Retrieval Confidence (Inverse Density): {signal.retrieval_confidence:.2f}\n"
            f"- Temporal Coverage (Post-Cutoff Ratio): {signal.temporal_coverage:.2f}\n"
            f"- Information Uncertainty (InfoNCE): {signal.uncertainty:.2f}\n"
            f"- Estimated Insufficiency Type: {signal.construction_family_estimate}\n\n"
            "Provide a concise, 2-3 sentence natural language explanation of these metrics, "
            "focusing on the dominant reason for insufficiency (e.g., high contradiction, "
            "temporal recency, or total information void)."
        )
            
        result = await self.llm_provider.generate_structured_output(prompt, ExplanationOutput)
        return result.explanation
