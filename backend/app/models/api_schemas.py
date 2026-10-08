from pydantic import BaseModel
from typing import List
from app.models.claim import ExtractedClaim
from app.models.schemas import InsufficiencySignal

class AnalyzeRequest(BaseModel):
    source_text: str

class ClaimResult(BaseModel):
    claim: ExtractedClaim
    signal: InsufficiencySignal
    explanation: str

class AnalyzeResponse(BaseModel):
    results: List[ClaimResult]
