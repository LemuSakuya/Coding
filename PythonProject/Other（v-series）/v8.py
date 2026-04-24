#(1)
print("(1):")
#创建字典
my_dict = {'apple': 3, 'banana': 5, 'orange': 2}

#添加键值对
my_dict['pear'] = 4

#删除键值对
del my_dict['orange']
my_dict.pop('banana')

#更新键值对
my_dict['apple'] = 2

#访问键值对
print(my_dict['apple'])
print(my_dict.get('pear'))
print("\n")

#(2)
print("(2):")
key = {'高等数学': 37, '线性代数': 88, '程序设计基础': 90, '大学英语': 73}
value = list(key.values())
print("最高成绩是",max(value))
print("最低成绩是",min(value))
print("平均成绩是",sum(value)/len(value))
print("\n")

#(3)
print("(3):")
students = {}

for i in range(1, 6):
    name = input(f"请输入第{i}位学生姓名喵~:")
    subjects = {}
    print(f"请依次输入{name}的五门课程及成绩喵~:")
    
    for j in range(1, 6):
        course = input(f"课程{j}名称:").strip()
        score = float(input(f"课程{j}分数:"))
        subjects[course] = score
    
    students[name] = subjects

while 1:
    query = input("\n请输入要查询的学生姓名喵~(输入q退出捏~)").strip()
    
    if query.lower() == 'q':
        break
    
    if query not in students:
        print("该学生不存在！😡.jpg")
        continue
    
    scores = students[query]
    
    subject_max = max(scores.items(), key=lambda x: x[1])
    
    print(f"\n{query}的成绩分析：")
    print(f"最高分科目：{subject_max[0]}，成绩：{subject_max[1]}")
print("\n")

#(4)
print("(4):")
def find_top_student(students_data):
    max_avg = -1
    top_students = []
    
    for name, scores in students_data.items():
        avg = sum(scores.values()) / len(scores)
        
        if avg > max_avg:
            max_avg = avg
            top_students = [name]
        elif avg == max_avg:
            top_students.append(name)
    
    return top_students, max_avg

while 1:
    query = input("\n输入avg显示最高平均分:").strip()
    
    if query.lower() == 'q':
        break
    elif query.lower() == 'avg':
        best_students, highest_avg = find_top_student(students)
        
        if len(best_students) == 1:
            print(f"最高平均分:{highest_avg:.2f}")
            print(f"获得学生:{best_students[0]}")
        else:
            print(f"并列最高平均分:{highest_avg:.2f}")
            print("获奖学生：", "、".join(best_students))
        continue
print("\n")