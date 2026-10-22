# 2111 · Apples and Bananas

[返回总目录](../../README.md) · [高级技巧](../../chapters/10.md) · [官网题目](https://cses.fi/problemset/task/2111)

## 中文思路

**算法：**卷积

把苹果与香蕉重量频率分别作为多项式系数，乘积中 x^s 的系数就是总重量 s 的配对数。

**时间复杂度：**O(M log M)。这里按上述解法说明；采用其他数据结构时复杂度可能不同。

**容易写错：**系数统计出现次数；FFT 结果需正确四舍五入。

## 核对答案

本题可先按空白分隔后的输出项与样例核对；样例通过仍不代表完整正确或达到时间限制。

[样例输入](sample.in) · [样例输出](sample.out)。样例取自公开题面镜像，仅作输入输出参考；本次未执行。

## 完整参考代码

- [reference.cpp](reference.cpp) · [原始来源](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Advanced%20Techniques/Apples%20and%20Bananas/code/Apples%20and%20Bananas.cpp) · hhoangcp/CSES-Solution

代码保持原文件字节内容，未擅自删改模板或优化选项。目标环境以 CSES 的 GNU C++17/20 为主；部分使用 PBDS 或 x86 优化选项，在 macOS 自带编译器中不一定可直接编译。

## 来源与状态

- [参考代码所在目录](https://github.com/hhoangcp/CSES-Solution/tree/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Advanced%20Techniques/Apples%20and%20Bananas)，作者 hhoangcp，固定版本 `e5e35e104d11`。AC 为作者自述，本次未独立核验。
- [作者的详细英文解析](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Advanced%20Techniques/Apples%20and%20Bananas/solution/Apples%20and%20Bananas-solution.md)。作者注明为 AI 根据 AC 代码生成，可能含错；本合集中文速查及订正优先。

- [另一位作者的同名实现（Jonathan Uy）](https://github.com/Jonathan-Uy/CSES-Solutions/blob/56a1847dbc80494d688544aee6b9005fe917f23f/Advanced%20Techniques/Apples%20and%20Bananas.cpp)：供比较；本次未逐行审查。
- 当前题号与标题对照 [官网题单](https://cses.fi/problemset/list/)。本地题单快照为 2026-10-22，后续题面更新以官网为准。

**本次检查状态：文件和来源对应已核对；未编译、未运行、未提交；未作逐题完整证明审查。**
