# 2427 · Letter Pair Move Game

[返回总目录](../../README.md) · [附加题一](../../chapters/17.md) · [官网题目](https://cses.fi/problemset/task/2427)

## 中文思路

**算法：**相邻字母对移动构造

把相邻两个字母移到两空格中，利用确定的优先级逐步把 A 移到前面、B 移到后面；死锁状态需专门调整。

**时间复杂度：**参考实现为 O(n²) 级别。这里按上述解法说明；采用其他数据结构时复杂度可能不同。

**容易写错：**原文给出的简单奇偶不变量不足以证明构造；应逐步核对合法移动及总步数限制。

> **原解析订正 / 待审点：** 原文所列奇偶不变量及其示例不足以证明所有移动与可解性。参考资料只保留为构造实现线索，本次未验证它的完整正确性。

## 核对答案

本题输出可能不唯一、允许不同顺序，或需要专用合法性判断；与 sample.out 不同并不自动表示错误。

[样例输入](sample.in) · [样例输出](sample.out)。样例取自公开题面镜像，仅作输入输出参考；本次未执行。

## 完整参考代码

- [reference.cpp](reference.cpp) · [原始来源](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20I/Letter%20Pair%20Move%20Game/code/Letter%20Pair%20Move%20Game.cpp) · hhoangcp/CSES-Solution

代码保持原文件字节内容，未擅自删改模板或优化选项。目标环境以 CSES 的 GNU C++17/20 为主；部分使用 PBDS 或 x86 优化选项，在 macOS 自带编译器中不一定可直接编译。

## 来源与状态

- [参考代码所在目录](https://github.com/hhoangcp/CSES-Solution/tree/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20I/Letter%20Pair%20Move%20Game)，作者 hhoangcp，固定版本 `e5e35e104d11`。AC 为作者自述，本次未独立核验。
- [作者的详细英文解析](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20I/Letter%20Pair%20Move%20Game/solution/Letter%20Pair%20Move%20Game-solution.md)。作者注明为 AI 根据 AC 代码生成，可能含错；本合集中文速查及订正优先。

- 当前题号与标题对照 [官网题单](https://cses.fi/problemset/list/)。本地题单快照为 2026-10-22，后续题面更新以官网为准。

**本次检查状态：文件和来源对应已核对；未编译、未运行、未提交；未作逐题完整证明审查。**
