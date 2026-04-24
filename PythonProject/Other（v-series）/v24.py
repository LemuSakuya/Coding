# 从pandas库中导入Series和DataFrame类
from pandas import Series, DataFrame
import pandas as pd

def create_dataframe():
    '''
    函数功能:创建指定结构的DataFrame并添加新列
    返回值:
    df1: 一个符合要求的DataFrame类型数据,包含指定行列索引和新增列
    '''
    # 请在此添加代码 完成本关任务
    # ********** Begin *********#
    # 1. 构建字典数据，作为DataFrame的基础数据
    # 键为列名（states、pops、years），值为对应列的5行数据 
    dictionary = {
        # 第一列：states，5行数据均为1
        'states': [1, 1, 1, 1, 1],

        # 第二列：pops，5行数据均为2
        'pops': [2, 2, 2, 2, 2],

        # 第三列：years，5行数据均为3
        'years': [3, 3, 3, 3, 3]
    }
    
    # 2. 创建DataFrame对象df1
    # 参数1：字典数据；参数2：index指定行索引为['one','two','three','four','five']
    df1 = DataFrame(dictionary, index=['one', 'two', 'three', 'four', 'five'])
    
    # 3. 为df1新增列new_add，列值为[7,4,5,8,2]
    # 直接通过列名赋值的方式添加新列，数据长度需与DataFrame行数一致
    df1['new_add'] = [7, 4, 5, 8, 2]

    # ********** End **********#
    print(df1)
    # 返回创建并修改后的DataFrame对象
    return df1