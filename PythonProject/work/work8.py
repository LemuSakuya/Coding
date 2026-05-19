import numpy as np


def mlp_and(x1, x2):
    r'''
    使用感知机实现与逻辑门。

    参数：
    - x1: int (0 or 1)
    - x2: int (0 or 1)

    输出：
    - y: int (0 or 1)
        y = x1 and x2
    '''
    ########## Begin ##########
    x = np.array([x1, x2]).astype(np.float32)
    weight = np.array([0.5, 0.5]).astype(np.float32)
    bias = -0.7
    y = np.dot(weight, x) + bias
    if y <= 0:
        return 0
    else:
        return 1
    ########## End ##########


def mlp_or(x1, x2):
    r'''
    使用感知机实现或逻辑门。

    参数：
    - x1: int (0 or 1)
    - x2: int (0 or 1)

    输出：
    - y: int (0 or 1)
        y = x1 or x2
    '''
    ########## Begin ##########
    x = np.array([x1, x2]).astype(np.float32)
    weight = np.array([0.5, 0.5]).astype(np.float32)
    bias = -0.2
    y = np.dot(weight, x) + bias
    if y <= 0:
        return 0
    else:
        return 1
    ########## End ##########


def mlp_nand(x1, x2):
    r'''
    使用感知机实现与非逻辑门。

    参数：
    - x1: int (0 or 1)
    - x2: int (0 or 1)

    输出：
    - y: int (0 or 1)
        y = x1 nand x2
    '''
    ########## Begin ##########
    x = np.array([x1, x2]).astype(np.float32)
    weight = np.array([-0.5, -0.5]).astype(np.float32)
    bias = 0.7
    y = np.dot(weight, x) + bias
    if y <= 0:
        return 0
    else:
        return 1
    ########## End ##########

