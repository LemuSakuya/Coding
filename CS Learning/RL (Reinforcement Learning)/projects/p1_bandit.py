"""P1 多臂老虎机实验室。对照学习路线第 1 章。

运行: python p1_bandit.py
比较贪心 / ε-greedy / UCB1 / Thompson Sampling 的累积 regret。
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class BernoulliBandit:
    probs: list[float]
    rng: random.Random = field(default_factory=random.Random)

    def K(self) -> int:
        return len(self.probs)

    def pull(self, arm: int) -> float:
        return 1.0 if self.rng.random() < self.probs[arm] else 0.0

    @property
    def best(self) -> float:
        return max(self.probs)


class EpsilonGreedy:
    def __init__(self, k: int, eps: float = 0.1):
        self.eps, self.n, self.q = eps, [0] * k, [0.0] * k

    def act(self, t: int) -> int:
        if random.random() < self.eps:
            return random.randrange(len(self.q))
        return int(np.argmax(self.q))

    def update(self, a: int, r: float) -> None:
        self.n[a] += 1
        self.q[a] += (r - self.q[a]) / self.n[a]


class UCB1:
    def __init__(self, k: int, c: float = math.sqrt(2)):
        self.c, self.n, self.q = c, [0] * k, [0.0] * k

    def act(self, t: int) -> int:
        for i, n in enumerate(self.n):
            if n == 0:
                return i
        scores = [
            q + self.c * math.sqrt(math.log(t + 1) / n)
            for q, n in zip(self.q, self.n)
        ]
        return int(np.argmax(scores))

    def update(self, a: int, r: float) -> None:
        self.n[a] += 1
        self.q[a] += (r - self.q[a]) / self.n[a]


class ThompsonBernoulli:
    def __init__(self, k: int):
        self.alpha, self.beta = [1] * k, [1] * k

    def act(self, t: int) -> int:
        samples = [random.betavariate(a, b) for a, b in zip(self.alpha, self.beta)]
        return int(np.argmax(samples))

    def update(self, a: int, r: float) -> None:
        self.alpha[a] += r
        self.beta[a] += 1 - r


def run(agent_cls, kwargs, probs, T=2000, seeds=30):
    curves = []
    for seed in range(seeds):
        random.seed(seed)
        env = BernoulliBandit(probs, random.Random(seed))
        agent = agent_cls(env.K(), **kwargs) if kwargs else agent_cls(env.K())
        regret, cum = [], 0.0
        for t in range(T):
            a = agent.act(t)
            r = env.pull(a)
            agent.update(a, r)
            cum += env.best - env.probs[a]
            regret.append(cum)
        curves.append(regret)
    return np.mean(curves, axis=0)


def main():
    probs = [0.15, 0.35, 0.55, 0.42, 0.28]
    series = {
        "ε-greedy 0.1": run(EpsilonGreedy, {"eps": 0.1}, probs),
        "ε-greedy 0.01": run(EpsilonGreedy, {"eps": 0.01}, probs),
        "UCB1": run(UCB1, {}, probs),
        "Thompson": run(ThompsonBernoulli, {}, probs),
    }
    plt.figure(figsize=(7, 4))
    for name, y in series.items():
        plt.plot(y, label=name)
    plt.xlabel("t")
    plt.ylabel("cumulative regret")
    plt.title("Bernoulli bandit: sublinear vs linear regret")
    plt.legend()
    plt.tight_layout()
    plt.savefig("p1_bandit_regret.png", dpi=140)
    print("saved p1_bandit_regret.png")
    print("final mean regret:", {k: float(v[-1]) for k, v in series.items()})


if __name__ == "__main__":
    main()
