import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

# 加载数据集
iris = datasets.load_iris()
X = iris.data
y = iris.target
target_names = iris.target_names
feature_names = iris.feature_names

# K-Means聚类
kmeans = KMeans(n_clusters=3, random_state=42)
y_pred = kmeans.fit_predict(X)
centers = kmeans.cluster_centers_

# 可视化真实标签
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis')
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')
plt.title('True Labels')
plt.colorbar(ticks=[0, 1, 2], label='Class')

# 可视化聚类结果
plt.subplot(1, 2, 2)
plt.scatter(X[:, 0], X[:, 1], c=y_pred, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='X', s=200, alpha=0.8)
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')
plt.title('K-Means Clustering')
plt.colorbar(ticks=[0, 1, 2], label='Cluster')
plt.tight_layout()
plt.show()

# 评估指标
ari = adjusted_rand_score(y, y_pred)
nmi = normalized_mutual_info_score(y, y_pred)
conf_mat = confusion_matrix(y, y_pred)

print(f"调整兰德指数(ARI): {ari:.3f}")
print(f"标准化互信息(NMI): {nmi:.3f}")
print("\n混淆矩阵:\n", conf_mat)
print("\n分类报告:")
print(classification_report(y, y_pred, target_names=target_names))