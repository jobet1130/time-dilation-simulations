import numpy as np
from .relativity_utils import lorentz_gamma

def compute_lorentz_dilation(velocities: np.ndarray, t_proper: float = 1.0) -> np.ndarray:
    """
    Compute time dilation for each velocity using special relativity.

    Parameters:
    - velocities: np.ndarray of speeds (m/s)
    - t_proper: proper time in seconds

    Returns:
    - np.ndarray of dilated times
    """
    gamma_values = np.array([lorentz_gamma(v) for v in velocities])
    return gamma_values * t_proper
