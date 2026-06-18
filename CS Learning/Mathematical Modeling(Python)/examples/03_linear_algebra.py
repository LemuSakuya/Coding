import numpy as np

def solve_linear_system():
    A = np.array([[3, 1, -1], [2, 4, 1], [-1, 2, 5]], dtype=float)
    b = np.array([4, 1, 1], dtype=float)
    x = np.linalg.solve(A, b)
    residual = np.linalg.norm(A @ x - b)
    return x, residual

def least_squares_demo():
    x = np.linspace(0, 10, 20)
    y = 2.5 * x + 1.2 + np.random.default_rng(42).normal(0, 1, len(x))
    A = np.column_stack([x, np.ones_like(x)])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    return beta

def markov_stationary_distribution():
    P = np.array([[0.7, 0.3, 0.0],
                  [0.2, 0.6, 0.2],
                  [0.1, 0.2, 0.7]])
    pi = np.array([1.0, 0.0, 0.0])
    for _ in range(100):
        pi = pi @ P
    return pi

if __name__ == "__main__":
    print("Ax=b:", solve_linear_system())
    print("least squares beta:", least_squares_demo())
    print("stationary distribution:", markov_stationary_distribution())
