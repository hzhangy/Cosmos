#!/usr/bin/env python3
"""
s_from_composite_source.py

从正确的物理图像重新计算宇宙学参数。

物理图像：
  - 发射源 = C8 + K4 复合体（不是裸 K4）
  - 红 K4 = 质子，蓝 K4 = 中子
  - 氢原子 = 1 个 K4 嵌入 C8
  - 从复合体发射 1D 边（光/时间）
  - 沿 1D 线，弱力产生等势 2D 球壳（空间）
  - 膨胀 = 1D 线延伸

计算：
  1. C8+K4 复合体的密度
  2. 球壳的几何
  3. 从网络统计推导宇宙学参数
"""

import numpy as np

pi = np.pi
Delta = 1 - np.sqrt(3)/2
R = 1/(1 + pi)
eps = 1/10
eps2 = 1/100

# 几何常量
V_C8 = 8; E_C8 = 12; B1_C8 = 5
V_K4 = 4; E_K4 = 6; B1_K4 = 3
V_octa = 6; gen = 3; weak = 2; spinor = 4
Stride = 10

# 物理常量
U_EM = 0.4 * pi
f_ext_0 = 4/5
x_dec = 100 * (f_ext_0 - 1/U_EM)

print("=" * 90)
print("  从 C8+K4 复合体发射源出发")
print("=" * 90)
print()

# ============================================================
# 1. 发射源的几何
# ============================================================
print("=" * 90)
print("  1. 发射源 = C8 + K4 复合体")
print("=" * 90)
print()

# 一个 C8 单元有 8 个顶点
# 红色 K4 占 4 个顶点（偶数子格）
# 蓝色 K4 占 4 个顶点（奇数子格）
# 一个 C8 可容纳 1 个红 K4 + 1 个蓝 K4（= 1 个 H2？不对）
# 或者：一个 C8 嵌入 1 个 K4（= 氢）

print("  C8 单元结构：")
print(f"    8 个顶点，12 条边")
print(f"    红色 K4：4 个顶点（偶数子格）")
print(f"    蓝色 K4：4 个顶点（奇数子格）")
print()

# 发射源数量
# 每个 C8 单元可以容纳 1 个 K4（氢）
# 或者 2 个 K4（氦）
# 发射强度 ∝ 嵌入的 K4 数

print("  发射源密度：")
print(f"    ∝ C8 中 K4 的嵌入数")
print(f"    最小：1 个 K4 / C8（氢）")
print()

# ============================================================
# 2. 球壳的几何
# ============================================================
print("=" * 90)
print("  2. 球壳（空间）的几何")
print("=" * 90)
print()

# V 论文的球壳公式
# |S_r| = 4r^2 + 2
# 这是 L1 球壳的节点数
# 物理：等势球壳的空间节点数

print("  V 论文的球壳面积定律：")
print(f"    |S_r| = 4r^2 + 2")
print()

for r in [1, 5, 10, 20]:
    S_r = 4*r**2 + 2
    print(f"    r = {r:>3}: |S_r| = {S_r}")
print()

# ============================================================
# 3. 从网络统计推导 Omega_m/Omega_L
# ============================================================
print("=" * 90)
print("  3. Omega_m/Omega_L 从网络统计")
print("=" * 90)
print()

# Omega_m = 有 K4 的 C8 比例（发射源）
# Omega_L = 无 K4 的 C8 比例（空空间）

# 退耦时刻：f_ext = 1/U_EM
# 此时有多少 C8 有 K4？

# 尝试：Omega_m/Omega_L = C8 发射态 vs 未发射态
# = f_ext 的某个函数

print("  网络图像：")
print(f"    有 K4 的 C8：物质源")
print(f"    无 K4 的 C8：空空间")
print()

# 从 x_dec 推导
print(f"  x_dec = {x_dec:.6f}")
print(f"  退耦时 f_ext = 1/U_EM = {1/U_EM:.6f}")
print()

# 尝试不同公式
print("  Omega_m/Omega_L 候选：")
candidates = {
    'U_EM - 1/U_EM': U_EM - 1/U_EM,
    'x_dec/(1-x_dec)': x_dec/(1-x_dec),
    'sqrt(x_dec)': np.sqrt(x_dec),
    '(1-x_dec)/x_dec': (1-x_dec)/x_dec,
    'x_dec^1.5': x_dec**1.5,
    'x_dec * (1+Delta)': x_dec*(1+Delta),
}
obs_K = 0.460494
for name, val in candidates.items():
    err = abs(val - obs_K) / obs_K
    marker = " ✓" if err < 0.05 else ""
    print(f"    {name:<25} = {val:.6f}  (偏差 {err:.4%}){marker}")
print()

# ============================================================
# 4. 从球壳推导 theta_star
# ============================================================
print("=" * 90)
print("  4. theta_star 从球壳几何")
print("=" * 90)
print()

# theta_star = pi/(gen*Stride^2) = pi/300
# 从网络图像：声学振荡 = 球壳的径向模

print("  声学振荡的物理：")
print(f"    1D 线上的球壳 = 声学模")
print(f"    振荡周期 ∝ 球壳半径")
print()

# 从球壳节点数 |S_r| = 4r^2+2
# 振荡模数 = 某个几何量

# 第一声学峰 l_1 = 220
# theta_star = pi/l_1 ≈ pi/220 = 0.01428 （不对，应该是 0.0104）

# 声学峰间距 l_A = pi/theta_star = 301.8
print(f"  声学峰间距 l_A = pi/theta_star")
print(f"    l_A = pi/(gen*Stride^2) = {pi/(gen*Stride**2):.6f}")
print(f"    l_A = 300")
print(f"  观测 l_A = 301.8")
print(f"  偏差 = {abs(300 - 301.8)/301.8:.4%}")
print()

# ============================================================
# 5. 尝试：从发射源密度推导其他参数
# ============================================================
print("=" * 90)
print("  5. 从发射源密度推导")
print("=" * 90)
print()

# 发射源密度 n_source
# C8 密度 × K4 嵌入概率

# 关键：C8 的密度 = 1/(晶格间距)^3
# 物理：a_0 = 485 fm（Z 论文）
a_0 = 485.26  # fm

print(f"  C8 晶格间距：a_0 = {a_0} fm = {a_0 * 1e-15} m")
print()

# C8 密度
# 1 C8 占 a_0^3 体积
n_C8 = 1 / (a_0 * 1e-15)**3  # 1/m^3
print(f"  C8 密度：n_C8 = 1/a_0^3 = {n_C8:.3e} m^-3")
print()

# 可观测宇宙半径
R_universe = 4.4e26  # m
print(f"  可观测宇宙半径：R = {R_universe:.2e} m")
print()

# 宇宙中的 C8 总数
N_C8_total = (4/3) * pi * R_universe**3 * n_C8
print(f"  宇宙中 C8 总数：N_C8 = {N_C8_total:.3e}")
print()

# 这个数和 N_max 有关系吗？
N_max = np.exp(10*np.sqrt(3))
print(f"  N_max = exp(10sqrt3) = {N_max:.3e}")
print(f"  N_C8 / N_max = {N_C8_total / N_max:.3e}")
print()

# ============================================================
# 6. 尝试：从球壳节点数推导 Omega_b/Omega_c
# ============================================================
print("=" * 90)
print("  6. Omega_b/Omega_c 从球壳几何")
print("=" * 90)
print()

# Omega_b/Omega_c = 0.1849
# 从球壳 |S_r| = 4r^2+2

# 球壳在 r=1 时的节点数 = 6
# 这是八面体的顶点数
print(f"  球壳 r=1：|S_1| = 4 + 2 = 6")
print(f"  这是八面体顶点数 V(octa) = 6")
print()

# Omega_b/Omega_c = 0.1849
# 尝试：
candidates = {
    'Delta*(1+pi)/3': Delta*(1+pi)/3,
    'Delta/(1+pi)': Delta/(1+pi),
    'Delta/pi': Delta/pi,
    'R^2/2': R**2/2,
    '(1-R)*(1-R)': (1-R)**2,
    'Delta^2*10': Delta**2*10,
}
obs_ratio = 0.184906
for name, val in candidates.items():
    err = abs(val - obs_ratio) / obs_ratio
    marker = " ✓" if err < 0.05 else ""
    print(f"    {name:<20} = {val:.6f}  (偏差 {err:.4%}){marker}")
print()

# ============================================================
# 7. 网络的自洽性检查
# ============================================================
print("=" * 90)
print("  7. 网络的自洽性检查")
print("=" * 90)
print()

# 发射源数量 = 有 K4 的 C8 数
# Omega_m = 有 K4 的 C8 比例
# Omega_L = 无 K4 的 C8 比例

# 但总 C8 数 = N_max？
# 如果 Omega_m = 0.315，有 K4 的 C8 数 = 0.315 * N_C8_total
# 无 K4 的 C8 数 = 0.685 * N_C8_total

print("  网络自洽性：")
print(f"    有 K4 的 C8（物质）：{0.315:.3f} × N_total")
print(f"    无 K4 的 C8（暗能量）：{0.685:.3f} × N_total")
print()

# 但为什么是 0.315？
# Omega_m = K/(1+K), K = U_EM - 1/U_EM

# 物理：K = 发射态 / 未发射态的比例
# U_EM = 1.257 = C8 横向周期比 × pi
# 1/U_EM = 0.796 = 退耦时的 f_ext

# 所以：
# K = (1 - 1/U_EM^2) / (1/U_EM)
#   = U_EM - 1/U_EM
# 物理：发射态（U_EM）减去退耦后的剩余

print(f"  K = U_EM - 1/U_EM = {U_EM - 1/U_EM:.6f}")
print(f"  物理：C8 横向周期比 - 退耦剩余")
print()

# ============================================================
# 8. 新的尝试：球壳的"发射深度"
# ============================================================
print("=" * 90)
print("  8. 球壳的发射深度")
print("=" * 90)
print()

# 每个 C8+K4 复合体发射 1D 线
# 线延伸到 r_max
# 在半径 r 处的球壳有 |S_r| 个节点

# 发射总强度 ∝ 复合体数 × 线的长度

# 平均发射深度 = <r>
# 从 V 论文：phi(r) = (r/100)/(4r^2+2)

# r_max 是什么？
# 如果 x = <r>/r_max = 0.42
# 则 r_max = <r>/0.42

# 从球壳节点数：|S_r| = 4r^2+2
# 球壳总面积 ~ 4pi r^2
# 比例：|S_r|/4pi r^2 → 1（大 r）

print(f"  球壳节点数：|S_r| = 4r^2 + 2")
print(f"  欧几里得面积：4pi r^2")
print(f"  比例：|S_r|/(4pi r^2) → 1/pi（大 r）")
print()

# 检查发射源的总数
# 从物质密度 Omega_m * rho_crit

rho_crit = 9.47e-27  # kg/m^3
m_proton = 1.67e-27  # kg

# 物质密度
rho_m = 0.315 * rho_crit
print(f"  物质密度：rho_m = Omega_m × rho_crit = {rho_m:.3e} kg/m^3")
print()

# 每 m^3 有 rho_m / m_p 个质子
n_protons = rho_m / m_proton
print(f"  质子密度：n_p = {n_protons:.3e} m^-3")
print()

# 每个质子 = 1 个 K4
# C8 密度
print(f"  C8 密度：n_C8 = {n_C8:.3e} m^-3")
print(f"  质子密度 / C8 密度 = {n_protons/n_C8:.3e}")
print()

# 太小的比例，说明 C8 密度估计不对
print("  如果 C8 间距不是 a_0 = 485 fm，而是更大")
print()

# 从质子密度反推 C8 间距
a_C8_actual = (1/n_protons)**(1/3) * 1e15  # fm
print(f"  从质子密度反推：a_C8 = {a_C8_actual:.3e} fm")
print()

# 这个值巨大，说明质子非常稀疏
print(f"  质子间距 ≈ {a_C8_actual:.2e} fm = {a_C8_actual*1e-15:.2e} m")
print(f"  这是宇宙中质子的平均间距")
print()

# ============================================================
# 9. 结论
# ============================================================
print("=" * 90)
print("  9. 结论")
print("=" * 90)
print()

print("  从正确物理图像（C8+K4 发射源）：")
print()
print("  已确认：")
print(f"    1. 球壳面积定律 |S_r| = 4r^2+2")
print(f"    2. r=1 球壳 = 八面体（6 节点）")
print(f"    3. C8 是脚手架，K4 是发射源核心")
print()
print("  未确认：")
print(f"    1. Omega_m/Omega_L 从网络密度的精确推导")
print(f"    2. theta_star = pi/300 的物理机制")
print(f"    3. sigma_8 的网络意义")
print()
print("  关键物理问题：")
print(f"    C8 密度 vs 质子密度的巨大差异如何解释？")
print(f"    C8 是脚手架，但可能不是每个 C8 都有 K4")
print()