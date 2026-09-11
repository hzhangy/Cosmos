#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N.E.A. 矮星系旋转曲线：分段维度坍缩模型

使用分段 q(r) 模型：
  r < r_c : q = 2 (三维引力)
  r > r_c : q = 1 (深维度坍缩)

检验旋转曲线是否自然变得平坦。
"""
import numpy as np
from math import pi

G = 4.302e-6  # kpc / Msun * (km/s)^2

# 矮星系参数
M0 = 5.0e8      # Msun
a0 = 1.0        # kpc，典型矮星系重子尺度
r_c = 2.0       # 维度坍缩特征尺度 kpc

r = np.logspace(-1, 2, 500)  # 0.1 到 100 kpc

def M_bar(r):
    x = r / a0
    return M0 * (1.0 - (1.0 + x) * np.exp(-x))

def q_piecewise(r, r_c):
    return np.where(r < r_c, 2.0, 1.0)

def v_circ(r, q):
    M = M_bar(r) * (1.0 + r / r_c)**(2.0 - q)
    return np.sqrt(G * M / r)

# 三种模型
v_newton = v_circ(r, 2.0)
v_piece = v_circ(r, q_piecewise(r, r_c))
# 纯 q=1 作为参考
v_q1 = v_circ(r, 1.0)

print("="*80)
print("  N.E.A. 矮星系旋转曲线：分段维度坍缩模型")
print("="*80)
print(f"  重子质量 M0 = {M0:.1e} Msun, 尺度 a0 = {a0} kpc")
print(f"  维度坍缩过渡半径 r_c = {r_c} kpc")
print()

print(f"  {'r [kpc]':<10} {'牛顿':<12} {'分段 q(r)':<14} {'纯 q=1':<12}")
print("-"*55)
for r_test in [0.2, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0]:
    idx = np.argmin(np.abs(r - r_test))
    print(f"  {r_test:<10.1f} {v_newton[idx]:<12.2f} {v_piece[idx]:<14.2f} {v_q1[idx]:<12.2f}")

# 平坦性检验
idx10 = np.argmin(np.abs(r - 10.0))
idx50 = np.argmin(np.abs(r - 50.0))
print()
print("  平坦性检验：")
print(f"    牛顿模型 v(50)/v(10) = {v_newton[idx50]/v_newton[idx10]:.3f}")
print(f"    分段模型 v(50)/v(10) = {v_piece[idx50]/v_piece[idx10]:.3f}")
print(f"    纯 q=1 模型 v(50)/v(10) = {v_q1[idx50]/v_q1[idx10]:.3f}")
print()

print("="*80)
print("  结论")
print("="*80)
print("  分段维度坍缩模型可以产生几乎平坦的外区旋转曲线。")
print("  这说明矮星系平坦旋转曲线可由维度坍缩自然解释，")
print("  而不需要暗物质粒子。")