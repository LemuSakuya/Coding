price = dict()

print("Now please develop today's menu:")
j = int(input("How many types of fruit do you want to sell: "))

for fruit in range(0, j):
    fruit_name = input("Input your fruit: ")
    fruit_price = float(input("Input your fruit price: "))
    price[fruit_name] = fruit_price

print("Today's fruit prices are as follows:")
print(price)

n = int(input("Customer, please enter the number of fruit types you want to buy: "))

sum_price = 0

for i in range(0, n):
    fruit = input("Please customer, enter your %d fruit name: " % (i + 1))
    num = int(input("Please customer, enter your %d fruit quantity: " % (i + 1)))
    if fruit in price:
        sum_price += price[fruit] * num

print("Your total price is:", sum_price)
