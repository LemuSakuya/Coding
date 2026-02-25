import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm # 导入tqdm用于显示进度条

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

def bootstrap_km_confidence_interval(excel_filepath, threshold=0.04, n_iterations=500, alpha=0.05):
    # 设置和加载数据
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    print("步骤1: 正在加载和预处理数据...")
    
    try:
        df = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        print(f"错误: 加载Excel文件失败。错误信息: {e}")
        return

    df.columns = df.columns.str.strip()
    df['检测孕周(周)'] = df['检测孕周'].apply(parse_preg_week)
    
    target_cols = ['检测孕周(周)', 'Y染色体浓度']
    analysis_df = df[target_cols].copy().dropna().reset_index(drop=True)
    
    analysis_df['T'] = analysis_df['检测孕周(周)']
    analysis_df['E'] = (analysis_df['Y染色体浓度'] < threshold).astype(int)
    print(f"数据准备完成，共 {len(analysis_df)} 条有效记录。")

    # 在原始数据上拟合KM模型
    kmf_original = KaplanMeierFitter()
    kmf_original.fit(analysis_df['T'], analysis_df['E'], label='Kaplan-Meier (原始数据)')
 
    # 定义一个统一的时间轴，用于评估所有曲线
    timeline = np.linspace(analysis_df['T'].min(), analysis_df['T'].max(), 100)
    bootstrap_survival_curves = []

    for i in tqdm(range(n_iterations)):
        # 创建自助样本
        bootstrap_sample = analysis_df.sample(n=len(analysis_df), replace=True).reset_index(drop=True)
        
        # 在自助样本上拟合KM模型
        kmf_boot = KaplanMeierFitter()
        kmf_boot.fit(bootstrap_sample['T'], bootstrap_sample['E'])
        
        # 在统一时间轴上预测生存概率并存储
        curve = kmf_boot.survival_function_at_times(timeline)
        bootstrap_survival_curves.append(curve)
        
    print("自助法循环完成。")
    # 将所有曲线合并成一个DataFrame，每一列是一条曲线
    all_curves_df = pd.concat(bootstrap_survival_curves, axis=1)

    # 计算置信区间
    lower_p = (alpha / 2.0) * 100
    upper_p = (1 - alpha / 2.0) * 100
    
    # 对每一行（即每个时间点）计算百分位数
    lower_bound = all_curves_df.quantile(lower_p / 100, axis=1)
    upper_bound = all_curves_df.quantile(upper_p / 100, axis=1)
    print("置信区间计算完成。")

    # 可视化结果
    plt.figure(figsize=(12, 8))
    
    # 绘制原始的KM曲线
    kmf_original.plot_survival_function()
    
    # 绘制自助法计算出的置信区间（阴影区域）
    plt.fill_between(timeline, lower_bound, upper_bound, alpha=0.2, color='orange', label='95% 自助法置信区间')
    
    plt.title('Kaplan-Meier 生存曲线及其95%自助法置信区间', fontsize=16)
    plt.xlabel('检测孕周 (周)', fontsize=12)
    plt.ylabel(f'生存概率 (Y染色体浓度 >= {threshold*100}%)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    bootstrap_km_confidence_interval(excel_filepath, n_iterations=500)
