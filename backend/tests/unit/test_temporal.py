import pytest
from app.services.analysis.temporal import TemporalAnalysisService
from app.models.schemas import Evidence, ConstructionFamily

def test_temporal_empty_evidence():
    service = TemporalAnalysisService(cutoff_year=2023)
    coverage = service.compute_temporal_coverage([])
    assert coverage == 0.0

def test_temporal_all_pre_cutoff():
    service = TemporalAnalysisService(cutoff_year=2023)
    ev1 = Evidence(id="1", text="old", construction_family=ConstructionFamily.ambiguous_claim)
    ev1.publication_year = 2020
    coverage = service.compute_temporal_coverage([ev1])
    assert coverage == 0.0
    assert not service.extract_temporal_feature_ratio(coverage)

def test_temporal_all_post_cutoff():
    service = TemporalAnalysisService(cutoff_year=2023)
    ev1 = Evidence(id="1", text="new", construction_family=ConstructionFamily.ambiguous_claim)
    ev1.publication_year = 2024
    coverage = service.compute_temporal_coverage([ev1])
    assert coverage == 1.0
    assert service.extract_temporal_feature_ratio(coverage)

def test_temporal_mixed_cutoff():
    service = TemporalAnalysisService(cutoff_year=2023)
    ev1 = Evidence(id="1", text="old", construction_family=ConstructionFamily.ambiguous_claim)
    ev1.publication_year = 2020
    ev2 = Evidence(id="2", text="new", construction_family=ConstructionFamily.ambiguous_claim)
    ev2.publication_year = 2024
    coverage = service.compute_temporal_coverage([ev1, ev2])
    assert coverage == 0.5
    assert not service.extract_temporal_feature_ratio(coverage)
    
def test_temporal_missing_year():
    service = TemporalAnalysisService(cutoff_year=2023)
    ev1 = Evidence(id="1", text="missing date", construction_family=ConstructionFamily.ambiguous_claim)
    # The current stub defaults to cutoff_year - 1 (i.e. pre-cutoff) for missing dates.
    coverage = service.compute_temporal_coverage([ev1])
    assert coverage == 0.0
