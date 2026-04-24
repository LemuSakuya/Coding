#(1)
foods = ("米饭", "面条", "馒头", "鸡蛋", "青菜", "蛋花汤")

for food in foods:
    print(food)
print("\n")

# try:
#     foods[0] = "包子"
# except TypeError as error:
#     print(error)

food_list = list(foods)
food_list[0] = "包子"
food_list[1] = "意大利面"
new_foods = tuple(food_list)

for food in new_foods:
    print(food)

#(2)
data = [
    ('zyh', 18, ('Student', 'Python')),
    ('yh', 18, ('Student', 'C++')),
    ('zjh', 19, ('Student', 'Matlab'))
]

for man in data:
    name, age, _ = man
    print(f"姓名：{name}, 年龄：{age}")

type = []
for person in data:
    _, _, (occupation, _) = person
    type.append(occupation)

print(type)

total_age = sum(person[1] for person in data)
average_age = total_age / len(data)
print("平均年龄：",average_age)