import pandas as pd
import numpy as np

def load_initial_conditions(csv_path, x_model):
  df = pd.read_csv(csv_path, names=["dist", "conc"], header=0,encoding='latin-1')
  #all rows column 0 become the distance column, and all rows in column 1 become the concentration coulmn

  distances = df.iloc[:,0].values
  concentration = df.iloc[:,1].values
  theta0 = np.interp(x_model, distances, concentration)
  return theta0
#Time and Space domain
L = 3.0
T = 300.0
#step sizes
dx = 0.1
dt = 0.5
#No. intervals
Nx = int(L / dx)
Nt = int(T / dt)
#Space grid:
x_model = np.linspace(0, L, Nx +1)
#intital conditions
theta = load_initial_conditions( "initial_conditions.csv", x_model)
print("No. grid points:", len(x_model))
print ("length of theta:", len(theta))
print("First comple of theta values:", theta[:5])
