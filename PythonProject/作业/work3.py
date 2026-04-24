import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family']='SimHei'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']

########### Begin ############
# 定义y轴数据列表，存储各位老师对应的平均分
import numpy as np
y = [84.12, 81.83, 79.89, 78.19, 76.83, 75.09, 74.58, 73.71]

# 创建一个新的绘图画布，为后续绘制条形图提供载体
plt.figure()

# 生成x轴的位置索引，从1开始，长度与y轴数据列表一致
sj = np.linspace(1, 8, 8)

# 根据x轴位置索引sj和y轴数据y绘制条形图，设置条形宽度为0.5，条形颜色为蓝色
plt.bar(sj, height=y, width=0.5, color='b')

# 定义x轴的标签文本列表，存储各位老师的姓名，与平均分数据顺序一一对应
x = ['何老师', '张老师', '蒋老师', '黄老师', '王老师', '李老师', '唐老师', '刘老师']

# 将x轴的位置索引sj替换为对应的老师姓名标签x，让图表x轴更具可读性
plt.xticks(sj, x)

# 设置图表的标题为“平均成绩”，用于说明图表展示的核心内容
plt.title('平均成绩')

# 将绘制完成的条形图保存到image4目录下，文件名为tzt.jpg
import os
os.makedirs('image4', exist_ok=True)
plt.savefig('image4/tzt.jpg')

########### End ############