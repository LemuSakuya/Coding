import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 导入生存分析库
try:
    from lifelines import KaplanMeierFitter
    from lifelines.statistics import logrank_test
    from lifelines import CoxPHFitter
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

def perform_survival_analysis(excel_filepath, threshold=0.04):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    try:
        df = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        return

    df.columns = df.columns.str.strip()
    df['检测孕周(周)'] = df['检测孕周'].apply(parse_preg_week)
    
    target_cols = ['孕妇BMI', '检测孕周(周)', 'Y染色体浓度']
    analysis_df = df[target_cols].copy().dropna()
    print(f"  - 数据预处理完成，剩余 {len(analysis_df)} 条有效数据用于分析。")

    # 定义生存分析的“时间”和“事件”
    # T: 生存时间 (Duration) -> 检测孕周
    # E: 事件是否发生 (Event) -> Y染色体浓度是否低于阈值
    analysis_df['T'] = analysis_df['检测孕周(周)']
    analysis_df['E'] = (analysis_df['Y染色体浓度'] < threshold).astype(int)
    print(f"\n步骤3: 已定义事件（Y染色体浓度 < {threshold}）。")
    print(f"  - 数据集中共发生 {analysis_df['E'].sum()} 例事件。")

    # Kaplan-Meier 生存分析 (按BMI分组)
    median_bmi = analysis_df['孕妇BMI'].median()
    analysis_df['BMI分组'] = np.where(analysis_df['孕妇BMI'] >= median_bmi, '高BMI组', '低BMI组')
    print(f"  - 已将孕妇按BMI中位数 ({median_bmi:.2f}) 分为高、低两组。")

    # 绘制生存曲线
    kmf_high = KaplanMeierFitter()
    kmf_low = KaplanMeierFitter()

    ax = plt.subplot(111)
    
    high_bmi_group = (analysis_df['BMI分组'] == '高BMI组')
    low_bmi_group = (analysis_df['BMI分组'] == '低BMI组')

    kmf_high.fit(analysis_df['T'][high_bmi_group], event_observed=analysis_df['E'][high_bmi_group], label=f'高BMI组 (n={high_bmi_group.sum()})')
    kmf_high.plot_survival_function(ax=ax)

    kmf_low.fit(analysis_df['T'][low_bmi_group], event_observed=analysis_df['E'][low_bmi_group], label=f'低BMI组 (n={low_bmi_group.sum()})')
    kmf_low.plot_survival_function(ax=ax)
    
    plt.title('Kaplan-Meier 生存曲线 (按BMI分组)')
    plt.xlabel('检测孕周 (周)')
    plt.ylabel('生存概率 (Y染色体浓度 >= 4%)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

    # 执行对数秩检验 (Log-Rank Test)
    results = logrank_test(
        analysis_df['T'][high_bmi_group], 
        analysis_df['T'][low_bmi_group], 
        event_observed_A=analysis_df['E'][high_bmi_group], 
        event_observed_B=analysis_df['E'][low_bmi_group]
    )
    print("\n对数秩检验 (Log-Rank Test) 结果:")
    results.print_summary()
    if results.p_value < 0.05:
        print("结论: p值 < 0.05，高、低BMI组的生存曲线存在显著差异。")
    else:
        print("结论: p值 >= 0.05，高、低BMI组的生存曲线没有显著差异。")

    # Cox模型使用的数据不能包含用于分组的列
    cox_df = analysis_df[['T', 'E', '孕妇BMI', '检测孕周(周)']].copy()
    
    cph = CoxPHFitter()
    cph.fit(cox_df, duration_col='T', event_col='E')
    
    print("\nCoxPH 模型回归结果:")
    cph.print_summary()

if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    perform_survival_analysis(excel_filepath)
