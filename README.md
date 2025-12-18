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
- `TestCase12.py` - Test cases 1 & 2
- `edited_test3_4_5.py` – Test cases 3, 4, and 5
- `Initial Plot.py` – Initial plotting utilities
- `initial_conditions.csv` – Provided initial concentration data
- `initial_conditions.py` – Initial condition handling
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

## How to Run the Model
## How to Run the Model

1. Clone the repository:
   ```bash
   git clone https://github.com/liz-lewis-manchester/CNM_2025_group_07.git
   cd CNM_2025_group_07

python -m pip install numpy matplotlib pandas pillow

python edited_test3_4_5.py

python TestCase12.py

## Test Cases

The following test cases were implemented to verify the numerical model and explore its behaviour:

### Test Case 1 – Constant Initial Condition
A 1D river domain of length 20 m is simulated with a spatial resolution of 0.2 m and a temporal resolution of 10 s.
The pollutant concentration is initialised as 250 µg/m³ at the inlet (x = 0) and zero elsewhere, with a constant velocity of U = 0.1 m/s.

### Test Case 2 – Initial Conditions from CSV
Initial pollutant concentrations are read from `initial_conditions.csv` and interpolated onto the model grid.
This tests the model’s ability to handle real measurement data that does not align with the computational grid.

### Test Case 3 – Sensitivity Analysis
The sensitivity of the model to velocity (U), spatial resolution (dx), and temporal resolution (dt) is investigated.
Multiple simulations are run to observe how numerical parameters influence solution stability and accuracy.

### Test Case 4 – Time-Varying Inlet Concentration
An exponentially decaying inlet concentration is applied to investigate how time-dependent boundary conditions affect pollutant transport.

### Test Case 5 – Variable Velocity Profile
A spatially varying velocity profile is introduced by adding a 10% random perturbation to a constant velocity.
Results are compared against the constant velocity case to assess the impact of flow variability.


