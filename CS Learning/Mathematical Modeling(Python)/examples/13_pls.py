import numpy as np
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import cross_val_score, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def pls_demo():
    rng = np.random.default_rng(42)
    latent = rng.normal(size=(80, 2))
    X = latent @ np.array([[1, 0.8, 0.6, 0.2, 0.1],
                           [0.1, 0.3, 0.5, 0.8, 1.0]]) + rng.normal(0, 0.05, (80, 5))
    y = latent @ np.array([2.0, -1.0]) + rng.normal(0, 0.1, 80)
    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("pls", PLSRegression(n_components=2)),
    ])
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    score = cross_val_score(pipe, X, y, cv=cv, scoring="neg_root_mean_squared_error")
    pipe.fit(X, y)
    return -score.mean(), pipe.named_steps["pls"].coef_.ravel()

if __name__ == "__main__":
    print("PLS:", pls_demo())
