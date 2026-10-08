import numpy as np

class SimilarityDistributionEntropy:
    def __init__(self, temperature: float = 0.1):
        self.temperature = temperature
        
    def compute_uncertainty(self, claim_embedding: np.ndarray, evidence_embeddings: np.ndarray) -> float:
        """
        Computes uncertainty using the entropy of a softmax distribution over cosine similarities 
        between the claim and the retrieved evidence set.
        Higher entropy indicates higher uncertainty.
        """
        if len(evidence_embeddings) == 0:
            return 1.0 # Max uncertainty if no evidence
            
        # Ensure 2D arrays
        if claim_embedding.ndim == 1:
            claim_embedding = claim_embedding.reshape(1, -1)
            
        # Compute cosine similarities
        claim_norm = claim_embedding / np.linalg.norm(claim_embedding, axis=1, keepdims=True)
        ev_norm = evidence_embeddings / np.linalg.norm(evidence_embeddings, axis=1, keepdims=True)
        
        similarities = np.dot(claim_norm, ev_norm.T).flatten()
        
        # InfoNCE style softmax distribution over the evidence set
        scaled_sims = similarities / self.temperature
        exp_sims = np.exp(scaled_sims - np.max(scaled_sims)) # for numerical stability
        probs = exp_sims / np.sum(exp_sims)
        
        # Calculate entropy of the distribution
        entropy = -np.sum(probs * np.log(probs + 1e-9))
        
        # Normalize entropy by max possible entropy (log(N)) to get a 0-1 score
        max_entropy = np.log(len(evidence_embeddings)) if len(evidence_embeddings) > 1 else 1.0
        normalized_uncertainty = entropy / max_entropy if max_entropy > 0 else 0.0
        
        return float(normalized_uncertainty)
