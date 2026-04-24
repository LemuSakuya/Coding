import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lifelines import LogLogisticAFTFitter

def parse_preg_week(week_str):
    try:
        if isinstance(week_str, str) and 'w+' in week_str:
            parts = week_str.split('w+')
            weeks = int(parts[0])
            days = int(parts[1])
            return round(weeks + days / 7.0, 2)
        return float(week_str)
    except (ValueError, TypeError, IndexError):
        return np.nan

def plot_grouped_survival_curves():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    try:
        df_raw = pd.read_excel(r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx', sheet_name='男胎检测数据')
    except Exception as e:
        return
    
    df_raw.columns = df_raw.columns.str.strip()
    analysis_df = df_raw[['检测孕周', 'Y染色体浓度', '孕妇BMI']].copy()
    
    threshold = 0.04
    analysis_df['T'] = analysis_df['检测孕周'].apply(parse_preg_week)
    analysis_df.dropna(subset=['T', '孕妇BMI'], inplace=True)
    
    # 创建BMI 50分位分组
    analysis_df['BMI分组'] = pd.qcut(analysis_df['孕妇BMI'], q=50, labels=False, duplicates='drop')

    num_groups = analysis_df['BMI分组'].nunique()
    print(f"BMI分组完成，根据50分位法，实际创建了 {num_groups} 个分组。")
    
    analysis_df['E_fail'] = (analysis_df['Y染色体浓度'] < threshold).astype(int)
    
    # 创建虚拟变量用于模型拟合
    regression_df_fail = pd.get_dummies(analysis_df, columns=['BMI分组'], drop_first=True, dtype=float)
    
    aft = LogLogisticAFTFitter()
    aft.fit(regression_df_fail[['T', 'E_fail'] + [col for col in regression_df_fail.columns if 'BMI分组_' in col]], 
            duration_col='T', event_col='E_fail')

    # 预测并绘图
    
    fig, ax = plt.subplots(figsize=(14, 9))

    # 设置颜色映射
    cmap = plt.get_cmap('viridis')
    unique_groups = sorted(analysis_df['BMI分组'].unique())
    norm = plt.Normalize(vmin=min(unique_groups), vmax=max(unique_groups))

    # 循环遍历每个分组并绘制其生存曲线
    dummy_cols = [col for col in regression_df_fail.columns if 'BMI分组_' in col]
    
    for group_idx in unique_groups:
        # 构建用于预测的条件DataFrame
        X_test = pd.DataFrame(columns=dummy_cols)
        X_test.loc[0] = 0 # 基线组
        
        # 为非基线组设置对应的虚拟变量为1
        dummy_col_name = f'BMI分组_{group_idx}'
        if dummy_col_name in X_test.columns:
            X_test[dummy_col_name] = 1
        
        # 预测生存函数
        survival_function = aft.predict_survival_function(X_test)
        
        # 获取颜色并绘图
        color = cmap(norm(group_idx))
        ax.plot(survival_function.index, survival_function.values, color=color, alpha=0.7)

    ax.set_title('Log-logistic AFT生存曲线 (按BMI 50分位数分组)', fontsize=18)
    ax.set_xlabel('检测孕周 (周)', fontsize=14)
    ax.set_ylabel('生存概率 (Y染色体浓度 >= 4.0%)', fontsize=14)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_ylim(bottom=min(0.45, ax.get_ylim()[0]), top=1.01)

    # 添加颜色条作为图例
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, ticks=np.linspace(min(unique_groups), max(unique_groups), 5))
    cbar.set_label('BMI 分位数组 (低 -> 高)', rotation=270, labelpad=20, fontsize=12)
    cbar.set_ticklabels(['最低', '较低', '中等', '较高', '最高'])
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    plot_grouped_survival_curves()

