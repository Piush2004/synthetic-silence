export enum ConstructionFamily {
  missing_evidence = "missing_evidence",
  retrieved_insufficient = "retrieved_insufficient",
  wrong_retrieval = "wrong_retrieval",
  contradictory = "contradictory",
  rare_valid = "rare_valid",
  long_tail = "long_tail",
  temporal_novelty = "temporal_novelty",
  ood = "ood",
  hallucination = "hallucination",
  ambiguous_claim = "ambiguous_claim"
}

export interface Evidence {
  id: string;
  text: string;
  source_url?: string;
  construction_family: ConstructionFamily;
}

export interface InsufficiencySignal {
  evidence_coverage: number;
  semantic_support: number;
  retrieval_confidence: number;
  contradiction_level: number;
  temporal_coverage: number;
  representation_density: number;
  uncertainty: number;
  insufficiency_signal: number;
  construction_family_estimate: string | null;
  calibration_status: string; // default should be "NOT_CALIBRATED"
}

// API Response Models
export interface ClaimResult {
  claim: {
    id: string;
    original_text: string;
    context: string;
  };
  signal: InsufficiencySignal;
  explanation: string;
}

export interface AnalyzeResponse {
  results: ClaimResult[];
}
