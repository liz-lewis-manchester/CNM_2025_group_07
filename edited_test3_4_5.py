import numpy as np
import matplotlib.pyplot as plt
import os

from pde_grids import build_grid, run_model
from initials_conditions import plot_profiles
# =========================
# Global simulation parameters
# =========================
L = 20.0        # domain length [m]
T_end = 300.0   # total simulation time [s]
dx = 0.2        # spatial step [m]
dt = 10.0       # time step [s]

U_base = 0.1    # base velocity [m/s]
STORE_EVERY = 10

OUTPUT_DIR = "Results"
os.makedirs(OUTPUT_DIR, exist_ok=True)
#test case 3(test how the sensitivity are to the parameters)
#(U, spatial and temporal resolution)
#starting from the sensitivity of U
velocity=[0.05, 0.1, 0.2] 
plt.figure(figsize=(8, 5))

#setting up new grid
for U in velocity:
    x_u, t_u, Nx_u, Nt_u = build_grid(L, T_end, dx, dt)

    #intitial condition for the graph
    theta_init = np.zeros(Nx_u)
    theta_init[0] = 250.0

    #boundry setting
    def inlet_velocityBC(time):
        return 250.0

    #storing the first and last file 
    times_u, thetas_u = run_model(
        x_u, t_u, theta_init, U, inlet_velocityBC,
        store_every = Nt_u - 1
    )

    #plotting set up
    plt.plot(x_u, thetas_u[-1], label=f"U = {U:.2f} m/s")
plt.xlabel("Distance x [m]")
plt.ylabel("Concentration θ [µg/m³]")
plt.title("Test 3 – Sensitivity to U")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "test3_sensitivity_U.png"), dpi=300)
plt.close()

#sensitivity to temporal resolution
dt_options = [5.0, 10.0, 20.0]
plt.figure(figsize=(8, 5))

for dt_choice in dt_options:
    x_dt, t_dt, Nx_dt, Nt_dt = build_grid(L, T_end, dx, dt_choice)
    theta_init = np.zeros(Nx_dt)
    theta_init[0] = 250.0

    def inlet_dt(time):
        return 250.0
    times_dt, thetas_dt = run_model(
        x_dt, t_dt, theta_init, U_base, inlet_dt, store_every=Nt_dt - 1
    )

    plt.plot(x_dt, thetas_dt[-1], label=f"dt = {dt_choice:.1f} s")

#setting up plot
plt.xlabel("Distance x [m]")
plt.ylabel("Concentration θ [µg/m³]")
plt.title("Test 3 – Sensitivity to time step dt (final state)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "test3_sensitivity_dt.png"), dpi=300)
plt.close()


#sensitivity to spatial dx
#new grid
dx_options = [0.4, 0.2, 0.1]
plt.figure(figsize=(8, 5))
for dx_choice in dx_options:
    x_dx, t_dx, Nx_dx, Nt_dx = build_grid(L, T_end, dx_choice, dt)
    theta_init = np.zeros(Nx_dx)
    theta_init[0] = 250.0

    def inlet_dx(time):
        return 250.0
    times_dx, thetas_dx = run_model(
        x_dx, t_dx, theta_init, U_base, inlet_dx,
        store_every=Nt_dx - 1
    )
    plt.plot(x_dx, thetas_dx[-1], label=f"dx = {dx_choice:.2f} m")

#plot set up and saving
plt.xlabel("Distance x [m]")
plt.ylabel("Concentration θ [µg/m³]")
plt.title("Test 3 – Sensitivity to spatial step dx (final state)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "test3_sensitivity_dx.png"), dpi=300)
plt.close()

print("done test cases 3")

#test case 4: exponentially decaying inlet

#new geid build up 
x4, t4, Nx4, Nt4 = build_grid(L, T_end, dx, dt)

# Start with zero concentration
theta4_initial = np.zeros(Nx4)

#time scale
tau = 100.0

# Inlet boundary condition
def decaying_inlet(time):
    return 250.0 * np.exp(-time / tau)

#run the model and store each profile
times4, thetas4 = run_model(x4, t4, theta4_initial, U_base, decaying_inlet, store_every=STORE_EVERY)

#plot 
plot_profiles(x4, times4, thetas4, title_prefix="Test 4 – exponentially decaying inlet", save_path=os.path.join(OUTPUT_DIR, "test4_profiles.png"))

print ("done test case 4")
# -----------------------------
# Test case 5: variable velocity
# -----------------------------

# build grid for test case 5
x5, t5, Nx5, Nt5 = build_grid(L, T_end, dx, dt)

#test case 5: how variable stream velocity profile alters the results(ten percent random perturbation)

#create a spatially varying velocity profile around the base velocity
rng = np.random.default_rng(123) 
variable_U = U_base * (1 + 0.1 * (2 * rng.random(Nx5) - 1))

#set up nitial condition
theta5_initial = np.zeros(Nx5)
theta5_initial[0] = 250.0

#set up inlet boundry condition
def inlet_test5(time):return 250.0

#simulation and run model with varying velocity
t5_var, th5_var = run_model(
    x5, t5, theta5_initial, variable_U, inlet_test5, 
    store_every=STORE_EVERY
)

#simulation and run model with uniform velocity
t5_const, th5_const = run_model(
    x5, t5, theta5_initial, U_base, inlet_test5,
    store_every=STORE_EVERY
)

#plot set up
plt.figure(figsize=(8, 5))
plt.plot(x5, th5_const[-1], label="constant U")
plt.plot(x5, th5_var[-1], label="variable U(x)")
plt.xlabel("Distance x [m]")
plt.ylabel("Concentration θ [µg/m³]")
plt.title("Test 5 – comparison of constant vs variable velocity")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "test5_variable_U.png"), dpi=300)
plt.close()

print("finished test cases 3, 4, 5")
