import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

def read_and_interpolate_ic(filename, x):

    #Reads initial_conditions.csv and interpolates onto model grid x
    #first column = distance [m], second column = concentration.

    df = pd.read_csv(filename, encoding="latin1")
    xp = df.iloc[:, 0].to_numpy(dtype=float)
    fp = df.iloc[:, 1].to_numpy(dtype=float)
    theta0 = np.interp(x, xp, fp)
    return theta0
  
