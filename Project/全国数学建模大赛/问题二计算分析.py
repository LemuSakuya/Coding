import pandas as pd
import math

EPSILON = 2.944

def calculate_predicted_weeks(bmi):
    # 计算 log(T)，这里的 log 是指自然对数 (ln)
    log_T = 1.2703 + (0.0184 * bmi) + (0.1519 * EPSILON)
    
    # T = e^(log(T))，使用 math.exp() 进行计算
    T = math.exp(log_T)
    
    return T

# 定义输入数据
group_names = ['较低BMI组', '中等BMI组', '较高BMI组']
# 基于代表性BMI值，我们假设BMI区间如下
bmi_ranges = ['< 31.81', '31.81 - 35.96', '≥ 35.97'] 
representative_bmis = [31.80, 35.96, 46.88]


# 执行计算
predicted_weeks_list = []

for bmi in representative_bmis:
    # 使用我们的公式进行准确计算
    p_weeks = calculate_predicted_weeks(bmi)
    predicted_weeks_list.append(p_weeks)

# 整理并输出结果
final_data = {
    '分组名称': group_names,
    'BMI区间': bmi_ranges,
    '代表性BMI': representative_bmis,
    '预测的P95达标孕周 (周)': [round(pw, 2) for pw in predicted_weeks_list], # 将结果四舍五入到两位小数
    '最佳NIPT时点 (建议)':  [f"孕{round(pw)}周" for pw in predicted_weeks_list] # 格式化为 "孕X周"
}

df = pd.DataFrame(final_data)
df = df.set_index('分组名称')

# 打印输出表格
print(f"Epsilon = {EPSILON} 的结果")
print(df.to_string())
