import pandas as pd
import numpy as np

def load_initial_conditions(csv_path, x_model):
    df = pd.read_csv(
        csv_path,
        names=["dist","conc"],
        header=0,
        encoding='latin-1'
    )

distances = df.iloc[:, 0].values
concentration = df.iloc[:, 1].values

theta0 = np.interp(x_model, distances, concentration)
return theta0
