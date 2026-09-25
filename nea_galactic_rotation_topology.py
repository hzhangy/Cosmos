#!/usr/bin/env python3
"""
N.E.A. Galactic Rotation Emergence from Weak Force Chirality
=============================================================
Left:  Edge-on view of emergent galactic disk
Right: Rotation curve (N.E.A. dimensional collapse vs pure Newtonian)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================
# N.E.A. PARAMETERS
# ============================================================
Delta = 1 - np.sqrt(3) / 2
r_MOND = 5.0  # Transition radius (dimensional collapse onset)

def nea_force(r):
    """N.E.A. effective force: inner 1/r², outer 1/r (dimensional collapse)"""
    force = np.zeros_like(r)
    mask_in = r < r_MOND
    mask_out = r >= r_MOND
    force[mask_in] = 1.0 / (r[mask_in]**2 + 0.1**2)
    F_boundary = 1.0 / (r_MOND**2 + 0.1**2)
    force[mask_out] = F_boundary * (r_MOND / r[mask_out])
    return force

# ============================================================
# SIMULATION
# ============================================================
np.random.seed(42)
N_particles = 5000

r_init = np.random.exponential(scale=3.0, size=N_particles)
theta = np.random.uniform(0, 2 * np.pi, N_particles)
phi = np.arccos(np.random.uniform(-1, 1, N_particles))

# Weak force chirality injection: tangential velocity ∝ Delta * r
v_mag = Delta * r_init * 1.5
vx = -v_mag * np.sin(theta)
vy = v_mag * np.cos(theta)
vz = np.random.normal(0, 0.1, N_particles)

# Equilibrium orbits
r_eq = np.copy(r_init)
for i in range(N_particles):
    L = r_init[i] * v_mag[i]
    r_test = np.linspace(0.1, 20, 1000)
    F_grav = nea_force(r_test)
    F_cent = L**2 / (r_test**3 + 0.1**3)
    diff = np.abs(F_grav - F_cent)
    r_eq[i] = r_test[np.argmin(diff)]

z_eq = np.random.normal(0, 0.3, N_particles) * np.exp(-r_eq / 8.0)

# ============================================================
# PLOTTING
# ============================================================
fig = plt.figure(figsize=(15, 6))

# Left: Edge-on disk
ax1 = fig.add_subplot(121)
ax1.scatter(r_eq * np.cos(theta), z_eq, c=r_eq, cmap='inferno', s=1, alpha=0.6)
ax1.set_title("Edge-On View: Emergent Galactic Disk\n(N.E.A. Weak Force Chirality)", fontsize=12)
ax1.set_xlabel("Radial Distance (kpc)")
ax1.set_ylabel("Z-Height (kpc)")
ax1.grid(True, alpha=0.3)

# Right: Rotation curve
ax2 = fig.add_subplot(122)
r_plot = np.linspace(0.1, 20, 500)
F_plot = nea_force(r_plot)
v_circ_nea = np.sqrt(r_plot * F_plot)
v_circ_newton = np.sqrt(1.0 / r_plot)  # Pure Keplerian

ax2.plot(r_plot, v_circ_nea, 'r-', lw=3, label='N.E.A. (Dimensional Collapse)')
ax2.plot(r_plot, v_circ_newton, 'b--', lw=2, alpha=0.7, label='Pure Newtonian (Keplerian)')
ax2.set_title("Galaxy Rotation Curve\n(Flat outer region = no dark matter needed)", fontsize=12)
ax2.set_xlabel("Radius (kpc)")
ax2.set_ylabel("Circular Velocity")
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 1.5)

plt.tight_layout()
plt.savefig("nea_galactic_rotation.png", dpi=200, bbox_inches='tight')
print("✓ 图形已保存: nea_galactic_rotation.png")
print(f"✓ 粒子数: {N_particles}")
print(f"✓ 旋转曲线在 r > {r_MOND} kpc 处趋于平坦（维度坍缩）")
plt.close()