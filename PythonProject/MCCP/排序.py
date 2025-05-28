#排序.py
import pandas as pd

df = pd.read_excel('专家ICC分析_逐个计算2.xlsx', sheet_name='ICC结果')

df['专家'] = df['专家'].astype(str)

df_sorted = df.sort_values(by='专家', key=lambda x: x.str.extract('(\d+)')[0].astype(int))

df_sorted = df_sorted.reset_index(drop=True)

print(df_sorted)

df_sorted.to_excel('ICC_colum2.xlsx', index=False)