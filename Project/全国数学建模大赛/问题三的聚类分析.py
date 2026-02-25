import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
except ImportError:
    exit()

def perform_clustering_analysis(excel_filepath):
    # 设置和加载数据
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    try:
        df_male = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
        df_female = pd.read_excel(excel_filepath, sheet_name='女胎检测数据')
        df_raw = pd.concat([df_male, df_female], ignore_index=True)
    except Exception as e:
        print(f"错误: 加载Excel文件失败。错误信息: {e}")
        return

    # 数据清洗与准备
    df_raw.columns = df_raw.columns.str.strip()
    
    # 选取您指定的变量
    variables_for_clustering = ['孕妇BMI', 'Y染色体的Z值', 'X染色体浓度', '被过滤掉读段数的比例', '生产次数']
    if not all(col in df_raw.columns for col in variables_for_clustering):
        print(f"错误: 数据中缺少必要的列。请确保以下列存在: {variables_for_clustering}")
        return
    
    analysis_df = df_raw[variables_for_clustering].copy()

    # 清洗和转换数据
    analysis_df['生产次数'] = pd.to_numeric(analysis_df['生产次数'].astype(str).str.replace('≥', ''), errors='coerce')
    # 对于女胎，Y染色体Z值为NaN，我们用0填充，这是一个中性值
    analysis_df['Y染色体的Z值'].fillna(0, inplace=True)
    
    # 删除任何剩余的缺失值
    initial_rows = len(analysis_df)
    analysis_df.dropna(inplace=True)
    print(f"  - 清理了 {initial_rows - len(analysis_df)} 条包含缺失值的记录。")
    print(f"数据准备完成，共 {len(analysis_df)} 条有效记录用于聚类。")

    # 数据标准化
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(analysis_df)

    # 确定最佳分组数 (K值)
    inertia = []
    k_range = range(2, 11)
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(scaled_data)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(10, 6))
    plt.plot(k_range, inertia, marker='o', linestyle='--')
    plt.xlabel('分组数量 (K)')
    plt.ylabel('簇内误差平方和 (Inertia)')
    plt.title('肘部法则确定最佳K值')
    plt.grid(True)
    plt.show()
    
    # 根据肘部法则，我们选择一个K值。通常是曲线变化最剧烈的“肘部”。
    OPTIMAL_K = 5
    print(f"根据肘部法则，我们选择将孕妇分为 {OPTIMAL_K} 组进行分析。")

    # 执行最终的K-Means聚类
    kmeans_final = KMeans(n_clusters=OPTIMAL_K, random_state=42, n_init=10)
    analysis_df['聚类分组'] = kmeans_final.fit_predict(scaled_data)
    print("聚类完成。")

    # 结果解读：聚类画像
    cluster_centers_scaled = kmeans_final.cluster_centers_
    cluster_centers_original = scaler.inverse_transform(cluster_centers_scaled)
    
    df_centers = pd.DataFrame(cluster_centers_original, columns=variables_for_clustering)
    df_centers['样本数量'] = analysis_df['聚类分组'].value_counts().sort_index()
    
    print(df_centers.to_string(formatters={col: '{:,.2f}'.format for col in df_centers.columns}))

    # 可视化聚类结果
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(scaled_data)
    df_pca = pd.DataFrame(data=principal_components, columns=['主成分1', '主成分2'])
    df_pca['聚类分组'] = analysis_df['聚类分组'].values

    plt.figure(figsize=(12, 8))
    sns.scatterplot(x='主成分1', y='主成分2', hue='聚类分组', data=df_pca, palette='viridis', s=50, alpha=0.7)
    plt.title('孕妇聚类分析结果可视化 (PCA降维)', fontsize=16)
    plt.xlabel('主成分1')
    plt.ylabel('主成分2')
    plt.legend(title='聚类分组')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    perform_clustering_analysis(excel_filepath)
