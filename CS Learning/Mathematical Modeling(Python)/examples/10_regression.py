import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression, RidgeCV
from sklearn.metrics import accuracy_score

def ols_demo():
    rng = np.random.default_rng(42)
    X = rng.normal(size=(120, 3))
    y = 1.5 + X @ np.array([2.0, -1.0, 0.5]) + rng.normal(0, 0.5, 120)
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    return model.params, model.rsquared, model.pvalues

def ridge_demo():
    rng = np.random.default_rng(7)
    X = rng.normal(size=(100, 5))
    y = X @ np.array([1, 1, 0, 0, 0.5]) + rng.normal(0, 0.3, 100)
    model = RidgeCV(alphas=[0.01, 0.1, 1, 10]).fit(X, y)
    return model.alpha_, model.coef_

def logistic_demo():
    rng = np.random.default_rng(11)
    X = rng.normal(size=(150, 2))
    y = (X[:, 0] - 0.8 * X[:, 1] + rng.normal(0, 0.5, 150) > 0).astype(int)
    clf = LogisticRegression().fit(X, y)
    pred = clf.predict(X)
    return clf.coef_, clf.intercept_, accuracy_score(y, pred)

if __name__ == "__main__":
    print("OLS:", ols_demo())
    print("Ridge:", ridge_demo())
    print("Logistic:", logistic_demo())
