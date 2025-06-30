import numpy as np
from relativity_utils import G, c

def schwarzschild_radius(M: float) -> float:
    """
    Compute Schwarzschild radius for mass M.
    """
    return 2 * G * M / c**2

def gravitational_time_dilation(Rs: float, r: np.ndarray) -> np.ndarray:
    """
    Compute gravitational time dilation factors.

    Parameters:
    - Rs: Schwarzschild radius
    - r: array of radial distances

    Returns:
    - array of dilation factors
    """
    with np.errstate(invalid='ignore'):
        dilation = np.sqrt(1 - Rs / r)
    dilation[np.isnan(dilation)] = 0
    return dilation