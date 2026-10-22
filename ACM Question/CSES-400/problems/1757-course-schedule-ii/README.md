# 1757 · Course Schedule II

[返回总目录](../../README.md) · [高级图论](../../chapters/15.md) · [官网题目](https://cses.fi/problemset/task/1757)

## 中文思路

**算法：**逆向拓扑贪心

本题优先让课程 1 尽早，再让课程 2 尽早，优化的是各课程完成位置。反向处理出度为 0 的点，每次把编号最大的课程放到当前最后空位。

**时间复杂度：**O((n+m)log n)。这里按上述解法说明；采用其他数据结构时复杂度可能不同。

**容易写错：**与正向最小堆求字典序最小课程序列不同；原英文解析误述了目标。

> **原解析订正 / 待审点：** 原文把本题误述为字典序最小拓扑序。实际目标按课程编号依次最小化完成位置。参考代码使用反图和最大堆，中文说明已按实际题意订正。

## 核对答案

本题可先按空白分隔后的输出项与样例核对；样例通过仍不代表完整正确或达到时间限制。

[样例输入](sample.in) · [样例输出](sample.out)。样例取自公开题面镜像，仅作输入输出参考；本次未执行。

## 完整参考代码

- [reference.cpp](reference.cpp) · [原始来源](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Advanced%20Graph%20Problems/Course%20Schedule%20II/code/Course%20Schedule%20II.cpp) · hhoangcp/CSES-Solution

代码保持原文件字节内容，未擅自删改模板或优化选项。目标环境以 CSES 的 GNU C++17/20 为主；部分使用 PBDS 或 x86 优化选项，在 macOS 自带编译器中不一定可直接编译。

## 来源与状态

- [参考代码所在目录](https://github.com/hhoangcp/CSES-Solution/tree/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Advanced%20Graph%20Problems/Course%20Schedule%20II)，作者 hhoangcp，固定版本 `e5e35e104d11`。AC 为作者自述，本次未独立核验。
- [作者的详细英文解析](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Advanced%20Graph%20Problems/Course%20Schedule%20II/solution/Course%20Schedule%20II-solution.md)。作者注明为 AI 根据 AC 代码生成，可能含错；本合集中文速查及订正优先。

- [另一位作者的同名实现（Jonathan Uy）](https://github.com/Jonathan-Uy/CSES-Solutions/blob/56a1847dbc80494d688544aee6b9005fe917f23f/Advanced%20Graph%20Problems/Course%20Schedule%20II.cpp)：供比较；本次未逐行审查。
- 当前题号与标题对照 [官网题单](https://cses.fi/problemset/list/)。本地题单快照为 2026-10-22，后续题面更新以官网为准。

**本次检查状态：文件和来源对应已核对；未编译、未运行、未提交；未作逐题完整证明审查。**
