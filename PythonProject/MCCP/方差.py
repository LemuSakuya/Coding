import pandas as pd
import matplotlib.pyplot as plt

file_path = 'Sequential_teacher.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

expert_columns = [f'专家{i+10}号' for i in range(1, 11)]
expert_data = df[expert_columns]

variance_per_expert = expert_data.var()

print("Expert：")
print(variance_per_expert)

plt.figure(figsize=(10, 6))
variance_per_expert.plot(kind='bar', color='skyblue')
plt.title('every Variance in expert')
plt.xlabel('num')
plt.ylabel('Variance')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--')
plt.show()