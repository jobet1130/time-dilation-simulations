"""
Simulates how time dilation affects the distance particles (e.g., muons) can travel
before decaying when moving at relativistic speeds.

Outputs:
- particle_decay_time_dilation.csv (in ../data/raw/)
"""

import numpy as np
import pandas as pd
from pathlib import Path

# -----------------------------
# 🔧 Physical Constants
# -----------------------------
c = 299_792_458               # Speed of light (m/s)
t_proper = 2.2e-6             # Proper lifetime of a muon (s) in its rest frame

# -----------------------------
# ⚙️ Simulation Range
# -----------------------------
velocity_fractions = np.linspace(0.1, 0.999, 50000)    # 0.1c to 0.999c (50,000 records)
velocities = velocity_fractions * c

# -----------------------------
# 🧠 Time Dilation (Lorentz factor)
# -----------------------------
gamma = 1 / np.sqrt(1 - (velocities / c) ** 2)
t_dilated = gamma * t_proper  # Lifetime in lab frame

# -----------------------------
# 🚀 Distance Traveled
# Distance = velocity * dilated time (from lab frame)
# -----------------------------
distances = velocities * t_dilated    # in meters

# -----------------------------
# 📁 Create DataFrame
# -----------------------------
df = pd.DataFrame({
    'Velocity Fraction of c': velocity_fractions,
    'Velocity (m/s)': velocities,
    'Lorentz Factor (γ)': gamma,
    'Proper Lifetime (s)': t_proper,
    'Dilated Lifetime (s)': t_dilated,
    'Distance Traveled (m)': distances,
    'Distance Traveled (km)': distances / 1000
})

# -----------------------------
# 💾 Save to CSV
# -----------------------------
output_path = Path(__file__).resolve().parents[1] / "data" / "raw"
output_path.mkdir(parents=True, exist_ok=True)

csv_file = output_path / "particle_decay_time_dilation.csv"
df.to_csv(csv_file, index=False)

print(f"✅ Dataset saved to {csv_file}")