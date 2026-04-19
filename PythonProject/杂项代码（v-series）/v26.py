import numpy as np
import pandas as pd
from sklearn import datasets

def demo3():
    # 加载鸢尾花数据集的特征数据
    iris = datasets.load_iris().data
    #********** Begin **********#
    # 1. 将鸢尾花数据转换为DataFrame，指定列名为a、b、c、d
    df = pd.DataFrame(iris, columns=list("abcd"))
    # 2. 截取前30行数据
    data = df.iloc[:30, :]
    print("原始数据：\n", data.head(3), "\n")  # 打印前3行预览

    # 3. 每行数据减去第一行对应列的值
    df1 = data - data.iloc[0]
    print("每行减去第一行后的数据：\n", df1.head(3), "\n")

    # 4. 将所有小于0的值替换为缺失值（np.nan）
    df1[df1 < 0] = np.nan
    
    print("替换小于0的值为缺失值后：\n", df1.head(3), "\n")

    # 4.1 检测缺失值：isnull()标记缺失值（True表示缺失）
    null_mask = df1.isnull()
    print("缺失值掩码（True=缺失）：\n", null_mask.head(3), "\n")

    # 4.2 检测非缺失值：notnull()
    notnull_mask = df1.notnull()
    print("非缺失值掩码（True=非缺失）：\n", notnull_mask.head(3), "\n")

    # 4.3 统计每行列缺失值数量,按行统计缺失值
    null_count = df1.isnull().sum(axis=1)
    
    print("每行缺失值数量：\n", null_count.head(3), "\n")

    # 5. 删除非缺失值数量不足2的行
    df2 = df1.dropna(thresh=2)
    print("删除非缺失值<2的行后：\n", df2.head(3), "\n")

    # 6. 前向填充（ffill）缺失值：用前一行有效值填充
    df3 = df2.ffill()
    
    print("前向填充缺失值后的最终结果：\n", df3.head(3))

    #********** End **********#