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
def lorentz_gamma(v: float) -> float:
    if v >= c:
        raise ValueError("Velocity must be less than the speed of light.")
    return 1.0 / np.sqrt(1 - (v / c)**2)
# relativity_utils.py

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
def lorentz_gamma(v: float) -> float:
    if v >= c:
        raise ValueError("Velocity must be less than the speed of light.")
    return 1.0 / np.sqrt(1 - (v / c)**2)
