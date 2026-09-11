#!/usr/bin/env python3
"""
nea_cmb_detail_spectrum.py

N.E.A. CMB detailed spectrum: peak structure.
"""
import numpy as np
from math import pi, sqrt, exp

# N.E.A. parameters (enthalpy-decomposition values)
Omega_b = 0.049241
Omega_c = 0.266232
Omega_m = Omega_b + Omega_c
Omega_L = 0.684527
h = 0.6804
H0 = 100 * h
c = 299792.458

# Locked cosmological scales
r_d = 149.39      # Mpc
D_M = 13725.56    # Mpc (comoving distance to z_*)

# Spectral parameters
n_s = 0.964852
k_D = 0.14        # Silk damping scale, Mpc^-1

# k range
k_min, k_max, n_k = 0.001, 0.3, 600
k_arr = np.linspace(k_min, k_max, n_k)

# Acoustic oscillation envelope
P0 = k_arr**(n_s - 2.0)
osc = np.cos(k_arr * r_d)**2
damp = np.exp(-(k_arr / k_D)**2)
P_k = P0 * (1 + osc) * damp

# Peak positions
ell_arr = np.array([220.6, 537.5, 810.8, 1500.0, 2500.0])
k_peaks = ell_arr / D_M

print("="*70)
print("  N.E.A. CMB Peak Structure")
print("="*70)
print(f"  r_d = {r_d:.2f} Mpc, D_M = {D_M:.2f} Mpc, k_D = {k_D}")
print()

P_peak1 = None
for i, (ell, k) in enumerate(zip(ell_arr, k_peaks)):
    idx = np.argmin(np.abs(k_arr - k))
    P = P_k[idx]
    if i == 0:
        P_peak1 = P
        rel = 1.0
    else:
        rel = P / P_peak1
    print(f"  Peak {i+1}: ell={ell:.0f}, k={k:.4f}, P(k)={P:.6e}, rel={rel:.4f}")

print()
print("  Observed: peak1/peak2 ≈ 2.2, peak1/peak3 ≈ 3.1")