import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 导入生存分析库
try:
    from lifelines import WeibullAFTFitter
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

def perform_weibull_aft_analysis(excel_filepath, threshold=0.04):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 加载和预处理数据
    try:
        df = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        return

    df.columns = df.columns.str.strip()
    df['检测孕周(周)'] = df['检测孕周'].apply(parse_preg_week)
    
    target_cols = ['孕妇BMI', '检测孕周(周)', 'Y染色体浓度']
    analysis_df = df[target_cols].copy().dropna().reset_index(drop=True)
    print(f"  - 数据预处理完成，剩余 {len(analysis_df)} 条有效数据。")

    # 定义生存变量和BMI分组
    analysis_df['T'] = analysis_df['检测孕周(周)']
    analysis_df['E'] = (analysis_df['Y染色体浓度'] < threshold).astype(int)
    print(f"  - 已定义事件（Y染色体浓度 < {threshold}）。共发生 {analysis_df['E'].sum()} 例事件。")

    quartiles = [30.208806, 31.811598, 33.926237]

    simple_labels = ['Q1', 'Q2', 'Q3', 'Q4']
    analysis_df['BMI分组'] = pd.cut(
        analysis_df['孕妇BMI'],
        bins=[-np.inf, quartiles[0], quartiles[1], quartiles[2], np.inf],
        labels=simple_labels
    )
    print(f"  - 已根据您提供的固定阈值将BMI分为四组: Q1 (≤{quartiles[0]:.2f}), Q2 (≤{quartiles[1]:.2f}), Q3 (≤{quartiles[2]:.2f}), Q4 (>{quartiles[2]:.2f})")

    # 构建并拟合 Weibull AFT 模型
    regression_df = pd.get_dummies(analysis_df, columns=['BMI分组'], drop_first=True, dtype=float)
    cols_for_fit = ['T', 'E'] + [col for col in regression_df.columns if 'BMI分组_' in col]
    
    aft = WeibullAFTFitter()
    aft.fit(regression_df[cols_for_fit], duration_col='T', event_col='E')

    aft.print_summary(decimals=3)
    plt.figure(figsize=(12, 8))
    
    label_map = {
        'Q1': f'Q1 (BMI ≤ {quartiles[0]:.2f})',
        'Q2': f'Q2 ({quartiles[0]:.2f} < BMI ≤ {quartiles[1]:.2f})',
        'Q3': f'Q3 ({quartiles[1]:.2f} < BMI ≤ {quartiles[2]:.2f})',
        'Q4': f'Q4 (BMI > {quartiles[2]:.2f})'
    }
    
    dummy_cols = [col for col in aft.params_.index.get_level_values('covariate') if 'BMI分组_' in col]

    for group_label in simple_labels:
        X_test = pd.DataFrame(np.zeros((1, len(dummy_cols))), columns=dummy_cols)
        
        if group_label != 'Q1':
            group_col_name = f"BMI分组_{group_label}"
            if group_col_name in X_test.columns:
                 X_test[group_col_name] = 1

        survival_function = aft.predict_survival_function(X_test)
        
        descriptive_label = label_map[group_label]
        plt.plot(survival_function.index, survival_function.values.flatten(), label=descriptive_label)
    
    plt.title('Weibull-AFT模型预测的生存曲线 (按BMI分组)')
    plt.xlabel('检测孕周 (周)')
    plt.ylabel(f'生存概率 (Y染色体浓度 >= {threshold*100}%)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title="BMI 分组")
    plt.show()


if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    perform_weibull_aft_analysis(excel_filepath)

