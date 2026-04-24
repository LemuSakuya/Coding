# #The First Q
# input_string = input()

# #The First Way
# print("The First Way:")
# print(input_string.upper())

# #The Second Way
# print("The Second Way:")
# uppercase_string = ""
# for char in input_string:
#     if ord('a') <= ord(char) <= ord('z'):
#         uppercase_char = chr(ord(char) - 32)
#         uppercase_string += uppercase_char
#     else:
#         uppercase_string += char
# print(uppercase_string)

# #The Second Q
# number = input()
# sum = 0
# for i in number:
#     sum += int(i)
# print(sum)

# #The Third Q
# input_setA = input()
# setA = set(input_setA.split())
# input_setB = input()
# setB = set(input_setB.split())

# interaction = setA & setB

# union = setA | setB

# difference = setA - setB

# print(interaction, union, difference)

# #The Fourth Q
# num = int(input())
# x2 = bin(num)[2:]
# x8 = oct(num)[2:]
# x16 = hex(num)[2:]
# print(x2,x8,x16)

# #The Fifth Q
# import random
# import time
# import math

# def monte_kaluo_pi(num_darts):
#     inside_circle = 0

#     for _ in range(num_darts):
#         x = random.uniform(0, 2)
#         y = random.uniform(0, 2)
#         distance = math.sqrt((1 - x)**2 + (1 - y)**2)

#         if distance <= 1:
#             inside_circle += 1

#     pi_estimate = (inside_circle / num_darts) * 4
#     return pi_estimate

# def main():
#     num_darts = int(input())

#     start_time = time.time()
#     pi_estimate = monte_kaluo_pi(num_darts)
#     end_time = time.time()

#     time_elapsed = end_time - start_time
#     pi_error = abs(pi_estimate - math.pi)

#     print(f"计算值{pi_estimate}")
#     print(f"准确值{math.pi}")
#     print(f"误差值{pi_error}")
#     print(f"{time_elapsed:.6f}")

# if __name__ == "__main__":
#     main()

