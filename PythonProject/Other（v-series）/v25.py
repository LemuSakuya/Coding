# 导入pandas库并简写为pd
import pandas as pd

def read_csv_data():
    '''
    返回值:
    df1: 一个DataFrame类型数据（存储读取的CSV数据）
    length1: 一个int类型数据（存储DataFrame的总行数）
    '''
    # 请在此添加代码 完成本关任务
    # ********** Begin *********#
    # 读取指定路径的CSV文件，header=0表示以第一行作为列名
    df1 = pd.read_csv('test3/uk_rain_2014.csv', header=0)

    # 批量修改df1的列名为指定的简洁名称
    df1.columns = [
        'water_year',
        'rain_octsep',
        'outflow_octsep',
        'rain_decfeb',
        'outflow_decfeb',
        'rain_junaug',
        'outflow_junaug'
    ]


    # 计算df1的总行数并赋值给length1
    length1 = len(df1)

    print(length1)
    print(df1)
    # ********** End **********#
    #返回df1,length1
    return df1, length1