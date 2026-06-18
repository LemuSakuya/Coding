import numpy as np

def moving_average(y, window=3):
    y = np.asarray(y, dtype=float)
    return np.array([y[i-window:i].mean() for i in range(window, len(y) + 1)])

def simple_exp_smoothing(y, alpha=0.4):
    y = np.asarray(y, dtype=float)
    s = [y[0]]
    for t in range(1, len(y)):
        s.append(alpha * y[t] + (1 - alpha) * s[-1])
    return np.array(s)

def gm11_forecast(x0, steps=3):
    x0 = np.asarray(x0, dtype=float)
    x1 = np.cumsum(x0)
    z1 = 0.5 * (x1[1:] + x1[:-1])
    B = np.column_stack([-z1, np.ones(len(z1))])
    Y = x0[1:]
    a, b = np.linalg.lstsq(B, Y, rcond=None)[0]

    def x1_hat(k):
        return (x0[0] - b / a) * np.exp(-a * k) + b / a

    total = len(x0) + steps
    x1_pred = np.array([x1_hat(k) for k in range(total)])
    x0_pred = np.r_[x0[0], np.diff(x1_pred)]
    return x0_pred

def mape(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-12)))

if __name__ == "__main__":
    y = np.array([10, 12, 13, 15, 18, 20, 23, 25], dtype=float)
    print("MA:", moving_average(y))
    print("SES:", simple_exp_smoothing(y))
    print("GM11:", gm11_forecast(y, steps=2))
