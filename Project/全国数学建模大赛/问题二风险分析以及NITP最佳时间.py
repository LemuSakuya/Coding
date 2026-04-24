import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings('ignore')

# 数据加载与预处理

def load_and_preprocess_data(filepath):
    try:
        df = pd.read_excel(filepath, sheet_name='男胎检测数据')
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

    def convert_week_to_float(week_str):
        if isinstance(week_str, str) and 'w+' in week_str:
            parts = week_str.replace('w', '').split('+')
            return float(parts[0]) + float(parts[1]) / 7
        return np.nan

    df['检测孕周数值'] = df['检测孕周'].apply(convert_week_to_float)
    df.rename(columns={'Y染色体浓度': 'y_concentration', '孕妇BMI': 'bmi', '年龄': 'age'}, inplace=True)
    df['is_failed'] = (df['y_concentration'] < 0.04).astype(int)
    required_cols = ['检测孕周数值', 'bmi', 'age', 'is_failed']
    df_model = df[required_cols].dropna()

    print("数据预处理完成。")
    print(f"有效数据样本数: {len(df_model)}")
    print("数据预览:\n", df_model.head())
    return df_model


# 建立预测模型
def train_failure_prediction_model(df_model):
    X = df_model[['检测孕周数值', 'bmi', 'age']]
    y = df_model['is_failed']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("\n--- 模型评估 ---")
    print(f"模型准确率: {accuracy_score(y_test, y_pred):.4f}")
    print("分类报告:\n", classification_report(y_test, y_pred))
    return model

# 定义风险参数

def get_timing_risk(week):
    if week <= 12:
        return 1
    elif 13 <= week <= 27:
        return 5
    else:
        return 10

FAILURE_RISK_CONSTANT = 20

# 目标函数计算与优化 (按要求寻找新目标函数的最小值)

def analyze_and_find_minimum_point(df, model, num_bmi_groups=4):
    df['bmi_group'] = pd.qcut(df['bmi'], q=num_bmi_groups, labels=False, duplicates='drop')
    group_info = df.groupby('bmi_group')['bmi'].agg(['mean', 'min', 'max']).reset_index()
    group_info.columns = ['bmi_group_index', 'bmi_mean', 'bmi_min', 'bmi_max']
    group_info['bmi_range'] = group_info.apply(lambda row: f"[{row['bmi_min']:.2f}, {row['bmi_max']:.2f}]", axis=1)
    print("\n--- BMI 分组情况 ---")
    print(group_info[['bmi_group_index', 'bmi_range', 'bmi_mean']])

    possible_weeks = np.arange(10, 26, 0.5)
    results = []

    for idx, group in group_info.iterrows():
        avg_bmi = group['bmi_mean']
        avg_age = df[df['bmi_group'] == group['bmi_group_index']]['age'].mean()
        
        group_objective_values = []
        for week in possible_weeks:
            input_features = pd.DataFrame([[week, avg_bmi, avg_age]], columns=['检测孕周数值', 'bmi', 'age'])
            prob_failure = model.predict_proba(input_features)[0][1]
            r_t = get_timing_risk(week)

            # 计算原始风险
            total_risk = (r_t + FAILURE_RISK_CONSTANT) * prob_failure
            
            # 计算新的目标函数
            objective_value = 40 - total_risk
            
            group_objective_values.append({'week': week, 'objective': objective_value})

        min_obj_info = min(group_objective_values, key=lambda x: x['objective'])
        target_week = min_obj_info['week']
        min_obj_value = min_obj_info['objective']

        results.append({
            'BMI分组': group['bmi_group_index'],
            'BMI范围': group['bmi_range'],
            '代表BMI': avg_bmi,
            '目标孕周(风险最低点)': target_week,
            '目标函数最小值': min_obj_value,
            '目标函数曲线数据': group_objective_values
        })

    return pd.DataFrame(results)


# 可视化
def plot_objective_curves(results_df):
    plt.figure(figsize=(14, 8))
    
    for idx, row in results_df.iterrows():
        data = pd.DataFrame(row['目标函数曲线数据'])
        sns.lineplot(data=data, x='week', y='objective', label=f"BMI组 {row['BMI分组']}: {row['BMI范围']}")
        plt.axvline(x=row['目标孕周(风险最低点)'], color=sns.color_palette()[idx], linestyle='--', alpha=0.7)
        plt.scatter(row['目标孕周(风险最低点)'], row['目标函数最小值'], color=sns.color_palette()[idx], s=100, zorder=5)

    plt.title('各BMI分组的目标函数曲线及最小值点', fontsize=16)
    plt.xlabel('检测孕周 (周)', fontsize=12)
    plt.ylabel('目标函数值(Risk)', fontsize=12)
    plt.legend(title='BMI分组信息')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

# 敏感性分析

def sensitivity_analysis(df, model, failure_risk_values):
    global FAILURE_RISK_CONSTANT
    
    all_target_weeks = {}
    original_failure_risk = FAILURE_RISK_CONSTANT

    for risk_val in failure_risk_values:
        print(f"\n当 R_f = {risk_val} 时:")
        FAILURE_RISK_CONSTANT = risk_val
        
        results_df = analyze_and_find_minimum_point(df, model) # 调用更新后的函数
        target_weeks = results_df[['BMI范围', '目标孕周(风险最低点)']].set_index('BMI范围')
        all_target_weeks[f'R_f = {risk_val}'] = target_weeks['目标孕周(风险最低点)']

    FAILURE_RISK_CONSTANT = original_failure_risk
    summary_df = pd.DataFrame(all_target_weeks)
    print("\n--- 敏感性分析总结 ---")
    print("不同 R_f 取值下的目标孕周(风险最低点):")
    print(summary_df)


if __name__ == '__main__':
    filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    df_processed = load_and_preprocess_data(filepath)
    
    if df_processed is not None:
        prediction_model = train_failure_prediction_model(df_processed)
        
        final_results = analyze_and_find_minimum_point(df_processed, prediction_model)
        plot_objective_curves(final_results)
        
        sensitivity_analysis(df_processed, prediction_model, failure_risk_values=[10, 20, 30])

