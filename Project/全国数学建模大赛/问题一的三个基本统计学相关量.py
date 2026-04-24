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

def visualize_and_analyze_male_data(excel_filepath):
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.rcParams['axes.unicode_minus'] = False 

    # 加载数据
    try:
        df = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        return
    
    # 清理列名中的空格
    df.columns = df.columns.str.strip()

    # 定义研究所需的列
    required_cols = ['孕妇BMI', '检测孕周', 'Y染色体浓度']
    
    # 检查所需列是否存在
    if not all(col in df.columns for col in required_cols):
        print(f"错误: 数据中缺少必要的列。请确保包含以下列: {required_cols}")
        return

    # 转换孕周格式
    df['检测孕周(周)'] = df['检测孕周'].apply(parse_preg_week)
    print("  - '检测孕周' 已转换为数值型 '检测孕周(周)'。")

    # 筛选出用于可视化的列，并确保它们是数值类型
    plot_df = df[['孕妇BMI', '检测孕周(周)', 'Y染色体浓度']].copy()
    for col in plot_df.columns:
        plot_df[col] = pd.to_numeric(plot_df[col], errors='coerce')
    
    # 删除包含空值的行，确保绘图数据是干净的
    initial_rows = len(plot_df)
    plot_df.dropna(inplace=True)
    rows_dropped = initial_rows - len(plot_df)
    print(f"  - 已删除 {rows_dropped} 行在关键列（BMI, 孕周, Y浓度）中存在缺失值的记录。")
    print(f"  - 清理后剩余 {len(plot_df)} 条有效数据用于统计。")

    if plot_df.empty:
        print("错误: 清理后没有足够的数据进行统计。")
        return

    # 使用 describe() 获取大部分统计数据
    desc_stats = plot_df.describe()

    # 计算方差并添加到结果中
    variance = plot_df.var()
    desc_stats.loc['方差'] = variance

    # 计算众数并添加到结果中 (mode() 可能返回多个值，这里只取第一个)
    mode = plot_df.mode().iloc[0]
    desc_stats.loc['众数'] = mode
    
    # 调整列名以便更好地展示
    desc_stats = desc_stats.rename(index={
        'count': '样本数',
        'mean': '平均数',
        'std': '标准差',
        'min': '最小值',
        '25%': '25%分位数',
        '50%': '中位数(50%)',
        '75%': '75%分位数',
        'max': '最大值'
    })

    print("统计计算完成。结果如下：\n")
    print(desc_stats.transpose())


if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    visualize_and_analyze_male_data(excel_filepath)

