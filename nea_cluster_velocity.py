#!/usr/bin/env python3
"""
nea_cluster_velocity.py

N.E.A. 星系团速度弥散。
用维度坍缩的 q(r) 修正引力加速度，计算速度弥散曲线，
与观测（例如 Coma 星系团 σ ≈ 1000 km/s）对比。
"""
import numpy as np
from math import sqrt, pi

G = 4.302e-6  # kpc/Msun * (km/s)^2

# 星系团参数（典型，如 Coma）
M_bar = 1.0e14   # Msun（可见重子物质）
r_c = 500.0      # kpc（维度坍缩特征尺度）
q_in = 2.0       # 内部维度
q_out = 1.0      # 外部维度（深坍缩）

def v_circ(r, q):
    """用 q(r) 修正的旋转曲线"""
    if r < 1.0:
        return 0.0
    factor = (1.0 + r/r_c)**(2.0 - q)
    return sqrt(G * M_bar * factor / r)

# 速度弥散 ~ 圆形速度（位力定理，粗略近似）
print("="*70)
print("  N.E.A. 星系团速度弥散")
print("="*70)
print(f"  M_bar = {M_bar:.1e} Msun, r_c = {r_c} kpc")
print()
print(f"  {'r [kpc]':>10} | {'q=2 (牛顿)':>14} | {'q=1.5':>10} | {'q=1.0':>10}")
print("-"*56)

for r in [50, 100, 200, 500, 1000, 2000, 3000]:
    v2 = v_circ(r, 2.0)
    v15 = v_circ(r, 1.5)
    v1 = v_circ(r, 1.0)
    print(f"  {r:>10.0f} | {v2:>14.1f} | {v15:>10.1f} | {v1:>10.1f}")

# 观测对比
print()
print("  观测参考：")
print("    Coma 星系团中心速度弥散 ≈ 1000 km/s")
print("    外围弥散 ≈ 800-900 km/s")
print()
print("  N.E.A. 解释：")
print("    内部 (r < r_c)：q ≈ 2，牛顿引力主导")
print("    外围 (r > r_c)：q → 1，维度坍缩使引力保持强")
print("    无需暗物质即可维持高速度弥散")