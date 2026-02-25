from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y_true, y_pred)

rmse = np.sqrt(mean_squared_error(y_true, y_pred))


from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y_true, y_pred)

def logcosh(true, pred):
      return np.mean(np.log(np.cosh(pred - true)))

from sklearn.metrics import explained_variance_score
evs = explained_variance_score(y_true, y_pred)

from sklearn.linear_model import HuberRegressor
huber = HuberRegressor(epsilon=1.35).fit(X, y)  # epsilon为delta超参数

from sklearn.metrics import mean_squared_error
y_true = [3, -0.5, 2, 7]
y_pred = [2.5, 0.0, 2, 8]
mse = mean_squared_error(y_true, y_pred)  # MSE
rmse = mean_squared_error(y_true, y_pred, squared=False)  # RMSE

from sklearn.metrics import r2_score
r2 = r2_score(y_true, y_pred)

from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(y_true, y_pred)

from sklearn.metrics import median_absolute_error
medae = median_absolute_error(y_true, y_pred)

from sklearn.linear_model import HuberRegressor
huber = HuberRegressor(epsilon=1.35).fit(X, y)  # epsilon 控制对异常值的敏感度
y_pred = huber.predict(X_test)

from sklearn.metrics import mean_squared_error
def huber_loss(y_true, y_pred, delta=1.0):
    error = y_true - y_pred
    is_small_error = np.abs(error) <= delta
    squared_loss = 0.5 * (error ** 2)
    linear_loss = delta * (np.abs(error) - 0.5 * delta)
    return np.mean(np.where(is_small_error, squared_loss, linear_loss))
huber_loss_value = huber_loss(y_true, y_pred, delta=1.35)

from sklearn.linear_model import QuantileRegressor
# 预测中位数（τ=0.5）
quantile_reg = QuantileRegressor(quantile=0.5, alpha=0).fit(X, y)
y_pred = quantile_reg.predict(X_test)

def quantile_loss(y_true, y_pred, tau=0.5):
    error = y_true - y_pred
    return np.mean(np.maximum(tau * error, (tau - 1) * error))
q_loss = quantile_loss(y_true, y_pred, tau=0.5)

def logcosh_loss(y_true, y_pred):
    return np.mean(np.log(np.cosh(y_pred - y_true)))
logcosh = logcosh_loss(y_true, y_pred)



