import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def parse_preg_week(week_str):
    try:
        if isinstance(week_str, str) and 'w+' in week_str:
            parts = week_str.split('w+')
            weeks = int(parts[0])
            days = int(parts[1])
            return round(weeks + days / 7.0, 2)
        return float(week_str)
    except (ValueError, TypeError, IndexError):
        return np.nan

def analyze_specific_correlations(excel_filepath):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 加载数据
    try:
        print(f"\n步骤2: 正在从 '{excel_filepath}' 加载 '男胎检测数据'...")
        df = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
        print("✅ 数据加载成功。")
    except Exception as e:
        print(f"错误: 加载Excel文件失败。请检查文件路径和工作表名称。错误信息: {e}")
        return

    # 数据预处理
    print("\n步骤3: 正在进行数据预处理...")
    df.columns = df.columns.str.strip()

    # 对特定列进行数值化转换
    df['检测孕周(周)'] = df['检测孕周'].apply(parse_preg_week)
    print("  - '检测孕周' 已转换为数值型。")

    # 定义并选取要分析的特定列
    target_cols = ['孕妇BMI', '检测孕周(周)', 'Y染色体浓度']
    
    # 检查所需列是否存在
    if not all(col in df.columns for col in target_cols):
        print(f"错误: 数据中缺少必要的列。请确保包含以下列: {target_cols}")
        return

    analysis_df = df[target_cols].copy()

    # 清理缺失值
    initial_rows = len(analysis_df)
    analysis_df.dropna(inplace=True)
    rows_dropped = initial_rows - len(analysis_df)
    print(f"  - 已删除 {rows_dropped} 行在目标列中存在缺失值的记录。")
    print(f"  - 清理后剩余 {len(analysis_df)} 条有效数据用于分析。")

    if analysis_df.empty:
        print("错误: 清理后没有足够的数据进行分析。")
        return

    # 使用 method='pearson' 明确指定计算皮尔逊相关系数
    correlation_matrix = analysis_df.corr(method='pearson')
    
    print(correlation_matrix)

    plt.figure(figsize=(8, 6))
    
    # 使用'coolwarm'色板，annot=True 在图中显示数值
    sns.heatmap(correlation_matrix, cmap='coolwarm', annot=True, fmt=".3f", linewidths=.5)
    
    plt.title('Y染色体浓度、检测孕周、孕妇BMI的相关性热力图', fontsize=16)
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    
    print("图表生成成功！即将显示...")
    plt.show()


if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    
    analyze_specific_correlations(excel_filepath)

