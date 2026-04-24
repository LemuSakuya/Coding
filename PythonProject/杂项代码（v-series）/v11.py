#(1)
print("(1):")

def sum_n(n):
    result = 0
    for i in range(n + 1):
        result += i

    return result

n = int(input ("Please entre your number: "))
print (sum_n(n))

#(2)
print("(2):")

def sum_between (a, b):
    result = 0
    for i in range (a, b + 1):
        result += i
    return result

a = int(input ("Pls input your a: "))
b = int(input ("Pls input your b: "))
print (sum_between(a, b))

#(3)
print ("(3):")

def capitalise_words (string):
    return string.title()

string = str(input ("Pls input your string line: "))
print (capitalise_words(string))

#(4)
print ("(4):")

def square_list(b_list):
    for i in range(len(b_list)):
        b_list[i] **= 2

b_list = [1, 4, 6, 6, 7, 8, 9, 22, 155]
square_list(b_list)
print(b_list)

#(5)
print ("(5):")

def multiply_dictionary(dictionary, n):
    return {key: v * n for key, v in dictionary.items()}

dictionary = {"a": 12, "b": 20, "c": 120}
n = int(input ("What num would you want to multiply: "))
new_dict = multiply_dictionary(dictionary, n)
print(new_dict)

#(6)
print("(6):")

def swap(a, b):
    return b, a

a = input("What numbers do you want to swap a: ")
b = input("What numbers do you want to swap b: ")
print(swap(a, b))

#(7)
print("(7):")

def average_n (*list):
    return sum(list) //  len(list) if list else None

my_list = []
n = int(input("The elements: "))
for i in range(n):
    item = input()
    my_list.append(item)
int_list = list(map(int, my_list))
print(average_n(*int_list))

#(8)
print("(8):")

def concatenate(*args):
    return ''.join(str(arg) for arg in args)

print (concatenate(1, 200, "caa", [1212, 33], (45, 55)))

#(9)
print("(9):")

def combine_dict(**dics):
    result = {}
    for dictionary in dics.values():
        result.update(dictionary)
    return result

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
dict3 = {'d': 5}
print(combine_dict(d1=dict1, d2=dict2, d3=dict3))

#(10)
print("(10):")

def reverse_list(list):
    for item in reversed(list):
        yield item

a_list = [1, 3, 5, 7, 9]
print (list(reverse_list(a_list)))