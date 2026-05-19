#encoding=utf8

def relu(x):
    '''
    x:负无穷到正无穷的实数
    '''
    #********* Begin *********#
    # 当输入x小于0时，输出0
    if x < 0:
        return 0

    # 当输入x大于等于0时，输出x本身
    return x

    #********* End *********#