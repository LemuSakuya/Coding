import numpy as np
from scipy.optimize import linprog
from scipy.optimize import linear_sum_assignment

def production_plan():
    # maximize 40 x1 + 30 x2 -> minimize negative profit
    c = np.array([-40, -30], dtype=float)
    A = np.array([[2, 1], [1, 1], [1, 0]], dtype=float)
    b = np.array([100, 80, 40], dtype=float)
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method="highs")
    return res.x, -res.fun

def assignment_demo():
    cost = np.array([[9, 2, 7], [6, 4, 3], [5, 8, 1]], dtype=float)
    row, col = linear_sum_assignment(cost)
    return list(zip(row, col)), cost[row, col].sum()

if __name__ == "__main__":
    print("production:", production_plan())
    print("assignment:", assignment_demo())
