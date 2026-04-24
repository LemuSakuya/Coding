import random
import string
import subprocess

def solve_dp(s, k):
    n = len(s)
    best = ""
    for mask in range(1, 1 << n):
        indices = [i for i in range(n) if (mask & (1 << i))]
        if len(indices) < k:
            continue
        gaps = 0
        for i in range(len(indices) - 1):
            if indices[i+1] > indices[i] + 1:
                gaps += 1
        if gaps <= k - 1:
            candidate = "".join(s[i] for i in indices)
            if candidate > best:
                best = candidate
    return best

for _ in range(100):
    n = random.randint(3, 10)
    k = random.randint(1, n)
    s = "".join(random.choice(['a', 'b', 'c']) for _ in range(n))
    
    with open("input.txt", "w") as f:
        f.write(f"1\n{n} {k}\n{s}\n")
    
    dp_ans = solve_dp(s, k)
    
    result = subprocess.run(["e:\\VSCode\\Coding\\test2.exe"], input=f"1\n{n} {k}\n{s}\n", text=True, capture_output=True)
    cpp_ans = result.stdout.strip()
    
    if dp_ans != cpp_ans:
        print(f"Failed! s={s}, k={k}")
        print(f"DP: {dp_ans}")
        print(f"CPP: {cpp_ans}")
        break
else:
    print("Passed 100 cases!")
