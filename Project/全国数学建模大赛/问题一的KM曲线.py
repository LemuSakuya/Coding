import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 导入生存分析库
try:
    from lifelines import KaplanMeierFitter
except ImportError:
    exit()

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

def visualize_km_curves(excel_filepath, threshold=0.04):
    # 设置和加载数据
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    try:
        # 默认从文件的第一行读取列标题
        df_raw = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        print(f"错误: 加载Excel文件失败。错误信息: {e}")
        return

    df_raw.columns = df_raw.columns.str.strip()
    essential_cols = ['检测孕周', 'Y染色体浓度', '孕妇BMI']
    if not all(col in df_raw.columns for col in essential_cols):
        print(f"错误: 数据中缺少必要的列: {essential_cols}")
        return
    
    analysis_df = df_raw[essential_cols].copy()

    analysis_df['T'] = analysis_df['检测孕周'].apply(parse_preg_week)
    analysis_df['E'] = (analysis_df['Y染色体浓度'] < threshold).astype(int)

    analysis_df['T'] = pd.to_numeric(analysis_df['T'], errors='coerce')
    analysis_df['孕妇BMI'] = pd.to_numeric(analysis_df['孕妇BMI'], errors='coerce')

    initial_rows = len(analysis_df)
    analysis_df.dropna(subset=['T', 'E', '孕妇BMI'], inplace=True)
    rows_dropped = initial_rows - len(analysis_df)
    print(f"  - 清理了 {rows_dropped} 条包含无效或缺失值的记录。")
    
    # 根据您指定的百分位数进行分组
    quartiles = [30.208806, 31.811598, 33.926237]
    labels = ['Q1(最低25%)', 'Q2(25-50%)', 'Q3(50-75%)', 'Q4(最高25%)']
    analysis_df['BMI分组'] = pd.cut(analysis_df['孕妇BMI'], 
                                   bins=[-np.inf, quartiles[0], quartiles[1], quartiles[2], np.inf], 
                                   labels=labels, right=True)
    
    analysis_df.dropna(subset=['BMI分组'], inplace=True)
    print(f"数据准备完成，共 {len(analysis_df)} 条有效记录。")
    print("各组人数分布:")
    print(analysis_df['BMI分组'].value_counts().sort_index())

    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    
    # 为每个BMI分组拟合KM模型并绘图
    for group_name in sorted(analysis_df['BMI分组'].unique()):
        group_data = analysis_df[analysis_df['BMI分组'] == group_name]
        kmf = KaplanMeierFitter().fit(group_data['T'], group_data['E'], label=group_name)
        kmf.plot_survival_function(ax=ax, ci_show=True) 

    # 格式化图表
    ax.set_title('Kaplan-Meier生存曲线 (按四分位数BMI分组)', fontsize=16)
    ax.set_xlabel('检测孕周 (周)', fontsize=12)
    ax.set_ylabel(f'生存概率 (Y染色体浓度 >= {threshold*100}%)', fontsize=12)
    ax.legend(title="BMI 分组")
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()
    print("图表生成成功！")

if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    visualize_km_curves(excel_filepath)

