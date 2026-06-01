# Algorithm Templates

本目录收录 OIer / ACMer 常用 C++17 模板。模板只放稳定、短小、可默写的版本；更详细的解释见 `../chapters/`。

## 模板列表

| 文件 | 用途 | 复杂度 |
|------|------|--------|
| `00_fast_io.cpp` | 通用代码骨架 | - |
| `01_dsu.cpp` | 并查集 | 近似 O(1) |
| `02_fenwick.cpp` | 树状数组 | O(log n) |
| `03_segment_tree_lazy.cpp` | 懒标记线段树 | O(log n) |
| `04_dijkstra.cpp` | 非负权单源最短路 | O((n+m)log n) |
| `05_lca_binary_lifting.cpp` | 倍增 LCA | 预处理 O(nlogn)，查询 O(logn) |
| `06_dinic.cpp` | 最大流 | 常用竞赛模板 |
| `07_kmp.cpp` | KMP 前缀函数 | O(n) |
| `08_string_hash.cpp` | 双哈希 | O(n) 预处理，O(1) 查询 |
| `09_math_comb.cpp` | 快速幂、组合数 | O(n) 预处理，O(1) 查询 |
| `10_stress_test.cpp` | 对拍框架 | 依赖 brute/solve |

## 使用原则

1. 复制模板前先确认适用条件。
2. 多组数据必须清空全局变量。
3. 图论模板默认点编号从 1 开始。
4. 线段树和树状数组默认区间为闭区间。
5. 模板改动后要用最小样例测试。
