# 3139 · Hidden Permutation

[返回总目录](../../README.md) · [交互题](../../chapters/12.md) · [官网题目](https://cses.fi/problemset/task/3139)

## 中文思路

**算法：**交互归并排序

对下标按隐藏值排序，比较由询问完成。排序后第 k 个下标处的隐藏值就是 k，反向赋值恢复排列。

**时间复杂度：**O(n log n) 次询问。这里按上述解法说明；采用其他数据结构时复杂度可能不同。

**容易写错：**归并排序可明确控制比较次数；交互答案需要刷新。

## 核对答案

交互题：需要评测器来回通信，不能用静态 sample.in 判断；每次询问必须刷新输出。

## 完整参考代码

- [reference.cpp](reference.cpp) · [原始来源](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Interactive%20Problems/Hidden%20Permutation/code/Hidden%20Permutation.cpp) · hhoangcp/CSES-Solution

代码保持原文件字节内容，未擅自删改模板或优化选项。目标环境以 CSES 的 GNU C++17/20 为主；部分使用 PBDS 或 x86 优化选项，在 macOS 自带编译器中不一定可直接编译。

## 来源与状态

- [参考代码所在目录](https://github.com/hhoangcp/CSES-Solution/tree/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Interactive%20Problems/Hidden%20Permutation)，作者 hhoangcp，固定版本 `e5e35e104d11`。AC 为作者自述，本次未独立核验。
- [作者的详细英文解析](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Interactive%20Problems/Hidden%20Permutation/solution/Hidden%20Permutation-solution.md)。作者注明为 AI 根据 AC 代码生成，可能含错；本合集中文速查及订正优先。

- [另一位作者的同名实现（Jonathan Uy）](https://github.com/Jonathan-Uy/CSES-Solutions/blob/56a1847dbc80494d688544aee6b9005fe917f23f/Interactive%20Problems/Hidden%20Permutation.cpp)：供比较；本次未逐行审查。
- 当前题号与标题对照 [官网题单](https://cses.fi/problemset/list/)。本地题单快照为 2026-10-22，后续题面更新以官网为准。

**本次检查状态：文件和来源对应已核对；未编译、未运行、未提交；未作逐题完整证明审查。**
