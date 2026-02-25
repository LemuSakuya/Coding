import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler

# 1. 数据加载
data = pd.read_csv('e:\\VSCode\\Coding\\Markdown\\机器学习笔记\\kmeans_data.csv', header=None)
data.columns = ['Feature1', 'Feature2']

# 2. 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data)

# 3. 确定最佳K值
range_n_clusters = range(2, 7)  # 增加K值范围到7
inertia = []
silhouette_scores = []

for n_clusters in range_n_clusters:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(X_scaled)
    inertia.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, cluster_labels))

# 4. 应用K-Means (选择K=4)
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_scaled)
data['Cluster'] = clusters
centers = scaler.inverse_transform(kmeans.cluster_centers_)

# 5. 评估指标
silhouette = silhouette_score(X_scaled, clusters)
calinski = calinski_harabasz_score(X_scaled, clusters)
davies = davies_bouldin_score(X_scaled, clusters)

# 6. 结果可视化
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.scatter(data['Feature1'], data['Feature2'], c=data['Cluster'], cmap='viridis', alpha=0.7)
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='X', s=200, alpha=0.8)
plt.title('K-Means Clustering Results')
plt.xlabel('Feature1 (Purchase Amount)')
plt.ylabel('Feature2 (Browse Time)')
plt.colorbar(label='Cluster')

# 7. 聚类命名与解释
cluster_names = {
    0: "Low Value Users (Low Frequency, Low Amount)",
    1: "High Value Users (High Frequency, High Amount)",
    2: "Potential Users (Medium Consumption)",
    3: "Moderate Users"
}
data['Cluster_Name'] = data['Cluster'].map(cluster_names)

plt.subplot(1, 2, 2)
for cluster, name in cluster_names.items():
    cluster_data = data[data['Cluster'] == cluster]
    plt.scatter(cluster_data['Feature1'], cluster_data['Feature2'], 
                label=name, alpha=0.7)
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='X', s=200, alpha=0.8)
plt.title('Cluster Explanation')
plt.xlabel('Feature1 (Purchase Amount)')
plt.ylabel('Feature2 (Browse Time)')
plt.legend()

plt.tight_layout()
plt.show()

# 8. 输出结果
print("=== Clustering Evaluation Metrics ===")
print(f"Silhouette Score: {silhouette:.3f} (Closer to 1 is better)")
print(f"Calinski-Harabasz Index: {calinski:.3f} (Higher is better)")
print(f"Davies-Bouldin Index: {davies:.3f} (Lower is better)")

print("\n=== Cluster Proportions ===")
print(data['Cluster_Name'].value_counts(normalize=True).apply(lambda x: f"{x*100:.1f}%"))

print("\n=== Cluster Centers (Original Scale) ===")
centers_df = pd.DataFrame(centers, columns=['Feature1', 'Feature2'])
centers_df['Cluster_Name'] = [cluster_names[i] for i in range(4)]
print(centers_df)
