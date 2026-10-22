# 1148 · Maximum Building II

[返回总目录](../../README.md) · [附加题二](../../chapters/18.md) · [官网题目](https://cses.fi/problemset/task/1148)

## 中文思路

**算法：**按唯一最小柱计数

逐行建空格高度直方图，用左右不对称的比较规则把每个矩形唯一归给一个最小柱。对各种高度与宽度的计数贡献做二维差分、再累加。

**时间复杂度：**O(nm)。这里按上述解法说明；采用其他数据结构时复杂度可能不同。

**容易写错：**不能把每个最大延伸矩形的全部子矩形直接相加，会重复；原文简化解释漏掉唯一归属条件。

> **原解析订正 / 待审点：** 只累加各柱子的最大延伸矩形所包含的子矩形会重复。代码实际用左右不对称的栈比较及差分来划分唯一贡献，原文省略了这一关键点。

## 核对答案

本题可先按空白分隔后的输出项与样例核对；样例通过仍不代表完整正确或达到时间限制。

[样例输入](sample.in) · [样例输出](sample.out)。样例取自公开题面镜像，仅作输入输出参考；本次未执行。

## 完整参考代码

- [reference.cpp](reference.cpp) · [原始来源](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20II/Maximum%20Building%20II/code/Maximum%20Building%20II.cpp) · hhoangcp/CSES-Solution

代码保持原文件字节内容，未擅自删改模板或优化选项。目标环境以 CSES 的 GNU C++17/20 为主；部分使用 PBDS 或 x86 优化选项，在 macOS 自带编译器中不一定可直接编译。

## 来源与状态

- [参考代码所在目录](https://github.com/hhoangcp/CSES-Solution/tree/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20II/Maximum%20Building%20II)，作者 hhoangcp，固定版本 `e5e35e104d11`。AC 为作者自述，本次未独立核验。
- [作者的详细英文解析](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20II/Maximum%20Building%20II/solution/Maximum%20Building%20II-solution.md)。作者注明为 AI 根据 AC 代码生成，可能含错；本合集中文速查及订正优先。

- 当前题号与标题对照 [官网题单](https://cses.fi/problemset/list/)。本地题单快照为 2026-10-22，后续题面更新以官网为准。

**本次检查状态：文件和来源对应已核对；未编译、未运行、未提交；未作逐题完整证明审查。**
