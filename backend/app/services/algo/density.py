import numpy as np
from sklearn.covariance import LedoitWolf
from sklearn.neighbors import NearestNeighbors

class DensityEstimator:
    def __init__(self, n_neighbors: int = 5):
        self.n_neighbors = n_neighbors
        self.knn = NearestNeighbors(n_neighbors=self.n_neighbors, metric='cosine')
        # Ledoit-Wolf implements shrinkage for the covariance matrix, robust when n_samples < n_features
        self.cov_estimator = LedoitWolf()
        self.fitted = False
        self.reference_embeddings = None
        
    def fit(self, reference_embeddings: np.ndarray):
        """
        Fits the density estimator on a reference corpus of valid evidence.
        """
        if len(reference_embeddings) < 2:
            return
            
        self.reference_embeddings = reference_embeddings
        self.knn.fit(reference_embeddings)
        self.cov_estimator.fit(reference_embeddings)
        self.fitted = True
        
    def compute_density_signal(self, query_embeddings: np.ndarray) -> np.ndarray:
        """
        Computes the density/neighborhood signal for query embeddings.
        Returns an array of density scores (lower = denser/better support in the reference manifold).
        """
        if not self.fitted or len(query_embeddings) == 0:
            return np.zeros(len(query_embeddings))
            
        # 1. kNN Distance (cosine based)
        distances, _ = self.knn.kneighbors(query_embeddings)
        mean_knn_dist = distances.mean(axis=1)
        
        # 2. Mahalanobis Distance (using Ledoit-Wolf shrinkage covariance)
        precision_matrix = self.cov_estimator.precision_
        mean_vector = self.cov_estimator.location_
        
        diff = query_embeddings - mean_vector
        mahalanobis_sq = np.sum(np.dot(diff, precision_matrix) * diff, axis=1)
        mahalanobis_dist = np.sqrt(np.maximum(mahalanobis_sq, 0))
        
        # Raw uncalibrated signal combination. 
        # In a full pipeline, these might be passed as separate features to the calibration layer.
        density_score = (mean_knn_dist + (mahalanobis_dist / np.max(mahalanobis_dist + 1e-9))) / 2.0 
        
        return density_score
