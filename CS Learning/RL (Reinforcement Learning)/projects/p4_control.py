"""P4 悬崖漫步：SARSA vs Q-learning。对照学习路线第 4 章。

运行: python p4_control.py
训练后打印两条贪心路径。Q-learning 通常贴边，SARSA 通常远离悬崖。
"""
from __future__ import annotations

import random
from collections import defaultdict

import numpy as np

W, H = 12, 4
START, GOAL = (0, 3), (11, 3)
ACTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def transition(s, a):
    x, y = s
    dx, dy = ACTIONS[a]
    nx, ny = min(W - 1, max(0, x + dx)), min(H - 1, max(0, y + dy))
    if ny == 3 and 1 <= nx <= 10:
        return START, -100.0, False
    if (nx, ny) == GOAL:
        return (nx, ny), 0.0, True
    return (nx, ny), -1.0, False


def eps_greedy(Q, s, eps):
    if random.random() < eps:
        return random.randrange(4)
    qs = [Q[(s, a)] for a in range(4)]
    m = max(qs)
    cands = [a for a, v in enumerate(qs) if v == m]
    return random.choice(cands)


def train(kind: str, episodes=500, alpha=0.5, gamma=1.0, eps=0.1, seed=0):
    random.seed(seed)
    Q = defaultdict(float)
    returns = []
    for _ in range(episodes):
        s = START
        a = eps_greedy(Q, s, eps)
        G = 0.0
        for _t in range(200):
            ns, r, done = transition(s, a)
            G += r
            na = eps_greedy(Q, ns, eps)
            if kind == "sarsa":
                target = r if done else r + gamma * Q[(ns, na)]
            else:
                target = r if done else r + gamma * max(Q[(ns, b)] for b in range(4))
            Q[(s, a)] += alpha * (target - Q[(s, a)])
            s, a = ns, na
            if done:
                break
        returns.append(G)
    return Q, returns


def greedy_path(Q, limit=40):
    s = START
    path = [s]
    for _ in range(limit):
        a = eps_greedy(Q, s, 0.0)
        s, r, done = transition(s, a)
        path.append(s)
        if done or s == START and len(path) > 1 and r == -100:
            break
    return path


def ascii(path):
    cells = {p: "*" for p in path}
    cells[START] = "S"
    cells[GOAL] = "G"
    lines = []
    for y in range(H):
        row = []
        for x in range(W):
            if y == 3 and 1 <= x <= 10 and (x, y) not in cells:
                row.append("C")
            else:
                row.append(cells.get((x, y), "."))
        lines.append("".join(row))
    return "\n".join(lines)


def main():
    Qs, rs = train("sarsa")
    Qq, rq = train("q")
    print("SARSA last-50 mean return:", float(np.mean(rs[-50:])))
    print(ascii(greedy_path(Qs)))
    print()
    print("Q-learning last-50 mean return:", float(np.mean(rq[-50:])))
    print(ascii(greedy_path(Qq)))
    print()
    print("训练回报是 ε-greedy 在线表现：Q-learning 贴边所以训练时更常掉崖。")
    print("看贪心路径：Q-learning 短，SARSA 更安全。把 eps 退火到 0 后两者应对齐到最优。")


if __name__ == "__main__":
    main()
