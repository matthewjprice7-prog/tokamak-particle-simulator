import numpy as np
from scipy.integrate import solve_ivp

# ------------------------------------------------------------
# Physical constants
# ------------------------------------------------------------
q = 1.602e-19        # charge of proton (C)
m = 1.673e-27        # mass of proton (kg)

# ------------------------------------------------------------
# Tokamak magnetic field parameters
# ------------------------------------------------------------
B0 = 5.0          # Toroidal field strength at major radius (T)
R0 = 1.0          # Major radius (meters)
a_minor = 0.3     # Minor radius of the plasma column (meters)
q_safety = np.pi    # Safety factor (number of toroidal turns per poloidal turn)
# Magnetic perturbation parameters
epsilon = 0.2      # perturbation strength
m_mode = 2          # poloidal mode number
n_mode = 1          # toroidal mode number

def q_profile(r_minor):
    return 1.0 + 3.0 * (r_minor / a_minor)**2

def B_field(r):
    """
    Toroidal + Poloidal tokamak magnetic field creating helical field lines.
    """
    x, y, z = r

    R = np.sqrt(x**2 + y**2)
    if R < 1e-6:
        return np.array([0.0, 0.0, 0.0])

    phi_hat = np.array([-y / R, x / R, 0.0])

    r_minor = np.sqrt((R - R0)**2 + z**2)

    if r_minor < 1e-6:
        Bphi = B0 * R0 / R
        return Bphi * phi_hat

    Bphi = B0 * R0 / R

    q_local = q_profile(r_minor)
    Btheta = (r_minor * Bphi) / (R * q_local)

    cos_alpha = (R - R0) / r_minor
    sin_alpha = z / r_minor

    theta_hat = np.array([
        -sin_alpha * (x / R),
        -sin_alpha * (y / R),
         cos_alpha
    ])

    theta = np.arctan2(z, R - R0)
    phi = np.arctan2(y, x)

    perturb = epsilon * Btheta * np.cos(
        m_mode * theta - n_mode * phi
    )

    B_perturb = perturb * theta_hat

    return (
        Bphi * phi_hat
        + Btheta * theta_hat
        + B_perturb
    )


# ------------------------------------------------------------
# Electrostatic wave field (propagating azimuthally)
# ------------------------------------------------------------
# phi(theta, phi_ang, t) = phi0 * cos(m_wave*theta + n_wave*phi_ang - omega_wave*t)
# Chosen so that v_phase = omega_wave / k_theta < v_gyro (ion gyration speed),
# putting the ion in the resonant / stochastic-heating regime rather than
# simply being swept along coherently with the wave.

phi0 = 5000.0       # wave potential amplitude (V)
omega_wave = 2e6    # wave angular frequency (rad/s)
m_wave = 3          # poloidal mode number of the wave
n_wave = 0          # toroidal mode number (0 = pure poloidal propagation)


def E_field(r, t):
    """
    Electrostatic wave field: phi = phi0*cos(m_wave*theta + n_wave*phi_ang - omega_wave*t)
    E = -grad(phi), computed analytically in local (R, theta, phi_ang) coordinates
    and projected back into Cartesian using the same theta_hat/phi_hat convention
    as B_field.
    """
    x, y, z = r
    R = np.sqrt(x**2 + y**2)
    if R < 1e-6:
        return np.array([0.0, 0.0, 0.0])

    r_minor = np.sqrt((R - R0)**2 + z**2)
    if r_minor < 1e-6:
        return np.array([0.0, 0.0, 0.0])

    theta = np.arctan2(z, R - R0)
    phi_ang = np.arctan2(y, x)

    phase = m_wave * theta + n_wave * phi_ang - omega_wave * t
    dphi_dtheta = -phi0 * m_wave * np.sin(phase)   # d(phi)/d(theta)
    dphi_dphi = -phi0 * n_wave * np.sin(phase)     # d(phi)/d(phi_ang)

    # E_theta = -(1/r_minor) d(phi)/d(theta);  E_phi = -(1/R) d(phi)/d(phi_ang)
    E_theta = -dphi_dtheta / r_minor
    E_phi = -dphi_dphi / R

    phi_hat = np.array([-y / R, x / R, 0.0])
    cos_alpha = (R - R0) / r_minor
    sin_alpha = z / r_minor
    theta_hat = np.array([
        -sin_alpha * (x / R),
        -sin_alpha * (y / R),
         cos_alpha
    ])

    return E_theta * theta_hat + E_phi * phi_hat


## ------------------------------------------------------------
# Initial conditions
# ------------------------------------------------------------
v_perp = 2e5       # gyration speed
v_parallel = 1.2e6   # parallel speed

# Start inside the plasma core chamber
r0 = np.array([1.1, 0.0, 0.0])

B_vec0 = B_field(r0)
Bhat0 = B_vec0 / np.linalg.norm(B_vec0)

perp_dir = np.array([0.0, 0.0, 1.0])
perp_dir = perp_dir - np.dot(perp_dir, Bhat0) * Bhat0
perp_dir = perp_dir / np.linalg.norm(perp_dir)

v0 = v_parallel * Bhat0 + v_perp * perp_dir

# Cyclotron frequency and Larmor radius (for reference)
omega_c = q * B0 / m
r_Larmor = m * v_perp / (q * B0)
print("Cyclotron frequency (rad/s):", omega_c)
print("Larmor radius (m):", r_Larmor)

# ------------------------------------------------------------
# Resonance check: v_phase vs v_gyro
# ------------------------------------------------------------
r_minor0 = np.sqrt((np.sqrt(r0[0]**2 + r0[1]**2) - R0)**2 + r0[2]**2)
k_theta = m_wave / max(r_minor0, 1e-6)
v_phase = omega_wave / k_theta if k_theta > 0 else np.inf

print("Reference minor radius (m):", r_minor0)
print("k_theta (1/m):", k_theta)
print("Wave phase velocity v_phase = omega/k_theta (m/s):", v_phase)
print("Ion gyration speed v_perp (m/s):", v_perp)
if v_phase < v_perp:
    print("=> v_phase < v_gyro: resonant/stochastic heating regime")
else:
    print("=> WARNING: v_phase >= v_gyro; wave is faster than gyration. "
          "Increase m_wave or decrease omega_wave to enter the resonant regime.")

# ------------------------------------------------------------
# Lorentz force (dv/dt), now including the electrostatic wave field
# ------------------------------------------------------------
def acceleration(v, r, t, q, m):
    B = B_field(r)
    E = E_field(r, t)
    return (q / m) * (E + np.cross(v, B))

# ------------------------------------------------------------
# RK4 integrator step (time-dependent)
# ------------------------------------------------------------
def rk4_step(r, v, t, dt):
    k1_v = acceleration(v, r, t, q, m)
    k1_r = v

    k2_v = acceleration(v + 0.5*dt*k1_v, r + 0.5*dt*k1_r, t + 0.5*dt, q, m)
    k2_r = v + 0.5*dt*k1_v

    k3_v = acceleration(v + 0.5*dt*k2_v, r + 0.5*dt*k2_r, t + 0.5*dt, q, m)
    k3_r = v + 0.5*dt*k2_v

    k4_v = acceleration(v + dt*k3_v, r + dt*k3_r, t + dt, q, m)
    k4_r = v + dt*k3_v

    r_new = r + (dt/6)*(k1_r + 2*k2_r + 2*k3_r + k4_r)
    v_new = v + (dt/6)*(k1_v + 2*k2_v + 2*k3_v + k4_v)

    return r_new, v_new

# ------------------------------------------------------------
# Field line tracing (unaffected by the electrostatic wave --
# field lines follow B only)
# ------------------------------------------------------------

def field_line_step(r, ds):
    """
    RK4 step along magnetic field line.
    """

    def direction(pos):
        B = B_field(pos)
        Bmag = np.linalg.norm(B)

        if Bmag < 1e-12:
            return np.zeros(3)

        return B / Bmag

    k1 = direction(r)
    k2 = direction(r + 0.5 * ds * k1)
    k3 = direction(r + 0.5 * ds * k2)
    k4 = direction(r + ds * k3)

    r_new = r + (ds / 6) * (k1 + 2*k2 + 2*k3 + k4)

    return r_new

# ------------------------------------------------------------
# Time settings
# ------------------------------------------------------------
dt = 5e-10
steps = 100000

# Arrays to store the motion
r = np.zeros((steps, 3))
v = np.zeros((steps, 3))
t_arr = np.zeros(steps)

r[0] = r0
v[0] = v0
t_arr[0] = 0.0

# Diagnostics: kinetic energy, theta (poloidal angle), and wave phase
kinetic_energy = np.zeros(steps)
theta_arr = np.zeros(steps)
v_theta_arr = np.zeros(steps)

def _theta_and_vtheta(pos, vel):
    x, y, z = pos
    R = np.sqrt(x**2 + y**2)
    r_minor = np.sqrt((R - R0)**2 + z**2)
    theta = np.arctan2(z, R - R0)
    if r_minor < 1e-6 or R < 1e-6:
        return theta, 0.0
    cos_alpha = (R - R0) / r_minor
    sin_alpha = z / r_minor
    theta_hat = np.array([
        -sin_alpha * (x / R),
        -sin_alpha * (y / R),
         cos_alpha
    ])
    v_theta = np.dot(vel, theta_hat)
    return theta, v_theta

kinetic_energy[0] = 0.5 * m * np.dot(v0, v0)
theta_arr[0], v_theta_arr[0] = _theta_and_vtheta(r0, v0)

# ------------------------------------------------------------
# Simulation loop
# ------------------------------------------------------------
for i in range(1, steps):
    t_now = t_arr[i-1]
    r[i], v[i] = rk4_step(r[i-1], v[i-1], t_now, dt)
    t_arr[i] = t_now + dt

    kinetic_energy[i] = 0.5 * m * np.dot(v[i], v[i])
    theta_arr[i], v_theta_arr[i] = _theta_and_vtheta(r[i], v[i])

print("Initial kinetic energy (J):", kinetic_energy[0])
print("Final kinetic energy (J):", kinetic_energy[-1])
print("Fractional energy change:",
      (kinetic_energy[-1] - kinetic_energy[0]) / kinetic_energy[0])

# ------------------------------------------------------------
# Compute guiding center estimate
# ------------------------------------------------------------

guiding_center = np.zeros_like(r)

for i in range(steps):

    B = B_field(r[i])
    Bmag = np.linalg.norm(B)

    if Bmag < 1e-12:
        guiding_center[i] = r[i]
        continue

    Bhat = B / Bmag

    v_perp_vec = v[i] - np.dot(v[i], Bhat) * Bhat
    rho = (m / (q * Bmag)) * np.cross(v_perp_vec, Bhat)

    guiding_center[i] = r[i] + rho

gc_start = guiding_center[0]
gc_end = guiding_center[-1]

print("Guiding center displacement (m):")
print(gc_end - gc_start)

print("Total displacement magnitude (m):")
print(np.linalg.norm(gc_end - gc_start))

# ------------------------------------------------------------
# Trace multiple magnetic field lines
# ------------------------------------------------------------
field_steps = 50000
ds = 0.003

field_line_starts = [
    np.array([1.08, 0.0, 0.0]),
    np.array([1.15, 0.0, 0.0]),
    np.array([1.22, 0.0, 0.0]),
    np.array([1.15, 0.0, 0.1])
]

field_lines_data = []

poincare_R = []
poincare_Z = []

for start_pos in field_line_starts:

    line_r = np.zeros((field_steps, 3))
    line_r[0] = start_pos

    for i in range(1, field_steps):

        old_pos = line_r[i-1]
        new_pos = field_line_step(old_pos, ds)
        line_r[i] = new_pos

        y_old = old_pos[1]
        y_new = new_pos[1]

        if y_old < 0 and y_new >= 0:
            R_cross = np.sqrt(new_pos[0]**2 + new_pos[1]**2)
            z_cross = new_pos[2]
            poincare_R.append(R_cross)
            poincare_Z.append(z_cross)

    field_lines_data.append(line_r)

# ------------------------------------------------------------
# Build the Interactive 3D Visualization
# ------------------------------------------------------------
from visualization import plot_tokamak
import plotly.graph_objects as go

fig = plot_tokamak(
    r,
    R=1.0,
    a=0.3,
    title="Tokamak Orbit with Resonant Electrostatic Wave"
)

for idx, line_coords in enumerate(field_lines_data):
    field_trace = go.Scatter3d(
        x=line_coords[:, 0],
        y=line_coords[:, 1],
        z=line_coords[:, 2],
        mode='lines',
        line=dict(width=2.5, color='orange'),
        name='Magnetic Field Line',
        legendgroup='field_lines',
        showlegend=(idx == 0)
    )
    fig.add_trace(field_trace)

gc_trace = go.Scatter3d(
    x=guiding_center[:, 0],
    y=guiding_center[:, 1],
    z=guiding_center[:, 2],
    mode='lines',
    line=dict(width=5, color='red'),
    name='Guiding Center'
)

fig.add_trace(gc_trace)

fig.show()

# ------------------------------------------------------------
# Poincare Section Plot
# ------------------------------------------------------------

import matplotlib.pyplot as plt
print("Number of Poincare points:", len(poincare_R))
plt.figure(figsize=(7, 7))
plt.scatter(poincare_R, poincare_Z, s=2)
plt.xlabel("Major Radius R (m)")
plt.ylabel("Vertical Position Z (m)")
plt.title("Tokamak Poincare Section")
plt.axis('equal')
plt.show()

plt.figure(figsize=(7, 7))
R_particle = np.sqrt(r[:, 0]**2 + r[:, 1]**2)
plt.plot(R_particle, r[:, 2], linewidth=0.5)
plt.xlabel("R (m)")
plt.ylabel("Z (m)")
plt.title("Particle Orbit in Poloidal Plane")
plt.axis('equal')
plt.show()

# ------------------------------------------------------------
# Resonance diagnostics: energy evolution and phase-space portrait
# ------------------------------------------------------------

# 1) Kinetic energy vs time -- look for systematic heating (resonance)
#    vs bounded oscillation (no resonance / adiabatic).
plt.figure(figsize=(8, 5))
plt.plot(t_arr, kinetic_energy, linewidth=0.6)
plt.xlabel("Time (s)")
plt.ylabel("Kinetic energy (J)")
plt.title("Ion Kinetic Energy vs Time (Wave-Particle Interaction)")
plt.tight_layout()
plt.show()

# 2) Phase-space portrait (theta, v_theta) -- resonance islands / stochastic
#    layers show up here when v_phase < v_gyro causes phase trapping/scattering.
plt.figure(figsize=(7, 7))
plt.scatter(theta_arr, v_theta_arr, s=1, c=t_arr, cmap='viridis')
plt.colorbar(label="Time (s)")
plt.xlabel("Poloidal angle theta (rad)")
plt.ylabel("v_theta (m/s)")
plt.title("Phase-Space Portrait (theta, v_theta)")
plt.tight_layout()
plt.show()

# 3) Wave phase seen by the particle vs v_theta -- direct resonance check.
#    If the particle gets stuck near a particular phase while v_theta
#    grows/oscillates coherently, that's the resonance signature.
wave_phase_seen = (m_wave * theta_arr - omega_wave * t_arr) % (2 * np.pi)
plt.figure(figsize=(7, 7))
plt.scatter(wave_phase_seen, v_theta_arr, s=1, c=t_arr, cmap='plasma')
plt.colorbar(label="Time (s)")
plt.xlabel("Wave phase seen by particle (rad)")
plt.ylabel("v_theta (m/s)")
plt.title("Resonance Check: Wave Phase vs v_theta")
plt.tight_layout()
plt.show()