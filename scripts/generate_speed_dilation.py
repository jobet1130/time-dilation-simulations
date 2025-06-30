
"""
Simulates time dilation due to relativistic speeds using Special Relativity.

Outputs:
- time_dilation_high_speed_particles.csv (in ../data/raw/)
"""

import numpy as np 
import pandas as pd 
from pathlib import Path 

# -----------------------------
# 🔧 Constants
# -----------------------------
c = 299_792_458         # Speed of light (m/s)
t_proper = 1.0          # Proper time (s) experienced by the moving particle

# -----------------------------
# 📊 Generate velocities (10% to 99% of c)
# -----------------------------
velocity_fractions = np.linspace(0.1, 0.99, 50)     # 50 steps from 0.1c to 0.99c
velocities = velocity_fractions * c                 # Convert to m/s

# -----------------------------
# 🧠 Compute Lorentz Factor and Dilated Time
# -----------------------------
gamma = 1 / np.sqrt(1 - (velocities / c) ** 2)      # Lorentz factor
t_dilated = gamma * t_proper                        # Time experienced by stationary observer
delta_t = t_dilated - t_proper                      # Δ Time gained due to time dilation

# -----------------------------
# 📁 Create DataFrame
# -----------------------------
df = pd.DataFrame({
    'Velocity Fraction of c': velocity_fractions,
    'Velocity (m/s)': velocities,
    'Lorentz Factor (γ)': gamma,
    'Proper Time (s)': t_proper,
    'Dilated Time (s)': t_dilated,
    'Δ Time (s)': delta_t
})

# -----------------------------
# 💾 Save to CSV
# -----------------------------
output_path = Path(__file__).resolve().parents[1] / "data" / "raw"
output_path.mkdir(parents=True, exist_ok=True)

csv_file = output_path / "time_dilation_high_speed_particles.csv"
df.to_csv(csv_file, index=False)

print(f"✅ Dataset saved to {csv_file}")