# 3306 · Nearest Campsites I

[返回总目录](../../README.md) · [附加题一](../../chapters/17.md) · [官网题目](https://cses.fi/problemset/task/3306)

## 中文思路

**算法：**四象限扫描

把曼哈顿最近点拆成四个象限，每个象限通过坐标翻转化为二维偏序查询，用 BIT 维护 x+y 等变换量的最大值。最后取所有候选位置的最近距离中的最大值。

**时间复杂度：**O((n+m)log(n+m))。这里按上述解法说明；采用其他数据结构时复杂度可能不同。

**容易写错：**需先对各候选求最小，再求全局最大，不能颠倒。

## 核对答案

本题可先按空白分隔后的输出项与样例核对；样例通过仍不代表完整正确或达到时间限制。

[样例输入](sample.in) · [样例输出](sample.out)。样例取自公开题面镜像，仅作输入输出参考；本次未执行。

## 完整参考代码

- [reference.cpp](reference.cpp) · [原始来源](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20I/Nearest%20Campsites%20I/code/Nearest%20Campsites%20I.cpp) · hhoangcp/CSES-Solution

代码保持原文件字节内容，未擅自删改模板或优化选项。目标环境以 CSES 的 GNU C++17/20 为主；部分使用 PBDS 或 x86 优化选项，在 macOS 自带编译器中不一定可直接编译。

## 来源与状态

- [参考代码所在目录](https://github.com/hhoangcp/CSES-Solution/tree/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20I/Nearest%20Campsites%20I)，作者 hhoangcp，固定版本 `e5e35e104d11`。AC 为作者自述，本次未独立核验。
- [作者的详细英文解析](https://github.com/hhoangcp/CSES-Solution/blob/e5e35e104d1131b0bf4cbc0334658c4e1a90377b/Additional%20Problems%20I/Nearest%20Campsites%20I/solution/Nearest%20Campsites%20I-solution.md)。作者注明为 AI 根据 AC 代码生成，可能含错；本合集中文速查及订正优先。

- 当前题号与标题对照 [官网题单](https://cses.fi/problemset/list/)。本地题单快照为 2026-10-22，后续题面更新以官网为准。

**本次检查状态：文件和来源对应已核对；未编译、未运行、未提交；未作逐题完整证明审查。**
