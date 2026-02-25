import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score

# 设置随机数种子以保证结果可复现
np.random.seed(42)

# 定义要分析的偏差水平（作为小数）
DEVIATION_LEVELS = {'5%': 0.05, '10%': 0.10, '15%': 0.15}

def simulate_measurement(true_values, deviation_percentage):
    
    error_std_dev = true_values * deviation_percentage
    random_error = np.random.normal(loc=0, scale=error_std_dev, size=len(true_values))
    measured_values = true_values + random_error
    measured_values[measured_values < 0] = 0
    return measured_values

def plot_scatter(df, level_name, ax):
    sns.scatterplot(x='真实值', y=f'测量值_{level_name}', data=df, alpha=0.7, label=f'模拟数据', ax=ax)
    
    min_val = df['真实值'].min()
    max_val = df['真实值'].max()
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='恒等线 (y=x)')
    
    ax.set_title(f'测量值 vs. 真实值', fontsize=14)
    ax.set_xlabel('Y染色体真实浓度', fontsize=12)
    ax.set_ylabel('Y染色体测量浓度', fontsize=12)
    ax.legend()
    ax.grid(True)
    ax.axis('equal')

def plot_bland_altman(df, level_name, ax):
    true_val = df['真实值']
    measured_val = df[f'测量值_{level_name}']
    
    diff = measured_val - true_val
    avg = (measured_val + true_val) / 2
    
    mean_diff = np.mean(diff)
    std_diff = np.std(diff)
    
    upper_loa = mean_diff + 1.96 * std_diff
    lower_loa = mean_diff - 1.96 * std_diff
    
    sns.scatterplot(x=avg, y=diff, alpha=0.6, ax=ax)
    ax.axhline(mean_diff, color='red', linestyle='-', label=f'平均偏差: {mean_diff:.4f}')
    ax.axhline(upper_loa, color='gray', linestyle='--', label=f'一致性界限 (+1.96 SD)')
    ax.axhline(lower_loa, color='gray', linestyle='--', label=f'一致性界限 (-1.96 SD)')
    
    ax.set_title(f'Bland-Altman 图', fontsize=14)
    ax.set_xlabel('真实值与测量值的平均值', fontsize=12)
    ax.set_ylabel('差值 (测量值 - 真实值)', fontsize=12)
    ax.legend()
    ax.grid(True)

def calculate_metrics(df, level_name):
    true = df['真实值']
    measured = df[f'测量值_{level_name}']
    
    r2 = r2_score(true, measured)
    rmse = np.sqrt(mean_squared_error(true, measured))
    mape = np.mean(np.abs((true - measured) / np.where(true == 0, 1, true))) * 100
    
    return {'R平方 (R²)': r2, '均方根误差 (RMSE)': rmse, '平均绝对百分比误差 (MAPE %)': mape}

def main_analysis(excel_filepath):
    # 加载数据
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    try:
        df_raw = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        print(f"错误: 加载Excel文件失败。错误信息: {e}")
        return
        
    df_raw.columns = df_raw.columns.str.strip()
    
    print("成功加载的列名:", df_raw.columns.tolist())
    
    true_values = pd.to_numeric(df_raw['Y染色体浓度'], errors='coerce').dropna()
    print(f"数据加载成功，将使用 {len(true_values)} 条有效的'Y染色体浓度'记录作为“真实值”。")
    
    # 模拟数据生成
    simulation_results = {'真实值': true_values}

    for name, value in DEVIATION_LEVELS.items():
        simulation_results[f'测量值_{name}'] = simulate_measurement(true_values, value)

    df_simulation = pd.DataFrame(simulation_results)
    print("模拟数据生成成功。")
    print(df_simulation.head())
    print("\n" + "="*50 + "\n")

    # 可视化分析
    for level_name in DEVIATION_LEVELS.keys():
        print(f"--- 正在绘制 {level_name} 偏差的合并图表 ---")
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        
        # 在左侧子图(axes[0])上绘制散点图
        plot_scatter(df_simulation, level_name, ax=axes[0])
        
        # 在右侧子图(axes[1])上绘制Bland-Altman图
        plot_bland_altman(df_simulation, level_name, ax=axes[1])
        
        # 为整个图表添加一个总标题
        fig.suptitle(f'测量误差分析 (偏差水平: {level_name})', fontsize=18)
        
        # 调整布局以防止标题重叠
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

    # 量化指标计算
    print("步骤 4: 正在计算量化指标...")
    metrics_summary = []
    for level_name in DEVIATION_LEVELS.keys():
        metrics = calculate_metrics(df_simulation, level_name)
        metrics['偏差水平'] = level_name
        metrics_summary.append(metrics)

    df_metrics = pd.DataFrame(metrics_summary).set_index('偏差水平')
    print("量化指标总结:")
    print(df_metrics.to_string(formatters={
        'R平方 (R²)': '{:,.4f}'.format,
        '均方根误差 (RMSE)': '{:,.4f}'.format,
        '平均绝对百分比误差 (MAPE %)': '{:,.2f}%'.format
    }))
    print("\n" + "="*50 + "\n")
    print("分析完成。")

if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    main_analysis(excel_filepath)

