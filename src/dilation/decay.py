import numpy as np
from .relativity_utils import c, μ_proper_lifetime, lorentz_gamma

def compute_decay_distances(velocity_fractions: np.ndarray) -> np.ndarray:
    """
    Simulates muon decay distances at relativistic speeds.

    Parameters:
    - velocity_fractions: array of velocities as fractions of c

    Returns:
    - array of decay distances in meters
    """
    velocities = velocity_fractions * c
    gamma_values = np.array([lorentz_gamma(v) for v in velocities])
    dilated_lifetimes = gamma_values * μ_proper_lifetime
    return velocities * dilated_lifetimes
