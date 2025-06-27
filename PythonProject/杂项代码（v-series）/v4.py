container = {'apple':'A','peach':'B','banana':'C','pear':'D'}
print (container)
print (container['peach'])
container ['apple'] = 2
container ['peach'] = 3
container ['banana'] = 4
container ['pear'] = 5

print (container)

price = dict()

for i in range(0,2):
    if 'apple' in price:
        print("the apple's price is: ", price['apple'])
    else:
        price ['apple'] = int(input("your add apple price: "))
    if 'banana' in price:
        print("the banana's price is: ", price['banana'])
    else:
        price ['banana'] = int(input("your add banana price: "))
    if 'orange' in price:
        print("the orange's price is: ", price['orange'])
    else:
        price ['orange'] = int(input("your add orange price: "))
    if 'pear' in price:
        print("the pear's price is: ", price['pear'])
    else:
        price ['pear'] = int(input("your add pear price: "))

print (price)