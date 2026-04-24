import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def main_analysis(excel_filepath):
    # 数据加载与预处理
    try:
        male_df = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except FileNotFoundError:
        return
    except Exception as e:
        return

    # 定义一个函数，将孕周字符串（如 '11w+6'）转换为数值（周）
    def convert_gestational_week(week_str):
        if isinstance(week_str, str) and 'w+' in week_str:
            parts = week_str.split('w+')
            try:
                weeks = int(parts[0])
                days = int(parts[1])
                return weeks + days / 7
            except (ValueError, IndexError):
                return np.nan
        return np.nan

    # 应用转换函数，创建新的数值型孕周列
    male_df['检测孕周_数值'] = male_df['检测孕周'].apply(convert_gestational_week)

    # 清洗数据：移除在关键列中包含缺失值的行
    columns_to_check = ['孕妇BMI', '检测孕周_数值', 'Y染色体浓度']
    male_df_cleaned = male_df.dropna(subset=columns_to_check).copy()


    # BMI分组
    male_df_cleaned.loc[:, 'BMI_Group'] = pd.cut(male_df_cleaned['孕妇BMI'],
                                         bins=[0, 30, 35, float('inf')],
                                         labels=['较低BMI (<30)', '中等BMI (30-35)', '较高BMI (>=35)'])

    print("数据预处理和BMI分组完成。")
    print(f"总共处理了 {len(male_df_cleaned)} 条有效数据。")
    print("\n各BMI分组的样本数量:")
    print(male_df_cleaned['BMI_Group'].value_counts())


    # 建立Y染色体浓度预测模型
    X = male_df_cleaned[['孕妇BMI', '检测孕周_数值']]
    y = male_df_cleaned['Y染色体浓度']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    gbr.fit(X_train, y_train)
    y_pred = gbr.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"\n预测模型训练完成。")
    print(f"模型在测试集上的均方误差 (MSE): {mse:.6f}")


    # 为每个BMI分组确定最佳NIPT时点
    def get_risk(week):
        if week <= 12: return 1
        elif 13 <= week <= 27: return 10
        else: return 100

    bmi_groups_median = male_df_cleaned.groupby('BMI_Group')['孕妇BMI'].median()
    optimal_timings = {}

    for group, median_bmi in bmi_groups_median.items():
        min_risk = float('inf')
        optimal_time = -1
        concentration_at_optimal_time = 0

        for week in np.arange(10, 28, 1/7):
            predicted_concentration = gbr.predict([[median_bmi, week]])[0]
            if predicted_concentration >= 0.04:
                current_risk = get_risk(week)
                if current_risk < min_risk:
                    min_risk = current_risk
                    optimal_time = week
                    concentration_at_optimal_time = predicted_concentration
        
        optimal_timings[group] = (optimal_time, concentration_at_optimal_time)


    # 展示最终结果
    print("\n" + "="*60)
    print("--- 最终结论：各BMI分组的最佳NIPT时点建议 ---")
    print("="*60)
    print(f"{'BMI分组':<20} | {'建议检测时点':<15} | {'预测Y染色体浓度':<15}")
    print("-"*60)

    for group, (time, conc) in optimal_timings.items():
        if time != -1:
            weeks = int(time)
            days = int(round((time - weeks) * 7))
            timing_str = f"孕 {weeks}w+{days}d"
            conc_str = f"{conc*100:.2f}%"
            print(f"{group:<20} | {timing_str:<15} | {conc_str:<15}")
        else:
            print(f"{group:<20} | {'28周内未达标':<15} | {'N/A':<15}")
    print("="*60)

if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    
    # 调用主分析函数
    main_analysis(excel_filepath)

