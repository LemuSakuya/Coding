import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

try:
    from lifelines import (
        KaplanMeierFitter, 
        WeibullAFTFitter, 
        LogLogisticAFTFitter,
        CoxPHFitter
    )
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

def validate_and_compare_models(excel_filepath, threshold=0.04):
    # 设置和加载数据
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    try:
        df = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        print(f"错误: 加载Excel文件失败。错误信息: {e}")
        return

    df.columns = df.columns.str.strip()
    df['检测孕周(周)'] = df['检测孕周'].apply(parse_preg_week)
    target_cols = ['孕妇BMI', '检测孕周(周)', 'Y染色体浓度']
    analysis_df = df[target_cols].copy().dropna().reset_index(drop=True)
    
    analysis_df['T'] = analysis_df['检测孕周(周)']
    analysis_df['E'] = (analysis_df['Y染色体浓度'] < threshold).astype(int)

    quartiles = [30.208806, 31.811598, 33.926237]
    simple_labels = ['Q1', 'Q2', 'Q3', 'Q4']
    analysis_df['BMI分组'] = pd.cut(
        analysis_df['孕妇BMI'],
        bins=[-np.inf, quartiles[0], quartiles[1], quartiles[2], np.inf],
        labels=simple_labels
    )
    print(f"数据准备完成，共 {len(analysis_df)} 条有效记录。")

    # 拟合所有模型
    regression_df = pd.get_dummies(analysis_df, columns=['BMI分组'], drop_first=True, dtype=float)
    cols_for_fit = ['T', 'E'] + [col for col in regression_df.columns if 'BMI分组_' in col]

    kmf = KaplanMeierFitter()
    wft = WeibullAFTFitter().fit(regression_df[cols_for_fit], 'T', 'E')
    llf = LogLogisticAFTFitter().fit(regression_df[cols_for_fit], 'T', 'E')
    cph = CoxPHFitter().fit(regression_df[cols_for_fit], 'T', 'E')
    print("所有模型拟合完成。")

    plt.figure(figsize=(14, 9))
    
    for i, group in enumerate(simple_labels):
        ax = plt.subplot(2, 2, i + 1)
        
        # 绘制KM曲线 (黄金标准)
        group_data = analysis_df[analysis_df['BMI分组'] == group]
        kmf.fit(group_data['T'], group_data['E'], label=f'Kaplan-Meier ({group})')
        kmf.plot_survival_function(ax=ax, ci_show=False)

        # 准备用于预测的测试数据
        dummy_cols = [col for col in wft.params_.index.get_level_values('covariate') if 'BMI分组_' in col]
        X_test = pd.DataFrame(np.zeros((1, len(dummy_cols))), columns=dummy_cols)
        if group != 'Q1':
            X_test[f'BMI分组_{group}'] = 1

        # 叠加Weibull模型的预测曲线
        wft.predict_survival_function(X_test).rename(columns={0: 'Weibull AFT'}).plot(ax=ax)
        
        # 叠加Log-Logistic模型的预测曲线
        llf.predict_survival_function(X_test).rename(columns={0: 'Log-Logistic AFT'}).plot(ax=ax)

        plt.title(f'BMI分组: {group}')
        plt.xlabel('检测孕周 (周)')
        plt.ylabel('生存概率')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.suptitle('模型预测生存曲线与Kaplan-Meier曲线对比', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    # 检验Cox模型的比例风险假设
    print("\n步骤4: 正在检验Cox模型的比例风险假设...")
    cph.check_assumptions(regression_df[cols_for_fit], p_value_threshold=0.05, show_plots=True)
    print("比例风险假设检验完成。请查看上方输出的表格和图表。")
    print("如果p值 > 0.05，则假设成立。")
    print("如果图中的线接近水平，则假设成立。")


    # 使用AIC/BIC进行量化模型比较
    print("\n步骤5: 正在使用AIC和BIC比较模型性能...")
    
    # Cox模型使用 AIC_partial_，并且没有标准的BIC
    model_scores = pd.DataFrame({
        'AIC': [wft.AIC_, llf.AIC_, cph.AIC_partial_],
        'BIC': [wft.BIC_, llf.BIC_, np.nan]
    }, index=['Weibull AFT', 'Log-Logistic AFT', 'Cox PH'])

if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    validate_and_compare_models(excel_filepath)

