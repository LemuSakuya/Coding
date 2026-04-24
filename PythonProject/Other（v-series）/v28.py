# 导入需要的标准化工具类/函数
import numpy as np
from sklearn.preprocessing import MinMaxScaler  # 导入最小-最大标准化类
from sklearn.preprocessing import scale        # 导入Z-score标准化函数
from sklearn.preprocessing import StandardScaler  # 导入Z-score标准化类
from sklearn.datasets import fetch_california_housing  # 导入加载加州房价数据集的函数

# 加载California housing数据集（指定数据存储路径为./step4/）
dataset = fetch_california_housing("./step4/")
# 提取完整特征矩阵X_full和目标变量y（房价）
X_full, y = dataset.data, dataset.target
# 抽取指定的两个特征：第0列MedInc（收入中位数）和第5列AveOccup（平均居住人数），组成新的特征矩阵X
X = X_full[:, [0, 5]]

def getMinMaxScalerValue():
    '''
    函数功能：对特征数据X进行MinMaxScaler（最小-最大）标准化转换，返回转换后的数据前5条
    返回值:
    X_first5 - 转换后前5条数据的列表
    '''
    X_first5 = []  # 初始化返回结果列表
    #   请在此添加实现代码   #
    # ********** Begin *********#
    # 1. 初始化MinMaxScaler对象，并用fit_transform直接完成"拟合+转换"
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # 2. 提取转换后数据的前5条，赋值给X_first5
    X_first5 = np.round(X_scaled[:5], 8)

    # ********** End **********#
    return X_first5

def getScaleValue():
    '''
    函数功能：对目标数据y进行简单scale（Z-score）标准化转换，返回转换后的数据前5条
    返回值:
    y_first5 - 转换后前5条数据的列表
    '''
    y_first5 = []  # 初始化返回结果列表
    #   请在此添加实现代码   #
    # ********** Begin *********#
    # 1. 用scale函数对目标变量y进行Z-score标准化，直接返回转换后的数据
    y_scaled = scale(y)
    # 2. 提取转换后数据的前5条，赋值给y_first5
    y_first5 = np.round(y_scaled[:5], 8)

    # ********** End **********#
    return y_first5

def getStandardScalerValue():
    '''
    函数功能：对特征数据X进行StandardScaler（Z-score）标准化转换，返回转换后的均值和缩放比例
    返回值:
    X_mean - 标准化时使用的各特征均值
    X_scale - 标准化时使用的各特征缩放比例（即标准差）
    '''
    X_mean = None  # 初始化均值变量
    X_scale = None  # 初始化缩放比例变量
    #   请在此添加实现代码   #
    #********** Begin *********#
    # 1. 初始化StandardScaler对象，并用fit方法拟合特征数据X
    scaler = StandardScaler()
    scaler.fit(X)

    # 2. 获取拟合后得到的各特征均值（mean_为StandardScaler的属性）
    X_mean = scaler.mean_

    # 3. 获取拟合后得到的各特征缩放比例（scale_为StandardScaler的属性，即标准差）
    X_scale = scaler.scale_

    #********** End **********#
    return X_mean,X_scale