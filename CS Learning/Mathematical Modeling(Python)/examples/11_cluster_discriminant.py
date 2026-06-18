import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.datasets import make_blobs
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import silhouette_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def clustering_demo():
    X, _ = make_blobs(n_samples=240, centers=3, cluster_std=0.8, random_state=42)
    Xs = StandardScaler().fit_transform(X)
    km = KMeans(n_clusters=3, random_state=42, n_init="auto").fit(Xs)
    score = silhouette_score(Xs, km.labels_)
    return km.cluster_centers_, score

def lda_demo():
    X, y = make_blobs(n_samples=180, centers=3, cluster_std=1.2, random_state=10)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)
    lda = LinearDiscriminantAnalysis().fit(X_train, y_train)
    pred = lda.predict(X_test)
    return lda.coef_, confusion_matrix(y_test, pred)

if __name__ == "__main__":
    print("cluster:", clustering_demo())
    print("lda:", lda_demo())
