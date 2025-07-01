import sys
from pathlib import Path

# Allow src module discovery
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
from reportlab.pdfgen import canvas as pdf_canvas  # renamed to avoid clashing with speed of light 'c'

# Local modules
from src.dilation.lorentz import compute_lorentz_dilation
from src.dilation.gravity import gravitational_time_dilation, schwarzschild_radius
from src.dilation.decay import compute_decay_distances
from src.dilation.relativity_utils import c, M_sun, μ_proper_lifetime, lorentz_gamma

# ------------------------
# Streamlit Setup
# ------------------------
st.set_page_config(page_title="⏳ Time Dilation Simulator", layout="wide")
st.title("⏳ Time Dilation Simulator — Velocity, Gravity, and Decay")

# ------------------------
# Session State
# ------------------------
if "last_model" not in st.session_state:
    st.session_state.last_model = None
if "dataframe_result" not in st.session_state:
    st.session_state.dataframe_result = None
if "chart_figure" not in st.session_state:
    st.session_state.chart_figure = None

# ------------------------
# Model Selection
# ------------------------
model = st.sidebar.selectbox("Select Time Dilation Model", [
    "Special Relativity (Velocity)",
    "General Relativity (Gravity)",
    "Relativistic Particle Decay"
])

# Reset session data if model changed
if model != st.session_state.last_model:
    st.session_state.dataframe_result = None
    st.session_state.chart_figure = None
    st.session_state.last_model = model

# ------------------------
# File Upload
# ------------------------
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
t_proper = 1.0

# ------------------------
# Export to PDF Helper
# ------------------------
def export_chart_to_pdf(title, df):
    buffer = BytesIO()
    c = pdf_canvas.Canvas(buffer)
    c.drawString(100, 800, title)
    text = c.beginText(50, 770)
    for line in df.to_string(index=False).split("\n"):
        text.textLine(line)
    c.drawText(text)
    c.save()
    buffer.seek(0)
    return buffer

# ------------------------
# Simulation Display
# ------------------------
st.subheader(f"📊 Simulation: {model}")

fig = None
df = None

# =======================
# ✅ CSV MODE
# =======================
if uploaded_file:
    user_df = pd.read_csv(uploaded_file)

    if model == "Special Relativity (Velocity)" and "velocity_fraction" in user_df.columns:
        vf = user_df["velocity_fraction"]
        velocity = vf * c
        dilated_time = compute_lorentz_dilation(np.array(velocity), t_proper)
        gamma = dilated_time / t_proper

        df = pd.DataFrame({
            "Velocity Fraction of c": vf,
            "Velocity (m/s)": velocity,
            "Lorentz Factor (γ)": gamma,
            "Proper Time (s)": t_proper,
            "Dilated Time (s)": dilated_time,
            "Δ Time (s)": dilated_time - t_proper
        })

        fig = px.scatter(df, x="Velocity Fraction of c", y="Δ Time (s)", color="Δ Time (s)",
                         title="Δ Time vs Velocity", color_continuous_scale="Viridis")

    elif model == "General Relativity (Gravity)" and "radius_rs" in user_df.columns:
        r = user_df["radius_rs"]
        Rs = schwarzschild_radius(M_sun)
        dilation = gravitational_time_dilation(Rs, r * Rs)
        dilated_time = dilation * t_proper

        df = pd.DataFrame({
            "Radius from Center (m)": r * Rs,
            "Distance in Rs": r,
            "Proper Time (s)": t_proper,
            "Dilated Time (s)": dilated_time,
            "Δ Time (s)": dilated_time - t_proper
        })

        fig = px.scatter(df, x="Distance in Rs", y="Δ Time (s)", color="Δ Time (s)",
                         title="Δ Time vs Distance", color_continuous_scale="Plasma")

    elif model == "Relativistic Particle Decay" and "velocity_fraction" in user_df.columns:
        vf = user_df["velocity_fraction"]
        velocity = vf * c
        gamma = lorentz_gamma(np.array(velocity))
        dilated_lifetime = gamma * μ_proper_lifetime
        distance = compute_decay_distances(vf)

        df = pd.DataFrame({
            "Velocity Fraction of c": vf,
            "Velocity (m/s)": velocity,
            "Lorentz Factor (γ)": gamma,
            "Proper Decay Time (s)": μ_proper_lifetime,
            "Dilated Decay Time (s)": dilated_lifetime,
            "Distance Traveled (m)": distance
        })

        fig = px.scatter(df, x="Velocity Fraction of c", y="Distance Traveled (m)", color="Dilated Decay Time (s)",
                         title="Decay Distance vs Velocity", color_continuous_scale="Cividis")

    else:
        st.error(f"⚠️ Uploaded CSV does not match the expected columns for **{model}**.")
        st.info(
            "**Expected Columns by Model:**\n\n"
            "- **Special Relativity (Velocity):** `velocity_fraction`\n"
            "- **General Relativity (Gravity):** `radius_rs`\n"
            "- **Relativistic Particle Decay:** `velocity_fraction`\n"
        )
        st.stop()

# =======================
# ✅ Slider Mode
# =======================
else:
    if model == "Special Relativity (Velocity)":
        v_frac = st.slider("Velocity Fraction of c", 0.1, 0.99, 0.5, 0.01)
        velocity = v_frac * c
        dilated_time = compute_lorentz_dilation(np.array([velocity]), t_proper)[0]
        gamma = dilated_time / t_proper

        df = pd.DataFrame({
            "Velocity Fraction of c": [v_frac],
            "Velocity (m/s)": [velocity],
            "Lorentz Factor (γ)": [gamma],
            "Proper Time (s)": [t_proper],
            "Dilated Time (s)": [dilated_time],
            "Δ Time (s)": [dilated_time - t_proper]
        })

        fig = px.bar(df, x="Velocity Fraction of c", y="Δ Time (s)",
                     color="Δ Time (s)", color_continuous_scale="Viridis")

    elif model == "General Relativity (Gravity)":
        r = st.slider("Distance from BH (in Rₛ)", 1.1, 10.0, 2.0, 0.1)
        Rs = schwarzschild_radius(M_sun)
        dilation = gravitational_time_dilation(Rs, r * Rs)
        dilated_time = dilation * t_proper

        df = pd.DataFrame({
            "Radius from Center (m)": [r * Rs],
            "Distance in Rs": [r],
            "Proper Time (s)": [t_proper],
            "Dilated Time (s)": [dilated_time],
            "Δ Time (s)": [dilated_time - t_proper]
        })

        fig = px.bar(df, x="Distance in Rs", y="Δ Time (s)",
                     color="Δ Time (s)", color_continuous_scale="Plasma")

    elif model == "Relativistic Particle Decay":
        v = st.slider("Muon Speed (fraction of c)", 0.5, 0.999, 0.98, 0.001)
        velocity = v * c
        gamma = lorentz_gamma(np.array([velocity]))
        dilated_lifetime = gamma * μ_proper_lifetime
        distance = compute_decay_distances(np.array([v]))[0]

        df = pd.DataFrame({
            "Velocity Fraction of c": [v],
            "Velocity (m/s)": [velocity],
            "Lorentz Factor (γ)": [gamma],
            "Proper Decay Time (s)": [μ_proper_lifetime],
            "Dilated Decay Time (s)": [dilated_lifetime],
            "Distance Traveled (m)": [distance]
        })

        fig = px.bar(df, x="Velocity Fraction of c", y="Distance Traveled (m)",
                     color="Dilated Decay Time (s)", color_continuous_scale="Cividis")

# =======================
# ✅ Output Display
# =======================
if df is not None:
    st.dataframe(df.round(6))
if fig is not None:
    st.plotly_chart(fig)

st.session_state.dataframe_result = df
st.session_state.chart_figure = fig

# =======================
# ✅ Custom Manual Input Section
# =======================
with st.expander("🔧 Custom Manual Input Calculation"):
    st.write("Manually simulate using custom values.")

    if model == "Special Relativity (Velocity)":
        custom_vf = st.number_input("Custom Velocity Fraction of c", min_value=0.0, max_value=0.999999, value=0.8)
        velocity = custom_vf * c
        dilated_time = compute_lorentz_dilation(np.array([velocity]), t_proper)[0]
        gamma = dilated_time / t_proper
        delta_time = dilated_time - t_proper

        custom_df = pd.DataFrame({
            "Velocity Fraction of c": [custom_vf],
            "Velocity (m/s)": [velocity],
            "Lorentz Factor (γ)": [gamma],
            "Proper Time (s)": [t_proper],
            "Dilated Time (s)": [dilated_time],
            "Δ Time (s)": [delta_time]
        })

        st.markdown("#### 📋 Custom Input Results")
        st.dataframe(custom_df.round(6))

    elif model == "General Relativity (Gravity)":
        custom_rs = st.number_input("Custom Distance from Center (in Rₛ)", min_value=1.01, value=2.5)
        Rs = schwarzschild_radius(M_sun)
        radius_m = custom_rs * Rs
        dilation = gravitational_time_dilation(Rs, radius_m)
        dilated_time = dilation * t_proper
        delta_time = dilated_time - t_proper

        custom_df = pd.DataFrame({
            "Radius from Center (m)": [radius_m],
            "Distance in Rs": [custom_rs],
            "Proper Time (s)": [t_proper],
            "Dilated Time (s)": [dilated_time],
            "Δ Time (s)": [delta_time]
        })

        st.markdown("#### 📋 Custom Input Results")
        st.dataframe(custom_df.round(6))

    elif model == "Relativistic Particle Decay":
        custom_vf = st.number_input("Custom Muon Velocity Fraction of c", min_value=0.5, max_value=0.999, value=0.95)
        velocity = custom_vf * c
        gamma = lorentz_gamma(np.array([velocity]))
        dilated_lifetime = gamma * μ_proper_lifetime
        distance = compute_decay_distances(np.array([custom_vf]))[0]

        custom_df = pd.DataFrame({
            "Velocity Fraction of c": [custom_vf],
            "Velocity (m/s)": [velocity],
            "Lorentz Factor (γ)": [gamma],
            "Proper Decay Time (s)": [μ_proper_lifetime],
            "Dilated Decay Time (s)": [dilated_lifetime],
            "Distance Traveled (m)": [distance]
        })

        st.markdown("#### 📋 Custom Input Results")
        st.dataframe(custom_df.round(6))


# =======================
# ✅ Export Options
# =======================
if df is not None:
    st.markdown("### 📁 Export Options")
    col1, col2 = st.columns(2)

    with col1:
        export_format = st.selectbox("Export Data Format", ["Select...", "CSV", "PDF"])
        if export_format == "CSV":
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", csv, file_name="time_dilation_results.csv", mime="text/csv")
        elif export_format == "PDF":
            pdf = export_chart_to_pdf("Time Dilation Summary", df)
            st.download_button("📄 Download PDF", pdf, file_name="time_dilation_summary.pdf")

    with col2:
        chart_format = st.selectbox("Export Chart Format", ["Select...", "PNG", "SVG", "HTML"])
        if fig and chart_format != "Select...":
            if chart_format == "HTML":
                html = BytesIO(fig.to_html().encode("utf-8"))
                st.download_button("🌐 Download HTML", html, file_name="chart.html", mime="text/html")
            else:
                img = BytesIO()
                fig.write_image(img, format=chart_format.lower())
                img.seek(0)
                st.download_button(f"🖼 Download {chart_format}", img, file_name=f"chart.{chart_format.lower()}")
