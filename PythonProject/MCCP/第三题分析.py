#第三题分析.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats
plt.style.use('seaborn-v0_8-whitegrid')

def load_and_merge_data():
    table1 = pd.read_excel('teacher_raw_scores.xlsx', sheet_name='Sheet1')

    table1['TeachingStd'] = stats.zscore(table1['TeachingScore'])
    table1['ResearchStd'] = stats.zscore(table1['ResearchScore'])
    
    return table1

def exploratory_analysis(df):
    desc_stats = df[['TeachingScore', 'ResearchScore', 'FinalScore']].describe()

    corr_matrix = df[['TeachingScore', 'ResearchScore', 'FinalScore']].corr()

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    sns.histplot(df['TeachingScore'], kde=True, ax=axes[0,0], color='royalblue')
    axes[0,0].set_title('Teaching Score Distribution')
    
    sns.histplot(df['ResearchScore'], kde=True, ax=axes[0,1], color='orange')
    axes[0,1].set_title('Research Score Distribution')

    sns.scatterplot(x='TeachingScore', y='ResearchScore', hue='FinalScore', 
                    data=df, palette='viridis', ax=axes[1,0], s=100)
    axes[1,0].set_title('Teaching vs Research Scores')

    sns.boxplot(data=df[['TeachingScore', 'ResearchScore']], ax=axes[1,1])
    axes[1,1].set_title('Score Distributions Comparison')
    
    plt.tight_layout()
    plt.savefig('exploratory_analysis.png', dpi=300)
    
    return desc_stats, corr_matrix

def build_regression_model(df):
    X = df[['TeachingStd', 'ResearchStd']]
    X = sm.add_constant(X)
    y = df['FinalScore']

    model = sm.OLS(y, X).fit()

    teaching_contribution = model.params['TeachingStd'] / (model.params['TeachingStd'] + model.params['ResearchStd'])
    research_contribution = 1 - teaching_contribution

    df['PredictedScore'] = model.predict(X)
    
    return model, teaching_contribution, research_contribution

def detect_anomalies(df):
    df['Residual'] = df['FinalScore'] - df['PredictedScore']
    
    threshold = 1.5 * df['Residual'].std()
    anomalies = df[np.abs(df['Residual']) > threshold]

    plt.figure(figsize=(10,6))
    sns.scatterplot(x='PredictedScore', y='Residual', data=df, hue=np.abs(df['Residual']) > threshold)
    plt.axhline(y=threshold, color='r', linestyle='--')
    plt.axhline(y=-threshold, color='r', linestyle='--')
    plt.title('Residual Analysis')
    plt.savefig('residual_analysis.png', dpi=300)
    
    return anomalies[['TeacherID', 'FinalScore', 'PredictedScore', 'Residual']]

if __name__ == "__main__":
    df = load_and_merge_data()

    desc_stats, corr_matrix = exploratory_analysis(df)
    print("描述性统计:\n", desc_stats)
    print("\n相关系数矩阵:\n", corr_matrix)

    model, teach_contri, research_contri = build_regression_model(df)
    print("\n回归模型摘要:")
    print(model.summary())

    anomalies = detect_anomalies(df)
    print("\n异常值检测结果:\n", anomalies)

    df.to_excel('processed_teacher_scores.xlsx', index=False)