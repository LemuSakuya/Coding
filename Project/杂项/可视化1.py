import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = r'E:\VSCode\Coding\Project\Data\MoleculeNet\bace.csv'
data = pd.read_csv(file_path)

# 选择前200个数据，这里只有10个数据所以选择全部
selected_data = data.head(200)

# 创建图形
plt.figure(figsize=(10, 5))

# 绘制折线图或柱状图，这里以柱状图为例
plt.bar(range(1, len(selected_data) + 1), selected_data['Class'], color='blue')

# 添加标题和标签
plt.title('BACE Result Visualization')
plt.xlabel('Data Index (1-10)')
plt.ylabel('Class Value')

# 显示图形
plt.show()
