#!/usr/bin/env python3
"""
nea_bullet_cluster_peak_model.py

N.E.A. Bullet Cluster: qualitative model.

The dimensional-collapse halo is bound to the galaxy distribution
and follows the galaxies through the collision, while the gas is
stripped and remains at the collision center. The lensing peaks
therefore follow the galaxy peaks, while the X-ray peak stays at
the center.

This script illustrates the qualitative geometry. It does not
attempt a quantitative derivation of the ~300 kpc separation,
which is taken from observation for illustrative purposes.
"""
import numpy as np

x = np.linspace(-500, 500, 1000)

# Qualitative profiles (for illustration only)
sigma_gas = 100.0
gas = np.exp(-0.5 * (x / sigma_gas)**2)

offset = 300.0   # observed separation, used for illustration
sigma_gal = 50.0
galaxies = np.exp(-0.5 * ((x - offset) / sigma_gal)**2) + \
           np.exp(-0.5 * ((x + offset) / sigma_gal)**2)

print("="*70)
print("  N.E.A. Bullet Cluster: qualitative geometry")
print("="*70)
print()
print("  The dimensional-collapse halo is bound to the galaxies")
print("  and follows them through the collision.")
print("  The gas is stripped and remains at the collision center.")
print("  Lensing peaks therefore follow galaxy peaks;")
print("  the X-ray peak stays at the center.")
print()
print("  Observed peak separation: ~300 kpc (from observation, not derived)")
print()
print("  This is a qualitative consistency check.")
print("  A quantitative derivation is not attempted.")