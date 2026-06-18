import numpy as np
from scipy.interpolate import interp1d, CubicSpline
from scipy.optimize import curve_fit

def interpolation_demo():
    x = np.array([0, 1, 2, 3, 4], dtype=float)
    y = np.array([1.0, 2.0, 1.5, 3.2, 2.8])
    xs = np.linspace(0, 4, 50)
    linear = interp1d(x, y, kind="linear")
    spline = CubicSpline(x, y)
    return xs, linear(xs), spline(xs)

def nonlinear_fit_demo():
    rng = np.random.default_rng(42)
    x = np.linspace(0, 5, 40)
    y = 3.0 * np.exp(-0.7 * x) + 0.5 + rng.normal(0, 0.08, len(x))

    def model(x, a, b, c):
        return a * np.exp(-b * x) + c

    params, cov = curve_fit(model, x, y, p0=[2, 0.5, 0])
    return params, np.sqrt(np.diag(cov))

if __name__ == "__main__":
    print("interpolation arrays:", [arr.shape for arr in interpolation_demo()])
    print("fit params:", nonlinear_fit_demo())
