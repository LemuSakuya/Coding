import pandas as pd
import os

data_folder = r'E:\VSCode\Coding\Project\hot\附件'
# 打印文件列表和第一个文件的内容
print("文件列表:", os.listdir(data_folder))
sample_file = os.path.join(data_folder, os.listdir(data_folder)[0])
print("示例文件:", sample_file)

# 检查文件内容
df = pd.read_csv(sample_file)
print("列名:", df.columns.tolist())  # 查看实际列名
print("前2行数据:\n", df.head(2))