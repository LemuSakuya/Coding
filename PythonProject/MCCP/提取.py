import pandas as pd

df = pd.read_excel('附件12.xlsx', header=None, skiprows=4)#起始行

all_teachers_data = []

rows_per_teacher = 12
expected_cols = 11
max_teachers = 50

full_marks_template = [8, 10, 15, 7, 5, 10, 12, 8, 6, 5, 4, 10]#各个项的满分

for teacher_num in range(1, max_teachers + 1):#老师的遍历模块
    try:
        start_row = (teacher_num - 1) * (rows_per_teacher + 4)#检测的行

        data_block = df.iloc[start_row:start_row+rows_per_teacher, 1:12]#列的范围

        if data_block.shape[1] != expected_cols:
            print(f"{teacher_num}not exist,expect colum{expected_cols},actual colum{data_block.shape[1]}")
            continue

        teacher_data = data_block.copy()
        teacher_data.columns = ['评分项'] + [f'专家{i+10}号' for i in range(1, 11)]#处理sheet2时为i+10

        teacher_data['满分'] = full_marks_template
        teacher_data['教师编号'] = f'教师{teacher_num}'
        all_teachers_data.append(teacher_data)
        
    except Exception as e:
        print(f"{teacher_num}ERROR: {str(e)}")

if all_teachers_data:
    combined_data = pd.concat(all_teachers_data, ignore_index=True)

    combined_data.to_excel('All Data2.xlsx', index=False)
    print(f"Nice Save{len(all_teachers_data)}")

    extracted_teachers = combined_data['教师编号'].unique()
    print(f"Num: {extracted_teachers}")
else:
    print("ERROR")