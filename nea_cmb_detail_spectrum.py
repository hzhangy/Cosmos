#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N.E.A. CMB 细节谱 V2
修正：加入投影测度 k^2，使峰高比接近真实 C_l。
"""
import numpy as np
from math import pi, sqrt, exp

# N.E.A. 参数
Omega_b = 0.049753
Omega_c = 0.265547
Omega_m = Omega_b + Omega_c
Omega_L = 0.6847
h = 0.680398
H0 = 100 * h
c = 299792.458

# 已锁定宇宙学尺度
r_d = 149.20  # Mpc
D_A = 13728.55  # Mpc

# 谱参数
n_s = 0.965
k_D = 0.14  # Silk阻尼尺度 Mpc^-1

# k 范围
k_min = 0.001
k_max = 0.3
n_k = 600
k_arr = np.linspace(k_min, k_max, n_k)

# 声学振荡包络
# P(k) = k^2 * k^(n_s-4) = k^(n_s-2)
P0 = k_arr**(n_s - 2.0)
osc = np.cos(k_arr * r_d)**2
damp = np.exp(-(k_arr / k_D)**2)

P_k = P0 * (1 + osc) * damp

# 待测峰位置
ell_arr = np.array([220.6, 537.5, 810.8, 1500.0, 2500.0])
k_peaks = ell_arr / D_A

print("="*80)
print("  N.E.A. CMB 细节谱 V2：峰结构检验")
print("="*80)
print(f"  r_d = {r_d:.2f} Mpc, D_A = {D_A:.2f} Mpc, k_D = {k_D}")
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
    print(f"  峰{i+1}: ell={ell:.0f}, k={k:.4f}, P(k)={P:.6e}, 相对高度={rel:.4f}")

print()
print("  观测参考：")
print("  第一峰/第二峰 ≈ 2.2")
print("  第一峰/第三峰 ≈ 3.1")
print("="*80)