import numpy as np

# -----------------------------
# 🚀 Universal Scientific Constants
# -----------------------------
c = 299_792_458                # Speed of light (m/s)
G = 6.67430e-11                # Gravitational constant (m^3 kg^-1 s^-2)
M_earth = 5.972e24             # Mass of the Earth (kg)
M_sun = 1.989e30               # Mass of the Sun (kg)
μ_proper_lifetime = 2.2e-6     # Proper lifetime of muon (s)

# -----------------------------
# 📐 Lorentz Factor
# -----------------------------
def lorentz_gamma(v):
    """
    Compute Lorentz factor γ = 1 / sqrt(1 - (v/c)^2)
    Accepts scalar or np.ndarray.
    """
    v = np.asarray(v)

    # Validate input: velocities must be positive and less than c
    if np.any(v < 0):
        raise ValueError("All velocities must be non-negative.")
    
    if np.any(v >= c):
        raise ValueError("All velocities must be less than the speed of light.")

    with np.errstate(divide='ignore', invalid='ignore'):
        gamma = 1.0 / np.sqrt(1 - (v / c)**2)

    return gamma
