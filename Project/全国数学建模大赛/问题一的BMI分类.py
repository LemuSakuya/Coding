import pandas as pd
import numpy as np

def find_quartiles_from_excel(excel_filepath):
    # 加载数据
    try:
        df = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        return

    # 清理列名中的空格
    df.columns = df.columns.str.strip()
    
    # 确保 '孕妇BMI' 列是数值类型，并移除空值
    if '孕妇BMI' not in df.columns:
        print("错误: 数据中未找到 '孕妇BMI' 列。")
        return
        
    bmi_series = pd.to_numeric(df['孕妇BMI'], errors='coerce').dropna()
    
    q1 = bmi_series.quantile(0.25)
    q2 = bmi_series.quantile(0.50) # 中位数
    q3 = bmi_series.quantile(0.75)
    
    print(f"第一四分位数 (Q1, 25%): {q1:.4f}")
    print(f"第二四分位数 (Q2, 50% - 中位数): {q2:.4f}")
    print(f"第三四分位数 (Q3, 75%): {q3:.4f}")
    
    # 也可以一次性计算多个
    quartiles = bmi_series.quantile([0.25, 0.5, 0.75])
    print("\n一次性计算结果:")
    print(quartiles)

if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    find_quartiles_from_excel(excel_filepath)