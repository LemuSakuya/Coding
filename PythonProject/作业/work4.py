import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family']='SimHei'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.size']=8
plt.figure(figsize=(10,10))

########### Begin ############
# 导入pandas库，用于实现数据读取和数据分组汇总处理
import pandas as pd
import os

# 读取test目录下的gdp.csv文件，同时指定"年份"列的数据类型为字符串
df = pd.read_csv('test/gdp.csv', dtype={'年份': str})

# 以"省份"列为分组依据，对每个省份对应的"GDP"列进行求和运算，得到各省份的GDP总和
sj = df.groupby('省份')['GDP'].sum()

# 绘制饼图，数据为各省份GDP总和sj，设置饼图标签为省份名称（sj.index），并显示保留1位小数的百分比格式
plt.pie(sj, labels=sj.index, autopct='%.1f%%')

# 设置饼图的标题为"全国各地GDP饼图"，用于说明图表展示的核心内容
plt.title('全国各地GDP饼图')

# 将绘制完成的饼图保存到image7目录下，文件名为gdp7.jpg
os.makedirs('image7', exist_ok=True)
plt.savefig('image7/gdp7.jpg')

########### End ############