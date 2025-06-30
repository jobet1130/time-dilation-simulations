import numpy as np
from .relativity_utils import G, c

def schwarzschild_radius(M: float) -> float:
    """
    Compute the Schwarzschild radius Rs = 2GM / c^2
    """
    return 2 * G * M / c**2

def gravitational_time_dilation(Rs: float, r_actual: np.ndarray) -> np.ndarray:
    """
    Compute gravitational time dilation factor:
    
    Time runs slower in gravitational fields.
    For an observer at infinity, time measured at radius r appears to run by factor:
    sqrt(1 - Rs/r)
    
    To get the dilated time (what distant observer sees):
    t_dilated = t_proper / sqrt(1 - Rs/r)

    Parameters:
    - Rs: Schwarzschild radius (meters)
    - r_actual: actual distances from the mass center (in meters)

    Returns:
    - dilation factor (1/sqrt(1 - Rs/r))
    """
    r_actual = np.asarray(r_actual)
    
    if np.any(r_actual <= Rs):
        raise ValueError("All r values must be greater than Rs to avoid singularity.")
    
    return 1.0 / np.sqrt(1 - Rs / r_actual)

def compute_gravitational_dilation(r_multiples: np.ndarray, M: float, t_proper: float = 1.0) -> np.ndarray:
    """
    Computes dilated time as observed from infinity for given radius multiples of Rs.
    
    In gravitational fields, time runs slower. A distant observer sees local clocks
    running slow by a factor of sqrt(1 - Rs/r).

    Parameters:
    - r_multiples: array of radii as multiples of Schwarzschild radius (e.g., 1.1, 2.0, etc.)
    - M: mass (kg)
    - t_proper: proper time measured locally (in seconds)

    Returns:
    - array of dilated times as seen by distant observer (in seconds)
    """
    Rs = schwarzschild_radius(M)
    r_actual = r_multiples * Rs
    dilation_factors = gravitational_time_dilation(Rs, r_actual)
    return dilation_factors * t_proper
