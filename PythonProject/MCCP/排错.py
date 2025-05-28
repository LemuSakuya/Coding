#排错.py
import pandas as pd

file_path = 'All Data2.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1', header=0)

expert_columns = [col for col in df.columns if '专' in col and '号' in col]

for index, row in df.iterrows():
    if pd.notna(row['满分']):
        max_score = row['满分']
        over_scores = []
        
        for expert in expert_columns:
            if pd.notna(row[expert]):
                if row[expert] > max_score:
                    over_scores.append(f"{expert}: {row[expert]} (满分: {max_score})")
        
        if over_scores:
            print(f" {row['教师编号']} er:")
            for item in over_scores:
                print(item)
            print("-" * 30)

df['是否超标'] = df.apply(lambda row: any(row[expert] > row['满分'] for expert in expert_columns 
                         if pd.notna(row['满分']) and pd.notna(row[expert])), axis=1)

df.to_excel('Check2.xlsx', index=False)