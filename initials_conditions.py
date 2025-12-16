import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

def read_and_interpolate_ic(filename, x):

    #Reads initial_conditions.csv and interpolates onto model grid x
    #first column is distance (m) second column is concentration

    df = pd.read_csv(filename, encoding="latin1")
    xp = df.iloc[:, 0].to_numpy(dtype=float)
    fp = df.iloc[:, 1].to_numpy(dtype=float)
    theta0 = np.interp(x, xp, fp)
    return theta0
    
  #plotting and animation
#need to plot the concentration profiles at multiple times on the same graph
#should loop and plot theta(x) at each time
def plot_profiles(x, times, thetas, title_prefix="", save_path=None, show=False):
    plt.figure(figsize=(8, 5))
    for k in range(len(times)):
        plt.plot(x, thetas[k, :], label=f"t = {times[k]:.0f} s")
    plt.xlabel("Distance x [m]")
    plt.ylabel("Concentration θ [µg/m³]")
    plt.title(f"{title_prefix} pollutant concentration profiles")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    #saving the plot if file path is provided 
    #if not then display or close
    
    if save_path is not None:
        plt.savefig(save_path, dpi=300)
    if show:
        plt.show()
    else:
        plt.close()
#inimation of solution
def animate_solution(x, times, thetas, title="Animation",
                     save_path=None, show=False):
    fig, ax = plt.subplots(figsize=(8, 5))
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(0, np.max(thetas) * 1.1)
    ax.set_xlabel("Distance x [m]")
    ax.set_ylabel("Concentration θ [µg/m³]")
    ax.set_title(title)
    ax.grid(True)
#update means the plot is updated at each different time
#changes the title to show the time
    def update(frame):
        line.set_data(x, thetas[frame, :])
        ax.set_title(f"{title} — t = {times[frame]:.0f} s")
        return line,

    anim = FuncAnimation(fig, update, frames=len(times),
                         interval=300, blit=True)

    if save_path is not None:
        # Choose writer based on file extension
        ext = os.path.splitext(save_path)[1].lower()
        try:
            if ext in [".gif"]:
                anim.save(save_path, writer="pillow")
            else:
                anim.save(save_path, writer="ffmpeg")
            print(f"Saved animation to {save_path}")
        except Exception as e:
            print(f"Could not save animation ({save_path}): {e}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return anim
