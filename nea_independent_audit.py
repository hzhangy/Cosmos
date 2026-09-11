#!/usr/bin/env python3
"""
nea_independent_audit.py

C8 侧宇宙学参数的完全独立审计。
从拓扑基因出发，逐层验证，标注每层的独立性等级。

分层：
  L1: 拓扑基因
  L2: 动力学方程（K 论文 + S 论文一致性）
  L3: 核心恒等式
  L4: H0 和尺度
  L5: 红移和 CMB
  L6: BAO 和距离
  L7: S 论文重算审计
  Audit: 独立性总表

依赖：numpy
"""

import numpy as np
from math import sqrt, pi, log

# ============================================================
# 工具
# ============================================================
def header(t):
    print("\n" + "="*72)
    print(f"  {t}")
    print("="*72)

def sub(t):
    print(f"\n--- {t} ---")

def trapz(y, x):
    return np.sum((y[1:]+y[:-1])*(x[1:]-x[:-1]))/2.0

# 观测值
OBS = {
    'Omega_m': 0.3153,
    'Omega_L': 0.6847,
    'Omega_b_over_c': 0.18642,
    'z_dec': 1100.0,
    'T_CMB': 2.7255,
    'n_s': 0.9649,
    'l_1': 220.6,
    'H0_lo': 67.4,
    'H0_hi': 73.0,
    'r_d': 147.09,
    'sigma_8': 0.811,
}

# ============================================================
# L1: 拓扑基因
# ============================================================
header("L1: 拓扑基因（独立于 S 论文，定理级）")

Delta = 1 - sqrt(3)/2
U_EM = 0.4*pi
R = 1/(1+pi)
N_max = np.exp(10*sqrt(3))
f_geo = 1 + Delta/(4*pi)
U_weak = 10*sqrt(3)
m_e = 0.51099895
Z_mev = m_e/U_EM
t_Tick = 1.619e-21

print(f"  Δ         = {Delta:.15f}")
print(f"  U_EM      = {U_EM:.15f}")
print(f"  R         = {R:.15f}")
print(f"  N_max     = {N_max:.6e}")
print(f"  f_geo     = {f_geo:.15f}")
print(f"  U_weak    = {U_weak:.15f}")
print(f"  Z (MeV)   = {Z_mev:.9f}")
print(f"  t_Tick    = {t_Tick:.6e} s")

print(f"\n  自检:")
print(f"  1/Δ       = {1/Delta:.15f}  (应为 4+2√3 = {4+2*sqrt(3):.15f})")
print(f"  1/Δ - (4+2√3) = {abs(1/Delta - (4+2*sqrt(3))):.2e}")
print(f"  1/U_EM    = {1/U_EM:.15f}")

# ============================================================
# L2: 动力学方程
# ============================================================
header("L2: 动力学方程（K 论文 + S 论文一致性）")

sub("L2.1 从 f_ext(x) = 4/5 - x/100 出发")
f0 = 4/5
slope = 1/100
print(f"  f_ext(0)  = {f0}")
print(f"  slope     = -{slope}")
print(f"  注: 4/5 来自体对角线/圈空间（拓扑计数）")
print(f"      1/100 来自 Stride-10 平方（启发式）")

sub("L2.2 解耦点")
f_dec = 1/U_EM
x_dec = 100*(f0 - f_dec)
print(f"  f_ext(x_dec) = {f_dec:.15f}")
print(f"  x_dec        = {x_dec:.15f}")

sub("L2.3 指数解 f_ext(t) = (4/5)e^(-t/100)")
t_dec = -100*log(f_dec/f0)
print(f"  t_dec        = {t_dec:.15f}")
print(f"  f_ext(t_dec) = {f0*np.exp(-t_dec/100):.15f}")
print(f"  解析-观测偏差 = {abs(f0*np.exp(-t_dec/100) - f_dec):.2e}")

sub("L2.4 RK4 数值积分验证")
def dfdt(f): return -f/100.0
def rk4(f_init, t_end, n=100000):
    f = f_init; dt = t_end/n
    for _ in range(n):
        k1 = dfdt(f)
        k2 = dfdt(f + 0.5*dt*k1)
        k3 = dfdt(f + 0.5*dt*k2)
        k4 = dfdt(f + dt*k3)
        f += (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
    return f

f_rk4 = rk4(f0, t_dec)
print(f"  RK4(t_dec)   = {f_rk4:.15f}")
print(f"  解析(t_dec)  = {f0*np.exp(-t_dec/100):.15f}")
print(f"  |RK4-解析|   = {abs(f_rk4 - f0*np.exp(-t_dec/100)):.2e}")

sub("L2.5 σ 的形式验证")
sigma_0 = f0/(100*Delta)
sigma_dec = f_dec/(100*Delta)
print(f"  σ(0)         = {sigma_0:.9f}")
print(f"  σ(t_dec)     = {sigma_dec:.9f}")
print(f"  σ 变化率     = {(sigma_0-sigma_dec)/sigma_0*100:.4f}%")

sub("L2.6 积分约束验证")
t_arr = np.linspace(0, t_dec, 200001)
f_arr = f0*np.exp(-t_arr/100.0)
sigma_arr = f_arr/(100*Delta)

integral_sigma = trapz(sigma_arr, t_arr)
integral_fext = trapz(f_arr, t_arr)
required_sigma = (f0 - f_dec)/Delta
analytic_integral_fext = 80*(1 - f_dec/f0)

print(f"  ∫f_ext dt (数值)      = {integral_fext:.15f}")
print(f"  ∫f_ext dt (解析)      = {analytic_integral_fext:.15f}")
print(f"  偏差                  = {abs(integral_fext-analytic_integral_fext):.2e}")
print(f"  ∫σ dt (数值)          = {integral_sigma:.15f}")
print(f"  (4/5 - 1/U_EM)/Δ      = {required_sigma:.15f}")
print(f"  相对偏差              = {abs(integral_sigma-required_sigma)/required_sigma:.2e}")
print(f"  解析 80(1-f_dec/f0)  = {80*(1 - f_dec/f0):.15f}")
print(f"  解析 100*f0*(1-exp)  = {100*f0*(1 - np.exp(-t_dec/100)):.15f}")

print(f"\n  独立性: 否（依赖 S 论文的 f_ext(x) = 4/5 - x/100 假设）")
print(f"  等级: K 论文方程（定理）+ S 论文输入（唯象）+ 一致性")

# ============================================================
# L3: 核心恒等式
# ============================================================
header("L3: 核心恒等式（独立于 S 论文，定理级）")

sub("L3.1 K 的两种表达")
K_direct = (1 - f_dec**2)/f_dec
K_formula = U_EM - 1/U_EM
print(f"  K = f_int²/f_ext  = {K_direct:.15f}")
print(f"  K = U_EM - 1/U_EM = {K_formula:.15f}")
print(f"  偏差              = {abs(K_direct-K_formula):.2e}")

sub("L3.2 Ω_m, Ω_Λ")
Omega_m = K_formula/(1+K_formula)
Omega_L = 1/(1+K_formula)
print(f"  Ω_m  = {Omega_m:.9f}   (观测 {OBS['Omega_m']}, 偏差 {abs(Omega_m-OBS['Omega_m'])/OBS['Omega_m']*100:.4f}%)")
print(f"  Ω_Λ  = {Omega_L:.9f}   (观测 {OBS['Omega_L']}, 偏差 {abs(Omega_L-OBS['Omega_L'])/OBS['Omega_L']*100:.4f}%)")
print(f"  Ω_m + Ω_Λ = {Omega_m+Omega_L:.15f}")

sub("L3.3 Ω_b/Ω_c")
ob_oc = Delta*(1+pi)/3
print(f"  Ω_b/Ω_c = Δ(1+π)/3 = {ob_oc:.9f}")
print(f"  观测              = {OBS['Omega_b_over_c']}")
print(f"  偏差              = {abs(ob_oc-OBS['Omega_b_over_c'])/OBS['Omega_b_over_c']*100:.4f}%")

sub("L3.4 Ω_b, Ω_c")
Omega_b = Omega_m/(1 + 1/ob_oc)
Omega_c = Omega_m/(1 + ob_oc)
print(f"  Ω_b = {Omega_b:.9f}")
print(f"  Ω_c = {Omega_c:.9f}")
print(f"  Ω_b + Ω_c = {Omega_b + Omega_c:.15f}   (应等于 Ω_m = {Omega_m:.15f})")

print(f"\n  独立性: 是（独立于 S 论文）")
print(f"  等级: K 是定理级（Lean 验证）；Ω_b/Ω_c 是强候选")

# ============================================================
# L4: H0 和尺度
# ============================================================
header("L4: H0 和尺度（独立于 S 论文，结构论证）")

sub("L4.1 H0 几何因子")
H0_factor = (19 - 4*sqrt(3))/20
H0_factor_alt = (3 + Delta**2)/5
print(f"  (19-4√3)/20 = {H0_factor:.15f}")
print(f"  (3+Δ²)/5    = {H0_factor_alt:.15f}")
print(f"  偏差        = {abs(H0_factor - H0_factor_alt):.2e}")

sub("L4.2 H0 数值")
alpha_G = R / N_max**5
H0_per_s = (1/t_Tick) * alpha_G * H0_factor
H0_kmsMpc = H0_per_s * 3.086e19
print(f"  α_G = R/N_max⁵ = {alpha_G:.6e}")
print(f"  H0 = (1/t_Tick)·α_G·因子 = {H0_per_s:.6e} /s")
print(f"  H0 = {H0_kmsMpc:.4f} km/s/Mpc")
print(f"  观测范围: [{OBS['H0_lo']}, {OBS['H0_hi']}] km/s/Mpc")

print(f"\n  独立性: 是（独立于 S 论文）")
print(f"  等级: 结构论证（环空间面积守恒）")

# ============================================================
# L5: 红移和 CMB
# ============================================================
header("L5: 红移和 CMB")

sub("L5.1 解耦红移（独立于 S 论文）")
ln_1pz = 1/Delta - K_formula
z_dec = np.exp(ln_1pz) - 1
print(f"  ln(1+z_dec) = 1/Δ - K = {ln_1pz:.15f}")
print(f"  z_dec       = {z_dec:.4f}")
print(f"  观测        = {OBS['z_dec']}")
print(f"  偏差        = {abs(z_dec-OBS['z_dec'])/OBS['z_dec']*100:.4f}%")

sub("L5.2 CMB 温度（含维度警告）")
T_ratio = U_EM/K_formula
print(f"  U_EM/K = {T_ratio:.9f}   （无量纲数）")
print(f"  观测 T_CMB = {OBS['T_CMB']} K   （有量纲）")
print(f"  数值: {T_ratio:.4f} vs {OBS['T_CMB']:.4f}")
print(f"  ⚠️ 维度不一致：无量纲数 vs 有量纲量，数值吻合不能算验证")
print(f"  真实公式来自 S 论文: T_CMB = Z/(N_max·3·U_weak·k_B)")

sub("L5.3 谱指数（依赖慢滚假设）")
x_gen_ratio = 2*sqrt(3)/pi
x_gen = x_dec * x_gen_ratio
f_ext_gen = f0 - x_gen/100
epsilon = 3*(x_gen/100)/f_ext_gen
n_s = 1 - 2*epsilon
print(f"  投影锁定 = {x_gen_ratio:.9f}")
print(f"  x_gen    = {x_gen:.9f}")
print(f"  f_ext_gen = {f_ext_gen:.9f}")
print(f"  ε        = {epsilon:.9f}")
print(f"  n_s      = {n_s:.9f}")
print(f"  观测 n_s = {OBS['n_s']}, 偏差 {abs(n_s-OBS['n_s'])/OBS['n_s']*100:.4f}%")
print(f"  ⚠️ 依赖慢滚假设 ε = 3(x_gen/100)/f_ext_gen")

sub("L5.4 第一声学峰（依赖组合规则）")
l_1 = 480/(pi*log(2))
print(f"  ℓ_1 = 480/(π·ln2) = {l_1:.4f}")
print(f"  观测 ℓ_1 = {OBS['l_1']}, 偏差 {abs(l_1-OBS['l_1'])/OBS['l_1']*100:.4f}%")
print(f"  ⚠️ 因子 8×10×3×2 的组合规则未推导")

sub("L5.5 投影锁定分解（独立，定理级）")
proj_lock = 2*sqrt(3)/pi
proj_lock_decomp = sqrt(3) * (2/pi)
print(f"  2√3/π           = {proj_lock:.15f}")
print(f"  分解 √3 × 2/π   = {proj_lock_decomp:.15f}")
print(f"  偏差            = {abs(proj_lock-proj_lock_decomp):.2e}")

print(f"\n  独立性: z_dec 独立；T_CMB、n_s、ℓ_1 部分依赖")
print(f"  等级: z_dec 候选；T_CMB 维度问题；n_s 依赖慢滚；ℓ_1 组合规则待推")

# ============================================================
# L6: BAO 和距离
# ============================================================
header("L6: BAO 和距离（部分独立，依赖标准 ΛCDM 背景）")

c_kms = 299792.458

def H_LCDM(z, Om, OL, H0):
    return H0*np.sqrt(Om*(1+z)**3 + OL)

def D_M(z, Om, OL, H0, n=2000):
    z_arr = np.linspace(0, z, n+1)
    y = c_kms / H_LCDM(z_arr, Om, OL, H0)
    return trapz(y, z_arr)

def D_H(z, Om, OL, H0):
    return c_kms/H_LCDM(z, Om, OL, H0)

def D_V(z, Om, OL, H0):
    return (z * D_M(z, Om, OL, H0)**2 * D_H(z, Om, OL, H0))**(1/3)

sub("L6.1 BAO 距离比（用 N.E.A. 的 Ω_m, Ω_Λ）")
H0_use = H0_kmsMpc
r_d_S = 149.39   # N.E.A. value
print(f"  r_d = {r_d_S:.2f} Mpc (N.E.A.)")

bao_data = [
    (0.295, 'D_M', 7.93),
    (0.295, 'D_H', 24.80),
    (0.51,  'D_M', 12.58),
    (0.71,  'D_M', 17.14),
    (1.32,  'D_M', 27.79),
    (1.32,  'D_H', 13.82),
    (2.33,  'D_M', 39.71),
    (2.33,  'D_H', 8.52),
]
print(f"\n  {'z':>6} {'量':>6} {'观测':>10} {'N.E.A.':>12} {'偏差':>10}")
print("  " + "-"*50)
chi2 = 0
for z, q, obs in bao_data:
    if q == 'D_M':
        val = D_M(z, Omega_m, Omega_L, H0_use)/r_d_S
    else:
        val = D_H(z, Omega_m, Omega_L, H0_use)/r_d_S
    dev = (val-obs)/obs*100
    print(f"  {z:>6.3f} {q:>6} {obs:>10.2f} {val:>12.4f} {dev:>+9.3f}%")
    chi2 += (dev/100)**2
print(f"\n  χ² ≈ {chi2:.3f}")

sub("L6.2 高红移检验")
for z in [2.33, 2.36]:
    dm = D_M(z, Omega_m, Omega_L, H0_use)/r_d_S
    dh = D_H(z, Omega_m, Omega_L, H0_use)/r_d_S
    print(f"  z={z}: D_M/r_d={dm:.4f}, D_H/r_d={dh:.4f}")

print(f"\n  独立性: 部分（Ω_m,Ω_Λ 独立；r_d 继承 S 论文；H(z) 用标准 ΛCDM）")
print(f"  等级: 数值一致，但背景演化不是 N.E.A. 自己的")

# ============================================================
# L7: S 论文重算审计
# ============================================================
header("L7: S 论文重算审计")

print(f"\n  参数对比: 新公式 vs S 论文")
print(f"  {'参数':>16} {'新公式':>14} {'S 论文':>14} {'观测':>14} {'独立?':>8}")
print("  " + "-"*75)

rows = [
    ('Ω_m',     f"{Omega_m:.6f}",  "—",         f"{OBS['Omega_m']}",       "是"),
    ('Ω_Λ',     f"{Omega_L:.6f}",  "0.6771",    f"{OBS['Omega_L']}",       "是"),
    ('Ω_b/Ω_c', f"{ob_oc:.6f}",    "0.187361",  f"{OBS['Omega_b_over_c']}", "是"),
    ('H0 因子', f"{H0_factor:.6f}", "—",        "—",                       "是"),
    ('z_dec',   f"{z_dec:.2f}",    "—",         f"{OBS['z_dec']}",         "是"),
    ('T_CMB',   f"{T_ratio:.4f}",  "2.7287",    f"{OBS['T_CMB']}",         "否"),
    ('n_s',     f"{n_s:.6f}",      "0.964852",  f"{OBS['n_s']}",           "否"),
    ('ℓ_1',     f"{l_1:.4f}",      "220.43",    f"{OBS['l_1']}",           "否"),
    ('r_d',     "—",               "147.79",    f"{OBS['r_d']}",           "否"),
    ('σ_8',     "—",               "0.8094",    f"{OBS['sigma_8']}",       "否"),
]
for name, new, s_paper, obs, indep in rows:
    print(f"  {name:>16} {new:>14} {s_paper:>14} {obs:>14} {indep:>8}")

# ============================================================
# Audit: 独立性总表
# ============================================================
header("独立性总表")

print(f"\n  {'参数':>16} {'公式来源':>24} {'独立于 S':>12} {'等级':>16}")
print("  " + "-"*72)
audit = [
    ('Δ, U_EM, R',  'C8 几何',           '是',  '定理'),
    ('K',            '代数恒等式',         '是',  '定理 (Lean)'),
    ('Ω_m, Ω_Λ',    'K/(1+K), 1/(1+K)',  '是',  '定理'),
    ('Ω_b/Ω_c',     'Δ(1+π)/3',          '是',  '强候选'),
    ('H0 因子',     '环空间面积',          '是',  '结构论证'),
    ('z_dec',        '1/Δ - K',           '是',  '候选'),
    ('1/100',        'Stride-10 平方',    '是',  '启发式'),
    ('σ 形式',      '两方程一致性',        '否',  '一致性'),
    ('f_ext(x)',     'S 论文',            '否',  '唯象'),
    ('T_CMB',        'S 论文',            '否',  '维度问题'),
    ('n_s',          '慢滚假设',           '否',  '假设'),
    ('ℓ_1',          '组合规则',           '否',  '待推'),
    ('r_d',          'S 论文',            '否',  '继承'),
    ('σ_8',          'S 论文',            '否',  '继承'),
]
for name, src, indep, grade in audit:
    print(f"  {name:>16} {src:>24} {indep:>12} {grade:>16}")

print("\n" + "="*72)
print("  审计完成")
print("="*72)