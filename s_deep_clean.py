#!/usr/bin/env python3
"""
s_deep_clean.py

聚焦在干净几何来源的两个发现：
  1. theta_star = pi/(gen * Stride^2)
  2. sigma_8 = sqrt(x_dec) * B1(C8)/(B1(C8)-1)

问题：
  1. 这两个公式是否有更深的物理？
  2. 能否从中推导其他参数？
  3. 网络图像是否统一了它们？
"""

import numpy as np

pi = np.pi
Delta = 1 - np.sqrt(3)/2
R = 1/(1 + pi)
eps = 1/10
Stride = 10
gen = 3
weak = 2
color = 3
spinor = 4

V_C8 = 8
B1_C8 = 5
E_C8 = 12
V_K4 = 4

# 物理常量
U_EM = 0.4 * pi
f_ext_0 = 4/5
x_dec = 100 * (f_ext_0 - 1/U_EM)

# 观测值
obs = {
    'theta_star': 0.010409,
    'sigma_8': 0.8111,
    'S8': 0.832,
    'Omega_m': 0.3153,
    'Omega_L': 0.6847,
    'n_s': 0.9649,
    'r_d': 147.09,
    'l_A': 301.8,
    'H0': 67.4,
}

print("=" * 90)
print("  S 论文：干净几何来源的深挖")
print("=" * 90)
print()

# ============================================================
# 1. theta_star = pi/(gen * Stride^2)
# ============================================================
print("=" * 90)
print("  1. theta_star = pi/(gen * Stride^2)")
print("=" * 90)
print()

theta_pred = pi / (gen * Stride**2)
theta_err = abs(theta_pred - obs['theta_star']) / obs['theta_star']

print(f"  theta_star = pi / (gen * Stride^2)")
print(f"             = pi / ({gen} * {Stride**2})")
print(f"             = pi / {gen * Stride**2}")
print(f"             = {theta_pred:.6f} rad")
print(f"  观测 = {obs['theta_star']:.6f} rad")
print(f"  偏差 = {theta_err:.4%}")
print()

# 深入检查
print("  因子的几何来源：")
print(f"    pi = 2D 相位折叠测度")
print(f"    gen = 3 = 三代数")
print(f"    Stride^2 = 100 = 1/eps^2（累积方差倒数）")
print()

# 从 theta_star 反推 r_d
# theta_star = r_d / D_M(z_star)
# D_M(z_star) ≈ 14000 Mpc
D_M_star = 14000  # Mpc

r_d_pred = theta_pred * D_M_star
print(f"  从 theta_star 反推 r_d：")
print(f"    r_d = theta_star * D_M(z_star)")
print(f"    = {theta_pred:.6f} * {D_M_star}")
print(f"    = {r_d_pred:.2f} Mpc")
print(f"  观测 r_d = {obs['r_d']} Mpc")
print(f"  偏差 = {(r_d_pred - obs['r_d'])/obs['r_d']:.4%}")
print()

# 或者：用 D_M 从几何推导
# D_M(z_star) = r_d / theta_star = 147.09 / 0.010409 = 14130
D_M_obs = obs['r_d'] / obs['theta_star']
print(f"  观测 D_M(z_star) = r_d / theta_star = {D_M_obs:.1f} Mpc")
print(f"  候选：D_M = c/H0 * f(z_star)")
print()

# ============================================================
# 2. sigma_8 = sqrt(x_dec) / f_ext(0)
# ============================================================
print("=" * 90)
print("  2. sigma_8 = sqrt(x_dec) / f_ext(0)")
print("=" * 90)
print()

sigma_8_pred = np.sqrt(x_dec) / f_ext_0
sigma_8_err = abs(sigma_8_pred - obs['sigma_8']) / obs['sigma_8']

print(f"  sigma_8 = sqrt(x_dec) / f_ext(0)")
print(f"          = sqrt({x_dec:.6f}) / {f_ext_0}")
print(f"          = {np.sqrt(x_dec):.6f} / {f_ext_0}")
print(f"          = {sigma_8_pred:.6f}")
print(f"  观测 = {obs['sigma_8']:.6f}")
print(f"  偏差 = {sigma_8_err:.4%}")
print()

print("  因子的几何来源：")
print(f"    sqrt(x_dec) = 连接饱和点的涨落")
print(f"    1/f_ext(0) = 5/4 = 循环空间外部比的倒数")
print()

# 深入：为什么是 sqrt(x_dec)？
print("  为什么 sigma_8 = sqrt(x_dec)？")
print(f"    x_dec = 连接饱和时的宏观参数")
print(f"    sqrt(x_dec) = 连接的'标准差'")
print(f"    物理：网络涨落 ∝ sqrt(平均连接数)")
print()

# ============================================================
# 3. 从这两个发现推导其他参数
# ============================================================
print("=" * 90)
print("  3. 从两个发现推导其他参数")
print("=" * 90)
print()

# S8
S8_pred = sigma_8_pred * np.sqrt(obs['Omega_m'] / 0.3)
print(f"  S8 = sigma_8 * sqrt(Omega_m/0.3)")
print(f"     = {sigma_8_pred:.4f} * sqrt({obs['Omega_m']}/0.3)")
print(f"     = {S8_pred:.4f}")
print(f"  观测 = {obs['S8']}")
print(f"  偏差 = {(S8_pred - obs['S8'])/obs['S8']:.4%}")
print()

# 声学峰间距 l_A = pi/theta_star
l_A_pred = pi / theta_pred
print(f"  l_A = pi / theta_star = 1/theta_star * pi")
print(f"      = pi / {theta_pred:.6f}")
print(f"      = {l_A_pred:.4f}")
print(f"  观测 = 301.8")
print(f"  偏差 = {(l_A_pred - 301.8)/301.8:.4%}")
print()

# ============================================================
# 4. 尝试：其他参数是否也可从 theta_star 得到
# ============================================================
print("=" * 90)
print("  4. 其他参数从 theta_star")
print("=" * 90)
print()

# r_d * theta_star = 常数？
r_d_from_theta = obs['theta_star'] * D_M_star
print(f"  r_d 从 theta_star：")
print(f"    需要 D_M(z_star) ≈ {D_M_obs:.0f} Mpc")
print()

# 尝试 D_M(z_star) 的几何形式
# D_M(z_star) = c/H0 * ∫ dz/E(z)
# 近似：D_M ≈ 3.3 * c/H0

c_over_H0 = 299792.458 / obs['H0']  # Mpc
print(f"  c/H0 = {c_over_H0:.2f} Mpc")
print(f"  D_M(z_star) / (c/H0) = {D_M_obs / c_over_H0:.4f}")
print(f"  候选：3.4 = 17/5")
print(f"    D_M = (17/5) * c/H0")
print(f"    = {(17/5) * c_over_H0:.1f} Mpc")
print()

# ============================================================
# 5. 网络图像的统一解释
# ============================================================
print("=" * 90)
print("  5. 网络图像的统一解释")
print("=" * 90)
print()

print("  网络图像：")
print("    - C8 甩出边（电子）")
print("    - 电子甩出光子")
print("    - 光子连接另一个 C8")
print("    - 光子-电子耦合产生振荡")
print()

print("  从网络图像看 theta_star：")
print(f"    theta_star = pi / (gen * Stride^2)")
print(f"    物理：")
print(f"      pi = 光子振荡半周期（标准声学）")
print(f"      gen = 3 = 三种连接类型（轻子/夸克/介质）")
print(f"      Stride^2 = 100 = 连接传播的方差归一化")
print()

# 尝试
print("  theta_star 的物理推导：")
print(f"    theta_star = (声学视界角度)")
print(f"              = pi / (声学振荡周期数)")
print(f"    = pi / (gen * Stride^2)")
print()

# 声学峰间距 l_A = gen * Stride^2
print(f"  声学峰间距 l_A = gen * Stride^2 = {gen * Stride**2}")
print(f"  物理：C8 网络的三个独立方向（gen），每个有 Stride^2 = 100 个模式")
print()

# ============================================================
# 6. 网络连接数
# ============================================================
print("=" * 90)
print("  6. 网络连接数的计算")
print("=" * 90)
print()

# 平均连接度
k_avg = B1_C8 - 1
print(f"  平均连接度 <k> = B1(C8) - 1 = {k_avg}")
print()

# 平均连接长度
# 从光子到另一个 C8 的距离
print(f"  光子从 C8_A 到 C8_B 的平均距离：")
print(f"    ~ 1 / (平均连接密度)^(1/3)")
print()

# 连接密度 ∝ 1/x_dec
density = 1 / x_dec
print(f"  连接密度 = 1/x_dec = {density:.4f}")
print()

# 平均连接长度 ~ density^(-1/3)
length = density**(-1/3)
print(f"  平均连接长度 ∝ density^(-1/3) = {length:.4f}")
print()

# ============================================================
# 7. 其他参数
# ============================================================
print("=" * 90)
print("  7. 其他参数")
print("=" * 90)
print()

# n_s
# 从几何推导
n_s_candidates = {
    '1 - 2/(gen * Stride)': 1 - 2/(gen*Stride),
    '1 - 2*eps^2/3': 1 - 2*eps**2/3,
    '1 - 2*Delta/pi': 1 - 2*Delta/pi,
    '1 - x_dec/14': 1 - x_dec/14,
    '1 - x_dec/15': 1 - x_dec/15,
    '1 - 2*Delta/(pi-gen*eps)': 1 - 2*Delta/(pi-gen*eps),
    '1 - 2/30': 1 - 2/30,
    '1 - Delta/(3*0.4)': 1 - Delta/(3*0.4),
}
print(f"  n_s 候选：")
for name, val in n_s_candidates.items():
    err = abs(val - obs['n_s']) / obs['n_s']
    marker = " ✓" if err < 0.01 else ""
    print(f"    {name:<30} = {val:.6f}  (偏差 {err:.4%}){marker}")
print()

# H0
# H0 的几何来源：S 论文有 (19-4sqrt3)/20
H0_factor = (19 - 4*np.sqrt(3))/20
print(f"  H0 的几何因子：{H0_factor:.6f}")
print(f"  H0 公式：H0 = (1/t_Tick) * alpha_G * H0_factor")
print()

# ============================================================
# 8. 所有参数汇总
# ============================================================
print("=" * 90)
print("  8. S 论文的参数汇总")
print("=" * 90)
print()

# 已知精确公式
param_formulas = {
    'Omega_m/Omega_L': ('U_EM - 1/U_EM', U_EM - 1/U_EM, obs['Omega_m']/obs['Omega_L']),
    'Omega_m': ('K/(1+K)', (U_EM - 1/U_EM)/(1 + U_EM - 1/U_EM), obs['Omega_m']),
    'Omega_L': ('1/(1+K)', 1/(1 + U_EM - 1/U_EM), obs['Omega_L']),
    'Omega_b/Omega_c': ('Delta*(1+pi)/3', Delta*(1+pi)/3, 0.184906),
    'sigma_8': ('sqrt(x_dec)/f_ext(0)', np.sqrt(x_dec)/f_ext_0, obs['sigma_8']),
    'theta_star': ('pi/(gen*Stride^2)', pi/(gen*Stride**2), obs['theta_star']),
    'l_A': ('gen*Stride^2', gen*Stride**2, obs['l_A']),
}

print(f"  {'参数':<20} | {'公式':<25} | {'预测':>10} | {'观测':>10} | {'偏差'}")
print("  " + "-" * 80)
for name, (formula, pred, ob) in param_formulas.items():
    err = (pred - ob) / ob
    marker = " ✓" if abs(err) < 0.02 else ""
    print(f"  {name:<20} | {formula:<25} | {pred:>10.6f} | {ob:>10.6f} | {err:>+8.4%}{marker}")
print()

# ============================================================
# 9. 深挖 theta_star 的物理
# ============================================================
print("=" * 90)
print("  9. theta_star = pi/300 的物理")
print("=" * 90)
print()

# theta_star = pi/300
# l_A = 300
print(f"  theta_star = pi/300")
print(f"  l_A = pi/theta_star = 300 = gen * Stride^2")
print()

# 从声学方程
# theta_star = r_d / D_A(z_star)
# r_d = 声学视界
# D_A = 角直径距离

# 尝试：r_d 和 D_A 的关系
# r_d / D_A = pi / 300
# → r_d = pi * D_A / 300

print(f"  声学方程：")
print(f"    theta_star = r_d / D_A")
print(f"    = pi / 300")
print(f"    → r_d = pi * D_A / 300")
print()

# 如果 D_A = D_M(z_star) ≈ 14000 Mpc
# r_d = pi * 14000 / 300 = 146.6 Mpc
r_d_pred = pi * D_M_obs / 300
print(f"  如果 D_A = {D_M_obs:.0f} Mpc：")
print(f"    r_d = pi * {D_M_obs:.0f} / 300 = {r_d_pred:.2f} Mpc")
print(f"  观测 = {obs['r_d']} Mpc")
print()

# 是否 D_A 的几何来源？
print(f"  D_A 的几何来源：")
print(f"    D_A = (17/5) * c/H0")
print(f"    = {(17/5) * c_over_H0:.0f} Mpc")
print(f"  观测 D_A = {D_M_obs:.0f} Mpc")
print()

# ============================================================
# 10. 结论
# ============================================================
print("=" * 90)
print("  10. 结论")
print("=" * 90)
print()

print("  两个发现：")
print("    1. theta_star = pi/(gen * Stride^2) = pi/300")
print("       偏差 0.61%")
print("       物理：声学视界的角度，由三代数 × 采样方差决定")
print()
print("    2. sigma_8 = sqrt(x_dec) / f_ext(0)")
print("       偏差 0.176%")
print("       物理：连接涨落 × C8 循环空间外部比")
print()

print("  含义：")
print("    - S 论文的更多参数可以从几何推导")
print("    - 网络图像可能统一了多个宇宙学量")
print("    - theta_star 和 sigma_8 是最干净的")
print()

print("  待探索：")
print("    - D_A 的几何来源")
print("    - n_s 的干净形式")
print("    - r_d 的几何来源")
print("    - 网络图像的更完整结构")
print()