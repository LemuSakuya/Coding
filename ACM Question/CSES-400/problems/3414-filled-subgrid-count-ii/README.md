# 3414 · Filled Subgrid Count II

[返回总目录](../../README.md) · [计数问题](../../chapters/16.md) · [官网题目](https://cses.fi/problemset/task/3414)

## 中文思路

**算法：**柱状图与单调栈

每列记录向上的连续同色高度，在当前行连续同色段内，用单调栈维护所有以当前列结尾区间的最小高度之和。

**时间复杂度：**O(n²)。这里按上述解法说明；采用其他数据结构时复杂度可能不同。

**容易写错：**行内颜色变化时必须清空栈；答案用 64 位。

## 核对答案

本题可先按空白分隔后的输出项与样例核对；样例通过仍不代表完整正确或达到时间限制。

[样例输入](sample.in) · [样例输出](sample.out)。样例取自公开题面镜像，仅作输入输出参考；本次未执行。

## 完整参考代码

- [reference.cpp](reference.cpp) · [原始来源](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Counting%20Problems/Filled%20Subgrid%20Count%20II/code/Filled%20Subgrid%20Count%20II.cpp) · hhoangcp/CSES-Solution

代码保持原文件字节内容，未擅自删改模板或优化选项。目标环境以 CSES 的 GNU C++17/20 为主；部分使用 PBDS 或 x86 优化选项，在 macOS 自带编译器中不一定可直接编译。

## 来源与状态

- [参考代码所在目录](https://github.com/hhoangcp/CSES-Solution/tree/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Counting%20Problems/Filled%20Subgrid%20Count%20II)，作者 hhoangcp，固定版本 `e5e35e104d11`。AC 为作者自述，本次未独立核验。
- [作者的详细英文解析](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Counting%20Problems/Filled%20Subgrid%20Count%20II/solution/Filled%20Subgrid%20Count%20II-solution.md)。作者注明为 AI 根据 AC 代码生成，可能含错；本合集中文速查及订正优先。

- 当前题号与标题对照 [官网题单](https://cses.fi/problemset/list/)。本地题单快照为 2026-10-22，后续题面更新以官网为准。

**本次检查状态：文件和来源对应已核对；未编译、未运行、未提交；未作逐题完整证明审查。**
