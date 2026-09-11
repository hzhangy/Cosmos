#!/usr/bin/env python3
"""
nea_scale_relations.py

Proton mass and gravitational constant from the topological iron triangle.
Paper: Section 8 (Semi-Empirical Topological Scale Relations).
"""
from math import sqrt, pi, exp

# Topological genes
Delta = 1 - sqrt(3)/2
R = 1/(1+pi)
N_max = exp(10*sqrt(3))
f_geo = 1 + Delta/(4*pi)
Z_MeV = 0.406640

# Physical constants
hbar_SI = 1.054571817e-34
c_SI = 299792458.0
MeV_to_J = 1.602176634e-13

# Observed
m_p_obs = 938.272     # MeV
G_obs = 6.67430e-11   # m^3 kg^-1 s^-2

# --- Proton mass ---
m_p_over_Z = f_geo * (sqrt(R)/(1+R)) * sqrt(N_max)
m_p_NEA = m_p_over_Z * Z_MeV

# --- Gravitational constant ---
alpha_G_inv = N_max**5 / R
m_p_kg = m_p_NEA * MeV_to_J / c_SI**2
G_NEA = hbar_SI * c_SI / (m_p_kg**2 * alpha_G_inv)

print("="*60)
print("  Semi-Empirical Topological Scale Relations")
print("="*60)
print()
print(f"  m_p / Z         = {m_p_over_Z:.4f}")
print(f"  m_p (NEA)       = {m_p_NEA:.3f} MeV")
print(f"  m_p (obs)       = {m_p_obs:.3f} MeV")
print(f"  deviation       = {(m_p_NEA/m_p_obs-1)*100:+.3f}%")
print()
print(f"  alpha_G^-1      = {alpha_G_inv:.4e}")
print(f"  G (NEA)         = {G_NEA:.4e} m^3 kg^-1 s^-2")
print(f"  G (obs)         = {G_obs:.4e} m^3 kg^-1 s^-2")
print(f"  deviation       = {(G_NEA/G_obs-1)*100:+.3f}%")