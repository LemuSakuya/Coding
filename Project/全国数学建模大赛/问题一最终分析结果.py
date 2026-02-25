import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt
import re

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def convert_gestational_week(week_str):
    if pd.isna(week_str):
        return np.nan
    
    week_str = str(week_str).strip()
    
    # 匹配数字和周数
    match = re.match(r'(\d+)w\s*\+\s*(\d+)?', week_str)
    if match:
        weeks = int(match.group(1))
        days = int(match.group(2)) if match.group(2) else 0
        return weeks + days/7
    
    # 尝试匹配其他格式
    match = re.match(r'(\d+)[wW]?', week_str)
    if match:
        return float(match.group(1))
    
    # 尝试直接转换数字
    try:
        return float(week_str)
    except:
        return np.nan

def perform_bmi_analysis(df, time_col, event_col):
    # BMI四分位数阈值
    bmi_quantiles = {
        'Q1': 30.208806,  # 25%
        'Q2': 31.811598,  # 50%
        'Q3': 33.926237   # 75%
    }
    
    # 创建BMI分组
    df['bmi_group'] = pd.cut(df['孕妇BMI'], 
                            bins=[-np.inf, bmi_quantiles['Q1'], bmi_quantiles['Q2'], 
                                  bmi_quantiles['Q3'], np.inf],
                            labels=['Q1(<30.21)', 'Q2(30.21-31.81)', 'Q3(31.81-33.93)', 'Q4(>33.93)'])
    
    # 创建图表
    plt.figure(figsize=(12, 8))
    kmf = KaplanMeierFitter()
    
    # 获取分组并排序
    groups = sorted(df['bmi_group'].dropna().unique())
    
    for group in groups:
        group_data = df[df['bmi_group'] == group]
        label = f'BMI{group} (n={len(group_data)})'
        kmf.fit(group_data[time_col], group_data[event_col], label=label)
        kmf.plot(ci_show=False)
    
    plt.title('孕妇BMI四分位数分组对胎儿健康生存曲线的影响')
    plt.xlabel('孕周')
    plt.ylabel('健康胎儿比例')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    # 执行Log-Rank检验和输出结果
    print("=== 孕妇BMI四分位数分组 Log-Rank检验结果 ===")
    
    # 计算每组统计量
    for group in groups:
        group_data = df[df['bmi_group'] == group]
        event_count = group_data[event_col].sum()
        kmf_temp = KaplanMeierFitter()
        kmf_temp.fit(group_data[time_col], group_data[event_col])
        median_survival = kmf_temp.median_survival_time_
        
        print(f"BMI{group}: 样本数={len(group_data)}, 事件数={event_count}, "
              f"中位生存时间={median_survival:.2f}周")
    
    # 整体Log-Rank检验
    results = []
    for i in range(len(groups)):
        for j in range(i+1, len(groups)):
            group1_data = df[df['bmi_group'] == groups[i]]
            group2_data = df[df['bmi_group'] == groups[j]]
            
            lr_result = logrank_test(
                group1_data[time_col], group2_data[time_col],
                group1_data[event_col], group2_data[event_col]
            )
            
            results.append({
                '比较组': f'{groups[i]} vs {groups[j]}',
                'p值': lr_result.p_value
            })
    
    print("\n组间比较p值:")
    for result in results:
        print(f"{result['比较组']}: p={result['p值']:.6f}")
    
    return results

def perform_y_chromosome_analysis(df, time_col, event_col):
    # 设置4%阈值
    y_threshold = 0.04
    
    df['y_group'] = df['Y染色体浓度'] > y_threshold
    group_names = {True: '高Y浓度(>4%)', False: '低Y浓度(≤4%)'}
    
    # 创建图表
    plt.figure(figsize=(10, 6))
    kmf = KaplanMeierFitter()
    
    groups = sorted(df['y_group'].unique())
    
    for group in groups:
        group_data = df[df['y_group'] == group]
        label = f'{group_names[group]} (n={len(group_data)})'
        kmf.fit(group_data[time_col], group_data[event_col], label=label)
        kmf.plot(ci_show=False)
    
    # 执行Log-Rank检验
    group1 = df[df['y_group'] == groups[0]]
    group2 = df[df['y_group'] == groups[1]]
    
    results = logrank_test(
        group1[time_col], group2[time_col],
        group1[event_col], group2[event_col]
    )
    
    plt.title(f'Y染色体浓度对胎儿健康生存曲线的影响\n(阈值=4%, Log-Rank检验 p值: {results.p_value:.4f})')
    plt.xlabel('孕周')
    plt.ylabel('健康胎儿比例')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    # 输出结果
    print("=== Y染色体浓度(4%阈值) Log-Rank检验结果 ===")
    print(f"分组阈值: {y_threshold:.3f}")
    
    for group in groups:
        group_data = df[df['y_group'] == group]
        event_count = group_data[event_col].sum()
        kmf_temp = KaplanMeierFitter()
        kmf_temp.fit(group_data[time_col], group_data[event_col])
        median_survival = kmf_temp.median_survival_time_
        
        print(f"{group_names[group]}: 样本数={len(group_data)}, 事件数={event_count}, "
              f"中位生存时间={median_survival:.2f}周, "
              f"Y浓度均值={group_data['Y染色体浓度'].mean():.4f}±{group_data['Y染色体浓度'].std():.4f}")
    
    print(f"Log-Rank检验 p值: {results.p_value:.6f}")
    if results.p_value < 0.05:
        print("结果显著: 两组生存曲线有统计学差异")
    else:
        print("结果不显著: 两组生存曲线无统计学差异")
    
    return results

def load_data_from_excel(file_path, sheet_name='男胎检测数据'):
    print(f"步骤1: 正在从 '{file_path}' 加载 '{sheet_name}'...")
    
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"数据加载成功，共 {len(df)} 条记录。")
        return df
    except Exception as e:
        print(f"数据加载失败: {e}")
        return None

# 主分析函数
def analyze_fetal_health_data(df):
    if df is None or len(df) == 0:
        print("数据为空，无法进行分析")
        return None, None
    
    # 数据预处理
    df_clean = df.copy()
    
    print("步骤2: 正在预处理数据...")
    
    # 转换孕周为数值
    df_clean['孕周数值'] = df_clean['检测孕周'].apply(convert_gestational_week)
    
    # 创建事件变量: 1=不健康, 0=健康
    df_clean['事件'] = (df_clean['胎儿是否健康'] == '否').astype(int)
    
    # 清理数值列
    numeric_cols = ['Y染色体浓度', '孕妇BMI', '孕周数值']
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    # 删除缺失值
    initial_count = len(df_clean)
    df_clean = df_clean.dropna(subset=numeric_cols + ['事件'])
    removed_count = initial_count - len(df_clean)
    
    print(f"数据预处理完成，剩余 {len(df_clean)} 条有效数据，删除了 {removed_count} 条缺失数据。")
    
    if len(df_clean) == 0:
        print("预处理后无有效数据，请检查数据格式")
        return None, None
    
    print(f"健康胎儿: {(df_clean['事件'] == 0).sum()}")
    print(f"不健康胎儿: {(df_clean['事件'] == 1).sum()}")
    print(f"Y染色体浓度范围: {df_clean['Y染色体浓度'].min():.4f} - {df_clean['Y染色体浓度'].max():.4f}")
    print(f"孕妇BMI范围: {df_clean['孕妇BMI'].min():.2f} - {df_clean['孕妇BMI'].max():.2f}")
    print()
    
    # 执行分析
    bmi_results = perform_bmi_analysis(df_clean, '孕周数值', '事件')
    print()

    y_results = perform_y_chromosome_analysis(df_clean, '孕周数值', '事件')
    
    return bmi_results, y_results

# 主程序
if __name__ == "__main__":
    file_path = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    sheet_name = "男胎检测数据"
    
    df = load_data_from_excel(file_path, sheet_name)
    
    if df is not None:
        # 运行分析
        results = analyze_fetal_health_data(df)
        
        if results:
            bmi_results, y_results = results
            print("分析完成！")
        else:
            print("分析失败")
    else:
        print("无法加载数据文件")