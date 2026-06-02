import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family']='SimHei'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.size']='8'
plt.figure(figsize=(10,10))
########### Begin ############

# 导入pandas库，用于实现数据读取和数据筛选处理
import pandas as pd
import os

# 读取test目录下的gdp.csv文件，指定"年份"列的数据类型为字符串
data = pd.read_csv('test/gdp.csv', dtype={'年份': str})

# 定义子图索引变量i，用于指定后续子图的摆放位置，初始值为1
i = 1

# 循环遍历2010到2013年（range左闭右开，2014不包含，即遍历2010、2011、2012、2013）
for y in range(2010, 2014):
    # 筛选出数据中"年份"列等于当前循环年份的行，仅保留"省份"和"GDP"两列数据
    sj = data.loc[data['年份'] == str(y), ['省份', 'GDP']]
    # 创建子图，设置画布为2行2列的布局，当前绘制第i个子图
    plt.subplot(2, 2, i)
    # 绘制当前年份的饼图，饼图数据为该年份各省份的GDP，标签为对应省份名称
    plt.pie(sj['GDP'], labels=sj['省份'])
    # 设置当前子图的标题，显示为“当前年份+年”的格式，明确子图对应的年份
    plt.title(str(y) + '年')
    # 子图索引自增1，为下一次循环绘制下一个子图做准备
    i += 1

# 将绘制完成的2行2列子图（4个年份的GDP饼图）保存到image8目录下，文件名为gdp8.jpg
os.makedirs('image8', exist_ok=True)
plt.savefig('image8/gdp8.jpg')

########### End ############