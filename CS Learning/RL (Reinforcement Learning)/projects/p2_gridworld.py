"""P2 格子世界动态规划。对照学习路线第 2 章。

4x4，每步 -1，右下角终止。比较价值迭代与策略迭代。
运行: python p2_gridworld.py
"""
from __future__ import annotations

import numpy as np

N = 4
TERM = (3, 3)
ACTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # N E S W
GAMMA = 0.9


def step(s, a):
    if s == TERM:
        return TERM, 0.0
    x, y = s
    dx, dy = ACTIONS[a]
    nx, ny = x + dx, y + dy
    if not (0 <= nx < N and 0 <= ny < N):
        nx, ny = x, y
    ns = (nx, ny)
    r = 0.0 if ns == TERM else -1.0
    return ns, r


def greedy_policy(V):
    pi = np.zeros((N, N), dtype=int)
    for x in range(N):
        for y in range(N):
            s = (x, y)
            if s == TERM:
                continue
            q = []
            for a in range(4):
                ns, r = step(s, a)
                q.append(r + GAMMA * V[ns])
            pi[s] = int(np.argmax(q))
    return pi


def policy_evaluation(pi, tol=1e-6):
    V = np.zeros((N, N))
    for k in range(1000):
        delta = 0.0
        nv = np.zeros_like(V)
        for x in range(N):
            for y in range(N):
                s = (x, y)
                if s == TERM:
                    continue
                ns, r = step(s, int(pi[s]))
                nv[s] = r + GAMMA * V[ns]
                delta = max(delta, abs(nv[s] - V[s]))
        V = nv
        if delta < tol:
            return V, k + 1
    return V, 1000


def policy_iteration():
    pi = np.zeros((N, N), dtype=int)
    history = []
    for it in range(20):
        V, sweeps = policy_evaluation(pi)
        npi = greedy_policy(V)
        history.append((it, V.copy(), sweeps))
        if np.array_equal(npi, pi):
            return V, pi, history
        pi = npi
    return V, pi, history


def value_iteration(tol=1e-6):
    V = np.zeros((N, N))
    hist = [V.copy()]
    for k in range(200):
        nv = np.zeros_like(V)
        delta = 0.0
        for x in range(N):
            for y in range(N):
                s = (x, y)
                if s == TERM:
                    continue
                qs = []
                for a in range(4):
                    ns, r = step(s, a)
                    qs.append(r + GAMMA * V[ns])
                nv[s] = max(qs)
                delta = max(delta, abs(nv[s] - V[s]))
        V = nv
        hist.append(V.copy())
        if delta < tol:
            return V, greedy_policy(V), hist
    return V, greedy_policy(V), hist


ARROWS = {0: "↑", 1: "→", 2: "↓", 3: "←"}


def dump(V, pi, title):
    print(title)
    for y in range(N):
        row_v, row_p = [], []
        for x in range(N):
            if (x, y) == TERM:
                row_v.append("  0.0")
                row_p.append(" G")
            else:
                row_v.append(f"{V[x, y]:5.1f}")
                row_p.append(" " + ARROWS[int(pi[x, y])])
        print(" ".join(row_v), "   ", "".join(row_p))
    print()


def main():
    Vv, piv, hist = value_iteration()
    print(f"value iteration converged in {len(hist)-1} sweeps")
    dump(Vv, piv, "value iteration V and greedy policy")

    Vp, pip, h2 = policy_iteration()
    print(f"policy iteration outer loops: {len(h2)}")
    dump(Vp, pip, "policy iteration V and policy")
    print("max |Vv - Vp| =", float(np.max(np.abs(Vv - Vp))))


if __name__ == "__main__":
    main()
