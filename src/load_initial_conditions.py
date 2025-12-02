import pandas as pd
import numpy as np

def load_initial_conditions(csv_path, x_model):
  df = pd.read_csv(csv_path) 
  #all rows column 0 become the distance column, and all rows in column 1 become the concentration coulmn

  distances = df.iloc[:,0].values
  concentration = df.iloc[:,1].values
  theta0 = np.interp(x_model, distances, concentration)
  return theta0
