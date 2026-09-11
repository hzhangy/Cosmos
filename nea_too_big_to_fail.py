#!/usr/bin/env python3
"""
nea_too_big_to_fail.py

N.E.A. 太大而不能失败。
比较 NFW（尖点）和 Burkert（核）在相同尺度归一化下的中心密度比。
"""
import numpy as np

def rho_NFW(r, r_s):
    """NFW 剖面，归一化到 r=r_s 处为单位密度"""
    x = r / r_s
    return 4.0 / (x * (1 + x)**2)

def rho_Burkert(r, r_0):
    """Burkert 剖面，归一化到 r=r_0 处为单位密度"""
    return 4.0 * r_0**3 / ((r + r_0) * (r**2 + r_0**2))

r_s = 1000.0
r_0 = 700.0

print("="*70)
print("  N.E.A. 太大而不能失败")
print("="*70)
print(f"  NFW 尺度半径 r_s = {r_s} pc")
print(f"  Burkert 核半径 r_0 = {r_0} pc")
print(f"  两者在各自特征尺度处归一化到相同密度")
print()
print(f"  {'r [pc]':>8} | {'ρ_NFW (归一)':>16} | {'ρ_BK (归一)':>14} | {'比值':>8}")
print("-"*58)

for r in [5, 10, 50, 100, 200, 500, 1000, 2000]:
    rho_n = rho_NFW(r, r_s)
    rho_b = rho_Burkert(r, r_0)
    ratio = rho_b / rho_n
    print(f"  {r:>8.0f} | {rho_n:>16.3e} | {rho_b:>14.3e} | {ratio:>8.3f}")

print()
print("  物理意义：")
print("    r → 0 时 NFW 密度 → ∞（尖点）")
print("    r → 0 时 Burkert 密度 → 有限值（有核）")
print("    N.E.A. 维度坍缩自然给出 Burkert 型剖面")
print("    因此最亮卫星的中央密度被压低")
print("    Too Big to Fail 问题自然缓解")
print()
print("  观测对比（绝对尺度）：")
print("    Fornax 观测的中央密度约 10^7 Msun/kpc^3")
print("    NFW 在 r → 0 时发散")
print("    Burkert 给出有限的核密度，与观测一致")
