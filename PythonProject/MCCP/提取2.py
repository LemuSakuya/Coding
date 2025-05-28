import pandas as pd

# 读取Excel文件
df = pd.read_excel('教师综合评分结果.xlsx')

# 提取教师ID为纯数字的行
numeric_teachers = df[df['教师ID'].astype(str).str.isdigit()].copy()

# 将综合评分乘以1/100
numeric_teachers['综合评分'] = numeric_teachers['综合评分'] / 100

# 重置索引并输出结果
numeric_teachers.reset_index(drop=True, inplace=True)
print(numeric_teachers.to_string(index=False))

# 将结果保存到新的Excel文件
numeric_teachers.to_excel('数字教师评分结果.xlsx', index=False)
print("结果已保存到 '数字教师评分结果.xlsx'")