import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 数据加载与预处理
def load_and_preprocess_data():
    # 加载教学成果数据
    teaching_21 = pd.read_excel('附件3.xlsx', sheet_name='21年参评教师教学成果')
    teaching_22 = pd.read_excel('附件3.xlsx', sheet_name='22年参评教师教学成果')
    
    # 加载科研成果数据
    research_21 = pd.read_excel('附件3.xlsx', sheet_name='21年参评教师科研成果')
    research_22 = pd.read_excel('附件3.xlsx', sheet_name='22年参评教师科研成果')
    
    # 加载教学质量评分数据（假设附件1和附件2已处理）
    # 这里需要根据实际情况加载教学质量评分数据
    # 以下为示例代码，实际应根据附件1和2处理
    score_21 = pd.read_excel('附件11.xlsx')  # 需要实际处理
    score_22 = pd.read_excel('附件2.xlsx')  # 需要实际处理
    
    return teaching_21, teaching_22, research_21, research_22, score_21, score_22

# 2. 数据合并与特征工程
def preprocess_teaching_data(df):
    # 奖项映射
    award_mapping = {
        '国一': 10, '国二': 9, '国三': 8,
        '省一': 7, '省二': 6, '省三': 5,
        '校一': 4, '校二': 3, '校三': 2,
        '未获奖': 0
    }
    
    # 处理奖项类指标
    award_cols = ['指标6', '指标7']
    for col in award_cols:
        if col in df.columns:
            df[col] = df[col].map(award_mapping).fillna(0)
    
    # 处理逆向指标（教学事故）
    if '指标15' in df.columns:
        df['指标15'] = df['指标15'].max() - df['指标15']  # 逆向处理
    
    # 填充缺失值
    df.fillna(0, inplace=True)
    
    return df

def preprocess_research_data(df):
    # 处理科研成果奖项
    award_mapping = {
        '国家级': 10, '省一': 8, '省二': 6,
        '未获奖': 0
    }
    
    if '指标8' in df.columns:
        df['指标8'] = df['指标8'].map(award_mapping).fillna(0)
    
    # 填充缺失值
    df.fillna(0, inplace=True)
    
    return df

# 3. 相关性分析
def analyze_correlation(teaching_df, research_df, score_df):
    # 合并数据
    merged_df = pd.merge(teaching_df, research_df, on='教师\指标', how='inner')
    merged_df = pd.merge(merged_df, score_df, on='教师\指标', how='inner')
    
    # 计算相关系数
    teaching_cols = [f'指标{i}' for i in range(1, 16)]
    research_cols = [f'指标{i}' for i in range(1, 11)]
    
    # 教学成果与教学质量的相关系数
    teaching_corr = merged_df[teaching_cols].corrwith(merged_df['教学质量评分'])
    
    # 科研成果与教学质量的相关系数
    research_corr = merged_df[research_cols].corrwith(merged_df['教学质量评分'])
    
    return teaching_corr, research_corr

# 4. 回归分析
def regression_analysis(teaching_df, research_df, score_df):
    # 合并数据
    merged_df = pd.merge(teaching_df, research_df, on='教师\指标', how='inner')
    merged_df = pd.merge(merged_df, score_df, on='教师\指标', how='inner')
    
    # 准备特征和目标变量
    teaching_cols = [f'指标{i}' for i in range(1, 16)]
    research_cols = [f'指标{i}' for i in range(1, 11)]
    
    X = merged_df[teaching_cols + research_cols]
    y = merged_df['教学质量评分']
    
    # 数据标准化
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # 线性回归模型
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 预测与评估
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    
    # 使用statsmodels进行详细回归分析
    X_sm = sm.add_constant(X_scaled)
    model_sm = sm.OLS(y, X_sm).fit()
    
    return model, model_sm, r2

# 5. 可视化分析
def visualize_results(teaching_corr, research_corr, model_sm):
    # 教学成果指标相关性可视化
    plt.figure(figsize=(12, 6))
    teaching_corr.sort_values().plot(kind='barh')
    plt.title('教学成果指标与教学质量的相关性')
    plt.xlabel('相关系数')
    plt.ylabel('指标')
    plt.show()
    
    # 科研成果指标相关性可视化
    plt.figure(figsize=(12, 6))
    research_corr.sort_values().plot(kind='barh')
    plt.title('科研成果指标与教学质量的相关性')
    plt.xlabel('相关系数')
    plt.ylabel('指标')
    plt.show()
    
    # 回归系数可视化
    coef_df = pd.DataFrame({
        '指标': teaching_corr + research_corr,
        '系数': model_sm.params[1:]  # 忽略截距项
    })
    
    plt.figure(figsize=(12, 8))
    coef_df.sort_values('系数').plot(kind='barh', x='指标', y='系数')
    plt.title('各指标对教学质量的回归系数')
    plt.show()

# 主程序
def main():
    # 1. 加载数据
    teaching_21, teaching_22, research_21, research_22, score_21, score_22 = load_and_preprocess_data()
    
    # 2. 数据预处理
    teaching_21_processed = preprocess_teaching_data(teaching_21)
    teaching_22_processed = preprocess_teaching_data(teaching_22)
    research_21_processed = preprocess_research_data(research_21)
    research_22_processed = preprocess_research_data(research_22)
    
    # 3. 合并两年数据
    teaching_all = pd.concat([teaching_21_processed, teaching_22_processed])
    research_all = pd.concat([research_21_processed, research_22_processed])
    score_all = pd.concat([score_21, score_22])  # 假设已处理
    
    # 4. 相关性分析
    teaching_corr, research_corr = analyze_correlation(teaching_all, research_all, score_all)
    print("教学成果指标与教学质量的相关性:")
    print(teaching_corr)
    print("\n科研成果指标与教学质量的相关性:")
    print(research_corr)
    
    # 5. 回归分析
    model, model_sm, r2 = regression_analysis(teaching_all, research_all, score_all)
    print("\n回归模型R²分数:", r2)
    print("\n回归模型详细摘要:")
    print(model_sm.summary())
    
    # 6. 可视化
    visualize_results(teaching_corr, research_corr, model_sm)
    
    # 7. 结果解释
    print("\n结论:")
    print("1. 教学成果指标中，指标X、指标Y等与教学质量有较强相关性")
    print("2. 科研成果指标中，指标A、指标B等与教学质量有一定相关性")
    print("3. 综合模型可以解释教学质量变异的XX%")
    print("4. 建议：可以结合教学成果和科研成果指标评价教学质量，但需注意...")

if __name__ == "__main__":
    main()