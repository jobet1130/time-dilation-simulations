import sys
from pathlib import Path

# Ensure `src` is discoverable
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Core Libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import sympy as sp
from io import BytesIO
from reportlab.pdfgen import canvas
from sympy.parsing.sympy_parser import parse_expr
import base64

# Local Modules
from src.dilation.lorentz import compute_lorentz_dilation
from src.dilation.gravity import gravitational_time_dilation, schwarzschild_radius
from src.dilation.decay import compute_decay_distances
from src.dilation.relativity_utils import c, M_sun, μ_proper_lifetime, lorentz_gamma

# ------------------------
# Streamlit UI Config
# ------------------------
st.set_page_config(page_title="⏳ Time Dilation Simulator", layout="wide")
st.title("⏳ Time Dilation Simulator — Velocity, Gravity, and Decay")


# ------------------------
# ✏️ Editable Equation Preview
# ------------------------
st.sidebar.markdown("### ✏️ Custom Equation (Advanced)")
user_expr_input = st.sidebar.text_input("Enter a custom expression (use `v`, `c`, `r`, `Rs`)", "1 / sqrt(1 - v**2 / c**2)")
try:
    user_expr = parse_expr(user_expr_input, evaluate=False)
    st.sidebar.latex(sp.latex(user_expr))
except Exception:
    st.sidebar.error("❌ Invalid expression")

# ------------------------
# 🔽 Model Selection
# ------------------------
model = st.sidebar.selectbox("Select Time Dilation Model", [
    "Special Relativity (Velocity)",
    "General Relativity (Gravity)",
    "Relativistic Particle Decay"
])

t_proper = 1.0  # Default Proper Time (seconds)
dataframe_result = None

# ------------------------
# 📤 Upload CSV
# ------------------------
uploaded_file = st.sidebar.file_uploader("Upload CSV with `velocity_fraction` or `radius_rs`", type=["csv"])

# ------------------------
# 📥 Sample Templates
# ------------------------
st.sidebar.download_button("📄 Velocity Template", "velocity_fraction\n0.1\n0.5\n0.9", file_name="velocity_template.csv")
st.sidebar.download_button("📄 Radius Template", "radius_rs\n1.1\n2.0\n5.0", file_name="radius_template.csv")

# ------------------------
# 🧾 PDF Export Function
# ------------------------
def export_chart_to_pdf(title, df):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 800, title)
    text = c.beginText(50, 770)
    for line in df.to_string(index=False).split("\n"):
        text.textLine(line)
    c.drawText(text)
    c.save()
    buffer.seek(0)
    return buffer

# ------------------------
# 📊 Simulation Logic
# ------------------------
st.markdown(f"## 📊 Simulation: {model}")

if uploaded_file:
    user_df = pd.read_csv(uploaded_file)

    if "velocity_fraction" in user_df.columns:
        vf = user_df["velocity_fraction"].values
        velocities = vf * c
        dilated_time = compute_lorentz_dilation(velocities, t_proper)
        gamma = dilated_time / t_proper

        dataframe_result = pd.DataFrame({
            "Velocity Fraction of c": vf,
            "Velocity (m/s)": velocities,
            "Lorentz Factor (γ)": gamma,
            "Proper Time (s)": t_proper,
            "Dilated Time (s)": dilated_time,
            "Δ Time (s)": dilated_time - t_proper
        })

        st.dataframe(dataframe_result.round(6))

        fig = px.scatter(dataframe_result,
                         x="Velocity Fraction of c",
                         y="Δ Time (s)",
                         color="Δ Time (s)",
                         title="Δ Time vs Velocity (Interactive)",
                         labels={"Δ Time (s)": "Time Gained"},
                         color_continuous_scale="Viridis")
        st.plotly_chart(fig)

    elif "radius_rs" in user_df.columns:
        r = user_df["radius_rs"].values
        Rs = schwarzschild_radius(M_sun)
        dilation = gravitational_time_dilation(Rs, r * Rs)
        dilated_time = dilation * t_proper

        dataframe_result = pd.DataFrame({
            "Distance from BH (Rₛ)": r,
            "Proper Time (s)": t_proper,
            "Dilation Factor": dilation,
            "Dilated Time (s)": dilated_time,
            "Δ Time (s)": dilated_time - t_proper
        })

        st.dataframe(dataframe_result.round(6))

        fig = px.scatter(dataframe_result,
                         x="Distance from BH (Rₛ)",
                         y="Δ Time (s)",
                         color="Δ Time (s)",
                         title="Δ Time vs Distance (Interactive)",
                         labels={"Δ Time (s)": "Time Gained"},
                         color_continuous_scale="Plasma")
        st.plotly_chart(fig)

    else:
        st.error("⚠️ CSV must contain `velocity_fraction` or `radius_rs`.")

else:
    if model == "Special Relativity (Velocity)":
        v_frac = st.slider("Velocity Fraction of c", 0.1, 0.99, 0.5, 0.01)
        velocity = v_frac * c
        dilated_time = compute_lorentz_dilation(np.array([velocity]), t_proper)[0]
        gamma = dilated_time / t_proper

        st.markdown(f"**γ (Lorentz Factor):** `{gamma:.4f}`")
        st.markdown(f"**Dilated Time:** `{dilated_time:.6f} s`")

    elif model == "General Relativity (Gravity)":
        r = st.slider("Distance from BH (in Rₛ)", 1.1, 10.0, 2.0, 0.1)
        Rs = schwarzschild_radius(M_sun)
        dilation = gravitational_time_dilation(Rs, r * Rs)
        dilated_time = dilation * t_proper

        st.markdown(f"**Dilation Factor:** `{dilation:.4f}`")
        st.markdown(f"**Dilated Time:** `{dilated_time:.6f} s`")

    elif model == "Relativistic Particle Decay":
        v = st.slider("Muon Speed (fraction of c)", 0.5, 0.999, 0.98, 0.001)
        vf_array = np.array([v])
        distance_m = compute_decay_distances(vf_array)[0]

        gamma = lorentz_gamma(v * c)
        dilated_lifetime = gamma * μ_proper_lifetime

        st.markdown(f"**γ (Lorentz Factor):** `{gamma:.4f}`")
        st.markdown(f"**Dilated Lifetime:** `{dilated_lifetime:.6e} s`")
        st.markdown(f"**Decay Distance:** `{distance_m / 1000:.2f} km`")

# ------------------------
# 📁 Export Results Section
# ------------------------
if dataframe_result is not None:
    csv = dataframe_result.to_csv(index=False).encode("utf-8")
    st.download_button("💾 Download CSV", csv, file_name="time_dilation_results.csv", mime="text/csv")

    pdf_buffer = export_chart_to_pdf("Time Dilation Summary", dataframe_result)
    st.download_button("📄 Export as PDF", pdf_buffer, file_name="time_dilation_summary.pdf")

    if 'fig' in locals():
        # Chart download format selection
        chart_format = st.selectbox("📊 Select Chart Download Format", ["PNG", "PDF", "SVG", "HTML"])
        
        if chart_format == "PNG":
            img_buffer = BytesIO()
            fig.write_image(img_buffer, format="png")
            img_buffer.seek(0)
            st.download_button(
                "🖼️ Download Chart as PNG",
                img_buffer,
                file_name="time_dilation_chart.png",
                mime="image/png"
            )
        elif chart_format == "PDF":
            pdf_buffer = BytesIO()
            fig.write_image(pdf_buffer, format="pdf")
            pdf_buffer.seek(0)
            st.download_button(
                "📄 Download Chart as PDF",
                pdf_buffer,
                file_name="time_dilation_chart.pdf",
                mime="application/pdf"
            )
        elif chart_format == "SVG":
            svg_buffer = BytesIO()
            fig.write_image(svg_buffer, format="svg")
            svg_buffer.seek(0)
            st.download_button(
                "🖼️ Download Chart as SVG",
                svg_buffer,
                file_name="time_dilation_chart.svg",
                mime="image/svg+xml"
            )
        elif chart_format == "HTML":
            html_content = fig.to_html()
            html_buffer = BytesIO(html_content.encode('utf-8'))
            st.download_button(
                "🌐 Download Chart as HTML",
                html_buffer,
                file_name="time_dilation_chart.html",
                mime="text/html"
            )
