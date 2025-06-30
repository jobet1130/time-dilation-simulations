"""
Simulates gravitational time dilation near a black hole using General Relativity.

Outputs:
- gravitational_time_dilation.csv (in ../data/raw/)
"""

import numpy as np
import pandas as pd
from pathlib import Path

# -----------------------------
# 🔧 Physical Constants
# -----------------------------
G = 6.67430e-11               # Gravitational constant (m^3 kg^-1 s^-2)
c = 299_792_458               # Speed of light (m/s)
M_sun = 1.9885e30             # Mass of the Sun (kg)

# -----------------------------
# 🌀 Black Hole Properties
# -----------------------------
M = M_sun                     # Assume 1 solar mass black hole
Rs = 2 * G * M / c**2         # Schwarzschild radius (m)

# -----------------------------
# 🧪 Simulation Parameters
# -----------------------------
t_proper = 1.0                # Proper time in seconds (local clock)
radii = np.linspace(1.01 * Rs, 10 * Rs, 50000)   # Distances from BH center (avoid r = Rs)
r_over_Rs = radii / Rs        # Distance in multiples of Rs

# -----------------------------
# 🧠 Gravitational Time Dilation Formula:
#     t_dilated = t_proper / sqrt(1 - Rs/r)
# -----------------------------
dilation_factor = 1 / np.sqrt(1 - (Rs / radii))
t_dilated = t_proper * dilation_factor
delta_t = t_dilated - t_proper

# -----------------------------
# 📁 Create DataFrame
# -----------------------------
df = pd.DataFrame({
    'Radius from Center (m)': radii,
    'Distance in Rs': r_over_Rs,
    'Proper Time (s)': t_proper,
    'Dilated Time (s)': t_dilated,
    'Δ Time (s)': delta_t
})

# -----------------------------
# 💾 Save to CSV
# -----------------------------
output_path = Path(__file__).resolve().parents[1] / "data" / "raw"
output_path.mkdir(parents=True, exist_ok=True)

csv_file = output_path / "gravitational_time_dilation.csv"
df.to_csv(csv_file, index=False)

print(f"✅ Dataset saved to {csv_file}")
