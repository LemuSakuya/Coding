import time

#(1)
list_names = ['zyh', 'xpy', 'yxk', 'zzy', 'yh']
print(list_names)
print("\n")

#(2)
student_list = ['zyh', 'xpy', 'yxk', 'zzy', 'yh']
for student in student_list:
    print("请", student, "准时到达xxx")
print("\n")

#(3)
print("请输入删除的学生")
index = student_list.index(input())
print("请输入加入的学生")
student_list[index] = input()
for student in student_list:
    print("请", student, "准时到达xxx")
print("\n")

#(4)
addup = 0
list_sum = []
for num in range(1, 1000001):
    list_sum.append(num)

start_time = time.time()

for i in range(len(list_sum)):
    addup += list_sum[i]

    if int(list_sum[i]) == 1:
        print("最小值：", list_sum[i])
    
    if int(list_sum[i]) == 1000000:
        print("最大值：", list_sum[i])

end_time = time.time()

print(addup)
print("用时:", end_time - start_time)
print("\n")

#(5)
work_list = []
for j in range(3, 31):
    if j % 3 == 0:
        work_list.append(j)

for k in work_list:
    print(k)
print("\n")

#(6)
stack_list = [1,2,3,4]

for i in range(5,9):
    stack_list.append(i)

empty_list = []

for j in range(0,7):
    if stack_list:
        empty_list.append(stack_list.pop())

print(empty_list)
print(stack_list)
print("\n")

#(7)
team_list = [1, 2, 3, 4]

for i in range(5,9):
    team_list.append(i)

pop_ele = []
for _ in range(7):
    if team_list:
        pop_ele.append(team_list.pop(0))

print(pop_ele)
print(team_list)