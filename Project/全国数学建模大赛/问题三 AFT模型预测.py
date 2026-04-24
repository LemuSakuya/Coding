import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

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

def predict_with_bootstrap_ci(excel_filepath, threshold=0.04, bmi_to_predict=32.0, n_iterations=500, alpha=0.05):
    # 设置和加载数据
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    try:
        df_raw = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        print(f"错误: 加载Excel文件失败。错误信息: {e}")
        return

    # 数据清洗与筛选
    df_raw.columns = df_raw.columns.str.strip()
    
    essential_cols = ['检测孕周', 'Y染色体浓度', '孕妇BMI']
    analysis_df = df_raw[essential_cols].copy()

    analysis_df['T'] = analysis_df['检测孕周'].apply(parse_preg_week)
    analysis_df['E'] = (analysis_df['Y染色体浓度'] < threshold).astype(int)
    
    analysis_df['T'] = pd.to_numeric(analysis_df['T'], errors='coerce')
    analysis_df['孕妇BMI'] = pd.to_numeric(analysis_df['孕妇BMI'], errors='coerce')

    analysis_df.dropna(subset=analysis_df.columns, inplace=True)
    
    analysis_df = analysis_df[(analysis_df['T'] >= 10) & (analysis_df['T'] <= 25)]
    print(f"  - 经过筛选（10<=孕周<=25），最终剩余 {len(analysis_df)} 条有效记录。")

    if analysis_df.empty:
        print("错误: 筛选后无数据，无法进行分析。")
        return

    # 拟合主模型并进行主预测
    final_cols = ['T', 'E', '孕妇BMI']
    aft_main = LogLogisticAFTFitter()
    aft_main.fit(analysis_df[final_cols], duration_col='T', event_col='E')
    
    # 创建用于预测的“虚拟”数据
    X_predict = pd.DataFrame({'孕妇BMI': [bmi_to_predict]})
    
    # 预测主生存曲线
    main_prediction = aft_main.predict_survival_function(X_predict)
    timeline = main_prediction.index

    # 行自助法循环以构建置信区间
    bootstrap_predictions = []
    
    for i in tqdm(range(n_iterations)):
        try:
            bootstrap_sample = analysis_df.sample(n=len(analysis_df), replace=True).reset_index(drop=True)
            aft_boot = LogLogisticAFTFitter()
            aft_boot.fit(bootstrap_sample[final_cols], duration_col='T', event_col='E')
            
            # 在统一的时间轴上进行预测
            prediction_boot = aft_boot.predict_survival_function(X_predict, times=timeline)
            bootstrap_predictions.append(prediction_boot)
        except Exception:
            # 如果某个自助样本导致模型拟合失败，则跳过
            continue
            
    print("自助法循环完成。")
    all_predictions_df = pd.concat(bootstrap_predictions, axis=1)

    # 计算置信区间
    lower_p = (alpha / 2.0) * 100
    upper_p = (1 - alpha / 2.0) * 100
    
    lower_bound = all_predictions_df.quantile(lower_p / 100, axis=1)
    upper_bound = all_predictions_df.quantile(upper_p / 100, axis=1)
    print("置信区间计算完成。")

    # 可视化最终结果
    plt.figure(figsize=(12, 8))
    
    # 绘制主预测曲线
    plt.plot(main_prediction.index, main_prediction.values, color='blue', label=f'预测生存概率 (BMI={bmi_to_predict})')
    
    # 绘制置信区间（阴影区域）
    plt.fill_between(timeline, lower_bound, upper_bound, color='blue', alpha=0.2, label='95% 自助法置信区间')
    
    plt.title(f'BMI = {bmi_to_predict} 时，Y染色体浓度达标的预测生存概率', fontsize=16)
    plt.xlabel('检测孕周 (周)', fontsize=12)
    plt.ylabel(f'生存概率 (Y染色体浓度 >= {threshold*100}%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    plt.show()
    print("图表生成成功！")


if __name__ == '__main__':
    BMI_FOR_PREDICTION = 32.0 #可修改，这里是对某个BMI进行Bootstrap预测
    
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    predict_with_bootstrap_ci(excel_filepath, bmi_to_predict=BMI_FOR_PREDICTION)

