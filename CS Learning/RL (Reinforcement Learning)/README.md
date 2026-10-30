# 强化学习学习包

本目录对应课程源材料（简介 → 多智能体 / 前沿，以及 Sutton & Barto 教材与习题）。

## 先看这两个文件

| 文件 | 用途 |
|---|---|
| [强化学习完整学习路线.md](./强化学习完整学习路线.md) | 主文档。16 章理论推导、习题解答、12 周日历、综合项目。2500+ 行。 |
| [强化学习可视化学习.html](./强化学习可视化学习.html) | 交互动画。用浏览器直接打开，无需服务器。 |

建议：HTML 里把某个模块播放一遍，再回到 Markdown 同一章把公式推完，然后做 `projects/` 里对应的代码。

## 项目代码

| 脚本 | 对应章节 |
|---|---|
| `projects/p1_bandit.py` | 第 1 章 多臂老虎机 |
| `projects/p2_gridworld.py` | 第 2 章 价值迭代 / 策略迭代 |
| `projects/p4_control.py` | 第 4 章 SARSA 与 Q-learning |

```bash
pip install numpy matplotlib
python projects/p1_bandit.py
python projects/p2_gridworld.py
python projects/p4_control.py
```

其余项目（DQN、PPO、HER、离线 RL）的规格写在学习路线第 7–13 章与附录 C，按规格自建仓库即可。

## 源课件对照

源目录中的 `1-强化学习简介.pptx` … `14-多智能体强化学习.pptx`、`7-1策略梯度方法.pdf`、`习题.docx`、`Reinforcement Learning An Intr.pdf` 是本学习包的依据。章节编号以课件大纲 16 章为准。
