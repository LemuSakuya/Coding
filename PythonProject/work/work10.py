import torch

# /********** Begin *********/
# 创建32位有符号整数张量（一维）
def create():
    t = torch.IntTensor([0, 1, 2, 3, 4, 5])
    return t

# 获取张量
t = create()
print("原始张量：", t)
print()

# 正序索引
print("正序索引 t[2:5]：", t[2:5])

# 逆序索引
print("逆序索引 t[-4:-2]：", t[-4:-2])

# 步长切片
print("步长切片 t[2:6:3]：", t[2:6:3])

# /********** End *********/