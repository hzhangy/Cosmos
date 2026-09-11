#!/usr/bin/env python3
"""
nea_missing_satellites.py
"""
import numpy as np

M_min = 1e6
M_max = 1e10
alpha = -1.9
N_LCDM = 500

# 正确的归一化
# ∫_{M_min}^{M_max} M^alpha dM = (M_max^(alpha+1) - M_min^(alpha+1))/(alpha+1)
integral = (M_max**(alpha+1) - M_min**(alpha+1)) / (alpha+1)
C = N_LCDM / integral

def dN_dM(M):
    return C * M**alpha

M_threshold = 1e7
M_arr = np.logspace(np.log10(M_min), np.log10(M_max), 10000)
dN_arr = dN_dM(M_arr)

total_LCDM = np.trapezoid(dN_arr, M_arr)
mask = M_arr > M_threshold
total_nea = np.trapezoid(dN_arr * mask, M_arr)

print("="*70)
print("  N.E.A. 缺失卫星星系")
print("="*70)
print()
print(f"  子晕质量范围: {M_min:.0e} - {M_max:.0e} Msun")
print(f"  N.E.A. 质量门槛: M > {M_threshold:.0e} Msun")
print()
print(f"  ΛCDM 总子晕数: {total_LCDM:.1f}")
print(f"  N.E.A. 子晕数: {total_nea:.1f}")
print(f"  比例: {total_nea/total_LCDM*100:.1f}%")
print()
print(f"  观测：银河系卫星星系 ~ 50 个")
print(f"  N.E.A. 预言: {total_nea:.0f} 个")
print(f"  偏差: {abs(total_nea-50)/50*100:.1f}%")
print()
print("  物理意义：")
print("    ΛCDM 预言大量低质量子晕，但它们不形成可见星系")
print("    通常需要重子反馈机制来抑制")
print("    N.E.A.：低质量子晕（M < 1e7 Msun）不发生维度坍缩")
print("    因此天然缺少可观测卫星星系，无需反馈机制")