import pandas as pd

# 读取Excel文件
df = pd.read_excel('教师综合评分结果.xlsx')

# 提取教师ID为纯数字的行
numeric_teachers = df[df['教师ID'].astype(str).str.isdigit()].copy()

# 将教师ID转换为整数类型以便正确排序
numeric_teachers['教师ID'] = numeric_teachers['教师ID'].astype(int)

# 按教师ID升序排序
numeric_teachers_sorted = numeric_teachers.sort_values(by='教师ID', ascending=True)

# 重置索引并输出结果
numeric_teachers_sorted.reset_index(drop=True, inplace=True)
print(numeric_teachers_sorted.to_string(index=False))

# （可选）保存到新Excel文件
numeric_teachers_sorted.to_excel('数字教师评分结果_按ID升序.xlsx', index=False)
print("结果已保存到 '数字教师评分结果_按ID升序.xlsx'")