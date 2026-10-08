import pytest
import numpy as np
from app.services.algo.density import DensityEstimator

def test_density_no_leakage_on_init():
    estimator = DensityEstimator(n_neighbors=2)
    assert not estimator.fitted
    assert estimator.reference_embeddings is None

def test_density_fitting_isolation():
    estimator = DensityEstimator(n_neighbors=2)
    train_data = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    test_data = np.array([[0.5, 0.5]])
    
    estimator.fit(train_data)
    assert estimator.fitted
    
    initial_reference_shape = estimator.reference_embeddings.shape
    scores = estimator.compute_density_signal(test_data)
    
    assert len(scores) == 1
    assert estimator.reference_embeddings.shape == initial_reference_shape
    np.testing.assert_array_almost_equal(estimator.cov_estimator.location_, np.mean(train_data, axis=0))
