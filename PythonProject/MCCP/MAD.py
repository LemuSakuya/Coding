import pandas as pd
import pingouin as pg
import numpy as np
from tqdm import tqdm
from openpyxl.styles import Font, Alignment, PatternFill 

df = pd.read_excel('Sequential_teacher2.xlsx', sheet_name='Sheet1')
df.set_index('教师编号', inplace=True)

from scipy.stats import median_abs_deviation
def detect_outliers(series, threshold=3):
    median = series.median()
    mad = median_abs_deviation(series, scale='normal')
    z_score = 0.6745 * (series - median) / mad
    return series[abs(z_score) > threshold]

# 对每位专家评分进行检查
for expert in df.columns[1:]:   
    outliers = detect_outliers(df[expert])
    print(f"{expert} 异常值：{outliers.tolist()}")