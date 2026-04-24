import pandas as pd
import math

EPSILON = 2.944

def calculate_predicted_weeks(bmi):
    # 计算 log(T)，这里的 log 是指自然对数 (ln)
    log_T = 1.2703 + (0.0184 * bmi) + (0.1519 * EPSILON)
    
    # T = e^(log(T))，使用 math.exp() 进行计算
    T = math.exp(log_T)
    
    return T

def get_risk_level(weeks):
    if weeks <= 12:
        return "低风险"
    elif 13 <= weeks <= 27:
        return "高风险"
    else: # weeks >= 28
        return "极高风险"

# 定义输入数据
group_names = ['较低BMI组', '中等BMI组', '较高BMI组']
bmi_ranges = ['< 31.81', '31.81 - 35.96', '≥ 35.97'] 
representative_bmis = [31.80, 35.96, 46.88]


# 执行计算
predicted_weeks_list = []
risk_level_list = [] # 新增列表，用于存储风险等级

for bmi in representative_bmis:
    # 使用我们的公式进行准确计算
    p_weeks = calculate_predicted_weeks(bmi)
    predicted_weeks_list.append(p_weeks)
    
    # 根据预测的孕周计算风险等级
    risk = get_risk_level(p_weeks)
    risk_level_list.append(risk)

# 整理并输出结果
final_data = {
    '分组名称': group_names,
    'BMI区间': bmi_ranges,
    '代表性BMI': representative_bmis,
    '预测的P95达标孕周 (周)': [round(pw, 2) for pw in predicted_weeks_list],
    '最佳NIPT时点 (建议)':  [f"孕{round(pw)}周" for pw in predicted_weeks_list],
    '潜在风险等级': risk_level_list # 将风险等级添加到最终数据中
}

df = pd.DataFrame(final_data)
df = df.set_index('分组名称')

# 打印输出表格
print(f"--- 基于 Epsilon = {EPSILON} 的计算与风险分析结果 ---")
print(df.to_string())

