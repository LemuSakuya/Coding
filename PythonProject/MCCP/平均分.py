import pandas as pd

# 读取Excel文件
df = pd.read_excel('Sequential_teacher1.xlsx')

# 计算每位教师的平均分（跳过第一列"教师编号"）
df['平均分'] = df.iloc[:, 1:].apply(lambda row: row.mean(), axis=1)

# 只保留教师编号和平均分两列
result = df[['教师编号', '平均分']]

# 输出结果
print(result.to_string(index=False))

# 保存到新的Excel文件
result.to_excel('教师平均分结果.xlsx', index=False)
print("结果已保存到 '教师平均分结果.xlsx'")