#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
维度坍缩模型：更灵活的 q(r) 形式，渐近值可调
q(r) = q_in - (q_in - q_out) / (1 + (r/r_q)^n)
"""
import numpy as np
from math import pi
from scipy.optimize import curve_fit

# 重子模型
M0 = 1.0e10
a0 = 1.0
r_c = 2.0  # 先固定，也可以后面扫描

r = np.logspace(-2, 2, 300)
mask_fit = (r >= 0.1) & (r <= 50.0)
r_fit = r[mask_fit]

def M_bar(r):
    x = r / a0
    return M0 * (1.0 - (1.0 + x) * np.exp(-x))

def q_flex(r, q_in, q_out, r_q, n):
    return q_in - (q_in - q_out) / (1.0 + (r / r_q)**n)

def rho_DM_flex(r, q_in, q_out, r_q, n):
    q = q_flex(r, q_in, q_out, r_q, n)
    M = np.maximum(M_bar(r) * (1.0 + r / r_c)**(2.0 - q) - M_bar(r), 0.0)
    r_safe = np.maximum(r, 1e-4)
    dM_dr = np.gradient(M, r_safe)
    return dM_dr / (4.0 * pi * r_safe**2)

def burkert(r, rho0, r0):
    return rho0 * r0**3 / ((r + r0) * (r**2 + r0**2))

# 参数网格
q_in_values = [1.9, 2.0, 2.1]
q_out_values = np.linspace(1.0, 1.8, 9)
r_q_values = np.linspace(0.5, 10.0, 10)
n_values = np.linspace(0.5, 4.0, 8)

best_rmse = 1e9
best_params = None
best_burkert = None

print("扫描灵活 q(r) 参数空间...")
for q_in in q_in_values:
    for q_out in q_out_values:
        for r_q in r_q_values:
            for n in n_values:
                if q_in <= q_out:
                    continue
                rho_model = rho_DM_flex(r, q_in, q_out, r_q, n)
                rho_fit = rho_model[mask_fit]

                # 拟合 Burkert
                p0 = [rho_fit.max(), 3.0]
                try:
                    popt, _ = curve_fit(
                        lambda rr, lr0, lr1: np.log(burkert(rr, np.exp(lr0), np.exp(lr1)) + 1e-300),
                        r_fit,
                        np.log(rho_fit + 1e-300),
                        p0=[np.log(p0[0]), np.log(p0[1])],
                        maxfev=5000
                    )
                except:
                    continue

                rho0_opt = np.exp(popt[0])
                r0_opt = np.exp(popt[1])
                rho_burkert = burkert(r_fit, rho0_opt, r0_opt)

                log_res = np.log(rho_burkert + 1e-300) - np.log(rho_fit + 1e-300)
                rmse = np.sqrt(np.mean(log_res**2))

                if rmse < best_rmse:
                    best_rmse = rmse
                    best_params = (q_in, q_out, r_q, n)
                    best_burkert = (rho0_opt, r0_opt)

print("\n最优结果：")
print(f"  q_in = {best_params[0]:.3f}")
print(f"  q_out = {best_params[1]:.3f}")
print(f"  r_q = {best_params[2]:.3f}")
print(f"  n = {best_params[3]:.3f}")
print(f"  RMSE(log) = {best_rmse:.4f}")
print(f"  Burkert rho0 = {best_burkert[0]:.6e}")
print(f"  Burkert r0 = {best_burkert[1]:.4f}")

# 最终对比
q_in_opt, q_out_opt, r_q_opt, n_opt = best_params
rho_model_opt = rho_DM_flex(r, q_in_opt, q_out_opt, r_q_opt, n_opt)
rho_burkert_opt = burkert(r, best_burkert[0], best_burkert[1])

print("\n半径处密度对比（最优参数）：")
print(f"  {'r [kpc]':<10} {'模型 rho':<15} {'Burkert rho':<15} {'比值':<10}")
for r_test in [0.1, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0]:
    idx = np.argmin(np.abs(r - r_test))
    ratio = rho_burkert_opt[idx] / rho_model_opt[idx] if rho_model_opt[idx] > 0 else np.nan
    print(f"  {r_test:<10.1f} {rho_model_opt[idx]:<15.6e} {rho_burkert_opt[idx]:<15.6e} {ratio:<10.4f}")

print("\n结论：")
if best_rmse < 0.2:
    print("  维度坍缩模型可以很好地重现 Burkert 有核轮廓。")
elif best_rmse < 0.4:
    print("  维度坍缩模型与 Burkert 轮廓基本一致，但仍有轻微偏差。")
else:
    print("  需要更复杂的维度坍缩机制。")