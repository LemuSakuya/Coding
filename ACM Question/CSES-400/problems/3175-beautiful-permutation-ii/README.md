# 3175 · Beautiful Permutation II

[返回总目录](../../README.md) · [附加题一](../../chapters/17.md) · [官网题目](https://cses.fi/problemset/task/3175)

## 中文思路

**算法：**字典序回溯

逐位置从小到大尝试未用值，禁止与前一个相差 1，第一个完整解即字典序最小解；实现需利用排列结构或强剪枝应对大 n。

**时间复杂度：**朴素最坏 O(n!)，原实现是回溯。这里按上述解法说明；采用其他数据结构时复杂度可能不同。

**容易写错：**不要把普通奇偶构造当作字典序最小；n=4 的简单先奇后偶构造也不合法。

> **原解析订正 / 待审点：** 先奇后偶的简单构造在 n=4 时并不成立，也不保证本题要求的字典序最小。参考代码实际按字典序回溯，需另外分析其大规模性能，不能把典型运行快当成通用复杂度证明。

## 核对答案

本题可先按空白分隔后的输出项与样例核对；样例通过仍不代表完整正确或达到时间限制。

[样例输入](sample.in) · [样例输出](sample.out)。样例取自公开题面镜像，仅作输入输出参考；本次未执行。

## 完整参考代码

- [reference.cpp](reference.cpp) · [原始来源](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20I/Beautiful%20Permutation%20II/code/Beautiful%20Permutation%20II.cpp) · hhoangcp/CSES-Solution

代码保持原文件字节内容，未擅自删改模板或优化选项。目标环境以 CSES 的 GNU C++17/20 为主；部分使用 PBDS 或 x86 优化选项，在 macOS 自带编译器中不一定可直接编译。

## 来源与状态

- [参考代码所在目录](https://github.com/hhoangcp/CSES-Solution/tree/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20I/Beautiful%20Permutation%20II)，作者 hhoangcp，固定版本 `e5e35e104d11`。AC 为作者自述，本次未独立核验。
- [作者的详细英文解析](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20I/Beautiful%20Permutation%20II/solution/Beautiful%20Permutation%20II-solution.md)。作者注明为 AI 根据 AC 代码生成，可能含错；本合集中文速查及订正优先。

- 当前题号与标题对照 [官网题单](https://cses.fi/problemset/list/)。本地题单快照为 2026-10-22，后续题面更新以官网为准。

**本次检查状态：文件和来源对应已核对；未编译、未运行、未提交；未作逐题完整证明审查。**
