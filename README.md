# CNM_2025_group_07
Modelling Pollutant Transport in a River (CNM Coursework)

---

## Overview
This project models the 1D transport of a pollutant in a river using the advection equation

where:
- θ is pollutant concentration (µg/m³)
- t is time (s)
- x is distance along the river (m)
- U is flow velocity (m/s)

The model is implemented in Python using finite difference methods and produces plots and animations to visualise pollutant transport over time.

---

## Repository Structure
- `edited_test3_4_5.py` – Test cases 3, 4, and 5
- `Initial Plot.py` – Initial plotting utilities
- `initial_conditions.csv` – Provided initial concentration data
- `initial_conditions.py` / `initials_conditions.py` – Initial condition handling
- `pde_grids.py` – Grid setup and numerical solver functions
- `Results/` – Output figures and animations
- `README.md` – Project documentation

---

## Requirements
Python 3.x with the following packages:
- numpy
- matplotlib
- pandas
- pillow (for GIF animation output)

Install dependencies using:
```bash
python -m pip install numpy matplotlib pandas pillow
