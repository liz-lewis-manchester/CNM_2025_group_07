import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import os 

# Test 1 
# parameters 
L = 20.0 
Nx = 201 
t_end = 3600.0
Nt = 1000

# variables + conditions 
dx = L/(Nx - 1)
x = np.linspace(0, L, Nx)
t = np.linspace(0, t_end, Nt)
U_base = 0.5
Store_every = 10
output_dir = "Results"
IC_FILENAME = "initial_conditions.cvs"
if not os.path.exists(output_dir):
  os.makedirs(output_dir)

# Test 2 
# initial conditions 
def read_and_interpolate_ic(filename, x):
  df = pd.read_csv(filename, encoding="latin1")
  xp = df.iloc[:, 0].to_numpy(dtype=float)
  fp = df.iloc[:, 1].to_numpy(dtype=float)
  theta0 = np.interp(x, xp, fp)
  return theta0

# plot
def plot_profiles(x, times, thetas, title_prefix="", save_path=None, show=False):
  plt.figure(figsize=(8,5))
  for k in range(len(times)):
    plt.plot(x, thetas[k, :], label=f"t = {times[k]:.0f} s")
  plt.xlabel("Distance (x) in m")
  plt.ylabel("Concetration (ø) in µg/m³")
  plt.title(f"{title_prefix} pollutant concentration profiles")
  plt.grid(True)
  plt.legend()
  plt.tight_layout()
  if save_path is not None:
    plt.savefig(save_path, dpi=300)
  if show:
    plt.show()
  else:
    plt.close

# animation
def animate_solution(x, times, thetas, title="Animation", save_path=None, show=False):
  fig, ax = plt.subplots(figsize=(8, 5))
  line, = ax.plot([], [], lw=2)
  ax.set_xlim(x[0], x[-1])
  ax.set_ylim(0, np.max(thetas) * 1.1)
  ax.set_xlabel("Distance (x) in m")
  ax.set_ylabel("Concetration (ø) in µg/m³")
  ax.set_title(title)
  ax.grid(True)
  def update(frame):
    line.set_data(x, thetas[frame, :])
    ax.set_title(f"{title} - t = {times[frame]:.0f} s")
    return line,
  anim = FuncAnimation(fig, update, frames=len(times), interval=300, blit=False)
  if save_path is not None:
    ext = os.path.splitext(save_path)[1].lower()
    try:
      if ext in [".gif"]:
        anim.save(save_path, writer="pillow")
      else:
        anim.save(save_path, writer="ffmpeg")
      print(f"Savedanimation to {save_path}")
    except Exception as e:
        print(f"Couldn't save animation ({save_path}): {e}")
  if show:
    plt.show()
  else:
    plt.close(fig)
  return anim 

# Run test 
def main():
  #parameters
  L = 20.0
  Nx = 201
  t_end = 3600.0
  Nt = 1000
  
  dx = L / (Nx - 1)
  x = np.linspace(0, L, Nx)
  times = np.linspace(0, t_end, Nt)

  theta0 = read_and_interpolate_ic("initial_conditions.csv", x)

  thetas = np.tile(theta0, (Nt,1))

  plot_profiles(x, times[::200], thetas[::200], title_prefix="Test", show=True)

  anim = animate_solution(
    x,
   times,
   thetas,
   title="Animation Test", 
   save_path="Results/animation.gif",
   show=False
   )
plt.show()

if __name__ == "__main__":
  main()

    

