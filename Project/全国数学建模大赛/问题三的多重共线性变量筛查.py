import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

try:
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tools.tools import add_constant
except ImportError:
    exit()

def select_variables_with_vif(excel_filepath, vif_threshold=5):
    # 设置和加载数据
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    try:
        df_raw = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        print(f"错误: 加载Excel文件失败。错误信息: {e}")
        return

    df_raw.columns = df_raw.columns.str.strip()
    
    # 选取所有数值类型的列进行分析
    df_numeric = df_raw.select_dtypes(include=np.number)
    
    # 移除ID、目标变量和方差为0的列
    cols_to_drop = [col for col in ['序号', 'Y染色体浓度'] if col in df_numeric.columns]
    df_numeric = df_numeric.drop(columns=cols_to_drop)
    df_numeric = df_numeric.loc[:, df_numeric.var() != 0]
    
    # 清理缺失值
    df_clean = df_numeric.dropna()
    print(f"数据准备完成，共 {len(df_clean.columns)} 个数值型自变量用于筛选。")

    # 迭代筛选变量
    variables = df_clean.copy()
    dropped_variables = []
    
    # 定义一个函数来计算VIF
    def calculate_vif(df):
        X = add_constant(df.values)
        vif_data = pd.Series([variance_inflation_factor(X, i) for i in range(X.shape[1])], 
                             index=['const'] + df.columns.tolist())
        return vif_data.drop('const')

    iteration = 1
    while True:
        print(f"\n--- 第 {iteration} 轮迭代 ---")
        vif_scores = calculate_vif(variables)
        max_vif = vif_scores.max()
        
        print("当前VIF分数:")
        print(vif_scores.to_string())
        
        if max_vif > vif_threshold:
            # 找到VIF值最高的变量
            variable_to_drop = vif_scores.idxmax()
            dropped_variables.append(variable_to_drop)
            # 从数据框中移除该变量
            variables = variables.drop(columns=[variable_to_drop])
            print(f"\n决策: VIF最高值: {max_vif:.2f} (变量: '{variable_to_drop}') > {vif_threshold}。")
            print(f"正在移除 '{variable_to_drop}'...")
            iteration += 1
        else:
            # 如果所有VIF都低于阈值，则结束循环
            print(f"\n决策: VIF最高值 {max_vif:.2f} <= {vif_threshold}。")
            print("所有变量的VIF值均已低于阈值，筛选完成。")
            break
            
    # 报告结果
    print("\n" + "="*50)
    print("多重共线性筛选结果:")
    print("="*50)
    
    print("\n被剔除的变量列表:")
    if dropped_variables:
        for var in dropped_variables:
            print(f"- {var}")
    else:
        print("无")
        
    print("\n最终保留的变量及其VIF值:")
    final_vif = calculate_vif(variables)
    print(final_vif.to_string())
    print("\n" + "="*50)
    print("您现在可以使用这组筛选后的变量来构建最终的模型。")


if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    # 将阈值设为更严格的1.5，以进行更多轮迭代筛选
    select_variables_with_vif(excel_filepath, vif_threshold=1.5)

