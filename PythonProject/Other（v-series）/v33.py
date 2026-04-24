# 导入numpy库
import numpy as np
# 接收输入转列表
list_input = eval(input())  # 变量名改为list_input，避免覆盖内置list
# 列表转numpy数组
arrx = np.array(list_input)
########## Begin ##########
# 1. 数组元素求和
sum_result = np.sum(arrx)

# 2. 计算数组元素中的最大值
max_result = np.max(arrx)

# 3. 计算数组元素中的最小值
min_result = np.min(arrx)

# 4. 计算数组元素中的平均值
mean_result = np.mean(arrx)


# 5. 计算数组元素中的标准差
std_result = np.std(arrx)

# 6. 计算数组元素的绝对值
abs_arr = np.abs(arrx)

########## End ##########

# 依次输出所有计算结果
print("求和结果：", sum_result)
print("最大值：", max_result)
print("最小值：", min_result)
print("平均值：", mean_result)
print("标准差：", std_result)
print("绝对值数组：", abs_arr)