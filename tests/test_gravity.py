# tests/test_gravity.py

import numpy as np
import pytest

from src.dilation.gravity import compute_gravitational_dilation, schwarzschild_radius
from src.dilation.relativity_utils import G, c, M_sun, M_earth

# -----------------------------
# 📌 Test gravitational time dilation
# -----------------------------

def test_gravitational_dilation_basic():
    """Test basic gravitational time dilation calculation."""
    # Test with multiples of Schwarzschild radius
    r_multiples = np.array([2.0, 5.0, 10.0])  # 2Rs, 5Rs, 10Rs
    proper_time = 1.0  # seconds
    
    dilated_times = compute_gravitational_dilation(r_multiples, M_sun, proper_time)
    
    # Basic checks
    assert len(dilated_times) == len(r_multiples)
    assert np.all(dilated_times > 0)
    assert np.all(dilated_times > proper_time)  # Time should be dilated (appears longer)
    
    # Check that dilation decreases with distance
    for i in range(1, len(dilated_times)):
        assert dilated_times[i] < dilated_times[i-1], "Dilation should decrease with distance"

def test_gravitational_dilation_near_event_horizon():
    """Test extreme dilation near the event horizon."""
    # r just slightly above Rs (1.01 * Rs)
    r_multiples = np.array([1.01])
    t_dilated = compute_gravitational_dilation(r_multiples, M_sun, 1.0)
    
    # Near event horizon, dilation should be extreme
    assert t_dilated[0] > 5.0, f"Expected >5s dilation, got {t_dilated[0]:.3f}s"
    
    # Test even closer
    r_very_close = np.array([1.001])
    t_very_dilated = compute_gravitational_dilation(r_very_close, M_sun, 1.0)
    assert t_very_dilated[0] > t_dilated[0], "Closer to horizon should give more dilation"

def test_gravitational_dilation_invalid_radius():
    """Test error handling for invalid radii."""
    # r ≤ Rs should raise error
    with pytest.raises(ValueError, match="greater than Rs"):
        compute_gravitational_dilation(np.array([1.0]), M_sun, 1.0)  # exactly at Rs
    
    with pytest.raises(ValueError, match="greater than Rs"):
        compute_gravitational_dilation(np.array([0.5]), M_sun, 1.0)  # below Rs
    
    # Negative radius should also fail
    with pytest.raises(ValueError):
        compute_gravitational_dilation(np.array([-1.0]), M_sun, 1.0)

def test_schwarzschild_radius_calculation():
    """Test Schwarzschild radius calculation."""
    Rs_sun = schwarzschild_radius(M_sun)
    Rs_earth = schwarzschild_radius(M_earth)
    
    # Sun's Schwarzschild radius should be about 3 km
    assert 2500 < Rs_sun < 3500, f"Sun Rs should be ~3km, got {Rs_sun/1000:.2f}km"
    
    # Earth's Schwarzschild radius should be about 9 mm
    assert 0.008 < Rs_earth < 0.010, f"Earth Rs should be ~9mm, got {Rs_earth*1000:.1f}mm"
    
    # Sun should have much larger Rs than Earth
    assert Rs_sun > Rs_earth * 100000

def test_earth_gravitational_effects():
    """Test realistic Earth gravitational time dilation."""
    # GPS satellites orbit at ~20,000 km
    earth_radius = 6.371e6  # meters
    gps_altitude = 20.2e6   # meters from Earth center
    
    Rs_earth = schwarzschild_radius(M_earth)
    r_multiple = gps_altitude / Rs_earth
    
    # Time dilation for 1 day
    one_day = 24 * 3600  # seconds
    dilated_time = compute_gravitational_dilation(np.array([r_multiple]), M_earth, one_day)[0]
    
    # GPS satellites experience very small time dilation
    time_diff = dilated_time - one_day  # should be microseconds
    assert 0 < time_diff < 0.1, f"GPS time dilation should be microseconds, got {time_diff:.6f}s"

def test_physics_consistency():
    """Test that physics formulas are consistent."""
    # Test known physics: at 2*Rs, dilation factor should be sqrt(2) ≈ 1.414
    r_multiples = np.array([2.0])
    dilated_time = compute_gravitational_dilation(r_multiples, M_sun, 1.0)[0]
    
    expected_factor = 1.0 / np.sqrt(1 - 1/2)  # 1/sqrt(1 - Rs/(2*Rs))
    expected_time = expected_factor * 1.0
    
    assert np.isclose(dilated_time, expected_time, rtol=1e-10), \
        f"Expected {expected_time:.6f}, got {dilated_time:.6f}"

def test_array_operations():
    """Test that array operations work correctly."""
    r_multiples = np.array([1.5, 2.0, 3.0, 5.0, 10.0])
    dilated_times = compute_gravitational_dilation(r_multiples, M_sun, 1.0)
    
    # Should return same shape
    assert dilated_times.shape == r_multiples.shape
    
    # All should be finite and positive
    assert np.all(np.isfinite(dilated_times))
    assert np.all(dilated_times > 0)
    
    # Should be monotonically decreasing (less dilation at larger distances)
    assert np.all(np.diff(dilated_times) < 0), "Dilation should decrease with distance"

def test_extreme_cases():
    """Test behavior at extreme distances."""
    # Very far from mass (should approach no dilation)
    r_far = np.array([1000.0])  # 1000 * Rs
    dilated_far = compute_gravitational_dilation(r_far, M_sun, 1.0)[0]
    
    # Should be very close to 1.0 (no dilation) - adjust tolerance for realistic physics
    assert np.isclose(dilated_far, 1.0, rtol=1e-3), \
        f"Far from mass should have minimal dilation, got {dilated_far:.10f}"
    
    # Should be only slightly greater than 1.0
    assert 1.0 < dilated_far < 1.01, "Far dilation should be minimal but still present"
    
    # Very close to event horizon
    r_close = np.array([1.0001])  # just above Rs
    dilated_close = compute_gravitational_dilation(r_close, M_sun, 1.0)[0]
    
    # Should be very large
    assert dilated_close > 50.0, f"Very close to horizon should give extreme dilation"

def test_different_masses():
    """Test with different stellar masses."""
    # Test with different mass objects
    masses = [M_earth, M_sun, 10 * M_sun]  # Earth, Sun, massive star
    r_multiple = 3.0  # 3 * Rs for each
    
    dilations = []
    for mass in masses:
        dilation = compute_gravitational_dilation(np.array([r_multiple]), mass, 1.0)[0]
        dilations.append(dilation)
    
    # All should give the same dilation at 3*Rs (independent of mass)
    expected_dilation = 1.0 / np.sqrt(1 - 1/3)  # 1/sqrt(2/3)
    
    for dilation in dilations:
        assert np.isclose(dilation, expected_dilation, rtol=1e-10), \
            f"Dilation at 3Rs should be same for all masses: {expected_dilation:.6f}"
