import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

# 1. Set global style (disable Chinese fonts)
matplotlib.rcParams.update({'font.family': 'Arial'})
plt.style.use('seaborn-v0_8-whitegrid')

# 2. Data Loading (unchanged)
def load_data():
    teaching_21 = pd.read_excel('附件3.xlsx', sheet_name='21年参评教师教学成果')
    teaching_22 = pd.read_excel('附件3.xlsx', sheet_name='22年参评教师教学成果')
    research_21 = pd.read_excel('附件3.xlsx', sheet_name='21年参评教师科研成果')
    research_22 = pd.read_excel('附件3.xlsx', sheet_name='22年参评教师科研成果')
    return (
        pd.concat([teaching_21, teaching_22]),
        pd.concat([research_21, research_22])
    )

# 3. Data Preprocessing (unchanged)
def preprocess_teaching(df):
    award_map = {'国一':10, '国二':9, '国三':8, '省一':7, '省二':6, '省三':5,
                 '校一':4, '校二':3, '校三':2, '未获奖':0}
    df['指标6'] = df['指标6'].map(award_map).fillna(0)
    df['指标7'] = df['指标7'].map(award_map).fillna(0)
    if '指标15' in df.columns:
        df['指标15'] = df['指标15'].max() - df['指标15']
    teaching_cols = [f'指标{i}' for i in range(1,16)]
    for col in teaching_cols:
        if col not in df.columns:
            df[col] = 0
    return df[['教师\指标'] + teaching_cols]

def preprocess_research(df):
    award_map = {'国家级':10, '省一':8, '省二':6, '未获奖':0}
    if '指标8' in df.columns:
        df['指标8'] = df['指标8'].map(award_map).fillna(0)
    research_cols = [f'指标{i}' for i in range(1,11)]
    for col in research_cols:
        if col not in df.columns:
            df[col] = 0
    return df[['教师\指标'] + research_cols]

# 4. Enhanced Scoring Calculation
def calculate_scores(teaching_df, research_df):
    teaching_weights = [0.12,0.08,0.07,0.07,0.05,0.10,0.10,0.10,0.07,0.05,0.04,0.07,0.04,0.08,-0.05]
    research_weights = [0.15,0.10,0.12,0.08,0.10,0.10,0.08,0.15,0.07,0.05]
    
    teaching_scores = np.dot(teaching_df.iloc[:,1:].values, teaching_weights)
    research_scores = np.dot(research_df.iloc[:,1:].values, research_weights)
    
    result_df = pd.DataFrame({
        'TeacherID': teaching_df['教师\指标'],
        'TeachingScore': teaching_scores,
        'ResearchScore': research_scores
    })
    
    # Standardize scores
    result_df[['TeachingStd', 'ResearchStd']] = StandardScaler().fit_transform(
        result_df[['TeachingScore', 'ResearchScore']])
    
    # Composite score (60% teaching + 40% research)
    result_df['CompositeScore'] = 0.6*result_df['TeachingStd'] + 0.4*result_df['ResearchStd']
    result_df['FinalScore'] = MinMaxScaler(feature_range=(0,100)).fit_transform(
        result_df[['CompositeScore']])
    
    return result_df.sort_values('FinalScore', ascending=False)

# 5. Enhanced Visualization (English labels)
def generate_visualizations(result_df):
    # 1. Score Distribution
    plt.figure(figsize=(10,6))
    sns.histplot(result_df['FinalScore'], bins=20, kde=True, color='royalblue')
    plt.title('Distribution of Teacher Evaluation Scores', fontsize=14)
    plt.xlabel('Final Composite Score (0-100)')
    plt.ylabel('Count')
    plt.savefig('score_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Teaching vs Research (修正版)
    plt.figure(figsize=(10,6))
    scatter = plt.scatter(
        x=result_df['TeachingScore'],
        y=result_df['ResearchScore'],
        c=result_df['FinalScore'],
        cmap='viridis',
        s=100,
        alpha=0.7
    )
    plt.title('Teaching vs Research Performance', fontsize=14)
    plt.xlabel('Teaching Score (Raw)')
    plt.ylabel('Research Score (Raw)')
    
    # 正确添加颜色条的方式
    cbar = plt.colorbar(scatter)
    cbar.set_label('Final Score')
    
    plt.savefig('teaching_vs_research.png', dpi=300, bbox_inches='tight')
    plt.close()

# 6. Enhanced Report Generation
def generate_reports(result_df):
    # Report 1: Raw Scores
    raw_scores = result_df[['TeacherID', 'TeachingScore', 'ResearchScore', 'FinalScore']]
    raw_scores.to_excel('teacher_raw_scores.xlsx', index=False)
    
    # Report 2: Analysis Report
    report_stats = pd.DataFrame({
        'Metric': ['Mean', 'Median', 'Std Dev', 'Max', 'Min'],
        'Teaching': result_df['TeachingScore'].describe()[['mean','50%','std','max','min']].values,
        'Research': result_df['ResearchScore'].describe()[['mean','50%','std','max','min']].values,
        'Final': result_df['FinalScore'].describe()[['mean','50%','std','max','min']].values
    })
    
    with pd.ExcelWriter('teacher_analysis_report.xlsx') as writer:
        result_df.to_excel(writer, sheet_name='Full Results', index=False)
        report_stats.to_excel(writer, sheet_name='Statistics', index=False)
        
        # Add correlation matrix
        corr_matrix = result_df[['TeachingScore','ResearchScore','FinalScore']].corr()
        corr_matrix.to_excel(writer, sheet_name='Correlations')

# Main Execution
def main():
    # Load and preprocess
    teaching_df, research_df = load_data()
    teaching_processed = preprocess_teaching(teaching_df)
    research_processed = preprocess_research(research_df)
    
    # Calculate scores
    result_df = calculate_scores(teaching_processed, research_processed)
    
    # Generate outputs
    generate_visualizations(result_df)
    generate_reports(result_df)
    
    print("Processing completed. Generated:")
    print("- 2 Excel files: teacher_raw_scores.xlsx, teacher_analysis_report.xlsx")
    print("- 2 Visualization files: score_distribution.png, teaching_vs_research.png")

if __name__ == "__main__":
    main()