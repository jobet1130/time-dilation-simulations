# tests/test_decay.py

import numpy as np
import pytest
from src.dilation.decay import compute_decay_distances
from src.dilation.relativity_utils import c, μ_proper_lifetime

def test_output_shape():
    """Test that output array has the same shape as input array."""
    velocity_fractions = np.linspace(0.1, 0.99, 10)
    distances = compute_decay_distances(velocity_fractions)
    assert distances.shape == velocity_fractions.shape
    assert len(distances) == 10

def test_single_value_input():
    """Test computation with single velocity value."""
    single_v = np.array([0.5])
    distances = compute_decay_distances(single_v)
    assert distances.shape == (1,)
    assert distances[0] > 0

def test_physical_increase_with_speed():
    """Higher speed should lead to longer decay distance due to time dilation."""
    velocities = np.array([0.1, 0.5, 0.9, 0.99])
    distances = compute_decay_distances(velocities)
    
    # Check that distances increase monotonically with velocity
    for i in range(1, len(distances)):
        assert distances[i] > distances[i-1], f"Distance should increase: {distances[i-1]:.3f} vs {distances[i]:.3f}"

def test_known_gamma_muon():
    """Test against known physics calculation for muon at 0.998c."""
    v_fraction = 0.998
    v = v_fraction * c
    expected_gamma = 1 / np.sqrt(1 - v_fraction**2)

    expected_lifetime = expected_gamma * μ_proper_lifetime
    expected_distance = expected_lifetime * v

    # Use our function
    computed_distance = compute_decay_distances(np.array([v_fraction]))[0]

    assert np.isclose(computed_distance, expected_distance, rtol=1e-6)
    
    # Additional check: distance should be around 10 km for atmospheric muons
    distance_km = computed_distance / 1000
    assert 10 <= distance_km <= 15, f"Expected 10-15 km, got {distance_km:.2f} km"

def test_atmospheric_muon_physics():
    """Test realistic atmospheric muon scenario."""
    # Typical cosmic ray muon velocity
    muon_v = 0.998
    distance = compute_decay_distances(np.array([muon_v]))[0]
    
    # Should be able to travel about 10-12 km (realistic for atmospheric muons)
    # This allows muons from upper atmosphere (~15 km) to reach surface
    distance_km = distance / 1000
    assert 8 <= distance_km <= 15, f"Expected 8-15 km, got {distance_km:.2f}km"
    
    # This distance should be sufficient to reach Earth's surface from upper atmosphere
    assert distance > 8000, f"Distance should be >8km for atmospheric detection"
    
    # But shouldn't be unrealistically large
    assert distance < 50000, f"Distance seems too large: {distance/1000:.2f}km"

def test_low_velocity_newtonian_limit():
    """At very low velocities, should approximate Newtonian physics."""
    v_low = 0.01  # 1% speed of light
    distance = compute_decay_distances(np.array([v_low]))[0]
    
    # At low velocities, γ ≈ 1, so distance ≈ v * t_proper
    newtonian_distance = v_low * c * μ_proper_lifetime
    
    # Should be very close to Newtonian result
    assert np.isclose(distance, newtonian_distance, rtol=1e-4)

def test_very_high_velocity():
    """Test behavior at very high velocities (but still < c)."""
    v_high = 0.9999
    distance = compute_decay_distances(np.array([v_high]))[0]
    
    # Should be much larger than low velocity case
    v_low = 0.1
    distance_low = compute_decay_distances(np.array([v_low]))[0]
    
    assert distance > 100 * distance_low, "High velocity should give much larger distance"

def test_zero_and_invalid_inputs():
    """Test edge cases and invalid inputs."""
    # Test very small velocity
    distances = compute_decay_distances(np.array([1e-9]))
    assert distances[0] < 1e-3  # Very small distance in meters
    assert distances[0] > 0     # But still positive

    # Test invalid input (>1, which means > speed of light)
    with pytest.raises(ValueError):
        compute_decay_distances(np.array([1.1]))
    
    # Test exactly at speed of light (should fail)
    with pytest.raises(ValueError):
        compute_decay_distances(np.array([1.0]))
    
    # Test negative velocity (should fail)
    with pytest.raises(ValueError):
        compute_decay_distances(np.array([-0.5]))

def test_array_consistency():
    """Test that array operations are consistent with individual calculations."""
    velocities = np.array([0.1, 0.5, 0.9])
    
    # Compute as array
    distances_array = compute_decay_distances(velocities)
    
    # Compute individually
    distances_individual = []
    for v in velocities:
        dist = compute_decay_distances(np.array([v]))[0]
        distances_individual.append(dist)
    
    # Should be identical
    np.testing.assert_allclose(distances_array, distances_individual, rtol=1e-10)

def test_units_and_magnitudes():
    """Test that results have reasonable units and magnitudes."""
    v_test = 0.8  # 80% speed of light
    distance = compute_decay_distances(np.array([v_test]))[0]
    
    # Distance should be in meters and reasonable magnitude
    assert distance > 100, "Distance should be at least 100m"
    assert distance < 1e6, "Distance shouldn't exceed 1000km for realistic scenarios"
    
    # Should be much larger than non-relativistic case
    non_rel_distance = v_test * c * μ_proper_lifetime
    assert distance > non_rel_distance, "Relativistic distance should be larger"

def test_precision_and_numerical_stability():
    """Test numerical precision and stability."""
    # Test very close to speed of light
    v_close = 0.999999
    distance = compute_decay_distances(np.array([v_close]))[0]
    
    # Should not be infinite or NaN
    assert np.isfinite(distance), "Distance should be finite"
    assert distance > 0, "Distance should be positive"
    
    # Test multiple precision points
    velocities = np.linspace(0.1, 0.999, 100)
    distances = compute_decay_distances(velocities)
    
    # All should be finite and positive
    assert np.all(np.isfinite(distances)), "All distances should be finite"
    assert np.all(distances > 0), "All distances should be positive"
