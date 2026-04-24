import random

def solve(a, m, r):
    ans = 0
    s = 0
    for x in a:
        s += x
        if s > m:
            ans += 1
            s = 0
            continue
        s += r * x
        if s > m:
            ans += 1
            s = 0
    return ans

def find_counterexample():
    for _ in range(10000):
        n = random.randint(2, 10)
        m = random.randint(10, 100)
        a = [random.randint(1, 20) for _ in range(n)]
        if sum(a) > m:
            m = sum(a)
        
        last = solve(a, m, 0)
        for r in range(1, 50):
            cur = solve(a, m, r)
            if cur < last:
                print("Counterexample found!")
                print(f"a = {a}, m = {m}")
                print(f"r = {r-1}, ans = {last}")
                print(f"r = {r}, ans = {cur}")
                return True
            last = cur
    print("No counterexample found.")
    return False

find_counterexample()
