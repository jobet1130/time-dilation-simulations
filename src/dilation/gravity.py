import numpy as np
from .relativity_utils import G, c

def schwarzschild_radius(M: float) -> float:
    """
    Compute Schwarzschild radius for mass M.
    """
    return 2 * G * M / c**2

def gravitational_time_dilation(Rs: float, r: np.ndarray) -> np.ndarray:
    """
    Compute gravitational time dilation factor: sqrt(1 - Rs / r)

    Parameters:
    - Rs: Schwarzschild radius
    - r: array of radial distances (m)

    Returns:
    - array of dilation factors
    """
    if np.any(r <= Rs):
        raise ValueError("Radius must be greater than Schwarzschild radius.")

    return np.sqrt(1 - Rs / r)

def compute_gravitational_dilation(r: np.ndarray, Rs: float, t_proper: float = 1.0) -> np.ndarray:
    """
    Compute dilated time from gravitational time dilation.

    Parameters:
    - r: radial distances (np.ndarray)
    - Rs: Schwarzschild radius
    - t_proper: proper time (float)

    Returns:
    - dilated times (np.ndarray)
    """
    dilation_factor = gravitational_time_dilation(Rs, r)
    return t_proper / dilation_factor
