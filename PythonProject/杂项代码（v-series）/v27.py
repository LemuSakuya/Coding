# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

# ********** Begin *********#
# 1. 读取指定路径的CSV数据
df = pd.read_csv('step1/drinks.csv')

# 2. 自定义聚合函数：计算最大值与最小值的差
def max_min_diff(series):
	return series.max() - series.min()

# 3. 按continent分组，指定不同列的聚合规则
# 红酒列用自定义函数求极值差，啤酒列求和
agg_result = df.groupby('continent').agg({
	'wine_servings': max_min_diff,
	'beer_servings': 'sum'
})


# ********** End **********#
# 输出最终结果
print(agg_result)