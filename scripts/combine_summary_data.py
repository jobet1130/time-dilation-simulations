"""
Combines all time dilation datasets into a single summary CSV for analysis and visual comparison.

Inputs (from ../data/raw/):
- time_dilation_high_speed_particles.csv
- gravitational_time_dilation.csv
- particle_decay_time_dilation.csv

Output:
- combined_time_dilation_summary.csv (in ../data/processed/)
"""

import pandas as pd
from pathlib import Path

# -----------------------------
# 📁 Define paths
# -----------------------------
base_path = Path(__file__).resolve().parents[1]
raw_path = base_path / "data" / "raw"
processed_path = base_path / "data" / "processed"
processed_path.mkdir(parents=True, exist_ok=True)

# -----------------------------
# 📥 Load datasets
# -----------------------------
df_speed = pd.read_csv(raw_path / "time_dilation_high_speed_particles.csv")
df_gravity = pd.read_csv(raw_path / "gravitational_time_dilation.csv")
df_decay = pd.read_csv(raw_path / "particle_decay_time_dilation.csv")

# -----------------------------
# ✨ Standardize Length for Merging
# -----------------------------
min_len = min(len(df_speed), len(df_decay), len(df_gravity))

# Trim or resample each to match minimum length
df_speed = df_speed.iloc[:min_len].reset_index(drop=True)
df_decay = df_decay.iloc[:min_len].reset_index(drop=True)

# Gravity dataset is interpolated to match size
df_gravity_interp = df_gravity[['Distance in Rs', 'Δ Time (s)']].copy()
df_gravity_interp.columns = ['Distance from BH (Rₛ)', 'Gravity Δ Time (s)']
df_gravity_interp = df_gravity_interp.interpolate(method='linear')
df_gravity_interp = df_gravity_interp.iloc[::int(len(df_gravity_interp)/min_len)].reset_index(drop=True)

# -----------------------------
# 📊 Combine Summary Table
# -----------------------------
summary_df = pd.DataFrame({
    'Velocity Fraction of c': df_speed['Velocity Fraction of c'],
    'Lorentz Factor (γ)': df_speed['Lorentz Factor (γ)'],
    'Speed Δ Time (s)': df_speed['Δ Time (s)'],
    'Decay Distance (km)': df_decay['Distance Traveled (km)'],
    'Distance from BH (Rₛ)': df_gravity_interp['Distance from BH (Rₛ)'],
    'Gravity Δ Time (s)': df_gravity_interp['Gravity Δ Time (s)']
})

# -----------------------------
# 💾 Save to CSV
# -----------------------------
output_file = processed_path / "combined_time_dilation_summary.csv"
summary_df.to_csv(output_file, index=False)

print(f"✅ Combined summary saved to: {output_file}")
