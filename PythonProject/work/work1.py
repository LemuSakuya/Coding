import os
import matplotlib

matplotlib.use('Agg')

# 导入numpy
import numpy as np

# 导入matplotlib
import matplotlib.pyplot as plt

########### Begin ############
# 建立宽度10高度5的画布；
plt.figure(figsize=(10, 5))

# 在0到pi之间建立20个点；
x = np.linspace(0, np.pi, 20)

# 绘制y=sin(x)的折线图；
y = np.sin(x)
plt.plot(x, y)

# 将图片存为image1文件夹的zxt.jpg。
os.makedirs('image1', exist_ok=True)
plt.savefig('image1/zxt.jpg')

########### End ############
