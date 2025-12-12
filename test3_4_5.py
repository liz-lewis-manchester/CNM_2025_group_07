#test case 3(test how the sensitivity are to the parameters)
#(U, spatial and temporal resolution)
#starting from the sensitivity of U
velocity=[0.05, 0.1, 0.2] 
plt.figure(figsize=(8, 5))
#setting up new grid
for U in velocity_options:x_u, t_u, Nx_u, Nt_u = build_grid(L, T_end, dx, dt)
#intitial condition for the graph
theta_init = np.zeros(Nx_u)
theta_init[0] = 250.0
#boundry setting
def inlet_velocityBC(time):return 250.0
#storing the first and last file 
times_u, thetas_u = run_model(x_u, t_u, theta_init, U, inlet_velocityBC,store_every3=Nt_u - 1)
#plotting set up
plt.plot(x_u, thetas_u[-1], label=f"U = {U:.2f} m/s")
plt.xlabel("Distance x [m]")
plt.ylabel("Concentration θ [µg/m³]")
plt.title("Test 3 – Sensitivity to U)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "test3_sensitivity_U.png"), dpi=300)
plt.close()
