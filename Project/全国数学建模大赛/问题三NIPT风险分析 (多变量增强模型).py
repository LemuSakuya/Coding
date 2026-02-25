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

    # 重命名列以方便代码中使用
    df.rename(columns={
        'Y染色体浓度': 'y_concentration', '孕妇BMI': 'bmi', '年龄': 'age',
        'Y染色体的Z值': 'y_z_score', 'X染色体浓度': 'x_concentration',
        '被过滤掉读段数的比例': 'filtered_reads_ratio', '生产次数': 'productions'
    }, inplace=True)

    # 创建目标变量
    df['is_failed'] = (df['y_concentration'] < 0.04).astype(int)
    
    # 筛选用于建模的全部有效变量
    required_cols = [
        '检测孕周数值', 'bmi', 'age', 'y_z_score',
        'x_concentration', 'filtered_reads_ratio', 'productions', 'is_failed'
    ]
    df_model = df[required_cols].dropna()

    print("数据预处理完成。")
    print(f"有效数据样本数: {len(df_model)}")
    return df_model


# 建立预测模型

def train_failure_prediction_model(df_model):
    features = [col for col in df_model.columns if col not in ['is_failed']]
    X = df_model[features]
    y = df_model['is_failed']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = LogisticRegression(max_iter=2000, class_weight='balanced')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("\n--- 多变量模型评估 ---")
    print(f"模型准确率: {accuracy_score(y_test, y_pred):.4f}")
    print("分类报告:\n", classification_report(y_test, y_pred))
    return model

# 定义风险参数
def get_timing_risk(week):
    if week <= 12: return 1
    elif 13 <= week <= 27: return 5
    else: return 10

FAILURE_RISK_CONSTANT = 20

def analyze_and_find_minimum_point(model, cluster_profiles, average_age):
    possible_weeks = np.arange(10, 26, 0.5)
    results = []
    model_features = model.feature_names_in_

    for profile in cluster_profiles:
        group_objective_values = []
        for week in possible_weeks:
            # 准备模型输入
            input_data = profile.copy()
            input_data.pop('cluster_id') 
            input_data['age'] = average_age
            input_data['检测孕周数值'] = week
            input_df = pd.DataFrame([input_data])[model_features]

            # 计算原始风险
            prob_failure = model.predict_proba(input_df)[0][1]
            r_t = get_timing_risk(week)
            total_risk = (r_t + FAILURE_RISK_CONSTANT) * prob_failure
            
            # 计算新的目标函数
            objective_value = 40 - total_risk
            
            group_objective_values.append({'week': week, 'objective': objective_value})
        
        # 寻找目标函数的最小值
        min_obj_info = min(group_objective_values, key=lambda x: x['objective'])
        target_week = min_obj_info['week']
        min_obj_value = min_obj_info['objective']

        results.append({
            '聚类分组': profile['cluster_id'],
            '画像平均BMI': profile['bmi'],
            '目标孕周(风险最低点)': target_week,
            '目标函数最小值': min_obj_value,
            '目标函数曲线数据': group_objective_values
        })

    return pd.DataFrame(results)

# 可视化 (绘制目标函数曲线)

def plot_objective_curves(results_df):
    plt.figure(figsize=(14, 8))
    
    for idx, row in results_df.iterrows():
        data = pd.DataFrame(row['目标函数曲线数据'])
        label = f"聚类组 {row['聚类分组']} (BMI: {row['画像平均BMI']})"
        sns.lineplot(data=data, x='week', y='objective', label=label)
        plt.axvline(x=row['目标孕周(风险最低点)'], color=sns.color_palette()[idx], linestyle='--', alpha=0.7)
        plt.scatter(row['目标孕周(风险最低点)'], row['目标函数最小值'], color=sns.color_palette()[idx], s=100, zorder=5)

    plt.title('各聚类画像的目标函数曲线及最小值点', fontsize=16)
    plt.xlabel('检测孕周 (周)', fontsize=12)
    plt.ylabel('目标函数值 (Risk)', fontsize=12)
    plt.legend(title='聚类画像信息')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

# 敏感性分析

def sensitivity_analysis_for_clusters(model, cluster_profiles, average_age, failure_risk_values):
    global FAILURE_RISK_CONSTANT
    
    all_target_weeks = {}
    original_failure_risk = FAILURE_RISK_CONSTANT

    for risk_val in failure_risk_values:
        print(f"\n当 R_f = {risk_val} 时:")
        FAILURE_RISK_CONSTANT = risk_val
        results_df = analyze_and_find_minimum_point(model, cluster_profiles, average_age)
        optimal_weeks = results_df.set_index('聚类分组')['目标孕周(风险最低点)']
        all_target_weeks[f'R_f = {risk_val}'] = optimal_weeks

    FAILURE_RISK_CONSTANT = original_failure_risk
    summary_df = pd.DataFrame(all_target_weeks)

if __name__ == '__main__':
    cluster_profiles = [
        {'cluster_id': 0, 'bmi': 31.35, 'y_z_score': 0.20, 'x_concentration': 0.02, 'filtered_reads_ratio': 0.02, 'productions': 1.22},
        {'cluster_id': 1, 'bmi': 31.77, 'y_z_score': -0.40, 'x_concentration': 0.09, 'filtered_reads_ratio': 0.02, 'productions': 0.14},
        {'cluster_id': 2, 'bmi': 30.13, 'y_z_score': 0.00, 'x_concentration': -0.02, 'filtered_reads_ratio': 0.18, 'productions': 1.00},
        {'cluster_id': 3, 'bmi': 37.28, 'y_z_score': 0.57, 'x_concentration': 0.03, 'filtered_reads_ratio': 0.02, 'productions': 0.29},
        {'cluster_id': 4, 'bmi': 31.03, 'y_z_score': 0.23, 'x_concentration': 0.00, 'filtered_reads_ratio': 0.02, 'productions': 0.00},
    ]

    filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    df_processed = load_and_preprocess_data(filepath)
    
    if df_processed is not None:
        prediction_model = train_failure_prediction_model(df_processed)
        average_age = df_processed['age'].mean()
        
        final_results = analyze_and_find_minimum_point(prediction_model, cluster_profiles, average_age)
        
        plot_objective_curves(final_results)
        
        sensitivity_analysis_for_clusters(prediction_model, cluster_profiles, average_age, failure_risk_values=[10, 20, 30])

