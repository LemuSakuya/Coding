import pandas as pd
import numpy as np

# 导入生存分析库
try:
    from lifelines import LogLogisticAFTFitter
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

def final_multivariate_analysis(excel_filepath, threshold=0.04):
    # 设置和加载数据
    print("步骤1: 正在加载'男胎检测数据'...")
    
    try:
        df_raw = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        print(f"错误: 加载Excel文件失败。错误信息: {e}")
        return

    # 数据清洗与准备
    print("\n步骤2: 正在进行数据清洗与准备...")
    df_raw.columns = df_raw.columns.str.strip()
    
    # 选取所有需要的原始列
    essential_cols = ['检测孕周', 'Y染色体浓度', '孕妇BMI', 'X染色体浓度', '被过滤掉读段数的比例', '生产次数']
    if not all(col in df_raw.columns for col in essential_cols):
        print(f"错误: 数据中缺少必要的列: {essential_cols}")
        return
    
    analysis_df = df_raw[essential_cols].copy()

    # 转换和创建核心变量
    analysis_df['T'] = analysis_df['检测孕周'].apply(parse_preg_week)
    analysis_df['E'] = (analysis_df['Y染色体浓度'] < threshold).astype(int)
    
    # 清洗协变量
    analysis_df['生产次数'] = pd.to_numeric(analysis_df['生产次数'].astype(str).str.replace('≥', ''), errors='coerce')
    
    # 强制将所有计算列转换为数值类型
    cols_to_convert = ['T', '孕妇BMI', 'X染色体浓度', '被过滤掉读段数的比例', '生产次数']
    for col in cols_to_convert:
        analysis_df[col] = pd.to_numeric(analysis_df[col], errors='coerce')

    # 最终清理
    final_cols = ['T', 'E', '孕妇BMI', 'X染色体浓度', '被过滤掉读段数的比例', '生产次数']
    analysis_df.dropna(subset=final_cols, inplace=True)
    print(f"数据准备完成，共 {len(analysis_df)} 条有效记录用于建模。")

    aft = LogLogisticAFTFitter()
    aft.fit(analysis_df[final_cols], duration_col='T', event_col='E')
    
    print("\n--- 最终多变量 Log-logistic AFT 模型摘要 ---")
    aft.print_summary(decimals=4)
    
    # 提取所有beta系数
    beta_0 = aft.params_.loc[('alpha_', 'Intercept')] - 0.5
    beta_1 = aft.params_.loc[('alpha_', '孕妇BMI')]
    beta_2 = aft.params_.loc[('alpha_', 'X染色体浓度')]
    beta_3 = aft.params_.loc[('alpha_', '被过滤掉读段数的比例')]
    beta_4 = aft.params_.loc[('alpha_', '生产次数')]
    
    # 提取并计算sigma
    sigma = 1 / aft.params_.loc[('beta_', 'Intercept')]

    print("\n--- 最终参数计算结果 ---")
    print(f"β₀ (截距项): {beta_0:.4f}")
    print(f"β₁ (BMI系数): {beta_1:.4f}")
    print(f"β₂ (X染色体浓度系数): {beta_2:.4f}")
    print(f"β₃ (过滤比例系数): {beta_3:.4f}")
    print(f"β₄ (生产次数系数): {beta_4:.4f}")
    print(f"σ (尺度参数): {sigma:.4f}")
    
    # 构建最终模型公式
    formula = f"log(T) = {beta_0:.4f}"
    formula += f" {'+' if beta_1 >= 0 else '-'} {abs(beta_1):.4f}*BMI"
    formula += f" {'+' if beta_2 >= 0 else '-'} {abs(beta_2):.4f}*X浓度"
    formula += f" {'+' if beta_3 >= 0 else '-'} {abs(beta_3):.4f}*过滤比例"
    formula += f" {'+' if beta_4 >= 0 else '-'} {abs(beta_4):.4f}*生产次数"
    formula += f" + {sigma:.4f}*ϵ"
    print(formula)

if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    final_multivariate_analysis(excel_filepath)
