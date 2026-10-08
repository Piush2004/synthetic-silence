from typing import List, Tuple
from pydantic import BaseModel
from app.services.llm_provider import LLMProvider

class NLIPrediction(BaseModel):
    entailment_score: float # 0.0 to 1.0
    contradiction_score: float # 0.0 to 1.0
    neutral_score: float # 0.0 to 1.0
    explanation: str

class LLMNLIAdapter:
    def __init__(self, llm_provider: LLMProvider):
        """
        Uses an LLM provider to generate structured NLI judgments.
        This is a prototype adapter and NOT a verified off-the-shelf NLI baseline.
        """
        self.llm_provider = llm_provider

    async def verify_entailment(self, claim_text: str, evidence_texts: List[str]) -> Tuple[float, float]:
        """
        Returns an aggregate (entailment_level, contradiction_level) based on NLI.
        """
        if not evidence_texts:
            return 0.0, 0.0
            
        # Combine evidence for a single aggregate verification pass.
        combined_evidence = " | ".join(evidence_texts)
        
        prompt = (
            "You are an NLI (Natural Language Inference) engine. "
            f"Premise (Evidence Set): {combined_evidence}\n"
            f"Hypothesis (Claim): {claim_text}\n"
            "Score the relationship between the Premise and Hypothesis on a scale of 0.0 to 1.0 "
            "for Entailment, Contradiction, and Neutral."
        )
        
        result = await self.llm_provider.generate_structured_output(prompt, NLIPrediction)
        
        return result.entailment_score, result.contradiction_score
