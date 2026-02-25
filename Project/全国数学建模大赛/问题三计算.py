import pandas as pd
import io
import numpy as np

# 数据准备
data_string = """
孕妇BMI,Y染色体的Z值,X染色体浓度,被过滤掉读段数的比例,生产次数,样本数量
31.35,0.20,0.02,0.02,1.22,431.00
31.77,-0.40,0.09,0.02,0.14,464.00
37.28,0.57,0.03,0.02,0.29,251.00
31.03,0.23,0.00,0.02,0.00,538.00
"""

df = pd.read_csv(io.StringIO(data_string))

beta_0 =  2.1514       # 位置参数的基础值
beta_bmi = -0.0007       # BMI系数
beta_x_conc = 6.0951     # X染色体浓度系数
beta_filter_ratio = 15.9034  # 过滤读段比例系数
beta_prod_count = 0.0864 # 生产次数系数

sigma = 0.5882

logistic_median = 2.994

# Log-logistic模型计算
print("正在根据Log-logistic AFT模型计算NIPT检测时间点...")


def calculate_loglogistic_nipt(row, epsilon=0.0):
    linear_predictor = (
        beta_0 +
        beta_bmi * row['孕妇BMI'] +
        beta_x_conc * row['X染色体浓度'] +
        beta_filter_ratio * row['被过滤掉读段数的比例'] +
        beta_prod_count * row['生产次数']
    )
    return linear_predictor + sigma * epsilon

df['log(T)_中位数'] = df.apply(calculate_loglogistic_nipt, axis=1, epsilon=2.994)

# 计算预测的T值（检测时间，以天为单位）并转换为周数
df['预测检测时间T(天)'] = np.exp(df['log(T)_中位数'])
df['预测检测时间T(周)'] = df['预测检测时间T(天)'] / 7

# Log-logistic模型的分位数计算
def calculate_confidence_intervals(row):
    linear_predictor = (
        beta_0 +
        beta_bmi * row['孕妇BMI'] +
        beta_x_conc * row['X染色体浓度'] +
        beta_filter_ratio * row['被过滤掉读段数的比例'] +
        beta_prod_count * row['生产次数']
    )
    
    # Logistic分布的2.5%和97.5%分位数
    logistic_lower = -1.96  # 约对应2.5%分位数
    logistic_upper = 1.96   # 约对应97.5%分位数
    
    logT_lower = linear_predictor + sigma * logistic_lower
    logT_upper = linear_predictor + sigma * logistic_upper
    
    T_lower = np.exp(logT_lower) / 7  # 转换为周数
    T_upper = np.exp(logT_upper) / 7  # 转换为周数
    
    return T_lower, T_upper

# 计算置信区间
df[['95%CI下限(周)', '95%CI上限(周)']] = df.apply(
    lambda row: pd.Series(calculate_confidence_intervals(row)), axis=1
)

# 显示结果
result_columns = [
    '孕妇BMI', 'X染色体浓度', '被过滤掉读段数的比例', 
    '生产次数', 'log(T)_中位数', '预测检测时间T(周)',
    '95%CI下限(周)', '95%CI上限(周)'
]

print(df[result_columns].round({
    '孕妇BMI': 2,
    'X染色体浓度': 3,
    '被过滤掉读段数的比例': 3,
    '生产次数': 2,
    'log(T)_中位数': 4,
    '预测检测时间T(周)': 2,
    '95%CI下限(周)': 2,
    '95%CI上限(周)': 2
}).to_string(index=False))