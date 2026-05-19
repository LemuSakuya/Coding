import torch
t = torch.randn(2, 10, 8)
#/********** Begin *********/
# 将张量`t`的大小转为`40*4`，并在零位置插入尺寸为`1`的新张量，由此扩充原始张量`t`
#输出变化后的 t
t_new = t.view(40, 4).unsqueeze(0)
print(t_new)
#/********** End *********/
# 输出完整信息
print("原始张量形状：", t.size())
print("变形后张量形状：", t_new.size())
print("变形后张量维度：", t_new.dim())