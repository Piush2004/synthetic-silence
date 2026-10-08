from typing import List
from app.models.schemas import Evidence

class TemporalAnalysisService:
    def __init__(self, cutoff_year: int = 2023):
        """
        Analyzes the temporal distribution of evidence.
        The cutoff_year represents the boundary for the pre/post cutoff split test.
        """
        self.cutoff_year = cutoff_year

    def compute_temporal_coverage(self, evidence_list: List[Evidence]) -> float:
        """
        Computes a temporal coverage score. 
        Returns a float between 0.0 and 1.0 representing coverage density over the cutoff.
        """
        if not evidence_list:
            return 0.0

        post_cutoff_count = 0
        pre_cutoff_count = 0
        
        for ev in evidence_list:
            # We assume publication_year will be dynamically attached during OpenAlex mapping
            year = ev.publication_year if getattr(ev, 'publication_year', None) is not None else self.cutoff_year - 1
            if year >= self.cutoff_year:
                post_cutoff_count += 1
            else:
                pre_cutoff_count += 1

        total = len(evidence_list)
        if total == 0:
            return 0.0
            
        coverage_score = post_cutoff_count / total
        return float(coverage_score)

    def extract_temporal_feature_ratio(self, temporal_coverage: float) -> bool:
        """
        Heuristic prototype feature. 
        Note: This is a temporal feature calculation (ratio > 0.8), NOT a mathematically complete 
        temporal novelty detector. It flags anomalous post-cutoff distributions.
        """
        return temporal_coverage > 0.8
