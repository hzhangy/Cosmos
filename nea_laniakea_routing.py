#!/usr/bin/env python3
"""
N.E.A. Laniakea Cosmic Web Emergence via Suture Tension & Dimensional Collapse
===============================================================================
Simulates how matter self-organizes into the Cosmic Web (Laniakea) under the 
finite bandwidth constraint (B=1) and the dimensional collapse of gravity.

Ontology-First Baseline:
- C8 is strictly a virtual bookkeeping interface, NOT a physical lattice.
- Filaments emerge from "bandwidth routing" along 1/r topological string tension.
- Voids are "Protocol Vacuums" where causal links are severed due to bandwidth insolvency.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # 无GUI环境下保存图形
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

# ============================================================
# N.E.A. TOPOLOGICAL GENES & PARAMETERS
# ============================================================
np.random.seed(1337)
N_clusters = 60          # 原初密度涨落的团块数
nodes_per_cluster = 25   # 每个团块的物质节点数
N_nodes = N_clusters * nodes_per_cluster

# 维度坍缩的临界尺度 (对应 MOND 加速度阈值 a0 的宏观投影)
r_MOND = 6.0 

# ============================================================
# 1. GENERATE PRIMORDIAL MATTER DISTRIBUTION (K4 Defects)
# ============================================================
# 模拟原初量子涨落/因果图抖动带来的物质聚集
cluster_centers = np.random.uniform(-60, 60, size=(N_clusters, 3))
nodes = []
for center in cluster_centers:
    # 每个簇内的节点呈高斯分布，模拟局部的星系群
    cluster_nodes = np.random.normal(loc=center, scale=2.5, size=(nodes_per_cluster, 3))
    nodes.append(cluster_nodes)
nodes = np.vstack(nodes)

# ============================================================
# 2. N.E.A. SUTURE TENSION & DIMENSIONAL COLLAPSE IMPEDANCE
# ============================================================
def suture_impedance(vec):
    """
    计算两个物质节点间建立因果缝合线的带宽成本。
    
    物理机制：
    - 内区 (r < r_MOND): 3D 牛顿区。维持 3D 缝合的带宽成本随距离快速上升 (阻抗 ∝ r²)。
      这迫使物质在局部紧密成团（星系/星系团）。
    - 外区 (r >= r_MOND): 2D 壳层缝合区 (维度坍缩)。引力降维成 1/r 拓扑弦张力。
      长程连接的带宽成本被“摊薄” (阻抗 ∝ r)。这鼓励物质跨越巨大的空洞，
      形成跨越数百万秒差距的丝状结构 (Filaments)。
    """
    r = np.sqrt(np.sum(vec**2, axis=1)) + 1e-6
    
    # 内区：平方级阻抗 (极难维持长程 3D 连接)
    # 外区：线性阻抗 (维度坍缩带来的长程拓扑张力，相对“便宜”)
    cost = np.where(r < r_MOND, 
                    (r**2) / r_MOND,   # 内区：快速衰减的连通性
                    r)                 # 外区：维度坍缩鼓励长程寻径
    
    # 引入 Stride-10 寻址方差 (ε² = 1/100) 模拟原初离散抖动
    noise = 1.0 + np.random.normal(0, 0.03, size=r.shape)
    return cost * np.abs(noise)

# ============================================================
# 3. BUILD CAUSAL GRAPH & FIND MINIMUM SPANNING TREE (MST)
# ============================================================
# 寻找局部因果邻域 (每个节点只与最近的 k 个节点尝试建立缝合线)
tree = cKDTree(nodes)
distances, indices = tree.query(nodes, k=25) 

row_ind = []
col_ind = []
weights = []

for i in range(N_nodes):
    for j_idx in indices[i]:
        if i != j_idx:
            vec = nodes[j_idx] - nodes[i]
            cost = suture_impedance(vec[np.newaxis, :])[0]
            row_ind.append(i)
            col_ind.append(j_idx)
            weights.append(cost)

# 构建稀疏图
graph = csr_matrix((weights, (row_ind, col_ind)), shape=(N_nodes, N_nodes))

# 宇宙在 B=1 的严苛预算下，通过最小生成树 (MST) 优化其带宽路由
# 这就是“拉尼亚凯亚”骨架的涌现过程
mst = minimum_spanning_tree(graph)
mst_coo = mst.tocoo()

# ============================================================
# 4. PLOTTING THE COSMIC WEB (FIXED COLOR SCHEME)
# ============================================================
# 使用 Matplotlib 内置暗色风格，彻底解决黑白冲突
plt.style.use('dark_background')

fig = plt.figure(figsize=(14, 12), facecolor='black')
ax = fig.add_subplot(111, projection='3d', facecolor='black')

# 隐藏坐标轴与背景面板
ax.axis('off')
ax.xaxis.set_pane_color((0, 0, 0, 0))
ax.yaxis.set_pane_color((0, 0, 0, 0))
ax.zaxis.set_pane_color((0, 0, 0, 0))

deg_out = np.array(mst.sum(axis=1)).flatten()
deg_in = np.array(mst.sum(axis=0)).flatten()
degrees = deg_out + deg_in
norm_degrees = (degrees - degrees.min()) / (degrees.max() - degrees.min() + 1e-6)

# 1. 绘制缝合线 (深色背景下用亮青色/电光蓝，提亮透明度)
for i in range(len(mst_coo.row)):
    u = mst_coo.row[i]
    v = mst_coo.col[i]
    dist = np.linalg.norm(nodes[u] - nodes[v])
    # 距离近的骨架线更亮更实，跨空洞的长线稍淡
    alpha_val = np.clip(0.6 - (dist / 120), 0.15, 0.6)
    
    ax.plot(
        [nodes[u, 0], nodes[v, 0]],
        [nodes[u, 1], nodes[v, 1]],
        [nodes[u, 2], nodes[v, 2]],
        color='#00ffff', alpha=alpha_val, lw=0.8
    )

# 2. 绘制物质节点 (高亮显示超星系团)
sc = ax.scatter(
    nodes[:, 0], nodes[:, 1], nodes[:, 2],
    c=norm_degrees, cmap='autumn', # 用 autumn 或 hot (红到亮黄)，在黑底上对比极佳
    s=norm_degrees * 70 + 6,  
    alpha=0.9,
    edgecolors='none'
)

# 标题改为白色
ax.set_title(
    "N.E.A. Cosmic Web Emergence (Laniakea Simulation)\n"
    "Filaments via Minimum Spanning Suture on Clustered K4 Defects",
    fontsize=13, color='white', pad=10
)

cbar = plt.colorbar(sc, ax=ax, shrink=0.5, pad=0.05)
cbar.set_label("Cluster Density / Hub Degree", rotation=270, labelpad=20, color='white', fontsize=11)
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

plt.tight_layout()
output_file = "nea_laniakea_suture_routing_fixed.png"
plt.savefig(output_file, dpi=250, bbox_inches='tight', facecolor='black')
print(f"✓ 修复后的宇宙网已保存: {output_file}")
plt.close()