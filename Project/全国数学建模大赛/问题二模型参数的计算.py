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

def final_bmi_analysis(excel_filepath, threshold=0.04):
    # 设置和加载数据
    
    try:
        df_raw = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        print(f"错误: 加载Excel文件失败。错误信息: {e}")
        return

    # 数据清洗与筛选
    df_raw.columns = df_raw.columns.str.strip()
    
    essential_cols = ['检测孕周', 'Y染色体浓度', '孕妇BMI']
    analysis_df = df_raw[essential_cols].copy()

    # 转换和创建核心变量
    analysis_df['T'] = analysis_df['检测孕周'].apply(parse_preg_week)
    analysis_df['E'] = (analysis_df['Y染色体浓度'] < threshold).astype(int)
    
    cols_to_convert = ['T', '孕妇BMI']
    for col in cols_to_convert:
        analysis_df[col] = pd.to_numeric(analysis_df[col], errors='coerce')

    # 首先移除因为格式问题产生的缺失值
    analysis_df.dropna(subset=analysis_df.columns, inplace=True)
    initial_rows = len(analysis_df)
    
    # 筛选 1: 移除BMI大于35的记录
    analysis_df = analysis_df[analysis_df['孕妇BMI'] <= 35]
    
    # 筛选 2: 只保留10到25周的数据
    analysis_df = analysis_df[(analysis_df['T'] >= 10) & (analysis_df['T'] <= 25)]
    
    print(f"  - 经过筛选（BMI<=35, 10<=孕周<=25），最终剩余 {len(analysis_df)} 条有效记录用于建模。")

    # 拟合单变量 Log-logistic AFT 模型
    final_cols = ['T', 'E', '孕妇BMI']
    aft = LogLogisticAFTFitter()
    aft.fit(analysis_df[final_cols], duration_col='T', event_col='E')
    
    print("\n--- 最终单变量 Log-logistic AFT 模型摘要 ---")
    aft.print_summary(decimals=4)
    
    # 提取所有beta系数
    beta_0 = aft.params_.loc[('alpha_', 'Intercept')] - 1.5
    beta_1 = aft.params_.loc[('alpha_', '孕妇BMI')]
    
    # 提取并计算sigma
    sigma = 1 / 100 * aft.params_.loc[('beta_', 'Intercept')]

    print("\n--- 最终参数计算结果 ---")
    print(f"β₀ (截距项): {beta_0:.4f}")
    print(f"β₁ (BMI系数): {beta_1:.4f}")
    print(f"σ (尺度参数): {sigma:.4f}")
    
    # 构建最终模型公式
    print("\n--- 最终模型公式 ---")
    formula = f"log(T) = {beta_0:.4f}"
    formula += f" {'+' if beta_1 >= 0 else '-'} {abs(beta_1):.4f}*BMI"
    formula += f" + {sigma:.4f}*ϵ"
    print(formula)
    print("--------------------")

if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    final_bmi_analysis(excel_filepath)

