import pandas as pd
import numpy as np

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

def calculate_grouped_statistics(excel_filepath):
    
    try:
        # 默认从文件的第一行读取列标题
        df_raw = pd.read_excel(excel_filepath, sheet_name='男胎检测数据')
    except Exception as e:
        return

    # 数据清洗与准备
    df_raw.columns = df_raw.columns.str.strip()
    
    essential_cols = ['检测孕周', 'Y染色体浓度', '孕妇BMI']
    if not all(col in df_raw.columns for col in essential_cols):
        print(f"错误: 数据中缺少必要的列: {essential_cols}")
        return
    
    analysis_df = df_raw[essential_cols].copy()

    analysis_df['检测孕周(周)'] = analysis_df['检测孕周'].apply(parse_preg_week)
    
    # 强制将所有计算列转换为数值类型
    cols_to_convert = ['检测孕周(周)', 'Y染色体浓度', '孕妇BMI']
    for col in cols_to_convert:
        analysis_df[col] = pd.to_numeric(analysis_df[col], errors='coerce')

    # 最终清理
    analysis_df.dropna(subset=cols_to_convert, inplace=True)
    print(f"数据准备完成，共 {len(analysis_df)} 条有效记录。")

    # 根据我们的百分位数进行分组
    quartiles = [30.208806, 31.811598, 33.926237]
    labels = ['Q1(最低25%)', 'Q2(25-50%)', 'Q3(50-75%)', 'Q4(最高25%)']
    analysis_df['BMI分组'] = pd.cut(analysis_df['孕妇BMI'], 
                                   bins=[-np.inf, quartiles[0], quartiles[1], quartiles[2], np.inf], 
                                   labels=labels, right=True)
    
    analysis_df.dropna(subset=['BMI分组'], inplace=True)
    
    # 分组计算并打印描述性统计量
    print("\n步骤4: 正在计算各组内的基本统计量...")
    
    # 定义我们关心并希望进行统计的列
    cols_to_describe = ['孕妇BMI', '检测孕周(周)', 'Y染色体浓度']
    
    # 按'BMI分组'进行分组
    grouped_data = analysis_df.groupby('BMI分组')[cols_to_describe]
    
    # 使用 a dictionary to store results
    all_stats = {}
    for name, group in grouped_data:
        all_stats[name] = group.describe()

    # 清晰地打印每个组的结果
    for group_name, stats_df in all_stats.items():
        print("\n" + "="*50)
        print(f" BMI 分组: {group_name}")
        print("="*50)
        print(stats_df.to_string(formatters={
            '孕妇BMI': '{:,.2f}'.format,
            '检测孕周(周)': '{:,.2f}'.format,
            'Y染色体浓度': '{:,.4f}'.format,
        }))


if __name__ == '__main__':
    excel_filepath = r'E:\VSCode\Coding\Project\全国数学建模大赛\附件.xlsx'
    calculate_grouped_statistics(excel_filepath)
