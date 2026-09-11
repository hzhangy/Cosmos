#!/usr/bin/env python3
"""
nea_gravitational_lensing.py

N.E.A. 引力透镜偏折角。
在维度坍缩框架下，偏折来自有效质量 M_eff = M_bar × (1+r/r_c)^(2-q)。
与标准爱因斯坦偏折对比，看是否与强透镜观测一致。
"""
import numpy as np
from math import pi

c = 299792.458  # km/s
G = 4.302e-6    # kpc/Msun * (km/s)^2

# 透镜参数（星系团尺度）
M_bar = 1.0e14  # Msun
r_c = 500.0     # kpc
q_out = 1.0

def alpha_standard(b):
    """标准爱因斯坦偏折角"""
    return 4.0 * G * M_bar / (c**2 * b)

def alpha_nea(b, q):
    """N.E.A. 偏折角，用维度坍缩修正"""
    M_eff = M_bar * (1.0 + b/r_c)**(2.0 - q)
    return 4.0 * G * M_eff / (c**2 * b)

print("="*70)
print("  N.E.A. 引力透镜偏折角")
print("="*70)
print(f"  M_bar = {M_bar:.1e} Msun, r_c = {r_c} kpc")
print()
print(f"  {'b [kpc]':>10} | {'α_std [arcsec]':>16} | {'α_NEA (q=1)':>14} | {'比值':>8}")
print("-"*58)

# 转换：α [rad] → arcsec，并转换为表面密度比较
# 1 rad = 206265 arcsec

for b in [50, 100, 200, 500, 1000, 2000]:
    a_std = alpha_standard(b) * 206265  # arcsec
    a_nea = alpha_nea(b, q_out) * 206265
    ratio = a_nea / a_std
    print(f"  {b:>10.0f} | {a_std:>16.3f} | {a_nea:>14.3f} | {ratio:>8.2f}")

print()
print("  物理意义：")
print("    当 b > r_c，维度坍缩使有效质量比 M_bar 更大")
print("    → 产生额外的透镜效应，无需暗物质")
print("    当 b < r_c，q → 2，标准爱因斯坦偏折恢复")
print()
print("  观测参考：")
print("    强透镜星系团的偏折角通常在 10-30 arcsec 范围")