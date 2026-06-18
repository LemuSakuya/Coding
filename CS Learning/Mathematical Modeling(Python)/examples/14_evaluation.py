import numpy as np

def minmax_positive(X):
    X = np.asarray(X, dtype=float)
    return (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0) + 1e-12)

def entropy_weight(X):
    Z = minmax_positive(X) + 1e-12
    P = Z / Z.sum(axis=0, keepdims=True)
    n = X.shape[0]
    E = -(P * np.log(P)).sum(axis=0) / np.log(n)
    D = 1 - E
    return D / D.sum()

def topsis(X, weights=None):
    Z = minmax_positive(X)
    norm = Z / (np.sqrt((Z ** 2).sum(axis=0, keepdims=True)) + 1e-12)
    if weights is None:
        weights = entropy_weight(X)
    V = norm * weights
    best = V.max(axis=0)
    worst = V.min(axis=0)
    d_pos = np.sqrt(((V - best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((V - worst) ** 2).sum(axis=1))
    score = d_neg / (d_pos + d_neg + 1e-12)
    return score, np.argsort(-score)

if __name__ == "__main__":
    X = np.array([[80, 70, 90], [90, 65, 85], [75, 95, 80], [88, 82, 78]], dtype=float)
    print("weights:", entropy_weight(X))
    print("topsis:", topsis(X))
