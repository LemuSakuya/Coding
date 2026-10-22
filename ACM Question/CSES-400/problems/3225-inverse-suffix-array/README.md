# 3225 · Inverse Suffix Array

[返回总目录](../../README.md) · [字符串算法](../../chapters/08.md) · [官网题目](https://cses.fi/problemset/task/3225)

## 中文思路

**算法：**逆后缀数组构造

已知后缀顺序，建立 rank。依次给相邻后缀分配非递减字符；若去掉首字符后的 rank 顺序逆转，就必须增大首字符。

**时间复杂度：**O(n)。这里按上述解法说明；采用其他数据结构时复杂度可能不同。

**容易写错：**空后缀 rank 最小；需要超过 26 种字母时无解。

## 核对答案

本题输出可能不唯一、允许不同顺序，或需要专用合法性判断；与 sample.out 不同并不自动表示错误。

[样例输入](sample.in) · [样例输出](sample.out)。样例取自公开题面镜像，仅作输入输出参考；本次未执行。

## 完整参考代码

- [reference.cpp](reference.cpp) · [原始来源](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/String%20Algorithms/Inverse%20Suffix%20Array/code/Inverse%20Suffix%20Array.cpp) · hhoangcp/CSES-Solution

代码保持原文件字节内容，未擅自删改模板或优化选项。目标环境以 CSES 的 GNU C++17/20 为主；部分使用 PBDS 或 x86 优化选项，在 macOS 自带编译器中不一定可直接编译。

## 来源与状态

- [参考代码所在目录](https://github.com/hhoangcp/CSES-Solution/tree/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/String%20Algorithms/Inverse%20Suffix%20Array)，作者 hhoangcp，固定版本 `e5e35e104d11`。AC 为作者自述，本次未独立核验。
- [作者的详细英文解析](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/String%20Algorithms/Inverse%20Suffix%20Array/solution/Inverse%20Suffix%20Array-solution.md)。作者注明为 AI 根据 AC 代码生成，可能含错；本合集中文速查及订正优先。

- 当前题号与标题对照 [官网题单](https://cses.fi/problemset/list/)。本地题单快照为 2026-10-22，后续题面更新以官网为准。

**本次检查状态：文件和来源对应已核对；未编译、未运行、未提交；未作逐题完整证明审查。**
