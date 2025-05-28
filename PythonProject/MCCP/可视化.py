import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns  # 添加这行导入语句
from matplotlib.colors import LinearSegmentedColormap

# 1. 数据加载
icc_df = pd.read_excel('ICC_colum1.xlsx')
print("原始ICC数据：")
print(icc_df.to_string(index=False))

# 2. 数据增强（扩大可视化差异）
def enhance_icc_difference(icc_series, scale=2):
    """通过Sigmoid函数扩大中等ICC区域的差异"""
    return 1 / (1 + np.exp(-scale*(icc_series - 0.5)))

icc_df['ICC_enhanced'] = enhance_icc_difference(icc_df['ICC值'])
icc_df = icc_df.sort_values('ICC值', ascending=False)

# 3. 高级可视化设置
plt.style.use('seaborn')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False

# 4. 差异对比条形图（核心可视化）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# 左图：原始ICC值
colors = ['#E74C3C' if x < 0.5 else ('#F39C12' if x < 0.6 else '#2ECC71') for x in icc_df['ICC值']]
bars1 = ax1.barh(icc_df['专家'], icc_df['ICC值'], color=colors, edgecolor='black', height=0.7)
ax1.set_xlim(0.4, 0.65)  # 聚焦差异区域
ax1.axvline(0.5, color='#8E44AD', linestyle='--', linewidth=1.5, alpha=0.7)
ax1.axvline(0.6, color='#3498DB', linestyle='--', linewidth=1.5, alpha=0.7)
ax1.set_title('原始ICC值对比\n(红<0.5, 黄0.5-0.6, 绿>0.6)', pad=20, fontsize=14)
ax1.bar_label(bars1, fmt='%.3f', padding=5, fontsize=10)

# 右图：增强后ICC值
enhanced_colors = ['#E74C3C' if x < 0.5 else ('#F39C12' if x < 0.6 else '#2ECC71') for x in icc_df['ICC_enhanced']]
bars2 = ax2.barh(icc_df['专家'], icc_df['ICC_enhanced'], color=enhanced_colors, edgecolor='black', height=0.7)
ax2.set_xlim(0.4, 0.9)
ax2.axvline(0.5, color='#8E44AD', linestyle='--', linewidth=1.5, alpha=0.7)
ax2.axvline(0.6, color='#3498DB', linestyle='--', linewidth=1.5, alpha=0.7)
ax2.set_title('增强后ICC值对比\n(非线性缩放差异)', pad=20, fontsize=14)
ax2.bar_label(bars2, fmt='%.3f', padding=5, fontsize=10)

plt.tight_layout()

# 5. 热力图展示专家排名差异
plt.figure(figsize=(10, 6))
rank_df = icc_df[['专家', 'ICC值']].copy()
rank_df['原始排名'] = range(1, len(rank_df)+1)
rank_df = rank_df.sort_values('ICC_enhanced', ascending=False)
rank_df['增强排名'] = range(1, len(rank_df)+1)
rank_diff = rank_df.set_index('专家')

cmap = LinearSegmentedColormap.from_list('rank_diff', ['#2ECC71', '#F1C40F', '#E74C3C'])
sns.heatmap(rank_diff[['原始排名', '增强排名']], 
            annot=True, fmt="d",
            cmap=cmap,
            cbar_kws={'label': '排名变化'},
            linewidths=0.5)
plt.title('专家ICC排名变化对比', pad=20)
plt.xticks(rotation=0)
plt.tight_layout()

# 6. 输出统计摘要
print("\nICC值统计分析：")
print(f"均值: {icc_df['ICC值'].mean():.4f} ± {icc_df['ICC值'].std():.4f}")
print(f"中位数: {icc_df['ICC值'].median():.4f}")
print(f"极差: {icc_df['ICC值'].max() - icc_df['ICC值'].min():.4f}")
print("\n一致性等级分布：")
print(pd.cut(icc_df['ICC值'], 
             bins=[0, 0.4, 0.6, 0.8, 1],
             labels=['差', '中等', '良好', '优秀']).value_counts())

plt.show()