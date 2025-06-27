# calculator.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("ERROR")
    return a / b

def power(a, b):
    return a ** b

def factorial(n):
    if n < 0:
        raise ValueError("ERROR")
    result = 1
    for i in range(1, n+1):
        result *= i
    return result