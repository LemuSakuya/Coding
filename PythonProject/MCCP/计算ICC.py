#计算ICC值.py
import pandas as pd
import pingouin as pg
import numpy as np
from tqdm import tqdm
from openpyxl.styles import Font, Alignment, PatternFill 

def load_data():
    df = pd.read_excel('Sequential_teacher2.xlsx', sheet_name='Sheet1')
    df.set_index('教师编号', inplace=True)
    from scipy.stats import median_abs_deviation
    def detect_outliers(series, threshold=3):
        median = series.median()
        mad = median_abs_deviation(series, scale='normal')
        z_score = 0.6745 * (series - median) / mad
        return series[abs(z_score) > threshold]
    
    for expert in df.columns[1:]:
        outliers = detect_outliers(df[expert])
        print(f"{expert} 异常值：{outliers.tolist()}")
    
    return df

def calculate_individual_icc(data, expert):
    """
    计算单个专家与其他专家组的ICC值
    :param data: 评分数据框（教师×专家）
    :param expert: 当前专家名称
    :return: ICC值
    """
    other_experts = np.random.choice(
        [x for x in data.columns if x != expert], 
        size=min(3, len(data.columns)-1),
        replace=False
    )

    rating_matrix = data[[expert] + list(other_experts)].copy()

    long_format = rating_matrix.reset_index().melt(
        id_vars='教师编号',
        var_name='专家',
        value_name='评分'
    )
    
    try:
        icc = pg.intraclass_corr(
            data=long_format,
            targets='教师编号',
            raters='专家',
            ratings='评分'
        )
        return icc.loc[icc['Type'] == 'ICC2', 'ICC'].values[0]
    except:
        return np.nan

def main():
    df = load_data()

    results = []
    for expert in tqdm(df.columns, desc="计算ICC进度"):
        icc_value = calculate_individual_icc(df, expert)
        results.append({'专家': expert, 'ICC值': icc_value})

    icc_df = pd.DataFrame(results).sort_values('ICC值', ascending=False)

    print("\n各专家ICC值（降序排列）：")
    print(icc_df.to_string(index=False))

    with pd.ExcelWriter('专家ICC分析_逐个计算2.xlsx') as writer:
        icc_df.to_excel(writer, sheet_name='ICC结果', index=False)

        workbook = writer.book
        worksheet = writer.sheets['ICC结果']
    print("\n结果已保存到：专家ICC分析_逐个计算2.xlsx")

if __name__ == '__main__':
    main()