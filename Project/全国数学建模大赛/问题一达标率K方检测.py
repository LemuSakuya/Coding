import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def perform_qualification_rate_test(excel_filepath, threshold=0.04):
    # 设置和加载数据
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    try:
        df = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
        print("数据加载成功。")
    except Exception as e:
        print(f"错误: 加载Excel文件失败。错误信息: {e}")
        return

    df.columns = df.columns.str.strip()
    
    analysis_df = df[['孕妇BMI', 'Y染色体浓度']].copy().dropna()
    print(f"  - 数据预处理完成，剩余 {len(analysis_df)} 条有效记录。")

    # 定义“是否达标”
    analysis_df['是否达标'] = np.where(analysis_df['Y染色体浓度'] >= threshold, '达标', '不达标')
    print(f"  - 已根据阈值 {threshold*100}% 定义了'是否达标'。")

    # 根据您提供的固定百分位数进行分组
    quartiles = [30.208806, 31.811598, 33.926237]
    analysis_df['BMI分组'] = pd.cut(
        analysis_df['孕妇BMI'],
        bins=[-np.inf, quartiles[0], quartiles[1], quartiles[2], np.inf],
        labels=['Q1(最低25%)', 'Q2(25-50%)', 'Q3(50-75%)', 'Q4(最高25%)']
    )
    print("  - 已将'孕妇BMI'分为4组。")

    # 创建列联表 (Contingency Table)
    contingency_table = pd.crosstab(analysis_df['BMI分组'], analysis_df['是否达标'])
    
    print(contingency_table)

    # 执行卡方检验
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    print("\n卡方检验结果:")
    print(f"  - 卡方统计量: {chi2:.4f}")
    print(f"  - P值: {p_value:.4f}")
    
    # 解读p值
    if p_value < 0.05:
        print("  - 结论: P值 < 0.05，我们认为孕妇BMI分组与Y染色体浓度是否达标之间存在**显著关联**。")
    else:
        print("  - 结论: P值 >= 0.05，我们没有足够证据表明孕妇BMI分组与Y染色体浓度是否达标有关联。")

    # 计算每个组的达标率
    rate_df = contingency_table.div(contingency_table.sum(axis=1), axis=0)
    
    plt.figure(figsize=(12, 7))
    ax = sns.barplot(x=rate_df.index, y=rate_df['达标'], palette='viridis')
    
    # 在条形图上显示百分比
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2%}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 10), 
                    textcoords='offset points',
                    fontsize=12)

    plt.title('不同BMI分组的Y染色体浓度达标率', fontsize=16)
    plt.xlabel('孕妇BMI分组', fontsize=12)
    plt.ylabel('达标率', fontsize=12)
    plt.ylim(0, 1) # 将y轴范围设置为0到1（即0%到100%）
    plt.grid(True, linestyle='--', alpha=0.6, axis='y')
    plt.show()


if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    perform_qualification_rate_test(excel_filepath)
