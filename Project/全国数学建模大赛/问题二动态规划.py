import pandas as pd
import numpy as np

def calculate_cost_matrix(data):
    n = len(data)
    prefix_sum = np.zeros(n + 1)
    prefix_sum_sq = np.zeros(n + 1)
    for i in range(n):
        prefix_sum[i+1] = prefix_sum[i] + data[i]
        prefix_sum_sq[i+1] = prefix_sum_sq[i] + data[i]**2

    cost_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            count = j - i + 1
            # 计算 data[i] 到 data[j] 的和与平方和
            sum_val = prefix_sum[j+1] - prefix_sum[i]
            sum_sq_val = prefix_sum_sq[j+1] - prefix_sum_sq[i]
            
            # 方差公式: E[X^2] - (E[X])^2
            mean = sum_val / count
            cost = sum_sq_val - 2 * mean * sum_val + count * mean**2
            cost_matrix[i, j] = cost
            
    return cost_matrix

def find_optimal_groups(excel_filepath, max_k=5):
    # 数据加载与准备
    try:
        male_df = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        return

    # 获取唯一、排序后的BMI值
    bmi_values = np.sort(male_df['孕妇BMI'].dropna().unique())
    n = len(bmi_values)
    print(f"共找到 {n} 个唯一的BMI值用于分组。")

    # 预计算成本矩阵
    cost_matrix = calculate_cost_matrix(bmi_values)

    # 动态规划求解
    dp = np.full((n + 1, max_k + 1), np.inf)
    breaks = np.zeros((n + 1, max_k + 1), dtype=int)
    dp[0, 0] = 0
    
    for k in range(1, max_k + 1):
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                cost = dp[j - 1, k - 1] + cost_matrix[j - 1, i - 1]
                if cost < dp[i, k]:
                    dp[i, k] = cost
                    breaks[i, k] = j - 1
    
    # 输出结果
    print("\n" + "="*60)
    print("--- 不同分组数(K)对应的最小总方差 (SSE) ---")
    print("="*60)
    for k in range(1, max_k + 1):
        print(f"K = {k}:  总成本 (SSE) = {dp[n, k]:.2f}")
    print("="*60)
    print("\n提示：请观察SSE的下降趋势，选择一个“肘点”作为最佳K值。")

    # K=3时的最优分组结果
    chosen_k = 3
    print(f"\n--- 以 K={chosen_k} 为例的最优BMI分组边界 ---")
    print("="*60)
    
    boundaries = []
    current_break = n
    for k in range(chosen_k, 0, -1):
        prev_break = breaks[current_break, k]
        boundaries.append(prev_break)
        current_break = prev_break
    
    boundaries.reverse()
    
    start_index = 0
    for i, end_index in enumerate(boundaries[1:]):
        group_min = bmi_values[start_index]
        group_max = bmi_values[end_index - 1]
        print(f"第 {i+1} 组: BMI区间 ≈ [{group_min:.2f}, {group_max:.2f}]")
        start_index = end_index

    # 最后一组
    group_min = bmi_values[start_index]
    group_max = bmi_values[-1]
    print(f"第 {chosen_k} 组: BMI区间 ≈ [{group_min:.2f}, {group_max:.2f}]")
    print("="*60)
    print("\n您可以将这些数据驱动的BMI区间用于后续的AFT模型分析。")


if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    find_optimal_groups(excel_filepath, max_k=5)
