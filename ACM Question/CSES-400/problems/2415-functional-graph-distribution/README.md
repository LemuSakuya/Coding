# 2415 · Functional Graph Distribution

[返回总目录](../../README.md) · [计数问题](../../chapters/16.md) · [官网题目](https://cses.fi/problemset/task/2415)

## 中文思路

**算法：**循环顶点与第一类 Stirling 数

先选 i 个环上顶点，用 c(i,k) 把它们组成 k 个循环，再将其余点接成以这 i 点为根的有根森林。项系数化为 C(n−1,i−1)n^(n−i)c(i,k)。

**时间复杂度：**O(n²)。这里按上述解法说明；采用其他数据结构时复杂度可能不同。

**容易写错：**原文固定顶点 1 在环上的解释不正确；该系数来自有根森林计数恒等式。

> **原解析订正 / 待审点：** 系数 C(n−1,i−1)n^(n−i) 不是简单固定顶点 1 在环上。正确解释是选择 i 个环顶点，再使用以指定根集合为根的森林计数。

## 核对答案

本题可先按空白分隔后的输出项与样例核对；样例通过仍不代表完整正确或达到时间限制。

[样例输入](sample.in) · [样例输出](sample.out)。样例取自公开题面镜像，仅作输入输出参考；本次未执行。

## 完整参考代码

- [reference.cpp](reference.cpp) · [原始来源](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Counting%20Problems/Functional%20Graph%20Distribution/code/Functional%20Graph%20Distribution.cpp) · hhoangcp/CSES-Solution

代码保持原文件字节内容，未擅自删改模板或优化选项。目标环境以 CSES 的 GNU C++17/20 为主；部分使用 PBDS 或 x86 优化选项，在 macOS 自带编译器中不一定可直接编译。

## 来源与状态

- [参考代码所在目录](https://github.com/hhoangcp/CSES-Solution/tree/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Counting%20Problems/Functional%20Graph%20Distribution)，作者 hhoangcp，固定版本 `e5e35e104d11`。AC 为作者自述，本次未独立核验。
- [作者的详细英文解析](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Counting%20Problems/Functional%20Graph%20Distribution/solution/Functional%20Graph%20Distribution-solution.md)。作者注明为 AI 根据 AC 代码生成，可能含错；本合集中文速查及订正优先。

- [另一位作者的同名实现（Jonathan Uy）](https://github.com/Jonathan-Uy/CSES-Solutions/blob/56a1847dbc80494d688544aee6b9005fe917f23f/Counting%20Problems/Functional%20Graph%20Distribution.cpp)：供比较；本次未逐行审查。
- 当前题号与标题对照 [官网题单](https://cses.fi/problemset/list/)。本地题单快照为 2026-10-22，后续题面更新以官网为准。

**本次检查状态：文件和来源对应已核对；未编译、未运行、未提交；未作逐题完整证明审查。**
