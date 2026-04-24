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

def visualize_male_data(excel_filepath):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    try:
        df = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
        print("数据加载成功。")
    except Exception as e:
        print(f"错误: 加载Excel文件失败。请检查文件路径和工作表名称。错误信息: {e}")
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
    print(f"  - 清理后剩余 {len(plot_df)} 条有效数据用于绘图。")

    if plot_df.empty:
        print("错误: 清理后没有足够的数据进行绘图。")
        return
        
    # 新增: 为制作箱线图，对连续变量进行分组
    plot_df['BMI分组'] = pd.qcut(plot_df['孕妇BMI'], q=4, labels=['Q1(较低)', 'Q2', 'Q3', 'Q4(较高)'])
    plot_df['孕周分组'] = plot_df['检测孕周(周)'].astype(int)
    print("  - 已将'孕妇BMI'按四分位数分组，将'检测孕周'按整数周分组，用于制作箱线图。")

    # 创建一个1行2列的图表画布
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # 设置图表整体标题
    fig.suptitle('孕妇BMI及检测孕周分组下Y染色体浓度的分布', fontsize=16)

    # 第一个子图：孕妇BMI分组 vs Y染色体浓度
    sns.boxplot(ax=axes[0], data=plot_df, x='BMI分组', y='Y染色体浓度')
    axes[0].set_title('不同BMI分组下Y染色体浓度的分布')
    axes[0].set_xlabel('孕妇BMI (按四分位数分组)')
    axes[0].set_ylabel('Y染色体浓度')
    axes[0].grid(True, linestyle='--', alpha=0.6, axis='y')

    # 第二个子图：检测孕周分组 vs Y染色体浓度
    sns.boxplot(ax=axes[1], data=plot_df.sort_values('孕周分组'), x='孕周分组', y='Y染色体浓度')
    axes[1].set_title('不同检测孕周下Y染色体浓度的分布')
    axes[1].set_xlabel('检测孕周 (周)')
    axes[1].set_ylabel('Y染色体浓度')
    axes[1].grid(True, linestyle='--', alpha=0.6, axis='y')

    # 调整布局并显示图表
    plt.tight_layout(rect=[0, 0, 1, 0.95]) # 为总标题留出空间
    print("图表生成成功！即将显示...")
    plt.show()


if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    visualize_male_data(excel_filepath)