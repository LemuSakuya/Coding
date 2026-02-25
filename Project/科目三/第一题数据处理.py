import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer  # 从正确的模块导入
from scipy import stats
import matplotlib.font_manager as fm

font_path = 'path/to/SimHei.ttf'
font = fm.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

# ==================== 数据加载与清洗 ====================
file_path = r"E:\VSCode\Coding\Project\科目三\附件2.xlsx"
df = pd.read_excel(file_path)

# 重命名列
df.columns = [
    '时间', 'GPS车速', 'X轴加速度', 'Y轴加速度', 'Z轴加速度', 
    '经度', '纬度', '发动机转速', '扭矩百分比', 
    '瞬时油耗', '油门踏板开度', '空燃比', '发动机负荷百分比', '进气流量'
]

# 清理时间列，去除多余的空格或尾部字符
df['时间'] = df['时间'].str.strip()  # 去除空格
df['时间'] = df['时间'].str.rstrip(".")  # 去除末尾的点号

# 验证时间列的格式
try:
    df['时间'] = pd.to_datetime(df['时间'], format='%Y/%m/%d %H:%M:%S.%f')
except ValueError as e:
    # 找出不符合格式的行
    invalid_rows = df[pd.to_datetime(df['时间'], format='%Y/%m/%d %H:%M:%S.%f', errors='coerce').isnull()]
    if not invalid_rows.empty:
        print("不符合格式的时间数据示例：")
        print(invalid_rows)
    raise e

# 计算合成加速度
df['合成加速度'] = np.sqrt(df['X轴加速度']**2 + df['Y轴加速度']**2 + df['Z轴加速度']**2)

# 异常值处理（3σ原则）
z_scores = np.abs(stats.zscore(df[['X轴加速度', 'Y轴加速度', 'Z轴加速度']]))
df = df[(z_scores < 3).all(axis=1)]

# ==================== 异常值与噪声点检测 ====================
# 检测瞬时油耗中的负值或极端值
df = df[df['瞬时油耗'] >= 0]

# 使用 Z-score 方法检测异常值
z_scores = np.abs(stats.zscore(df[['合成加速度', 'GPS车速', '瞬时油耗']]))
df = df[(z_scores < 3).all(axis=1)]

# ==================== 特征选择与标准化 ====================
# 选择特征：合成加速度、瞬时油耗
features = ['合成加速度', '瞬时油耗']
df['加速度标准差'] = df['合成加速度'].rolling(window=10, min_periods=1).std()

# 数据标准化
scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])

# 填充NaN值
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
df[features] = imputer.fit_transform(df[features])

# ==================== 使用K-means自动划分加速度区间 ====================
def dynamic_classification(df):
    X = df[features].values  # 使用选定的特征进行聚类
    kmeans = KMeans(n_clusters=3, random_state=42).fit(X)
    
    # 获取聚类中心的瞬时油耗平均值
    cluster_centers_oil = kmeans.cluster_centers_[:, -1]  # 最后一个特征是瞬时油耗
    cluster_order = np.argsort(cluster_centers_oil)
    
    labels = ['平稳型', '混合型', '激进型']
    df['驾驶模式'] = [labels[np.where(cluster_order==x)[0][0]] for x in kmeans.labels_]
    
    return df

df = dynamic_classification(df)

# ==================== 数据检查 ====================
print("\n=== 驾驶模式分布 ===")
print(df['驾驶模式'].value_counts())

print("\n=== 数据完整性检查 ===")
print("数据总行数:", len(df))
print("分类后的唯一驾驶模式:", df['驾驶模式'].unique())
print("是否存在未分类的样本:", (df['驾驶模式'].isnull().sum() > 0))

# ==================== 可视化 ====================
plt.figure(figsize=(14, 8))

# 1. XYZ轴加速度散点图
plt.subplot(2, 1, 1)
scatter_x = plt.scatter(df['时间'], df['X轴加速度'], s=10, c='red', alpha=0.7, label='X轴（前进/刹车）')
scatter_y = plt.scatter(df['时间'], df['Y轴加速度'], s=10, c='blue', alpha=0.7, label='Y轴（转向）')
scatter_z = plt.scatter(df['时间'], df['Z轴加速度'], s=10, c='green', alpha=0.7, label='Z轴（颠簸）')
plt.plot(df['时间'], df['合成加速度'], 'k-', linewidth=1, label='合成加速度')
plt.title('XYZ轴加速度时间序列', fontsize=14)
plt.ylabel('加速度 (m/s²)', fontsize=12)
plt.xticks(rotation=45)
plt.legend()

# 2. 驾驶模式与油耗关系
plt.subplot(2, 1, 2)
colors = ['green', 'orange', 'red']
for mode, color in zip(['平稳型', '混合型', '激进型'], colors):
    subset = df[df['驾驶模式'] == mode]
    plt.scatter(subset['时间'], subset['瞬时油耗'], s=15, c=color, label=mode)
plt.title('不同驾驶模式的瞬时油耗对比', fontsize=14)
plt.ylabel('瞬时油耗 (L/h)', fontsize=12)
plt.xlabel('时间', fontsize=12)
plt.xticks(rotation=45)
plt.legend()

plt.tight_layout()
plt.show()

# ==================== 油耗统计 ====================
print("\n=== 油耗统计 ===")
print(df.groupby('驾驶模式')['瞬时油耗'].describe())

# ==================== 保存处理后的数据 ====================
df.to_csv('cleaned_driving_data.csv', index=False)
