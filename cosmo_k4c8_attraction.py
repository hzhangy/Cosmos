#!/usr/bin/env python3
"""
cosmos_k4c8_attraction.py

K4-C8 嵌合的拓扑关系。

关键事实：
  - C8 的 8 个顶点分为红（偶数）和蓝（奇数）
  - 红 K4 的 6 条边 = C8 的对角线（不在 C8 中）
  - 蓝 K4 的 6 条边 = C8 的对角线
  - C8 的 12 条边 = 红-蓝之间的连接
  - K4 嵌合后，K4 的边（对角线）成为"锁定"通道
  - C8 的边成为"发射"通道（光子从这发射）

两个 K4-C8 复合体靠近 → 共享 C8 边
"""

import numpy as np

Delta = 1 - np.sqrt(3)/2
eps2 = 1/100

def c8_vertices(origin):
    return [(origin[0]+i, origin[1]+j, origin[2]+k)
            for i in (0,1) for j in (0,1) for k in (0,1)]

def red_k4(origin):
    return [v for v in c8_vertices(origin) if sum(v) % 2 == 0]

def blue_k4(origin):
    return [v for v in c8_vertices(origin) if sum(v) % 2 == 1]

def c8_edges(origin):
    """C8 的 12 条边（红-蓝连接）"""
    verts = c8_vertices(origin)
    edges = []
    for v1 in verts:
        for v2 in verts:
            if v1 < v2 and sum((a-b)**2 for a,b in zip(v1,v2)) == 1:
                edges.append(frozenset([v1, v2]))
    return set(edges)

def k4_edges(origin, color='red'):
    """K4 的 6 条边（C8 的对角线）"""
    verts = red_k4(origin) if color == 'red' else blue_k4(origin)
    edges = []
    for v1 in verts:
        for v2 in verts:
            if v1 < v2:
                d = sum((a-b)**2 for a,b in zip(v1,v2))
                if d == 2:  # 对角线（差2）
                    edges.append(frozenset([v1, v2]))
    return set(edges)

print("=" * 70)
print("  K4-C8 嵌合的拓扑")
print("=" * 70)
print()

# 验证
origin = (0,0,0)
c8_e = c8_edges(origin)
red_e = k4_edges(origin, 'red')
blue_e = k4_edges(origin, 'blue')

print(f"  C8 边数：{len(c8_e)}")
print(f"  红 K4 边数：{len(red_e)}")
print(f"  蓝 K4 边数：{len(blue_e)}")
print(f"  C8 边 = 红-蓝连接：{len(c8_e - red_e - blue_e)} 条")
print()

# 验证 K4 边和 C8 边不重叠
print(f"  红 K4 边是否在 C8 中：{len(red_e & c8_e)} 条")
print(f"  蓝 K4 边是否在 C8 中：{len(blue_e & c8_e)} 条")
print()

# 两个复合体靠近，C8 边共享
print("=" * 70)
print("  两个 K4-C8 复合体靠近：C8 边共享")
print("=" * 70)
print()

print(f"{'r':>3} | {'共享 C8 边':>12} | {'总 C8 边':>12} | {'共享比例':>12}")
print("-" * 55)

for r in range(0, 4):
    A = c8_edges((0,0,0))
    B = c8_edges((r,0,0))
    shared = A & B
    total = A | B
    ratio = len(shared) / len(total) if total else 0
    print(f"{r:>3} | {len(shared):>12} | {len(total):>12} | {ratio:>12.4f}")

print()
print("物理：")
print("  - r=0（重合）：12 条完全共享")
print("  - r=1（相邻）：共享 4 条（共享面）")
print("  - r≥2：不共享边")
print()
print("  共享的 C8 边 → 光子从共享边发出 → 带宽分摊")
print("  共享越多，系统总带宽越低 → 吸引")
print()

# 能量估算
print("=" * 70)
print("  系统总带宽 vs 距离")
print("=" * 70)
print()

# 每个 C8 单元有 12 条边
# 每条边的带宽 = 1/12（假设均分）
# 两个复合体总边数（去重后）
bandwidth_per_edge = 1 / 12

print(f"{'r':>3} | {'总边数':>8} | {'总带宽':>12} | {'ΔE':>12}")
print("-" * 50)

baseline = None
for r in range(1, 5):
    A = c8_edges((0,0,0))
    B = c8_edges((r,0,0))
    total_edges = len(A | B)
    total_bw = total_edges * bandwidth_per_edge
    if baseline is None:
        baseline = total_bw
    delta = total_bw - baseline
    print(f"{r:>3} | {total_edges:>8} | {total_bw:>12.4f} | {delta:>+12.4f}")

print()
print("结论：")
print("  r=0（重合）：12 条边，完全共享")
print("  r=1（相邻）：20 条边，共享 4 条")
print("  r≥2：24 条边，不共享")
print()
print("  边数对比：r=1 比 r≥2 少 4 条边 → 相邻更优")
print("  但 r=0 边数更少。仅凭边数无法判定最低能量态，")
print("  需要完整的带宽分配计算。")
print()
print("  物理上 r=0 不成立（K4 重合会触发视界冻结）")
print("  → r=1 是最近的稳定距离")