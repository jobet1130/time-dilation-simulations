# tests/test_decay.py

import numpy as np
import pytest
from src.dilation.decay import compute_decay_distances
from src.dilation.relativity_utils import c, μ_proper_lifetime

def test_output_shape():
    velocity_fractions = np.linspace(0.1, 0.99, 10)
    distances = compute_decay_distances(velocity_fractions)
    assert distances.shape == velocity_fractions.shape

def test_physical_increase_with_speed():
    # Higher speed should lead to longer decay distance due to time dilation
    low_v = np.array([0.1])
    high_v = np.array([0.99])

    dist_low = compute_decay_distances(low_v)[0]
    dist_high = compute_decay_distances(high_v)[0]

    assert dist_high > dist_low

def test_known_gamma_muon():
    # Known γ at 0.998c ≈ 15.82
    v_fraction = 0.998
    v = v_fraction * c
    expected_gamma = 1 / np.sqrt(1 - v_fraction**2)

    expected_lifetime = expected_gamma * μ_proper_lifetime
    expected_distance = expected_lifetime * v

    # Use our function
    computed_distance = compute_decay_distances(np.array([v_fraction]))[0]

    assert np.isclose(computed_distance, expected_distance, rtol=1e-3)

def test_zero_and_invalid_inputs():
    # Test if velocity = 0 gives minimal distance
    distances = compute_decay_distances(np.array([1e-9]))
    assert distances[0] < 1e-3  # Very small distance in meters

    # Test invalid input (>1)
    with pytest.raises(ValueError):
        compute_decay_distances(np.array([1.1]))
