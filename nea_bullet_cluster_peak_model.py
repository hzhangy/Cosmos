#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
N.E.A. 子弹星系团：维度坍缩晕跟随星系的分离模型（峰值版）
"""
import numpy as np

x = np.linspace(-500, 500, 1000)  # kpc

# 气体分布：中心单峰
sigma_gas = 100.0
gas = np.exp(-0.5 * (x / sigma_gas)**2)

# 星系+维度坍缩晕：两侧双峰
offset = 300.0
sigma_gal = 50.0
gal1 = np.exp(-0.5 * ((x - offset) / sigma_gal)**2)
gal2 = np.exp(-0.5 * ((x + offset) / sigma_gal)**2)
galaxies = gal1 + gal2

# 主峰位置
xray_peak = x[np.argmax(gas)]
lensing_peak1 = x[np.argmax(gal1)]
lensing_peak2 = x[np.argmax(gal2)]

print("="*80)
print("  N.E.A. 子弹星系团：维度坍缩晕跟随星系（峰值版）")
print("="*80)
print(f"  X射线气体主峰位置 = {xray_peak:.1f} kpc")
print(f"  引力透镜主峰位置 1 = {lensing_peak1:.1f} kpc")
print(f"  引力透镜主峰位置 2 = {lensing_peak2:.1f} kpc")
print()
print(f"  中心分离 ≈ {abs(lensing_peak1 - xray_peak):.1f} kpc")
print()
print("  结论：")
print("  若维度坍缩晕绑定在星系周围，碰撞时跟随星系穿过，")
print("  则引力透镜主峰与X射线气体主峰自然分离。")
print("  这与子弹星系团观测一致。")
print("="*80)