#!/usr/bin/env python3
"""
cosmo-lambda-evolution.py

验证 Ω_m/Ω_Λ 是退耦值还是今天值。

核心问题：
  S 论文说 K = Ω_m/Ω_Λ = 0.460862 来自退耦点
  但 Planck 观测的 Ω_m = 0.3153 是今天值
  退耦到今天，ρ_m ∝ a^-3, ρ_Λ = 常数
  比值会变化——是巧合还是自洽？

验证：
  1. 从退耦点的 K 出发，用标准宇宙学演化到今天
  2. 对比 Planck 的今天值
  3. 判断 S 论文的物理
"""

import numpy as np

pi = np.pi
U_EM = 0.4 * pi
K_dec = U_EM - 1/U_EM  # 退耦点的物质/暗能量比

print("=" * 90)
print("  Ω_m/Ω_Λ 演化验证")
print("=" * 90)
print()

# ============================================================
# 1. 退耦点的 Ω 值
# ============================================================
print("=" * 90)
print("  1. 退耦点的 Ω_m 和 Ω_Λ")
print("=" * 90)
print()

Omega_m_dec = K_dec / (1 + K_dec)
Omega_L_dec = 1 / (1 + K_dec)

print(f"  退耦点 K = {K_dec:.6f}")
print(f"  退耦点 Ω_m = {Omega_m_dec:.6f}")
print(f"  退耦点 Ω_Λ = {Omega_L_dec:.6f}")
print()

# ============================================================
# 2. 从退耦演化到今天
# ============================================================
print("=" * 90)
print("  2. 从退耦演化到今天")
print("=" * 90)
print()

# 退耦红移
z_dec = 1100
a_dec = 1 / (1 + z_dec)
a_0 = 1

print(f"  退耦红移 z_dec = {z_dec}")
print(f"  退耦尺度因子 a_dec = 1/(1+z_dec) = {a_dec:.6e}")
print(f"  今天尺度因子 a_0 = 1")
print()

# 密度演化
# ρ_m(a) = ρ_m(a_dec) × (a_dec/a)^3
# ρ_Λ(a) = ρ_Λ(a_dec)（常数）
# ρ_crit(a) = ρ_m + ρ_Λ

# 设退耦点 ρ_crit(a_dec) = 1（归一化）
rho_m_dec = Omega_m_dec
rho_L_dec = Omega_L_dec
rho_crit_dec = 1

# 今天
rho_m_0 = rho_m_dec * (a_dec / a_0)**3
rho_L_0 = rho_L_dec  # 常数
rho_crit_0 = rho_m_0 + rho_L_0

Omega_m_0_evolved = rho_m_0 / rho_crit_0
Omega_L_0_evolved = rho_L_0 / rho_crit_0

print(f"  密度演化：")
print(f"    ρ_m ∝ a^-3，ρ_Λ = 常数")
print()
print(f"  退耦点 ρ_m = {rho_m_dec:.6f}")
print(f"  今天 ρ_m = ρ_m_dec × (a_dec/a_0)^3 = {rho_m_0:.6e}")
print()
print(f"  退耦点 ρ_Λ = {rho_L_dec:.6f}")
print(f"  今天 ρ_Λ = {rho_L_0:.6f}")
print()
print(f"  今天 Ω_m = {Omega_m_0_evolved:.6e}")
print(f"  今天 Ω_Λ = {Omega_L_0_evolved:.6f}")
print()

# 对比 Planck
Omega_m_Planck = 0.3153
Omega_L_Planck = 0.6847

print(f"  Planck 今天值：")
print(f"    Ω_m = {Omega_m_Planck}")
print(f"    Ω_Λ = {Omega_L_Planck}")
print()
print(f"  演化后 vs Planck：")
print(f"    Ω_m 比值 = {Omega_m_0_evolved / Omega_m_Planck:.4e}")
print(f"    Ω_Λ 比值 = {Omega_L_0_evolved / Omega_L_Planck:.6f}")
print()

print("  结论：")
print(f"    从退耦演化到今天，Ω_m 几乎为零（{Omega_m_0_evolved:.2e}）")
print(f"    完全不匹配 Planck 的 0.3153")
print()
print(f"    这说明 S 论文的 K = 0.461 不是退耦值")
print()

# ============================================================
# 3. 反推：如果 K 是今天的值
# ============================================================
print("=" * 90)
print("  3. 假设 K 是今天的值")
print("=" * 90)
print()

print(f"  如果 K = Ω_m/Ω_Λ = {K_dec:.6f} 是今天值：")
print(f"    今天 Ω_m = {Omega_m_dec:.6f}")
print(f"    今天 Ω_Λ = {Omega_L_dec:.6f}")
print()
print(f"  对比 Planck：")
print(f"    Ω_m 偏差 = {(Omega_m_dec - Omega_m_Planck) / Omega_m_Planck:.4%}")
print(f"    Ω_Λ 偏差 = {(Omega_L_dec - Omega_L_Planck) / Omega_L_Planck:.4%}")
print()

# ============================================================
# 4. 那退耦条件 f_ext = 1/U_EM 是什么意思？
# ============================================================
print("=" * 90)
print("  4. 退耦条件的正确理解")
print("=" * 90)
print()

print("  S 论文的推导：")
print(f"    f_ext = 4/5 - x/100")
print(f"    退耦时 f_ext = 1/U_EM = {1/U_EM:.6f}")
print(f"    解出 x_dec = 0.422528")
print()

# 退耦点在演化中的位置
x_dec = 100 * (4/5 - 1/U_EM)
print(f"  x_dec 是宇宙演化参数 x 在退耦时的值")
print(f"  x 从 0（初始）到 1（终点）")
print()

print("  可能的理解：")
print("    (a) x 是宇宙学时间参数，退耦发生在 x = 0.42")
print("    (b) K = U_EM - 1/U_EM 是今天的值")
print("    (c) 两者独立，只是巧合匹配")
print()

# ============================================================
# 5. 检验：K 是否可以用今天的 f_ext 推导
# ============================================================
print("=" * 90)
print("  5. K 从今天的 f_ext 推导")
print("=" * 90)
print()

# 今天的 f_ext
f_ext_0 = 4/5

# 如果 K = f_int²/f_ext
# 今天 f_int² = 1 - f_ext_0² = 1 - 16/25 = 9/25 = 0.36
f_int2_0 = 1 - f_ext_0**2
K_today = f_int2_0 / f_ext_0

print(f"  今天 f_ext(0) = 4/5 = {f_ext_0}")
print(f"  今天 f_int² = 1 - f_ext² = 1 - 16/25 = {f_int2_0}")
print(f"  K_today = f_int²/f_ext = {f_int2_0}/{f_ext_0} = {K_today}")
print()

print(f"  对比 K = U_EM - 1/U_EM = {K_dec:.6f}")
print(f"  K_today = {K_today}")
print(f"  差异：{abs(K_today - K_dec) / K_dec:.4%}")
print()

# 似乎不一样
print("  K_today ≠ U_EM - 1/U_EM")
print()

# ============================================================
# 6. 关键物理问题：为什么 K = U_EM - 1/U_EM？
# ============================================================
print("=" * 90)
print("  6. 关键物理问题")
print("=" * 90)
print()

print(f"  S 论文：K = U_EM - 1/U_EM = {K_dec:.6f}")
print()
print("  这个公式的几何来源：")
print(f"    U_EM = 电磁编织租金 = {U_EM:.6f}")
print(f"    1/U_EM = 退耦后剩余带宽 = {1/U_EM:.6f}")
print(f"    K = U_EM - 1/U_EM")
print()
print("  从退耦条件推导：")
print(f"    退耦时 f_ext = 1/U_EM")
print(f"    f_int² = 1 - f_ext² = 1 - 1/U_EM²")
print(f"    K = f_int²/f_ext = (1 - 1/U_EM²)/(1/U_EM)")
print(f"    = U_EM - 1/U_EM = {K_dec:.6f}")
print()

print("  所以 K 是退耦点的物质/暗能量比")
print()

# ============================================================
# 7. 自洽性检验
# ============================================================
print("=" * 90)
print("  7. 自洽性检验")
print("=" * 90)
print()

print("  S 论文的逻辑链：")
print(f"    1. f_ext = 4/5 - x/100（磨损方程）")
print(f"    2. 退耦时 f_ext = 1/U_EM")
print(f"    3. → x_dec = 0.422528")
print(f"    4. Ω_m/Ω_Λ = U_EM - 1/U_EM = 0.460862")
print(f"    5. → Ω_m = 0.315473, Ω_Λ = 0.684527")
print()

print("  与 Planck 对比：")
print(f"    Planck: Ω_m = 0.3153, Ω_Λ = 0.6847")
print(f"    偏差: Ω_m 0.055%, Ω_Λ -0.025%")
print()

print("  物理问题：")
print(f"    - Planck 的 Ω_m = 0.3153 是今天值")
print(f"    - S 论文的 Ω_m = 0.3155 是退耦值？还是今天值？")
print(f"    - 如果是退耦值，不可能匹配今天（演化差 10^9）")
print(f"    - 如果是今天值，为什么从退耦条件推？")
print()

# ============================================================
# 8. 可能的解释
# ============================================================
print("=" * 90)
print("  8. 可能的解释")
print("=" * 90)
print()

print("  解释 A：S 论文的 K 是今天的值")
print("    U_EM - 1/U_EM 是今天物质/暗能量比")
print("    退耦条件 f_ext = 1/U_EM 是另一个独立事件")
print("    两者碰巧都涉及 U_EM")
print()

print("  解释 B：S 论文的 K 是退耦值，与今天巧合接近")
print("    需要证明 Ω_m/Ω_Λ 从退耦到今天保持不变")
print("    但 ρ_m ∝ a^-3, ρ_Λ = 常数，比值会变")
print("    不成立")
print()

print("  解释 C：S 论文隐含了 Ω_m/Ω_Λ 的物理时间")
print("    可能 x 不是宇宙时间，是别的参数")
print("    需要重新理解 x 的物理")
print()

# ============================================================
# 9. 验证：演化到今天的具体数值
# ============================================================
print("=" * 90)
print("  9. 精确演化计算")
print("=" * 90)
print()

# 用 Planck 的今天值反推退耦值
print("  用 Planck 今天值反推退耦值：")
print(f"    Planck 今天：Ω_m = {Omega_m_Planck}, Ω_Λ = {Omega_L_Planck}")
print()

# 反推退耦
rho_m_today = Omega_m_Planck
rho_L_today = Omega_L_Planck
rho_m_dec_back = rho_m_today * (a_dec / a_0)**(-3)
rho_L_dec_back = rho_L_today
rho_crit_dec_back = rho_m_dec_back + rho_L_dec_back
Omega_m_dec_back = rho_m_dec_back / rho_crit_dec_back
Omega_L_dec_back = rho_L_dec_back / rho_crit_dec_back

print(f"  反推退耦时：")
print(f"    Ω_m(dec) = {Omega_m_dec_back:.6e}")
print(f"    Ω_Λ(dec) = {Omega_L_dec_back:.6f}")
print(f"    K(dec) = {Omega_m_dec_back/Omega_L_dec_back:.6e}")
print()

print(f"  对比 S 论文退耦值：")
print(f"    K(dec, S) = {K_dec:.6f}")
print(f"    K(dec, 从 Planck 反推) = {Omega_m_dec_back/Omega_L_dec_back:.6e}")
print(f"    差异：完全不一致")
print()

# ============================================================
# 10. 结论
# ============================================================
print("=" * 90)
print("  10. 结论")
print("=" * 90)
print()

print("  验证结果：")
print()
print("  ✓ 数值上 K = U_EM - 1/U_EM = 0.460862 匹配 Planck 的 0.460494")
print("  ✓ 偏差 0.08%")
print()
print("  ? 但物理上是退耦值还是今天值，S 论文说退耦")
print("  ? 退耦到今天，Ω_m 从 0.315 演化到 ~10^-9")
print("  ? 所以 S 论文的 Ω_m 不是退耦值")
print()
print("  可能的修正：")
print("    S 论文的 K = U_EM - 1/U_EM 应该就是今天的值")
print("    退耦条件 f_ext = 1/U_EM 可能不是推导 K 的来源")
print("    或者需要重新理解 x_dec 的物理")
print()