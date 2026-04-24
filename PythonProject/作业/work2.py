import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family']='SimHei'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']

########### Begin ############
# 导入pandas库，用于数据读取和数据处理
import pandas as pd

# 读取test目录下的gdp.csv文件，指定"年份"列的数据类型为字符串
df = pd.read_csv('test/gdp.csv', dtype={'年份': str})

# 以"年份"列为分组依据，对每个分组内的"GDP"列进行求和运算，得到每年的GDP总和
gdp_sum = df.groupby('年份')['GDP'].sum()

# 创建一个新的绘图画布
plt.figure()

# 绘制折线图，x轴为分组后的年份索引，y轴为对应年份的GDP总和
plt.plot(gdp_sum.index, gdp_sum.values)

# 将绘制完成的图表保存到image3目录下，文件名为gdp.jpg
plt.savefig('image3/gdp.jpg')

########### End ############