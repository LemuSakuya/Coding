# 1194 · Monsters

[返回总目录](../../README.md) · [图论基础](../../chapters/04.md) · [官网题目](https://cses.fi/problemset/task/1194)

## 中文思路

**算法：**多源 BFS

先从全部怪物同时 BFS 求最早危险时间，再从 A 搜索，只有人的到达时间严格小于怪物时才可进入。到边界即可逃出。

**时间复杂度：**O(nm)。这里按上述解法说明；采用其他数据结构时复杂度可能不同。

**容易写错：**同时到达也不安全；起点已在边界时路径长度可为 0。

## 核对答案

本题输出可能不唯一、允许不同顺序，或需要专用合法性判断；与 sample.out 不同并不自动表示错误。

[样例输入](sample.in) · [样例输出](sample.out)。样例取自公开题面镜像，仅作输入输出参考；本次未执行。

## 完整参考代码

- [reference.cpp](reference.cpp) · [原始来源](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Graph%20Algorithms/Monsters/code/Monsters.cpp) · hhoangcp/CSES-Solution

代码保持原文件字节内容，未擅自删改模板或优化选项。目标环境以 CSES 的 GNU C++17/20 为主；部分使用 PBDS 或 x86 优化选项，在 macOS 自带编译器中不一定可直接编译。

## 来源与状态

- [参考代码所在目录](https://github.com/hhoangcp/CSES-Solution/tree/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Graph%20Algorithms/Monsters)，作者 hhoangcp，固定版本 `e5e35e104d11`。AC 为作者自述，本次未独立核验。
- [作者的详细英文解析](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Graph%20Algorithms/Monsters/solution/Monsters-solution.md)。作者注明为 AI 根据 AC 代码生成，可能含错；本合集中文速查及订正优先。

- [另一位作者的同名实现（Jonathan Uy）](https://github.com/Jonathan-Uy/CSES-Solutions/blob/56a1847dbc80494d688544aee6b9005fe917f23f/Graph%20Algorithms/Monsters.cpp)：供比较；本次未逐行审查。
- 当前题号与标题对照 [官网题单](https://cses.fi/problemset/list/)。本地题单快照为 2026-10-22，后续题面更新以官网为准。

**本次检查状态：文件和来源对应已核对；未编译、未运行、未提交；未作逐题完整证明审查。**
