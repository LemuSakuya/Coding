n = float(input())
m = float(input())

def turn_string_in(num):
    s = str(num).split('.')
    if len(s) == 1:
        return num
    return float(s[0] + '.' + s[1][:2])
ability = 1.0

for i in range(1, 366):
    if (i - 1) % 7 < 5:
        ability *= (1 + n / 1000)
    else:
        ability *= (1 - m / 1000)
print (int(ability * 100) / 100) 
print (turn_string_in(ability))