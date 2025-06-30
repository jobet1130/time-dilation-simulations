# tests/test_lorentz.py

import numpy as np
import pytest

from src.dilation.relativity_utils import lorentz_gamma, c

# -----------------------------
# 📌 Test Lorentz Factor Calculations
# -----------------------------

def test_lorentz_gamma_basic():
    """Test basic Lorentz factor calculations."""
    # Test known values
    v_test = 0.5 * c  # Half speed of light
    gamma = lorentz_gamma(v_test)
    expected = 1.0 / np.sqrt(1 - 0.5**2)  # 1/sqrt(0.75) ≈ 1.155
    
    assert np.isclose(gamma, expected, rtol=1e-10)
    assert gamma > 1.0, "Lorentz factor should be > 1 for v > 0"

def test_lorentz_gamma_array():
    """Test Lorentz factor with array inputs."""
    velocities = np.array([0.1, 0.5, 0.9, 0.99]) * c
    gammas = lorentz_gamma(velocities)
    
    # Should return same shape
    assert gammas.shape == velocities.shape
    
    # All should be > 1
    assert np.all(gammas > 1.0)
    
    # Should increase with velocity
    assert np.all(np.diff(gammas) > 0), "Gamma should increase with velocity"

def test_lorentz_gamma_extreme_velocities():
    """Test Lorentz factor at extreme velocities."""
    # Very low velocity (should approach 1)
    v_low = 0.001 * c
    gamma_low = lorentz_gamma(v_low)
    assert np.isclose(gamma_low, 1.0, rtol=1e-6)
    
    # High velocity (should be large)
    v_high = 0.999 * c
    gamma_high = lorentz_gamma(v_high)
    assert gamma_high > 20.0, f"Expected γ > 20, got {gamma_high:.2f}"
    
    # Very high velocity
    v_very_high = 0.9999 * c
    gamma_very_high = lorentz_gamma(v_very_high)
    assert gamma_very_high > gamma_high, "Higher velocity should give higher γ"

def test_lorentz_gamma_invalid_inputs():
    """Test error handling for invalid velocities."""
    # Velocity at speed of light should fail
    with pytest.raises(ValueError, match="less than the speed of light"):
        lorentz_gamma(c)
    
    # Velocity faster than light should fail
    with pytest.raises(ValueError, match="less than the speed of light"):
        lorentz_gamma(1.1 * c)
    
    # Negative velocity should fail
    with pytest.raises(ValueError, match="non-negative"):
        lorentz_gamma(-0.5 * c)
    
    # Array with invalid values should fail
    with pytest.raises(ValueError):
        lorentz_gamma(np.array([0.5 * c, 1.1 * c]))

def test_lorentz_gamma_zero_velocity():
    """Test Lorentz factor at zero velocity."""
    gamma = lorentz_gamma(0.0)
    assert gamma == 1.0, "Lorentz factor should be exactly 1 at v=0"

def test_lorentz_gamma_physics_consistency():
    """Test that Lorentz factor matches known physics formulas."""
    # Test specific known values
    test_cases = [
        (0.6 * c, 1.25),    # γ = 1/sqrt(1-0.36) = 1/0.8 = 1.25
        (0.8 * c, 5/3),     # γ = 1/sqrt(1-0.64) = 1/0.6 = 5/3
        (0.866 * c, 2.0),   # γ = 1/sqrt(1-0.75) = 1/0.5 = 2
    ]
    
    for velocity, expected_gamma in test_cases:
        computed_gamma = lorentz_gamma(velocity)
        assert np.isclose(computed_gamma, expected_gamma, rtol=1e-3), \
            f"Expected γ={expected_gamma:.3f}, got {computed_gamma:.3f} for v={velocity/c:.3f}c"

def test_lorentz_gamma_numerical_stability():
    """Test numerical stability near edge cases."""
    # Test very close to speed of light
    v_close = 0.999999 * c
    gamma_close = lorentz_gamma(v_close)
    
    # Should be finite (not infinite or NaN)
    assert np.isfinite(gamma_close), "Gamma should be finite"
    assert gamma_close > 0, "Gamma should be positive"
    
    # Test array of values near edge
    velocities = np.linspace(0.99 * c, 0.9999 * c, 10)
    gammas = lorentz_gamma(velocities)
    
    # All should be finite and increasing
    assert np.all(np.isfinite(gammas)), "All gammas should be finite"
    assert np.all(np.diff(gammas) > 0), "Gammas should increase monotonically"
