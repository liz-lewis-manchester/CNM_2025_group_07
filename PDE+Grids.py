import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# USER SETTINGS 

L      = 20.0        # domain length [m]
T_end  = 300.0       # total time [s]
dx     = 0.2         # spatial step [m]
dt     = 10.0        # time step [s]
U_base = 0.1         # base velocity [m/s]

IC_FILENAME = "initial_conditions.csv"  

# store profiles every N time steps (for plots & animation)
STORE_EVERY = 6      # 6 * 10 s = 60 s between stored profiles

OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# CORE NUMERICAL FUNCTIONS (BACKWARD DIFFERENCES)


def build_grid(L, T_end, dx, dt):
    """
    Build 1D spatial and temporal grids.
    """
    Nx = int(round(L / dx)) + 1
    Nt = int(round(T_end / dt)) + 1
    x  = np.linspace(0.0, L, Nx)
    t  = np.linspace(0.0, T_end, Nt)
    return x, t, Nx, Nt


def assemble_AB(u_desc, x, dx, dt, t_val=None):
    """
    Assemble diagonal arrays A and B for the bidiagonal system using
    backward differences:

        a_i = 1/dt + u_i / dx
        b_i = -u_i / dx

    u_desc can be:
      - scalar U
      - 1D array u(x_i)
      - callable u(x, t) returning 1D array
    """
    # get u(x) at this time
    if callable(u_desc):
        u_vec = np.asarray(u_desc(x, t_val), dtype=float)
    elif np.isscalar(u_desc):
        u_vec = np.full_like(x, float(u_desc), dtype=float)
    else:
        u_vec = np.asarray(u_desc, dtype=float)
        if u_vec.shape != x.shape:
            raise ValueError("Velocity array must have same shape as x")

    a_i = 1.0 / dt + u_vec / dx
    b_i = -u_vec / dx           # minus sign here

    # A, B correspond to interior nodes i = 1..Nx-1
    A = a_i[1:].copy()
    B = b_i[1:].copy()
    return A, B


def forward_step(theta_old, A, B, dt, t_now, bc_func):
    """
    Perform one time step using sparse forward substitution:

        F[I]     = (1/dt) * theta_old[I+1]
        theta[0] = boundary at x=0
        theta[I] = (F[I-1] - B[I-1] * theta[I-1]) / A[I-1], I = 1..Nx-1
    """
    Nx = theta_old.size
    theta_new = np.zeros_like(theta_old)
    F = np.zeros(Nx - 1, dtype=float)

    # boundary at x = 0
    theta_new[0] = bc_func(t_now)

    # right-hand side
    F[:] = (1.0 / dt) * theta_old[1:]

    # forward substitution along x
    for I in range(1, Nx):
        theta_new[I] = (F[I - 1] - B[I - 1] * theta_new[I - 1]) / A[I - 1]

    return theta_new


def run_model(x, t, theta0, u_desc, bc_func, store_every=1):
    """
    Generic advection solver using the backward-difference scheme.

    u_desc: scalar, array, or callable u(x, t).
    bc_func: function giving theta(t, x=0).
    store_every: store every N-th timestep for plotting/animation.

    Returns:
        times_stored  : (n_store,)
        thetas_stored : (n_store, Nx)
    """
    Nx = x.size
    Nt = t.size
    dx = x[1] - x[0]
    dt = t[1] - t[0]

    theta_old = theta0.copy()

    times_stored  = [t[0]]
    thetas_stored = [theta_old.copy()]

    time_dependent_u = callable(u_desc)

    if not time_dependent_u:
        A, B = assemble_AB(u_desc, x, dx, dt)

    for j in range(1, Nt):
        t_now = t[j]

        if time_dependent_u:
            A, B = assemble_AB(u_desc, x, dx, dt, t_val=t_now)

        theta_new = forward_step(theta_old, A, B, dt, t_now, bc_func)

        if j % store_every == 0:
            times_stored.append(t_now)
            thetas_stored.append(theta_new.copy())

        theta_old[:] = theta_new

    return np.array(times_stored), np.array(thetas_stored)
