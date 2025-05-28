import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from scipy.linalg import eig

# 全局设置
matplotlib.rcParams.update({'font.family': 'Arial'})
plt.style.use('seaborn-v0_8-whitegrid')

# 1. 数据加载
def load_data():
    teaching_21 = pd.read_excel('附件3.xlsx', sheet_name='21年参评教师教学成果')
    teaching_22 = pd.read_excel('附件3.xlsx', sheet_name='22年参评教师教学成果')
    research_21 = pd.read_excel('附件3.xlsx', sheet_name='21年参评教师科研成果')
    research_22 = pd.read_excel('附件3.xlsx', sheet_name='22年参评教师科研成果')
    return (
        pd.concat([teaching_21, teaching_22]),
        pd.concat([research_21, research_22])
    )

# 2. 数据预处理
def preprocess_teaching(df):
    # 奖项量化映射
    award_map = {'国一':10, '国二':9, '国三':8, '省一':7, '省二':6, '省三':5,
                 '校一':4, '校二':3, '校三':2, '未获奖':0}
    df['指标6'] = df['指标6'].map(award_map).fillna(0)
    df['指标7'] = df['指标7'].map(award_map).fillna(0)
    
    # 逆向指标处理（教学事故）
    if '指标15' in df.columns:
        df['指标15'] = df['指标15']  # 保持原值，后续计算时作为惩罚项
    
    # 确保所有指标列存在
    teaching_cols = [f'指标{i}' for i in range(1,16)]
    for col in teaching_cols:
        if col not in df.columns:
            df[col] = 0
    
    return df[['教师\指标'] + teaching_cols]

def preprocess_research(df):
    # 科研成果奖项量化
    award_map = {'国家级':10, '省一':8, '省二':6, '未获奖':0}
    if '指标8' in df.columns:
        df['指标8'] = df['指标8'].map(award_map).fillna(0)
    
    # 确保所有指标列存在
    research_cols = [f'指标{i}' for i in range(1,11)]
    for col in research_cols:
        if col not in df.columns:
            df[col] = 0
    
    return df[['教师\指标'] + research_cols]

# 3. AHP权重计算
def calculate_ahp_weights():
    # 教学指标判断矩阵（14个正向指标，示例矩阵需根据实际情况调整）
    teaching_matrix = np.array([
        [1, 3, 5, 3, 3, 7, 7, 5, 3, 2, 2, 3, 1, 3],
        [1/3, 1, 3, 2, 2, 5, 5, 3, 2, 1, 1, 2, 1/2, 2],
        [1/5, 1/3, 1, 1/2, 1/2, 3, 3, 2, 1, 1/2, 1/2, 1, 1/3, 1],
        [1/3, 1/2, 2, 1, 1, 3, 3, 2, 1, 1/2, 1/2, 1, 1/3, 1],
        [1/3, 1/2, 2, 1, 1, 3, 3, 2, 1, 1/2, 1/2, 1, 1/3, 1],
        [1/7, 1/5, 1/3, 1/3, 1/3, 1, 1, 1/2, 1/3, 1/4, 1/4, 1/3, 1/5, 1/3],
        [1/7, 1/5, 1/3, 1/3, 1/3, 1, 1, 1/2, 1/3, 1/4, 1/4, 1/3, 1/5, 1/3],
        [1/5, 1/3, 1/2, 1/2, 1/2, 2, 2, 1, 1/2, 1/3, 1/3, 1/2, 1/4, 1/2],
        [1/3, 1/2, 1, 1, 1, 3, 3, 2, 1, 1/2, 1/2, 1, 1/3, 1],
        [1/2, 1, 2, 2, 2, 4, 4, 3, 2, 1, 1, 2, 1/2, 2],
        [1/2, 1, 2, 2, 2, 4, 4, 3, 2, 1, 1, 2, 1/2, 2],
        [1/3, 1/2, 1, 1, 1, 3, 3, 2, 1, 1/2, 1/2, 1, 1/3, 1],
        [1, 2, 3, 3, 3, 5, 5, 4, 3, 2, 2, 3, 1, 3],
        [1/3, 1/2, 1, 1, 1, 3, 3, 2, 1, 1/2, 1/2, 1, 1/3, 1]
    ])
    
    # 科研指标判断矩阵（10个指标）
    research_matrix = np.array([
    # 指标: 1  2  3  4  5  6  7  8  9 10
    [1, 5, 3, 5, 3, 3, 5, 1, 5, 7],  # 指标1
    [1/5,1,1/3,1,1/3,1/3,1,1/5,1,3],  # 指标2
    [1/3,3,1,3,1,1,3,1/3,3,5],  # 指标3
    [1/5,1,1/3,1,1/3,1/3,1,1/5,1,3],  # 指标4
    [1/3,3,1,3,1,1,3,1/3,3,5],  # 指标5
    [1/3,3,1,3,1,1,3,1/3,3,5],  # 指标6
    [1/5,1,1/3,1,1/3,1/3,1,1/5,1,3],  # 指标7
    [1,5,3,5,3,3,5,1,5,7],  # 指标8
    [1/5,1,1/3,1,1/3,1/3,1,1/5,1,3],  # 指标9
    [1/7,1/3,1/5,1/3,1/5,1/5,1/3,1/7,1/3,1]  # 指标10
])
    
    def calculate_weights(matrix):
        # 几何平均法计算权重
        n = matrix.shape[0]
        geom_means = np.prod(matrix, axis=1) ** (1/n)
        weights = geom_means / np.sum(geom_means)
        
        # 一致性检验
        eigenvalues, _ = eig(matrix)
        lambda_max = np.max(eigenvalues.real)
        CI = (lambda_max - n) / (n - 1)
        RI = {1:0, 2:0, 3:0.58, 4:0.90, 5:1.12, 6:1.24, 7:1.32, 8:1.41, 9:1.45, 10:1.49, 
              11:1.51, 12:1.54, 13:1.56, 14:1.58, 15:1.59}.get(n, 1.6)
        CR = CI / RI
        
        if CR > 0.1:
            print(f"警告: 判断矩阵一致性不通过 (CR={CR:.3f})")
        
        return weights
    
    teaching_weights = calculate_weights(teaching_matrix)
    research_weights = calculate_weights(research_matrix)
    
    # 教学惩罚系数（指标15）
    penalty_weight = 0.05
    
    return teaching_weights, research_weights, penalty_weight

# 4. 综合评分计算
def calculate_scores(teaching_df, research_df):
    # 获取AHP权重
    teaching_weights, research_weights, penalty_weight = calculate_ahp_weights()
    
    # 教学得分计算（前14个正向指标）
    teaching_scores = np.dot(teaching_df.iloc[:,1:15].values, teaching_weights)
    
    # 教学惩罚项（指标15）
    penalty = teaching_df['指标15'].values * penalty_weight
    
    # 科研得分计算
    research_scores = np.dot(research_df.iloc[:,1:11].values, research_weights)
    
    # 构建结果DataFrame
    result_df = pd.DataFrame({
        'TeacherID': teaching_df['教师\指标'],
        'TeachingScore': teaching_scores,
        'TeachingPenalty': penalty,
        'ResearchScore': research_scores
    })
    
    # 计算净教学得分（教学得分-惩罚）
    result_df['NetTeachingScore'] = result_df['TeachingScore'] - result_df['TeachingPenalty']
    
    # 标准化得分（0-100分）
    scaler = MinMaxScaler(feature_range=(0, 100))
    result_df[['TeachingStd', 'ResearchStd']] = scaler.fit_transform(
        result_df[['NetTeachingScore', 'ResearchScore']])
    
    # 综合得分（60%教学 + 40%科研）
    result_df['CompositeScore'] = 0.6*result_df['TeachingStd'] + 0.4*result_df['ResearchStd']
    result_df['FinalScore'] = scaler.fit_transform(result_df[['CompositeScore']])
    
    return result_df.sort_values('FinalScore', ascending=False)

# 5. 可视化分析
def generate_visualizations(result_df):
    # 1. 最终得分分布
    plt.figure(figsize=(10, 6))
    sns.histplot(result_df['FinalScore'], bins=20, kde=True, color='royalblue')
    plt.title('Distribution of Final Evaluation Scores', fontsize=14)
    plt.xlabel('Final Score (0-100)')
    plt.ylabel('Count')
    plt.savefig('final_score_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. 教学vs科研散点图
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        x=result_df['TeachingStd'],
        y=result_df['ResearchStd'],
        c=result_df['FinalScore'],
        cmap='viridis',
        s=100,
        alpha=0.7
    )
    plt.colorbar(scatter).set_label('Final Score')
    plt.title('Teaching vs Research Performance', fontsize=14)
    plt.xlabel('Standardized Teaching Score (0-100)')
    plt.ylabel('Standardized Research Score (0-100)')
    plt.savefig('teaching_vs_research.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. 前20名教师得分对比
    top20 = result_df.head(20)
    plt.figure(figsize=(12, 8))
    top20['TeacherID'] = top20['TeacherID'].astype(str)  # 确保教师ID为字符串
    top20.plot(x='TeacherID', y=['TeachingStd', 'ResearchStd', 'FinalScore'],
               kind='bar', figsize=(12, 6))
    plt.title('Top 20 Teachers: Score Comparison', fontsize=14)
    plt.xlabel('Teacher ID')
    plt.ylabel('Score (0-100)')
    plt.xticks(rotation=45)
    plt.legend(['Teaching', 'Research', 'Composite'])
    plt.tight_layout()
    plt.savefig('top20_score_comparison.png', dpi=300)
    plt.close()

# 6. 结果报告生成
def generate_reports(result_df):
    # 原始得分数据
    result_df.to_excel('teacher_evaluation_results.xlsx', index=False)
    
    # 统计分析报告
    stats_report = pd.DataFrame({
        'Metric': ['Mean', 'Median', 'Std Dev', 'Max', 'Min', 'Q1 (25%)', 'Q3 (75%)'],
        'TeachingScore': result_df['TeachingScore'].describe()[['mean','50%','std','max','min','25%','75%']].values,
        'ResearchScore': result_df['ResearchScore'].describe()[['mean','50%','std','max','min','25%','75%']].values,
        'FinalScore': result_df['FinalScore'].describe()[['mean','50%','std','max','min','25%','75%']].values
    })
    
    with pd.ExcelWriter('evaluation_analysis_report.xlsx') as writer:
        result_df.to_excel(writer, sheet_name='Full Results', index=False)
        stats_report.to_excel(writer, sheet_name='Statistics', index=False)
        
        # 相关系数矩阵
        corr_matrix = result_df[['TeachingScore','ResearchScore','FinalScore']].corr()
        corr_matrix.to_excel(writer, sheet_name='Correlations')

# 主程序
def main():
    print("Loading and preprocessing data...")
    teaching_df, research_df = load_data()
    teaching_processed = preprocess_teaching(teaching_df)
    research_processed = preprocess_research(research_df)
    
    print("Calculating AHP weights and scores...")
    result_df = calculate_scores(teaching_processed, research_processed)
    
    print("Generating visualizations and reports...")
    generate_visualizations(result_df)
    generate_reports(result_df)
    
    print("\nEvaluation completed. Generated files:")
    print("- teacher_evaluation_results.xlsx (原始得分数据)")
    print("- evaluation_analysis_report.xlsx (统计分析报告)")
    print("- final_score_distribution.png (得分分布图)")
    print("- teaching_vs_research.png (教学vs科研散点图)")
    print("- top20_score_comparison.png (前20名教师得分对比图)")
    
    # 打印前10名教师
    print("\nTop 10 Teachers:")
    print(result_df[['TeacherID', 'FinalScore']].head(10).to_string(index=False))

if __name__ == "__main__":
    main()