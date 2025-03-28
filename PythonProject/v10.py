#(1)
print("(1):")
num_users = int(input())
user_movies = []
for i in range(num_users):
    movies = input(f"请输入用户{i+1}喜欢的电影(用逗号分隔):").split(',')
    user_movies.append(set(m.strip() for m in movies))

common_movies = set.intersection(*user_movies) if user_movies else set()
print("共同喜欢的电影集合:", common_movies)
print("\n")

#(2)
print("(2):")
math_students = {'Alice', 'Bob', 'Charlie', 'David'}
physics_students = {'Alice', 'Charlie', 'Eve', 'Frank'}
chemistry_students = {'Bob', 'Charlie', 'David', 'Grace'}

math_physics = math_students & physics_students
print("数学和物理双修：", math_physics, "人数：", len(math_physics))

only_chem = chemistry_students - (math_students | physics_students)
print("仅化学：", only_chem, "人数：", len(only_chem))

all_subjects = math_students & physics_students & chemistry_students
print("三修全选：", all_subjects, "人数：", len(all_subjects))

at_least_two = (
    (math_students & physics_students) |
    (math_students & chemistry_students) |
    (physics_students & chemistry_students)
)
print("至少两门：", at_least_two, "人数：", len(at_least_two))
print("\n")

#(3)
print("(3):")
import re

text = """If you’re interested in learning more about our app and how you can get involved,
 please don’t hesitate to contact me at john.doe@example.com or our team at
 info@hunnu.edu.cn and someoneaddress@csu.edu.cn. We’d be happy to answer any
 questions you may have and provide you with more details about our launch plans"""

email_pattern = r'\b[\w\.-]+@[\w\.-]+\.\w+\b'
emails = re.findall(email_pattern, text)
EmailSet = set(emails)
email_counts = {email: emails.count(email) for email in EmailSet}

text_clean = re.sub(email_pattern, '', text)
word_pattern = r"\b[\w']+\b"
words = [word.lower() for word in re.findall(word_pattern, text_clean)]
StringSet = set(words)
word_counts = {word: words.count(word) for word in StringSet}

all_counts = {**word_counts, **email_counts}
max_count = max(all_counts.values(), default=0)
most_common = [k for k, v in all_counts.items() if v == max_count]

print("不重复英语字符串：", StringSet)
print("不重复邮件地址：", EmailSet)
print("出现次数最多的字符串：", most_common, "次数：", max_count)