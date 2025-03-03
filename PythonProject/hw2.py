subject1 = int(input("pls input your Chinese score:"))
subject2 = int(input("pls input your Math score:"))
subject3 = int(input("pls input your English score:"))
subject4 = int(input("pls input your Physics score:"))
subject5 = int(input("pls input your Chemistry score:"))
subject6 = int(input("pls input your Biology score:"))

score1 = (subject1 >= 120) * 2 + (subject1 < 120 and subject1 >= 90) * 1 + (subject1 < 90) * 0
score2 = (subject2 >= 120) * 2 + (subject2 < 120 and subject2 >= 90) * 1 + (subject2 < 90) * 0
score3 = (subject3 >= 120) * 2 + (subject3 < 120 and subject3 >= 90) * 1 + (subject3 < 90) * 0
score4 = (subject4 >= 85) * 2 + (subject4 < 85 and subject4 >= 60) * 1 + (subject4 < 60) * 0
score5 = (subject5 >= 85) * 2 + (subject5 < 85 and subject5 >= 60) * 1 + (subject5 < 60) * 0
score6 = (subject6 >= 85) * 2 + (subject6 < 85 and subject6 >= 60) * 1 + (subject6 < 60) * 0

TotalScore = score1 + score2 + score3 + score4 + score5 + score6

if int(TotalScore) >= 10:
    rating = 'A'
if int(TotalScore) > 6 and int(TotalScore) < 10:
    rating = 'B'
if int(TotalScore) <= 6:
    rating = 'C'


print ("your total subject score is:", int(TotalScore), "and your rating is: ", rating)