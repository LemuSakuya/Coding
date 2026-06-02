import torch

t = torch.randn(2, 10, 8)
print(t.size())
#/********** Begin *********/
# 输出张量`t`的大小转为`40*4`的大小
t = t.view(40, 4)
print(t.size())
# 在零位置插入尺寸为`1`的新张量，由此扩充原始张量`t`，输出变化后的 t
t = t.unsqueeze(0)
print(t.shape)
#/********** End *********/
