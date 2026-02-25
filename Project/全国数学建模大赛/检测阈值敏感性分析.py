import pandas as pd
import numpy as np
from lifelines import LogLogisticAFTFitter
import matplotlib.pyplot as plt
import seaborn as sns

CLUSTER_PROFILES = [
    {'cluster_id': 0, '孕妇BMI': 31.35, 'X染色体浓度': 0.02, '被过滤掉读段数的比例': 0.02, '生产次数': 1.22},
    {'cluster_id': 1, '孕妇BMI': 31.77, 'X染色体浓度': 0.09, '被过滤掉读段数的比例': 0.02, '生产次数': 0.14},
    {'cluster_id': 3, '孕妇BMI': 37.28, 'X染色体浓度': 0.03, '被过滤掉读段数的比例': 0.02, '生产次数': 0.29},
    {'cluster_id': 4, '孕妇BMI': 31.03, 'X染色体浓度': 0.00, '被过滤掉读段数的比例': 0.02, '生产次数': 0.00},
]

# 敏感性分析参数
THRESHOLDS_TO_TEST = [0.035, 0.040, 0.045]
CONFIDENCE_LEVEL = 0.95

EXCEL_FILEPATH = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
SHEET_NAME = '男胎检测数据'

# 辅助函数
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

def visualize_sensitivity_results(results_df):
    df_long = pd.melt(results_df, 
                      id_vars=['聚类分组', '画像平均BMI'], 
                      var_name='检测阈值', 
                      value_name='预测孕周')
    df_long['阈值(%)'] = df_long['检测阈值'].str.extract(r'(\d+\.\d+)').astype(float)

    # 绘制折线图
    plt.figure(figsize=(12, 8))
    sns.lineplot(data=df_long, 
                 x='阈值(%)', 
                 y='预测孕周', 
                 hue='聚类分组', 
                 style='聚类分组',
                 markers=True, 
                 dashes=False,
                 markersize=8)

    plt.title('检测阈值敏感性分析', fontsize=16)
    plt.xlabel('Y染色体浓度检测阈值 (%)', fontsize=12)
    plt.ylabel(f'达到 {CONFIDENCE_LEVEL*100}% 置信水平的预测孕周', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title='孕妇画像分组')
    plt.xticks(THRESHOLDS_TO_TEST_PERCENT)
    
    # 在每个点上标注数值
    for _, row in df_long.iterrows():
        plt.text(row['阈值(%)'], row['预测孕周'] + 0.05, f"{row['预测孕周']:.1f}", 
                 ha='center', va='bottom', fontsize=9)

    plt.show()
def run_threshold_sensitivity_analysis():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 加载数据
    try:
        df_raw = pd.read_excel(EXCEL_FILEPATH, sheet_name=SHEET_NAME)
    except Exception as e:
        return

    # 数据清洗与准备
    df_raw.columns = df_raw.columns.str.strip()
    
    essential_cols = ['检测孕周', 'Y染色体浓度', '孕妇BMI', 'X染色体浓度', '被过滤掉读段数的比例', '生产次数']
    if not all(col in df_raw.columns for col in essential_cols):
        return
        
    analysis_df = df_raw[essential_cols].copy()
    
    analysis_df['T'] = analysis_df['检测孕周'].apply(parse_preg_week)
    analysis_df['生产次数'] = pd.to_numeric(analysis_df['生产次数'].astype(str).str.replace('2', ''), errors='coerce')
    
    cols_to_convert = ['T', '孕妇BMI', 'X染色体浓度', '被过滤掉读段数的比例', '生产次数']
    for col in cols_to_convert:
        analysis_df[col] = pd.to_numeric(analysis_df[col], errors='coerce')

    results_data = []
    for profile in CLUSTER_PROFILES:
        row = {'聚类分组': f"聚类组 {profile['cluster_id']}", '画像平均BMI': profile['孕妇BMI']}
        results_data.append(row)
    results_df = pd.DataFrame(results_data)

    for threshold in THRESHOLDS_TO_TEST:
        
        analysis_df['E'] = (analysis_df['Y染色体浓度'] < threshold).astype(int)
        
        final_cols = ['T', 'E', '孕妇BMI', 'X染色体浓度', '被过滤掉读段数的比例', '生产次数']
        model_df = analysis_df.dropna(subset=final_cols).copy()

        if len(model_df) < 10:
            continue

        aft = LogLogisticAFTFitter()
        aft.fit(model_df[final_cols], duration_col='T', event_col='E')
        
        predicted_weeks = []
        for profile in CLUSTER_PROFILES:
            covariates = pd.DataFrame([profile])
            covariates = covariates.drop(columns=['cluster_id'])
            predicted_time = aft.predict_percentile(covariates, p=CONFIDENCE_LEVEL).iloc[0]
            predicted_weeks.append(predicted_time)
        
        results_df[f'阈值 = {threshold*100:.1f}% (孕周)'] = [round(w, 1) for w in predicted_weeks]
    print(f"固定置信水平 = {CONFIDENCE_LEVEL*100}%")
    print(results_df.to_string(index=False))
    
    # 调用可视化函数
    visualize_sensitivity_results(results_df)


if __name__ == '__main__':
    THRESHOLDS_TO_TEST_PERCENT = [t * 100 for t in THRESHOLDS_TO_TEST]
    run_threshold_sensitivity_analysis()

