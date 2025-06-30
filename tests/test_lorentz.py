# tests/test_gravity.py

import numpy as np
import pytest

from src.dilation.gravity import compute_gravitational_dilation
from src.dilation.relativity_utils import G, c, M_sun

# -----------------------------
# 📌 Fixtures for test values
# -----------------------------
@pytest.fixture
def schwarzschild_radius():
    return 2 * G * M_sun / c**2  # Schwarzschild radius of the Sun

@pytest.fixture
def radii(schwarzschild_radius):
    return np.array([
        1.1 * schwarzschild_radius,
        2 * schwarzschild_radius,
        5 * schwarzschild_radius
    ])

# -----------------------------
# ✅ Unit Tests
# -----------------------------
def test_gravitational_dilation_valid(radii, schwarzschild_radius):
    proper_time = 1.0  # seconds
    dilated_times = compute_gravitational_dilation(radii, schwarzschild_radius, proper_time)

    assert len(dilated_times) == len(radii)
    assert np.all(dilated_times > 0)
    assert np.all(dilated_times > proper_time)  # Should be dilated

def test_gravitational_dilation_near_event_horizon(schwarzschild_radius):
    # r just slightly above Rs
    r = np.array([1.000001 * schwarzschild_radius])
    t_dilated = compute_gravitational_dilation(r, schwarzschild_radius, 1.0)
    assert t_dilated[0] > 10.0  # Extreme dilation

def test_gravitational_dilation_invalid_radius(schwarzschild_radius):
    # r ≤ Rs should raise error
    r = np.array([schwarzschild_radius])
    with pytest.raises(ValueError):
        compute_gravitational_dilation(r, schwarzschild_radius, 1.0)
