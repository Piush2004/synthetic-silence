from fastapi import APIRouter, Depends, HTTPException
from app.models.api_schemas import AnalyzeRequest, AnalyzeResponse, ClaimResult
from app.services.pipeline import ResearchPipeline

router = APIRouter()

def get_pipeline():
    """
    Dependency injection stub for the ResearchPipeline.
    In a fully wired app, this returns the instantiated singleton pipeline.
    """
    raise NotImplementedError("Pipeline dependency not fully wired in this stub.")

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest, pipeline: ResearchPipeline = Depends(get_pipeline)):
    """
    Receives raw text from the Chrome Extension, runs it through the Research Pipeline,
    and returns the extracted claims with their calibrated insufficiency signals and explanations.
    """
    try:
        pipeline_results = await pipeline.run(request.source_text)
        
        response_results = []
        for claim, signal, explanation in pipeline_results:
            response_results.append(
                ClaimResult(
                    claim=claim,
                    signal=signal,
                    explanation=explanation
                )
            )
            
        return AnalyzeResponse(results=response_results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
