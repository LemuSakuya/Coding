import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

def analyze_x_chromosome():
    try:
        file_path = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
        sheet_name = '女胎检测数据'
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        plt.rcParams['font.sans-serif'] = ['SimHei'] 
        plt.rcParams['axes.unicode_minus'] = False 
        df_clean = df[['染色体的非整倍体', 'X染色体浓度']].dropna(subset=['X染色体浓度'])

        df_clean['胎儿状态'] = np.where(df_clean['染色体的非整倍体'].notna(), '异常', '正常')

        # 数据标准化
        scaler = StandardScaler()

        # 对 'X染色体浓度' 数据进行标准化
        x_concentration = df_clean['X染色体浓度'].values.reshape(-1, 1)
        df_clean['X染色体浓度_标准化'] = scaler.fit_transform(x_concentration)
        
        print("数据预览：")
        print(df_clean.head())
        print("\n各状态胎儿数量统计：")
        print(df_clean['胎儿状态'].value_counts())

        # 可视化对比
        plt.figure(figsize=(12, 7))
        sns.histplot(data=df_clean, x='X染色体浓度_标准化', hue='胎儿状态', 
                     multiple='layer', kde=True, stat='density', common_norm=False, 
                     alpha=0.5, bins=30)

        # 添加图表元素
        plt.title('标准化X染色体浓度在正常与异常女胎中的分布对比柱状图', fontsize=16)
        plt.xlabel('标准化的X染色体浓度 (Z-score)', fontsize=12)
        plt.ylabel('密度', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(title='胎儿状态', labels=['异常', '正常'])

        # 显示图表
        plt.show()

    except FileNotFoundError:
        return
    except Exception as e:
        return

if __name__ == '__main__':
    analyze_x_chromosome()

