v1 = True
v2 = False
v3 = True

print (v1)
print (v2)
print (v3)

print (int (v1))
print (int (v2))
print (int (v3))

print (v1 + v2)
print (v1 + v3)

print (4 < 5)
print (int (4 < 5))
print (float (4 < 5))

a = int (input ("pls input team A's totoal strength: "))
b = int (input ("pls input team B's totoal strength: "))
c = int (input ("pls input team C's totoal strength: "))
d = int (input ("pls input team D's totoal strength: "))

avsb = int (a > b) * 3 +  int (a == b)
avsc = int (a > c) * 3 +  int (a == c)
avsd = int (a > d) * 3 +  int (a == d)

score = avsb + avsc + avsd

print ("the team A's total score is: ", score)

a = int (input ("pls input team A's totoal strength: "))
b = int (input ("pls input team B's totoal strength: "))
c = int (input ("pls input team C's totoal strength: "))
d = int (input ("pls input team D's totoal strength: "))

avsb = (a > b) * 3 + (a == b)
avsc = (a > c) * 3 + (a == c)
avsd = (a > d) * 3 + (a == d)

score = avsb + avsc + avsd

print ("the team A's total score is: ", int(score))
print ("the team A's total score is: " %(score))