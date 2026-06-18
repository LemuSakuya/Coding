import numpy as np
from scipy.optimize import minimize

def constrained_nlp():
    def f(x):
        return (x[0] - 1) ** 2 + (x[1] - 2) ** 2

    constraints = [
        {"type": "ineq", "fun": lambda x: x[0] + x[1] - 2},
        {"type": "eq", "fun": lambda x: x[0] - x[1] + 1},
    ]
    res = minimize(f, x0=np.array([0.0, 0.0]), constraints=constraints, method="SLSQP")
    return res.x, res.fun, res.success

def weighted_multi_objective(weight=0.6):
    def f1(x):
        return (x[0] - 1) ** 2 + x[1] ** 2

    def f2(x):
        return x[0] ** 2 + (x[1] - 1) ** 2

    def objective(x):
        return weight * f1(x) + (1 - weight) * f2(x)

    res = minimize(objective, x0=np.array([0.5, 0.5]), method="BFGS")
    return res.x, res.fun

if __name__ == "__main__":
    print("constrained:", constrained_nlp())
    print("multi objective:", weighted_multi_objective())
