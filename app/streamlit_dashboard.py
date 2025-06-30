import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))  # Ensure `src` is discoverable

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from reportlab.pdfgen import canvas
import io

from src.dilation.lorentz import compute_lorentz_dilation
from src.dilation.gravity import gravitational_time_dilation, schwarzschild_radius
from src.dilation.decay import compute_decay_distances
from src.dilation.relativity_utils import c, G, M_sun, \
    μ_proper_lifetime, lorentz_gamma

st.set_page_config(page_title="⏳ Time Dilation Simulator", layout="wide",
                   menu_items={"About": "Toggle theme using top-right settings."})
st.title("⏳ Time Dilation Simulator — Velocity, Gravity, and Decay")

# ---------------------------------------
# 🔽 Select Model
# ---------------------------------------
model = st.sidebar.selectbox("Select Time Dilation Model", [
    "Special Relativity (Velocity)",
    "General Relativity (Gravity)",
    "Relativistic Particle Decay"
])

t_proper = 1.0  # Default Proper Time in seconds

# ---------------------------------------
# 🖐️ Editable Real-Time Equation Preview
# ---------------------------------------
v, r, Rs, c_sym = sp.symbols("v r R_s c")
st.sidebar.markdown("### ✏️ Custom Equation Input")
custom_input = st.sidebar.text_input("Enter expression (use 'v', 'r', etc.):", "sqrt(1 - 1/r)")

try:
    parsed_expr = parse_expr(custom_input, evaluate=False)
    st.sidebar.latex("f(v, r) = " + sp.latex(parsed_expr))

    # Preview value
    test_val = parsed_expr.evalf(subs={v: 0.9, r: 2.0, c_sym: c})
    st.sidebar.write("Test Evaluation:", test_val)
except Exception as e:
    st.sidebar.error(f"Error parsing equation: {e}")

# ---------------------------------------
# 📄 Equation Reference
# ---------------------------------------
st.sidebar.markdown("### 📝 Equation Preview")
if model == "Special Relativity (Velocity)":
    gamma_eq = sp.Eq(sp.Symbol("\u03b3"), 1 / sp.sqrt(1 - (v / c_sym) ** 2))
    st.sidebar.latex(r"t = \gamma \cdot t_0")
    st.sidebar.latex(sp.latex(gamma_eq))

elif model == "General Relativity (Gravity)":
    dilation_eq = sp.sqrt(1 - Rs / r)
    st.sidebar.latex(r"t = t_0 \cdot \sqrt{1 - \frac{R_s}{r}}")
    st.sidebar.latex(sp.latex(sp.Eq(sp.Symbol("Dilation Factor"), dilation_eq)))

elif model == "Relativistic Particle Decay":
    st.sidebar.latex(r"t = \gamma \cdot \tau_\mu")
    st.sidebar.latex(r"d = v \cdot t")

# ---------------------------------------
# 📅 Upload Section
# ---------------------------------------
st.sidebar.markdown("### 📄 Upload Parameters (CSV)")
uploaded_file = st.sidebar.file_uploader("Upload a CSV with `velocity_fraction` or `radius_rs`", type=["csv"])

# 📥 Download templates
st.sidebar.download_button("📄 Velocity Template", "velocity_fraction\n0.1\n0.5\n0.9", "velocity_template.csv")
st.sidebar.download_button("📄 Radius Template", "radius_rs\n1.1\n3.0\n5.0", "radius_template.csv")

# ---------------------------------------
# 📊 Main Simulation
# ---------------------------------------
st.markdown(f"## 📊 Simulation: {model}")

if uploaded_file:
    user_df = pd.read_csv(uploaded_file)

    if "velocity_fraction" in user_df.columns:
        st.subheader("🔁 Time Dilation from Velocity (Special Relativity)")
        vf = user_df["velocity_fraction"].values
        velocities = vf * c
        gamma = lorentz_gamma(velocities)
        dilated_time = gamma * t_proper

        result_df = pd.DataFrame({
            "Velocity Fraction of c": vf,
            "Velocity (m/s)": velocities,
            "Lorentz Factor (γ)": gamma,
            "Proper Time (s)": t_proper,
            "Dilated Time (s)": dilated_time,
            "Δ Time (s)": dilated_time - t_proper
        })
        st.dataframe(result_df.round(6))

        fig, ax = plt.subplots()
        sc = ax.scatter(result_df["Velocity Fraction of c"], result_df["Δ Time (s)"],
                        c=result_df["Δ Time (s)"], cmap="viridis", s=80, edgecolor="k")
        plt.colorbar(sc, label="Δ Time (s)")
        ax.set_xlabel("Velocity Fraction of c")
        ax.set_ylabel("Δ Time (s)")
        ax.set_title("Velocity Dilation")
        st.pyplot(fig)

    elif "radius_rs" in user_df.columns:
        st.subheader("🌀 Time Dilation from Gravity (General Relativity)")
        r = user_df["radius_rs"].values
        Rs_val = schwarzschild_radius(M_sun)
        dilation = gravitational_time_dilation(Rs_val, r * Rs_val)
        dilated_time = dilation * t_proper

        result_df = pd.DataFrame({
            "Distance from BH (Rₕ)": r,
            "Proper Time (s)": t_proper,
            "Dilation Factor": dilation,
            "Dilated Time (s)": dilated_time,
            "Δ Time (s)": dilated_time - t_proper
        })
        st.dataframe(result_df.round(6))

        fig, ax = plt.subplots()
        sc = ax.scatter(result_df["Distance from BH (Rₕ)"], result_df["Δ Time (s)"],
                        c=result_df["Δ Time (s)"], cmap="plasma", s=80, edgecolor="k")
        plt.colorbar(sc, label="Δ Time (s)")
        ax.set_xlabel("Distance from BH (Rₕ)")
        ax.set_ylabel("Δ Time (s)")
        ax.set_title("Gravitational Dilation")
        st.pyplot(fig)
    else:
        st.error("⚠️ Uploaded CSV must contain `velocity_fraction` or `radius_rs` column.")

else:
    if model == "Special Relativity (Velocity)":
        v_frac = st.slider("Velocity Fraction of c", 0.1, 0.99, 0.5, 0.01)
        gamma = lorentz_gamma(v_frac * c)
        dilated_time = gamma * t_proper
        st.write(f"**Lorentz Factor (γ):** `{gamma:.4f}`")
        st.write(f"**Dilated Time:** `{dilated_time:.6f} s`")

    elif model == "General Relativity (Gravity)":
        r = st.slider("Distance from Black Hole (in Rₕ)", 1.1, 10.0, 2.0, 0.1)
        Rs_val = schwarzschild_radius(M_sun)
        dilation = gravitational_time_dilation(Rs_val, r * Rs_val)
        dilated_time = dilation * t_proper
        st.write(f"**Dilation Factor:** `{dilation:.4f}`")
        st.write(f"**Dilated Time:** `{dilated_time:.6f} s`")

    elif model == "Relativistic Particle Decay":
        v = st.slider("Muon Speed (fraction of c)", 0.5, 0.999, 0.98, 0.001)
        distance_m = compute_decay_distances(np.array([v]))[0]
        gamma = lorentz_gamma(v * c)
        dilated_lifetime = gamma * μ_proper_lifetime

        st.write(f"**Lorentz Factor (γ):** `{gamma:.4f}`")
        st.write(f"**Dilated Lifetime:** `{dilated_lifetime:.6e} s`")
        st.write(f"**Decay Distance:** `{distance_m / 1000:.2f} km`")

# ---------------------------------------
# 📄 PDF Export
# ---------------------------------------
st.markdown("### 📄 Export Summary as PDF")
if st.button("🖋️ Generate PDF Summary"):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 800, "Time Dilation Summary")
    pdf.drawString(100, 780, f"Model: {model}")
    pdf.drawString(100, 760, f"Dilated Time: {dilated_time:.6f} s")
    pdf.save()
    buffer.seek(0)
    st.download_button("📅 Download PDF", data=buffer, file_name="time_dilation_summary.pdf")
