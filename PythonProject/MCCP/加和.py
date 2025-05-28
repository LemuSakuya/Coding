import pandas as pd

file_path = 'Check2_oversave.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1', header=0)

df.columns = df.columns.astype(str)

print("所有列名:", df.columns.tolist())

teacher_id_col = [col for col in df.columns if '教师' in col]
if not teacher_id_col:
    print("错误：找不到教师编号列")
    exit()
teacher_id_col = teacher_id_col[0]

expert_columns = [col for col in df.columns if '专家' in col]
if not expert_columns:
    expert_columns = [col for col in df.columns if any(char.isdigit() for char in col) and len(col) <= 4]
    
print("识别到的专家列:", expert_columns)

teacher_expert_scores = df.groupby(teacher_id_col)[expert_columns].sum()

print("\n每个专家对每个教师的总评分：")
print(teacher_expert_scores)

teacher_expert_scores.to_excel('评分总和2.xlsx')