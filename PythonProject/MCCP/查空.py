#查空.py
import pandas as pd

file_path = 'All Data1.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1', header=0)

print(df.isnull().sum())
print("\n")

expert_columns = [col for col in df.columns if '专家' in col and '号' in col]
expert_null = df[expert_columns].isnull().sum()
print(expert_null[expert_null > 0])
print("\n")

key_columns = ['满分', '教师编号']
key_null = df[key_columns].isnull().sum()
print(key_null[key_null > 0])
print("\n")

null_positions = df[df.isnull().any(axis=1)]
if not null_positions.empty:
    for index, row in null_positions.iterrows():
        null_cols = row.index[row.isnull()].tolist()
        teacher = row['教师编号'] if pd.notna(row['教师编号']) else "无教师编号"
        print(f"第 {index+2} 行（教师 {teacher}）有以下空值列: {null_cols}")
else:
    print("没有发现空值数据")
print("\n")

null_stats = pd.DataFrame({
    '列名': df.columns,
    '空值数量': df.isnull().sum(),
    '空值比例': df.isnull().mean().round(4)
})
null_stats.to_excel('Empty_check2.xlsx', index=False)