# ⏳ Time Dilation Simulations — Gravity, Speed, and Particle Decay

This project simulates and visualizes the effects of **time dilation** as described in Einstein’s **Special and General Relativity**, including the influence of **velocity**, **gravitational fields**, and **relativistic particle decay**. It provides educational datasets, scientific visualizations, and code for exploring how time behaves in extreme conditions.

---

## 📊 Datasets Included

All datasets are generated using physics formulas and are included in the `data/raw/` directory:

| Filename                               | Description |
|----------------------------------------|-------------|
| `time_dilation_high_speed_particles.csv` | Time dilation due to high velocity (Special Relativity) |
| `gravitational_time_dilation.csv`       | Time dilation near a black hole (General Relativity) |
| `particle_decay_time_dilation.csv`      | Particle decay (e.g., muons) affected by relativistic speeds |

A summary CSV of all three models is found in:  
➡️ `data/processed/combined_time_dilation_summary.csv`

---

## 🧠 Project Features

- ✔️ Physics-based simulations using NumPy & SciPy  
- ✔️ Jupyter Notebooks with visualizations and derivations  
- ✔️ Real-world example applications (GPS, muons)  
- ✔️ Optional machine learning exploration  
- ✔️ Optional Streamlit dashboard for interactive exploration  

---

## 📁 Folder Structure

**`time-dilation-simulations/`**  
- `data/` – Contains raw and processed datasets  
- `notebooks/` – Contains Jupyter notebooks for simulations and analysis  
- `scripts/` – Python scripts for generating and processing data  
- `src/dilation/` – Core physics calculation modules  
- `plots/` – Generated visualizations and charts  
- `reports/` – Data stories, writeups, and annotated figures  
- `app/` – Streamlit dashboard for interactive exploration  
- `tests/` – Unit tests for core functions and equations  
- Project root – Includes `README.md`, `requirements.txt`, `.gitignore`, and setup files

---

## ▶️ Getting Started

### 1. Install requirements
```bash
pip install -r requirements.txt
```

### 2. Run Jupyer Lab or Notebook
```bash
jupyter lab
```

### 3. Explore Notebooks
Navigate to the `notebooks/` folder and run any of the simulation notebooks.

### 🌐 Optional: Launch the Streamlit Dashboard
```bash
cd app/
streamlit run streamlit_dashboard.py
```

## 📖 License
This project is licensed under the [MIT License](LICENSE)

## ✨ Contributions
Contributions, feature requests, and improvements are welcome!
Please open an issue or pull request in the repository.

## 🚀 Credits

Developed as a scientific and educational tool to visualize how time is affected by speed, gravity, and relativistic decay inspired by Einstein’s vision and powered by modern data science.
