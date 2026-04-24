# 导入pandas库的Series和DataFrame类
from pandas import Series, DataFrame
# 导入pandas库
import pandas as pd

def create_series():
    '''
    返回值:
    series_a: 一个Series类型数据
    series_b: 一个Series类型数据
    dict_a: 一个字典类型数据
    '''
    # 请在此添加代码 完成本关任务
    # ********** Begin *********#
    # 1. 创建series_a：数据为[1,2,5,7]，索引为['nu','li','xue','xi']
    series_a = Series([1, 2, 5, 7], index=['nu', 'li', 'xue', 'xi'])
    
    # 2. 创建dict_a字典，键值对为指定内容
    dict_a = {'ting': 1, 'shuo': 2, 'du': 32, 'xie': 44}
    
    # 3. 将dict_a字典转化为series_b（字典键自动作为索引）
    series_b = Series(dict_a)
    # ********** End **********#

    # 返回series_a, dict_a, series_b
    return series_a, dict_a, series_b