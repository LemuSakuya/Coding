# CSES 400 题参考答案与中文思路

依据 [CSES 当前题单](https://cses.fi/problemset/list/) 整理，题单核对日期：2026-10-22（北京时间）。共 **400 题、18 类**。

这是供日后按题号对照的参考资料：每题包含中文思路、关键转移或不变量、时间复杂度、易错点、完整参考代码与来源链接。中文条目是思路速查；部分条目给出与所附代码不同但等价的解法，不代表对每行代码逐句注释。

**验证边界：**已核对 400 个官网题号与标题、中文条目及参考代码文件的完整对应，检查文件非空、链接与来源哈希。代码库作者自述这些代码已 AC；本次没有独立核验其账号记录，也没有逐题编译、运行、提交或测试性能。原英文解析由该作者注明为 AI 生成；发现的具体问题已在条目及订正清单标出。这里不将任何代码标为“本次实测 AC”。

## 从这里开始

- [400 题中文思路总览](中文思路总览.md)：可直接搜索题号、英文题名或算法。
- [怎么对答案与常见易错点](使用说明.md)：区分唯一输出、构造、浮点及交互题。
- [原英文解析订正清单](解析订正清单.md)：22 个已发现问题或论证不足的条目。
- [来源与核对记录](来源与核对记录.md)：覆盖统计、检查范围和固定来源版本。

每题的目录内有中文说明、原样参考代码、样例文件以及原作者详细解析链接。本合集没有把原英文 AI 解析批量复制成已审定的中文证明。

## 分类目录

|分类|题数|中文思路|
|---|---:|---|
|01 入门题 / Introductory Problems|24|[打开](chapters/01.md)|
|02 排序与查找 / Sorting and Searching|35|[打开](chapters/02.md)|
|03 动态规划 / Dynamic Programming|23|[打开](chapters/03.md)|
|04 图论基础 / Graph Algorithms|36|[打开](chapters/04.md)|
|05 区间查询 / Range Queries|25|[打开](chapters/05.md)|
|06 树算法 / Tree Algorithms|16|[打开](chapters/06.md)|
|07 数学 / Mathematics|37|[打开](chapters/07.md)|
|08 字符串算法 / String Algorithms|21|[打开](chapters/08.md)|
|09 计算几何 / Geometry|16|[打开](chapters/09.md)|
|10 高级技巧 / Advanced Techniques|25|[打开](chapters/10.md)|
|11 滑动窗口 / Sliding Window Problems|11|[打开](chapters/11.md)|
|12 交互题 / Interactive Problems|6|[打开](chapters/12.md)|
|13 位运算 / Bitwise Operations|11|[打开](chapters/13.md)|
|14 构造题 / Construction Problems|8|[打开](chapters/14.md)|
|15 高级图论 / Advanced Graph Problems|28|[打开](chapters/15.md)|
|16 计数问题 / Counting Problems|18|[打开](chapters/16.md)|
|17 附加题一 / Additional Problems I|30|[打开](chapters/17.md)|
|18 附加题二 / Additional Problems II|30|[打开](chapters/18.md)|

## 全部 400 题索引

|序号|题号|题名|主要方法|资料|
|---:|---:|---|---|---|
|1|1068|Weird Algorithm|模拟|[中文思路与参考代码](problems/1068-weird-algorithm/README.md)|
|2|1083|Missing Number|等差数列求和|[中文思路与参考代码](problems/1083-missing-number/README.md)|
|3|1069|Repetitions|连续段扫描|[中文思路与参考代码](problems/1069-repetitions/README.md)|
|4|1094|Increasing Array|贪心|[中文思路与参考代码](problems/1094-increasing-array/README.md)|
|5|1070|Permutations|构造|[中文思路与参考代码](problems/1070-permutations/README.md)|
|6|1071|Number Spiral|分层公式|[中文思路与参考代码](problems/1071-number-spiral/README.md)|
|7|1072|Two Knights|补集计数|[中文思路与参考代码](problems/1072-two-knights/README.md)|
|8|1092|Two Sets|贪心构造|[中文思路与参考代码](problems/1092-two-sets/README.md)|
|9|1617|Bit Strings|快速幂|[中文思路与参考代码](problems/1617-bit-strings/README.md)|
|10|1618|Trailing Zeros|因子计数|[中文思路与参考代码](problems/1618-trailing-zeros/README.md)|
|11|1754|Coin Piles|方程与可行性|[中文思路与参考代码](problems/1754-coin-piles/README.md)|
|12|1755|Palindrome Reorder|频次与回文构造|[中文思路与参考代码](problems/1755-palindrome-reorder/README.md)|
|13|2205|Gray Code|格雷码|[中文思路与参考代码](problems/2205-gray-code/README.md)|
|14|2165|Tower of Hanoi|递归|[中文思路与参考代码](problems/2165-tower-of-hanoi/README.md)|
|15|1622|Creating Strings|排列枚举|[中文思路与参考代码](problems/1622-creating-strings/README.md)|
|16|1623|Apple Division|子集枚举|[中文思路与参考代码](problems/1623-apple-division/README.md)|
|17|1624|Chessboard and Queens|回溯|[中文思路与参考代码](problems/1624-chessboard-and-queens/README.md)|
|18|3399|Raab Game I|构造|[中文思路与参考代码](problems/3399-raab-game-i/README.md)|
|19|3419|Mex Grid Construction|异或构造|[中文思路与参考代码](problems/3419-mex-grid-construction/README.md)|
|20|3217|Knight Moves Grid|BFS|[中文思路与参考代码](problems/3217-knight-moves-grid/README.md)|
|21|3311|Grid Coloring I|贪心染色|[中文思路与参考代码](problems/3311-grid-coloring-i/README.md)|
|22|2431|Digit Queries|数位定位|[中文思路与参考代码](problems/2431-digit-queries/README.md)|
|23|1743|String Reorder|字典序贪心|[中文思路与参考代码](problems/1743-string-reorder/README.md)|
|24|1625|Grid Path Description|带剪枝回溯|[中文思路与参考代码](problems/1625-grid-path-description/README.md)|
|25|1621|Distinct Numbers|排序去重|[中文思路与参考代码](problems/1621-distinct-numbers/README.md)|
|26|1084|Apartments|排序与双指针|[中文思路与参考代码](problems/1084-apartments/README.md)|
|27|1090|Ferris Wheel|双指针贪心|[中文思路与参考代码](problems/1090-ferris-wheel/README.md)|
|28|1091|Concert Tickets|有序多重集合|[中文思路与参考代码](problems/1091-concert-tickets/README.md)|
|29|1619|Restaurant Customers|扫描线|[中文思路与参考代码](problems/1619-restaurant-customers/README.md)|
|30|1629|Movie Festival|区间调度贪心|[中文思路与参考代码](problems/1629-movie-festival/README.md)|
|31|1640|Sum of Two Values|排序双指针|[中文思路与参考代码](problems/1640-sum-of-two-values/README.md)|
|32|1643|Maximum Subarray Sum|Kadane 算法|[中文思路与参考代码](problems/1643-maximum-subarray-sum/README.md)|
|33|1074|Stick Lengths|中位数|[中文思路与参考代码](problems/1074-stick-lengths/README.md)|
|34|2183|Missing Coin Sum|贪心覆盖|[中文思路与参考代码](problems/2183-missing-coin-sum/README.md)|
|35|2216|Collecting Numbers|位置数组|[中文思路与参考代码](problems/2216-collecting-numbers/README.md)|
|36|2217|Collecting Numbers II|局部贡献维护|[中文思路与参考代码](problems/2217-collecting-numbers-ii/README.md)|
|37|1141|Playlist|滑动窗口|[中文思路与参考代码](problems/1141-playlist/README.md)|
|38|1073|Towers|有序容器贪心|[中文思路与参考代码](problems/1073-towers/README.md)|
|39|1163|Traffic Lights|有序位置与间隔|[中文思路与参考代码](problems/1163-traffic-lights/README.md)|
|40|3420|Distinct Values Subarrays|滑动窗口计数|[中文思路与参考代码](problems/3420-distinct-values-subarrays/README.md)|
|41|3421|Distinct Values Subsequences|乘法原理|[中文思路与参考代码](problems/3421-distinct-values-subsequences/README.md)|
|42|2162|Josephus Problem I|约瑟夫模拟|[中文思路与参考代码](problems/2162-josephus-problem-i/README.md)|
|43|2163|Josephus Problem II|顺序统计树|[中文思路与参考代码](problems/2163-josephus-problem-ii/README.md)|
|44|2168|Nested Ranges Check|排序与前后缀|[中文思路与参考代码](problems/2168-nested-ranges-check/README.md)|
|45|2169|Nested Ranges Count|排序与树状数组|[中文思路与参考代码](problems/2169-nested-ranges-count/README.md)|
|46|1164|Room Allocation|最小堆|[中文思路与参考代码](problems/1164-room-allocation/README.md)|
|47|1620|Factory Machines|二分答案|[中文思路与参考代码](problems/1620-factory-machines/README.md)|
|48|1630|Tasks and Deadlines|排序贪心|[中文思路与参考代码](problems/1630-tasks-and-deadlines/README.md)|
|49|1631|Reading Books|下界与构造|[中文思路与参考代码](problems/1631-reading-books/README.md)|
|50|1641|Sum of Three Values|枚举与双指针|[中文思路与参考代码](problems/1641-sum-of-three-values/README.md)|
|51|1642|Sum of Four Values|两数和哈希|[中文思路与参考代码](problems/1642-sum-of-four-values/README.md)|
|52|1645|Nearest Smaller Values|单调栈|[中文思路与参考代码](problems/1645-nearest-smaller-values/README.md)|
|53|1660|Subarray Sums I|正数滑动窗口|[中文思路与参考代码](problems/1660-subarray-sums-i/README.md)|
|54|1661|Subarray Sums II|前缀和计数|[中文思路与参考代码](problems/1661-subarray-sums-ii/README.md)|
|55|1662|Subarray Divisibility|同余计数|[中文思路与参考代码](problems/1662-subarray-divisibility/README.md)|
|56|2428|Distinct Values Subarrays II|滑动窗口|[中文思路与参考代码](problems/2428-distinct-values-subarrays-ii/README.md)|
|57|1085|Array Division|二分与贪心分段|[中文思路与参考代码](problems/1085-array-division/README.md)|
|58|1632|Movie Festival II|多资源区间调度|[中文思路与参考代码](problems/1632-movie-festival-ii/README.md)|
|59|1644|Maximum Subarray Sum II|前缀和与窗口最小值|[中文思路与参考代码](problems/1644-maximum-subarray-sum-ii/README.md)|
|60|1633|Dice Combinations|线性 DP|[中文思路与参考代码](problems/1633-dice-combinations/README.md)|
|61|1634|Minimizing Coins|完全背包|[中文思路与参考代码](problems/1634-minimizing-coins/README.md)|
|62|1635|Coin Combinations I|有序方案 DP|[中文思路与参考代码](problems/1635-coin-combinations-i/README.md)|
|63|1636|Coin Combinations II|无序完全背包|[中文思路与参考代码](problems/1636-coin-combinations-ii/README.md)|
|64|1637|Removing Digits|数位 DP|[中文思路与参考代码](problems/1637-removing-digits/README.md)|
|65|1638|Grid Paths I|网格 DP|[中文思路与参考代码](problems/1638-grid-paths-i/README.md)|
|66|1158|Book Shop|01 背包|[中文思路与参考代码](problems/1158-book-shop/README.md)|
|67|1746|Array Description|相邻状态 DP|[中文思路与参考代码](problems/1746-array-description/README.md)|
|68|2413|Counting Towers|轮廓 DP|[中文思路与参考代码](problems/2413-counting-towers/README.md)|
|69|1639|Edit Distance|编辑距离 DP|[中文思路与参考代码](problems/1639-edit-distance/README.md)|
|70|3403|Longest Common Subsequence|LCS DP 与回溯|[中文思路与参考代码](problems/3403-longest-common-subsequence/README.md)|
|71|1744|Rectangle Cutting|矩形划分 DP|[中文思路与参考代码](problems/1744-rectangle-cutting/README.md)|
|72|3359|Minimal Grid Path|逐层字典序贪心|[中文思路与参考代码](problems/3359-minimal-grid-path/README.md)|
|73|1745|Money Sums|01 可达性 DP|[中文思路与参考代码](problems/1745-money-sums/README.md)|
|74|1097|Removal Game|区间博弈 DP|[中文思路与参考代码](problems/1097-removal-game/README.md)|
|75|1093|Two Sets II|子集和计数|[中文思路与参考代码](problems/1093-two-sets-ii/README.md)|
|76|3314|Mountain Range|单调栈与区间 DP|[中文思路与参考代码](problems/3314-mountain-range/README.md)|
|77|1145|Increasing Subsequence|最长上升子序列|[中文思路与参考代码](problems/1145-increasing-subsequence/README.md)|
|78|1140|Projects|带权区间调度|[中文思路与参考代码](problems/1140-projects/README.md)|
|79|1653|Elevator Rides|状压 DP|[中文思路与参考代码](problems/1653-elevator-rides/README.md)|
|80|2181|Counting Tilings|轮廓 DP|[中文思路与参考代码](problems/2181-counting-tilings/README.md)|
|81|2220|Counting Numbers|数位 DP|[中文思路与参考代码](problems/2220-counting-numbers/README.md)|
|82|1748|Increasing Subsequence II|树状数组 DP|[中文思路与参考代码](problems/1748-increasing-subsequence-ii/README.md)|
|83|1192|Counting Rooms|连通块搜索|[中文思路与参考代码](problems/1192-counting-rooms/README.md)|
|84|1193|Labyrinth|BFS 与路径恢复|[中文思路与参考代码](problems/1193-labyrinth/README.md)|
|85|1666|Building Roads|连通分量|[中文思路与参考代码](problems/1666-building-roads/README.md)|
|86|1667|Message Route|无权最短路|[中文思路与参考代码](problems/1667-message-route/README.md)|
|87|1668|Building Teams|二分图染色|[中文思路与参考代码](problems/1668-building-teams/README.md)|
|88|1669|Round Trip|无向图找环|[中文思路与参考代码](problems/1669-round-trip/README.md)|
|89|1194|Monsters|多源 BFS|[中文思路与参考代码](problems/1194-monsters/README.md)|
|90|1671|Shortest Routes I|Dijkstra|[中文思路与参考代码](problems/1671-shortest-routes-i/README.md)|
|91|1672|Shortest Routes II|Floyd–Warshall|[中文思路与参考代码](problems/1672-shortest-routes-ii/README.md)|
|92|1673|High Score|Bellman–Ford 与环影响|[中文思路与参考代码](problems/1673-high-score/README.md)|
|93|1195|Flight Discount|两次最短路|[中文思路与参考代码](problems/1195-flight-discount/README.md)|
|94|1197|Cycle Finding|负环检测|[中文思路与参考代码](problems/1197-cycle-finding/README.md)|
|95|1196|Flight Routes|第 k 短路|[中文思路与参考代码](problems/1196-flight-routes/README.md)|
|96|1678|Round Trip II|有向图三色 DFS|[中文思路与参考代码](problems/1678-round-trip-ii/README.md)|
|97|1679|Course Schedule|拓扑排序|[中文思路与参考代码](problems/1679-course-schedule/README.md)|
|98|1680|Longest Flight Route|DAG 最长路|[中文思路与参考代码](problems/1680-longest-flight-route/README.md)|
|99|1681|Game Routes|DAG 路径计数|[中文思路与参考代码](problems/1681-game-routes/README.md)|
|100|1202|Investigation|最短路附加统计|[中文思路与参考代码](problems/1202-investigation/README.md)|
|101|1750|Planets Queries I|倍增|[中文思路与参考代码](problems/1750-planets-queries-i/README.md)|
|102|1160|Planets Queries II|功能图分解|[中文思路与参考代码](problems/1160-planets-queries-ii/README.md)|
|103|1751|Planets Cycles|功能图环与入树|[中文思路与参考代码](problems/1751-planets-cycles/README.md)|
|104|1675|Road Reparation|最小生成树|[中文思路与参考代码](problems/1675-road-reparation/README.md)|
|105|1676|Road Construction|并查集|[中文思路与参考代码](problems/1676-road-construction/README.md)|
|106|1682|Flight Routes Check|正反可达性|[中文思路与参考代码](problems/1682-flight-routes-check/README.md)|
|107|1683|Planets and Kingdoms|强连通分量|[中文思路与参考代码](problems/1683-planets-and-kingdoms/README.md)|
|108|1684|Giant Pizza|2-SAT|[中文思路与参考代码](problems/1684-giant-pizza/README.md)|
|109|1686|Coin Collector|SCC 缩点与 DAG DP|[中文思路与参考代码](problems/1686-coin-collector/README.md)|
|110|1691|Mail Delivery|欧拉回路|[中文思路与参考代码](problems/1691-mail-delivery/README.md)|
|111|1692|De Bruijn Sequence|De Bruijn 图|[中文思路与参考代码](problems/1692-de-bruijn-sequence/README.md)|
|112|1693|Teleporters Path|有向欧拉路径|[中文思路与参考代码](problems/1693-teleporters-path/README.md)|
|113|1690|Hamiltonian Flights|状压路径 DP|[中文思路与参考代码](problems/1690-hamiltonian-flights/README.md)|
|114|1689|Knight's Tour|骑士周游回溯|[中文思路与参考代码](problems/1689-knight-s-tour/README.md)|
|115|1694|Download Speed|最大流|[中文思路与参考代码](problems/1694-download-speed/README.md)|
|116|1695|Police Chase|最小割|[中文思路与参考代码](problems/1695-police-chase/README.md)|
|117|1696|School Dance|二分图匹配|[中文思路与参考代码](problems/1696-school-dance/README.md)|
|118|1711|Distinct Routes|最大流与路径分解|[中文思路与参考代码](problems/1711-distinct-routes/README.md)|
|119|1646|Static Range Sum Queries|前缀和|[中文思路与参考代码](problems/1646-static-range-sum-queries/README.md)|
|120|1647|Static Range Minimum Queries|稀疏表|[中文思路与参考代码](problems/1647-static-range-minimum-queries/README.md)|
|121|1648|Dynamic Range Sum Queries|树状数组|[中文思路与参考代码](problems/1648-dynamic-range-sum-queries/README.md)|
|122|1649|Dynamic Range Minimum Queries|线段树|[中文思路与参考代码](problems/1649-dynamic-range-minimum-queries/README.md)|
|123|1650|Range Xor Queries|前缀异或|[中文思路与参考代码](problems/1650-range-xor-queries/README.md)|
|124|1651|Range Update Queries|差分与树状数组|[中文思路与参考代码](problems/1651-range-update-queries/README.md)|
|125|1652|Forest Queries|二维前缀和|[中文思路与参考代码](problems/1652-forest-queries/README.md)|
|126|1143|Hotel Queries|线段树上二分|[中文思路与参考代码](problems/1143-hotel-queries/README.md)|
|127|1749|List Removals|顺序统计|[中文思路与参考代码](problems/1749-list-removals/README.md)|
|128|1144|Salary Queries|离散化与树状数组|[中文思路与参考代码](problems/1144-salary-queries/README.md)|
|129|2166|Prefix Sum Queries|区间合并|[中文思路与参考代码](problems/2166-prefix-sum-queries/README.md)|
|130|2206|Pizzeria Queries|距离拆项|[中文思路与参考代码](problems/2206-pizzeria-queries/README.md)|
|131|3304|Visible Buildings Queries|可见记录与单调栈|[中文思路与参考代码](problems/3304-visible-buildings-queries/README.md)|
|132|3163|Range Interval Queries|归并排序树|[中文思路与参考代码](problems/3163-range-interval-queries/README.md)|
|133|1190|Subarray Sum Queries|最大子段和线段树|[中文思路与参考代码](problems/1190-subarray-sum-queries/README.md)|
|134|3226|Subarray Sum Queries II|四元组区间合并|[中文思路与参考代码](problems/3226-subarray-sum-queries-ii/README.md)|
|135|1734|Distinct Values Queries|离线查询与树状数组|[中文思路与参考代码](problems/1734-distinct-values-queries/README.md)|
|136|3356|Distinct Values Queries II|动态重复位置|[中文思路与参考代码](problems/3356-distinct-values-queries-ii/README.md)|
|137|2416|Increasing Array Queries|单调栈与区间代价|[中文思路与参考代码](problems/2416-increasing-array-queries/README.md)|
|138|1664|Movie Festival Queries|贪心后继与倍增|[中文思路与参考代码](problems/1664-movie-festival-queries/README.md)|
|139|1739|Forest Queries II|二维树状数组|[中文思路与参考代码](problems/1739-forest-queries-ii/README.md)|
|140|1735|Range Updates and Sums|懒标记线段树|[中文思路与参考代码](problems/1735-range-updates-and-sums/README.md)|
|141|1736|Polynomial Queries|等差更新懒标记|[中文思路与参考代码](problems/1736-polynomial-queries/README.md)|
|142|1737|Range Queries and Copies|可持久化线段树|[中文思路与参考代码](problems/1737-range-queries-and-copies/README.md)|
|143|2184|Missing Coin Sum Queries|值域结构与贪心覆盖|[中文思路与参考代码](problems/2184-missing-coin-sum-queries/README.md)|
|144|1674|Subordinates|子树大小|[中文思路与参考代码](problems/1674-subordinates/README.md)|
|145|1130|Tree Matching|树形 DP|[中文思路与参考代码](problems/1130-tree-matching/README.md)|
|146|1131|Tree Diameter|树的直径|[中文思路与参考代码](problems/1131-tree-diameter/README.md)|
|147|1132|Tree Distances I|直径端点|[中文思路与参考代码](problems/1132-tree-distances-i/README.md)|
|148|1133|Tree Distances II|换根 DP|[中文思路与参考代码](problems/1133-tree-distances-ii/README.md)|
|149|1687|Company Queries I|祖先倍增|[中文思路与参考代码](problems/1687-company-queries-i/README.md)|
|150|1688|Company Queries II|LCA|[中文思路与参考代码](problems/1688-company-queries-ii/README.md)|
|151|1135|Distance Queries|LCA 距离公式|[中文思路与参考代码](problems/1135-distance-queries/README.md)|
|152|1136|Counting Paths|树上差分|[中文思路与参考代码](problems/1136-counting-paths/README.md)|
|153|1137|Subtree Queries|DFS 序与树状数组|[中文思路与参考代码](problems/1137-subtree-queries/README.md)|
|154|1138|Path Queries|根路径和与子树更新|[中文思路与参考代码](problems/1138-path-queries/README.md)|
|155|2134|Path Queries II|树链剖分|[中文思路与参考代码](problems/2134-path-queries-ii/README.md)|
|156|1139|Distinct Colors|小并大|[中文思路与参考代码](problems/1139-distinct-colors/README.md)|
|157|2079|Finding a Centroid|重心|[中文思路与参考代码](problems/2079-finding-a-centroid/README.md)|
|158|2080|Fixed-Length Paths I|点分治|[中文思路与参考代码](problems/2080-fixed-length-paths-i/README.md)|
|159|2081|Fixed-Length Paths II|点分治与深度前缀|[中文思路与参考代码](problems/2081-fixed-length-paths-ii/README.md)|
|160|2164|Josephus Queries|递归约瑟夫|[中文思路与参考代码](problems/2164-josephus-queries/README.md)|
|161|1095|Exponentiation|模快速幂|[中文思路与参考代码](problems/1095-exponentiation/README.md)|
|162|1712|Exponentiation II|指数降幂|[中文思路与参考代码](problems/1712-exponentiation-ii/README.md)|
|163|1713|Counting Divisors|约数筛|[中文思路与参考代码](problems/1713-counting-divisors/README.md)|
|164|1081|Common Divisors|倍数计数|[中文思路与参考代码](problems/1081-common-divisors/README.md)|
|165|1082|Sum of Divisors|整除分块|[中文思路与参考代码](problems/1082-sum-of-divisors/README.md)|
|166|2182|Divisor Analysis|质因数分解公式|[中文思路与参考代码](problems/2182-divisor-analysis/README.md)|
|167|2185|Prime Multiples|容斥原理|[中文思路与参考代码](problems/2185-prime-multiples/README.md)|
|168|2417|Counting Coprime Pairs|莫比乌斯反演|[中文思路与参考代码](problems/2417-counting-coprime-pairs/README.md)|
|169|3396|Next Prime|素性测试|[中文思路与参考代码](problems/3396-next-prime/README.md)|
|170|1079|Binomial Coefficients|阶乘与逆元|[中文思路与参考代码](problems/1079-binomial-coefficients/README.md)|
|171|1715|Creating Strings II|多重集排列|[中文思路与参考代码](problems/1715-creating-strings-ii/README.md)|
|172|1716|Distributing Apples|隔板法|[中文思路与参考代码](problems/1716-distributing-apples/README.md)|
|173|1717|Christmas Party|错排 DP|[中文思路与参考代码](problems/1717-christmas-party/README.md)|
|174|3397|Permutation Order|康托展开|[中文思路与参考代码](problems/3397-permutation-order/README.md)|
|175|3398|Permutation Rounds|置换循环与最小公倍数|[中文思路与参考代码](problems/3398-permutation-rounds/README.md)|
|176|2064|Bracket Sequences I|卡特兰数|[中文思路与参考代码](problems/2064-bracket-sequences-i/README.md)|
|177|2187|Bracket Sequences II|带固定前缀的括号计数|[中文思路与参考代码](problems/2187-bracket-sequences-ii/README.md)|
|178|2209|Counting Necklaces|Burnside 引理|[中文思路与参考代码](problems/2209-counting-necklaces/README.md)|
|179|2210|Counting Grids|旋转等价计数|[中文思路与参考代码](problems/2210-counting-grids/README.md)|
|180|1722|Fibonacci Numbers|矩阵快速幂|[中文思路与参考代码](problems/1722-fibonacci-numbers/README.md)|
|181|1096|Throwing Dice|线性递推与矩阵幂|[中文思路与参考代码](problems/1096-throwing-dice/README.md)|
|182|1723|Graph Paths I|邻接矩阵幂|[中文思路与参考代码](problems/1723-graph-paths-i/README.md)|
|183|1724|Graph Paths II|min-plus 矩阵幂|[中文思路与参考代码](problems/1724-graph-paths-ii/README.md)|
|184|3154|System of Linear Equations|模意义高斯消元|[中文思路与参考代码](problems/3154-system-of-linear-equations/README.md)|
|185|3355|Sum of Four Squares|两平方和配对|[中文思路与参考代码](problems/3355-sum-of-four-squares/README.md)|
|186|3406|Triangle Number Sums|三角数定理|[中文思路与参考代码](problems/3406-triangle-number-sums/README.md)|
|187|1725|Dice Probability|概率 DP|[中文思路与参考代码](problems/1725-dice-probability/README.md)|
|188|1726|Moving Robots|期望线性性|[中文思路与参考代码](problems/1726-moving-robots/README.md)|
|189|1727|Candy Lottery|最大值分布|[中文思路与参考代码](problems/1727-candy-lottery/README.md)|
|190|1728|Inversion Probability|逆序贡献与期望|[中文思路与参考代码](problems/1728-inversion-probability/README.md)|
|191|1729|Stick Game|必胜必败 DP|[中文思路与参考代码](problems/1729-stick-game/README.md)|
|192|1730|Nim Game I|Nim 异或|[中文思路与参考代码](problems/1730-nim-game-i/README.md)|
|193|1098|Nim Game II|减法游戏 SG|[中文思路与参考代码](problems/1098-nim-game-ii/README.md)|
|194|1099|Stair Game|阶梯博弈|[中文思路与参考代码](problems/1099-stair-game/README.md)|
|195|2207|Grundy's Game|Sprague–Grundy|[中文思路与参考代码](problems/2207-grundy-s-game/README.md)|
|196|2208|Another Game|奇偶策略|[中文思路与参考代码](problems/2208-another-game/README.md)|
|197|1731|Word Combinations|Trie 与后缀 DP|[中文思路与参考代码](problems/1731-word-combinations/README.md)|
|198|1753|String Matching|KMP|[中文思路与参考代码](problems/1753-string-matching/README.md)|
|199|1732|Finding Borders|前缀函数|[中文思路与参考代码](problems/1732-finding-borders/README.md)|
|200|1733|Finding Periods|Z 函数|[中文思路与参考代码](problems/1733-finding-periods/README.md)|
|201|1110|Minimal Rotation|最小表示法|[中文思路与参考代码](problems/1110-minimal-rotation/README.md)|
|202|1111|Longest Palindrome|Manacher|[中文思路与参考代码](problems/1111-longest-palindrome/README.md)|
|203|3138|All Palindromes|回文树|[中文思路与参考代码](problems/3138-all-palindromes/README.md)|
|204|1112|Required Substring|KMP 自动机 DP|[中文思路与参考代码](problems/1112-required-substring/README.md)|
|205|2420|Palindrome Queries|动态字符串哈希|[中文思路与参考代码](problems/2420-palindrome-queries/README.md)|
|206|2102|Finding Patterns|Aho–Corasick|[中文思路与参考代码](problems/2102-finding-patterns/README.md)|
|207|2103|Counting Patterns|AC 自动机计数|[中文思路与参考代码](problems/2103-counting-patterns/README.md)|
|208|2104|Pattern Positions|AC 自动机最早位置|[中文思路与参考代码](problems/2104-pattern-positions/README.md)|
|209|2105|Distinct Substrings|后缀数组与 LCP|[中文思路与参考代码](problems/2105-distinct-substrings/README.md)|
|210|1149|Distinct Subsequences|不同子序列 DP|[中文思路与参考代码](problems/1149-distinct-subsequences/README.md)|
|211|2106|Repeating Substring|后缀数组|[中文思路与参考代码](problems/2106-repeating-substring/README.md)|
|212|2107|String Functions|Z 与前缀函数|[中文思路与参考代码](problems/2107-string-functions/README.md)|
|213|3225|Inverse Suffix Array|逆后缀数组构造|[中文思路与参考代码](problems/3225-inverse-suffix-array/README.md)|
|214|1113|String Transform|逆 BWT|[中文思路与参考代码](problems/1113-string-transform/README.md)|
|215|2108|Substring Order I|第 k 小不同子串|[中文思路与参考代码](problems/2108-substring-order-i/README.md)|
|216|2109|Substring Order II|后缀自动机加权选择|[中文思路与参考代码](problems/2109-substring-order-ii/README.md)|
|217|2110|Substring Distribution|子串长度分布|[中文思路与参考代码](problems/2110-substring-distribution/README.md)|
|218|2189|Point Location Test|叉积|[中文思路与参考代码](problems/2189-point-location-test/README.md)|
|219|2190|Line Segment Intersection|线段相交|[中文思路与参考代码](problems/2190-line-segment-intersection/README.md)|
|220|2191|Polygon Area|鞋带公式|[中文思路与参考代码](problems/2191-polygon-area/README.md)|
|221|2192|Point in Polygon|射线法|[中文思路与参考代码](problems/2192-point-in-polygon/README.md)|
|222|2193|Polygon Lattice Points|Pick 定理|[中文思路与参考代码](problems/2193-polygon-lattice-points/README.md)|
|223|2194|Minimum Euclidean Distance|最近点对|[中文思路与参考代码](problems/2194-minimum-euclidean-distance/README.md)|
|224|2195|Convex Hull|凸包|[中文思路与参考代码](problems/2195-convex-hull/README.md)|
|225|3410|Maximum Manhattan Distances|坐标变换|[中文思路与参考代码](problems/3410-maximum-manhattan-distances/README.md)|
|226|3411|All Manhattan Distances|分维贡献|[中文思路与参考代码](problems/3411-all-manhattan-distances/README.md)|
|227|1740|Intersection Points|扫描线与树状数组|[中文思路与参考代码](problems/1740-intersection-points/README.md)|
|228|3427|Line Segments Trace I|李超树|[中文思路与参考代码](problems/3427-line-segments-trace-i/README.md)|
|229|3428|Line Segments Trace II|区间李超树|[中文思路与参考代码](problems/3428-line-segments-trace-ii/README.md)|
|230|3429|Lines and Queries I|动态直线最值|[中文思路与参考代码](problems/3429-lines-and-queries-i/README.md)|
|231|3430|Lines and Queries II|动态线段最值|[中文思路与参考代码](problems/3430-lines-and-queries-ii/README.md)|
|232|1741|Area of Rectangles|面积扫描线|[中文思路与参考代码](problems/1741-area-of-rectangles/README.md)|
|233|1742|Robot Path|二分首次自交|[中文思路与参考代码](problems/1742-robot-path/README.md)|
|234|1628|Meet in the Middle|折半搜索|[中文思路与参考代码](problems/1628-meet-in-the-middle/README.md)|
|235|2136|Hamming Distance|位压缩|[中文思路与参考代码](problems/2136-hamming-distance/README.md)|
|236|3360|Corner Subgrid Check|鸽巢与列对|[中文思路与参考代码](problems/3360-corner-subgrid-check/README.md)|
|237|2137|Corner Subgrid Count|位集与组合数|[中文思路与参考代码](problems/2137-corner-subgrid-count/README.md)|
|238|2138|Reachable Nodes|DAG 位集 DP|[中文思路与参考代码](problems/2138-reachable-nodes/README.md)|
|239|2143|Reachability Queries|SCC 缩点与位集|[中文思路与参考代码](problems/2143-reachability-queries/README.md)|
|240|2072|Cut and Paste|隐式 Treap|[中文思路与参考代码](problems/2072-cut-and-paste/README.md)|
|241|2073|Substring Reversals|隐式 Treap 与翻转标记|[中文思路与参考代码](problems/2073-substring-reversals/README.md)|
|242|2074|Reversals and Sums|序列树区间维护|[中文思路与参考代码](problems/2074-reversals-and-sums/README.md)|
|243|2076|Necessary Roads|桥|[中文思路与参考代码](problems/2076-necessary-roads/README.md)|
|244|2077|Necessary Cities|割点|[中文思路与参考代码](problems/2077-necessary-cities/README.md)|
|245|2078|Eulerian Subgraphs|环空间计数|[中文思路与参考代码](problems/2078-eulerian-subgraphs/README.md)|
|246|2084|Monster Game I|凸包优化 DP|[中文思路与参考代码](problems/2084-monster-game-i/README.md)|
|247|2085|Monster Game II|李超树优化 DP|[中文思路与参考代码](problems/2085-monster-game-ii/README.md)|
|248|2086|Subarray Squares|分段平方和 DP|[中文思路与参考代码](problems/2086-subarray-squares/README.md)|
|249|2087|Houses and Schools|一维设施选址|[中文思路与参考代码](problems/2087-houses-and-schools/README.md)|
|250|2088|Knuth Division|Knuth 优化|[中文思路与参考代码](problems/2088-knuth-division/README.md)|
|251|2111|Apples and Bananas|卷积|[中文思路与参考代码](problems/2111-apples-and-bananas/README.md)|
|252|2112|One Bit Positions|相关运算|[中文思路与参考代码](problems/2112-one-bit-positions/README.md)|
|253|2113|Signal Processing|互相关与卷积|[中文思路与参考代码](problems/2113-signal-processing/README.md)|
|254|2101|New Roads Queries|合并树与 LCA|[中文思路与参考代码](problems/2101-new-roads-queries/README.md)|
|255|2133|Dynamic Connectivity|时间线段树与回滚并查集|[中文思路与参考代码](problems/2133-dynamic-connectivity/README.md)|
|256|2121|Parcel Delivery|最小费用流|[中文思路与参考代码](problems/2121-parcel-delivery/README.md)|
|257|2129|Task Assignment|指派问题|[中文思路与参考代码](problems/2129-task-assignment/README.md)|
|258|2130|Distinct Routes II|带费用流与路径分解|[中文思路与参考代码](problems/2130-distinct-routes-ii/README.md)|
|259|3220|Sliding Window Sum|滑动窗口求和|[中文思路与参考代码](problems/3220-sliding-window-sum/README.md)|
|260|3221|Sliding Window Minimum|单调队列|[中文思路与参考代码](problems/3221-sliding-window-minimum/README.md)|
|261|3426|Sliding Window Xor|前缀异或或滚动异或|[中文思路与参考代码](problems/3426-sliding-window-xor/README.md)|
|262|3405|Sliding Window Or|双栈聚合队列|[中文思路与参考代码](problems/3405-sliding-window-or/README.md)|
|263|3222|Sliding Window Distinct Values|频次窗口|[中文思路与参考代码](problems/3222-sliding-window-distinct-values/README.md)|
|264|3224|Sliding Window Mode|频次与有序集合|[中文思路与参考代码](problems/3224-sliding-window-mode/README.md)|
|265|3219|Sliding Window Mex|缺失值集合|[中文思路与参考代码](problems/3219-sliding-window-mex/README.md)|
|266|1076|Sliding Window Median|动态第 k 小|[中文思路与参考代码](problems/1076-sliding-window-median/README.md)|
|267|1077|Sliding Window Cost|中位数与两侧和|[中文思路与参考代码](problems/1077-sliding-window-cost/README.md)|
|268|3223|Sliding Window Inversions|树状数组维护逆序|[中文思路与参考代码](problems/3223-sliding-window-inversions/README.md)|
|269|3227|Sliding Window Advertisement|单调栈与区间直线|[中文思路与参考代码](problems/3227-sliding-window-advertisement/README.md)|
|270|3112|Hidden Integer|交互二分|[中文思路与参考代码](problems/3112-hidden-integer/README.md)|
|271|3139|Hidden Permutation|交互归并排序|[中文思路与参考代码](problems/3139-hidden-permutation/README.md)|
|272|3305|K-th Highest Score|两有序数组第 k 大|[中文思路与参考代码](problems/3305-k-th-highest-score/README.md)|
|273|3228|Permuted Binary Strings|二进制编码询问|[中文思路与参考代码](problems/3228-permuted-binary-strings/README.md)|
|274|3273|Colored Chairs|奇偶不变量二分|[中文思路与参考代码](problems/3273-colored-chairs/README.md)|
|275|3140|Inversion Sorting|逆序差恢复|[中文思路与参考代码](problems/3140-inversion-sorting/README.md)|
|276|1146|Counting Bits|按二进制位计数|[中文思路与参考代码](problems/1146-counting-bits/README.md)|
|277|1655|Maximum Xor Subarray|前缀异或 Trie|[中文思路与参考代码](problems/1655-maximum-xor-subarray/README.md)|
|278|3191|Maximum Xor Subset|异或线性基|[中文思路与参考代码](problems/3191-maximum-xor-subset/README.md)|
|279|3211|Number of Subset Xors|线性基秩|[中文思路与参考代码](problems/3211-number-of-subset-xors/README.md)|
|280|3192|K Subset Xors|规范线性基与第 k 小|[中文思路与参考代码](problems/3192-k-subset-xors/README.md)|
|281|3233|All Subarray Xors|异或卷积 FWHT|[中文思路与参考代码](problems/3233-all-subarray-xors/README.md)|
|282|2419|Xor Pyramid Peak|Lucas 定理|[中文思路与参考代码](problems/2419-xor-pyramid-peak/README.md)|
|283|3194|Xor Pyramid Diagonal|SOS 异或变换|[中文思路与参考代码](problems/3194-xor-pyramid-diagonal/README.md)|
|284|3195|Xor Pyramid Row|二进制倍增|[中文思路与参考代码](problems/3195-xor-pyramid-row/README.md)|
|285|1654|SOS Bit Problem|SOS 计数|[中文思路与参考代码](problems/1654-sos-bit-problem/README.md)|
|286|3141|And Subset Count|超集变换与莫比乌斯反演|[中文思路与参考代码](problems/3141-and-subset-count/README.md)|
|287|2214|Inverse Inversions|逆序预算构造|[中文思路与参考代码](problems/2214-inverse-inversions/README.md)|
|288|2215|Monotone Subsequences|分块构造|[中文思路与参考代码](problems/2215-monotone-subsequences/README.md)|
|289|3422|Third Permutation|置换避禁构造|[中文思路与参考代码](problems/3422-third-permutation/README.md)|
|290|3423|Permutation Prime Sums|素数配对构造|[中文思路与参考代码](problems/3423-permutation-prime-sums/README.md)|
|291|1697|Chess Tournament|Havel–Hakimi|[中文思路与参考代码](problems/1697-chess-tournament/README.md)|
|292|3424|Distinct Sums Grid|矩阵构造与局部交换|[中文思路与参考代码](problems/3424-distinct-sums-grid/README.md)|
|293|2423|Filling Trominos|L 形三格骨牌|[中文思路与参考代码](problems/2423-filling-trominos/README.md)|
|294|2418|Grid Path Construction|网格哈密顿路径构造|[中文思路与参考代码](problems/2418-grid-path-construction/README.md)|
|295|3303|Nearest Shops|多源 BFS|[中文思路与参考代码](problems/3303-nearest-shops/README.md)|
|296|1134|Prüfer Code|Prüfer 解码|[中文思路与参考代码](problems/1134-pr-fer-code/README.md)|
|297|1702|Tree Traversals|二叉树遍历重建|[中文思路与参考代码](problems/1702-tree-traversals/README.md)|
|298|1757|Course Schedule II|逆向拓扑贪心|[中文思路与参考代码](problems/1757-course-schedule-ii/README.md)|
|299|1756|Acyclic Graph Edges|无环定向|[中文思路与参考代码](problems/1756-acyclic-graph-edges/README.md)|
|300|2177|Strongly Connected Edges|DFS 强连通定向|[中文思路与参考代码](problems/2177-strongly-connected-edges/README.md)|
|301|2179|Even Outdegree Edges|出度奇偶调整|[中文思路与参考代码](problems/2179-even-outdegree-edges/README.md)|
|302|1707|Graph Girth|最短环|[中文思路与参考代码](problems/1707-graph-girth/README.md)|
|303|3357|Fixed Length Walk Queries|带奇偶状态 BFS|[中文思路与参考代码](problems/3357-fixed-length-walk-queries/README.md)|
|304|3111|Transfer Speeds Sum|按权倒序并查集|[中文思路与参考代码](problems/3111-transfer-speeds-sum/README.md)|
|305|3407|MST Edge Check|MST 边可选性|[中文思路与参考代码](problems/3407-mst-edge-check/README.md)|
|306|3408|MST Edge Set Check|MST 边集可选性|[中文思路与参考代码](problems/3408-mst-edge-set-check/README.md)|
|307|3409|MST Edge Cost|强制包含某边的 MST|[中文思路与参考代码](problems/3409-mst-edge-cost/README.md)|
|308|1677|Network Breakdown|逆序删边|[中文思路与参考代码](problems/1677-network-breakdown/README.md)|
|309|3114|Tree Coin Collecting I|树路径绕行|[中文思路与参考代码](problems/3114-tree-coin-collecting-i/README.md)|
|310|3149|Tree Coin Collecting II|必要子树与遍历|[中文思路与参考代码](problems/3149-tree-coin-collecting-ii/README.md)|
|311|1700|Tree Isomorphism I|有根树规范编码|[中文思路与参考代码](problems/1700-tree-isomorphism-i/README.md)|
|312|1701|Tree Isomorphism II|无根树同构|[中文思路与参考代码](problems/1701-tree-isomorphism-ii/README.md)|
|313|1699|Flight Route Requests|请求图弱连通分量|[中文思路与参考代码](problems/1699-flight-route-requests/README.md)|
|314|1703|Critical Cities|支配树|[中文思路与参考代码](problems/1703-critical-cities/README.md)|
|315|1203|Visiting Cities|最短路 DAG 的支配点|[中文思路与参考代码](problems/1203-visiting-cities/README.md)|
|316|3308|Graph Coloring|独立集状压 DP|[中文思路与参考代码](problems/3308-graph-coloring/README.md)|
|317|3158|Bus Companies|辅助节点建图|[中文思路与参考代码](problems/3158-bus-companies/README.md)|
|318|3358|Split into Two Paths|DAG 最小路径覆盖|[中文思路与参考代码](problems/3358-split-into-two-paths/README.md)|
|319|1704|Network Renovation|树叶配对增边|[中文思路与参考代码](problems/1704-network-renovation/README.md)|
|320|1705|Forbidden Cities|圆方树或割点祖先关系|[中文思路与参考代码](problems/1705-forbidden-cities/README.md)|
|321|1752|Creating Offices|树上距离贪心|[中文思路与参考代码](problems/1752-creating-offices/README.md)|
|322|1685|New Flight Routes|SCC 缩点增边|[中文思路与参考代码](problems/1685-new-flight-routes/README.md)|
|323|3413|Filled Subgrid Count I|最大同色正方形 DP|[中文思路与参考代码](problems/3413-filled-subgrid-count-i/README.md)|
|324|3414|Filled Subgrid Count II|柱状图与单调栈|[中文思路与参考代码](problems/3414-filled-subgrid-count-ii/README.md)|
|325|3415|All Letter Subgrid Count I|字母掩码与倍增|[中文思路与参考代码](problems/3415-all-letter-subgrid-count-i/README.md)|
|326|3416|All Letter Subgrid Count II|二维 OR 查询与双指针|[中文思路与参考代码](problems/3416-all-letter-subgrid-count-ii/README.md)|
|327|3417|Border Subgrid Count I|对角线扫描与树状数组|[中文思路与参考代码](problems/3417-border-subgrid-count-i/README.md)|
|328|3418|Border Subgrid Count II|枚举行对与边框计数|[中文思路与参考代码](problems/3418-border-subgrid-count-ii/README.md)|
|329|3400|Raab Game II|错排的胜负分布|[中文思路与参考代码](problems/3400-raab-game-ii/README.md)|
|330|1080|Empty String|区间 DP 与交错删除|[中文思路与参考代码](problems/1080-empty-string/README.md)|
|331|2229|Permutation Inversions|逆序生成函数|[中文思路与参考代码](problems/2229-permutation-inversions/README.md)|
|332|2176|Counting Bishops|黑白棋盘 DP|[中文思路与参考代码](problems/2176-counting-bishops/README.md)|
|333|2228|Counting Sequences|满射容斥|[中文思路与参考代码](problems/2228-counting-sequences/README.md)|
|334|1078|Grid Paths II|障碍点组合 DP|[中文思路与参考代码](problems/1078-grid-paths-ii/README.md)|
|335|1075|Counting Permutations|禁邻容斥递推|[中文思路与参考代码](problems/1075-counting-permutations/README.md)|
|336|2429|Grid Completion|双排列与冲突容斥|[中文思路与参考代码](problems/2429-grid-completion/README.md)|
|337|2421|Counting Reorders|相同字符粘合容斥|[中文思路与参考代码](problems/2421-counting-reorders/README.md)|
|338|3232|Tournament Graph Distribution|强连通竞赛图分布|[中文思路与参考代码](problems/3232-tournament-graph-distribution/README.md)|
|339|3157|Collecting Numbers Distribution|欧拉数|[中文思路与参考代码](problems/3157-collecting-numbers-distribution/README.md)|
|340|2415|Functional Graph Distribution|循环顶点与第一类 Stirling 数|[中文思路与参考代码](problems/2415-functional-graph-distribution/README.md)|
|341|1087|Shortest Subsequence|贪心分块|[中文思路与参考代码](problems/1087-shortest-subsequence/README.md)|
|342|3150|Distinct Values Sum|逐出现位置贡献|[中文思路与参考代码](problems/3150-distinct-values-sum/README.md)|
|343|3190|Distinct Values Splits|合法分段 DP|[中文思路与参考代码](problems/3190-distinct-values-splits/README.md)|
|344|1670|Swap Game|状态压缩 BFS|[中文思路与参考代码](problems/1670-swap-game/README.md)|
|345|3175|Beautiful Permutation II|字典序回溯|[中文思路与参考代码](problems/3175-beautiful-permutation-ii/README.md)|
|346|2422|Multiplication Table|乘法表中位数|[中文思路与参考代码](problems/2422-multiplication-table/README.md)|
|347|3151|Bubble Sort Rounds I|稳定排序位移|[中文思路与参考代码](problems/3151-bubble-sort-rounds-i/README.md)|
|348|3152|Bubble Sort Rounds II|有限轮冒泡与堆|[中文思路与参考代码](problems/3152-bubble-sort-rounds-ii/README.md)|
|349|3306|Nearest Campsites I|四象限扫描|[中文思路与参考代码](problems/3306-nearest-campsites-i/README.md)|
|350|3307|Nearest Campsites II|四象限最近点|[中文思路与参考代码](problems/3307-nearest-campsites-ii/README.md)|
|351|1142|Advertisement|柱状图最大矩形|[中文思路与参考代码](problems/1142-advertisement/README.md)|
|352|2186|Special Substrings|频次差状态|[中文思路与参考代码](problems/2186-special-substrings/README.md)|
|353|3169|Counting LCM Arrays|按质因子拆分|[中文思路与参考代码](problems/3169-counting-lcm-arrays/README.md)|
|354|3193|Square Subsets|质因子奇偶与线性基|[中文思路与参考代码](problems/3193-square-subsets/README.md)|
|355|3294|Subarray Sum Constraints|带权并查集|[中文思路与参考代码](problems/3294-subarray-sum-constraints/README.md)|
|356|3213|Water Containers Moves|状态图 Dijkstra|[中文思路与参考代码](problems/3213-water-containers-moves/README.md)|
|357|3214|Water Containers Queries|gcd 可达性|[中文思路与参考代码](problems/3214-water-containers-queries/README.md)|
|358|2425|Stack Weights|后缀和支配|[中文思路与参考代码](problems/2425-stack-weights/README.md)|
|359|3301|Maximum Average Subarrays|前缀和凸包|[中文思路与参考代码](problems/3301-maximum-average-subarrays/README.md)|
|360|3302|Subsets with Fixed Average|平移后的子集和|[中文思路与参考代码](problems/3302-subsets-with-fixed-average/README.md)|
|361|3361|Two Array Average|二分平均值|[中文思路与参考代码](problems/3361-two-array-average/README.md)|
|362|1747|Pyramid Array|剥离最小值贪心|[中文思路与参考代码](problems/1747-pyramid-array/README.md)|
|363|3404|Permutation Subsequence|排列位置映射与 LIS|[中文思路与参考代码](problems/3404-permutation-subsequence/README.md)|
|364|1188|Bit Inversions|连续段维护|[中文思路与参考代码](problems/1188-bit-inversions/README.md)|
|365|1086|Writing Numbers|数位计数与二分|[中文思路与参考代码](problems/1086-writing-numbers/README.md)|
|366|2427|Letter Pair Move Game|相邻字母对移动构造|[中文思路与参考代码](problems/2427-letter-pair-move-game/README.md)|
|367|1147|Maximum Building I|逐行柱状图|[中文思路与参考代码](problems/1147-maximum-building-i/README.md)|
|368|1162|Sorting Methods|四种排序代价|[中文思路与参考代码](problems/1162-sorting-methods/README.md)|
|369|1191|Cyclic Array|环形倍长与倍增|[中文思路与参考代码](problems/1191-cyclic-array/README.md)|
|370|2414|List of Sums|枚举初值与多重集恢复|[中文思路与参考代码](problems/2414-list-of-sums/README.md)|
|371|3215|Bouncing Ball Steps|反射展开与容斥|[中文思路与参考代码](problems/3215-bouncing-ball-steps/README.md)|
|372|3216|Bouncing Ball Cycle|反射周期与格点计数|[中文思路与参考代码](problems/3216-bouncing-ball-cycle/README.md)|
|373|3218|Knight Moves Queries|马步下界与边界修正|[中文思路与参考代码](problems/3218-knight-moves-queries/README.md)|
|374|3108|K Subset Sums I|堆枚举子集和|[中文思路与参考代码](problems/3108-k-subset-sums-i/README.md)|
|375|3109|K Subset Sums II|固定大小子集枚举|[中文思路与参考代码](problems/3109-k-subset-sums-ii/README.md)|
|376|2132|Increasing Array II|保序回归与堆|[中文思路与参考代码](problems/2132-increasing-array-ii/README.md)|
|377|1189|Food Division|环上流量与中位数|[中文思路与参考代码](problems/1189-food-division/README.md)|
|378|1698|Swap Round Sorting|置换分解成两次对合|[中文思路与参考代码](problems/1698-swap-round-sorting/README.md)|
|379|2430|Binary Subsequences|反推不同子序列数|[中文思路与参考代码](problems/2430-binary-subsequences/README.md)|
|380|1706|School Excursion|连通块背包|[中文思路与参考代码](problems/1706-school-excursion/README.md)|
|381|1709|Coin Grid|二分图最小点覆盖|[中文思路与参考代码](problems/1709-coin-grid/README.md)|
|382|3312|Grid Coloring II|2-SAT 染色|[中文思路与参考代码](problems/3312-grid-coloring-ii/README.md)|
|383|2426|Programmers and Artists|差值排序与双堆|[中文思路与参考代码](problems/2426-programmers-and-artists/README.md)|
|384|2174|Removing Digits II|十进制分块记忆化|[中文思路与参考代码](problems/2174-removing-digits-ii/README.md)|
|385|2180|Coin Arrangement|两行运输贪心|[中文思路与参考代码](problems/2180-coin-arrangement/README.md)|
|386|3159|Replace with Difference|等和划分与构造|[中文思路与参考代码](problems/3159-replace-with-difference/README.md)|
|387|2432|Grid Puzzle I|二分图流量|[中文思路与参考代码](problems/2432-grid-puzzle-i/README.md)|
|388|2131|Grid Puzzle II|带费用二分图流|[中文思路与参考代码](problems/2131-grid-puzzle-ii/README.md)|
|389|2115|Bit Substrings|前缀 1 数与卷积|[中文思路与参考代码](problems/2115-bit-substrings/README.md)|
|390|2075|Reversal Sorting|隐式 Treap 排列排序|[中文思路与参考代码](problems/2075-reversal-sorting/README.md)|
|391|1159|Book Shop II|多重背包|[中文思路与参考代码](problems/1159-book-shop-ii/README.md)|
|392|3161|GCD Subsets|倍数反演|[中文思路与参考代码](problems/3161-gcd-subsets/README.md)|
|393|3402|Minimum Cost Pairs|路径匹配与反悔贪心|[中文思路与参考代码](problems/3402-minimum-cost-pairs/README.md)|
|394|3425|Same Sum Subsets|鸽巢与折半计数|[中文思路与参考代码](problems/3425-same-sum-subsets/README.md)|
|395|1157|Mex Grid Queries|Nim 表公式|[中文思路与参考代码](problems/1157-mex-grid-queries/README.md)|
|396|1148|Maximum Building II|按唯一最小柱计数|[中文思路与参考代码](problems/1148-maximum-building-ii/README.md)|
|397|1161|Stick Divisions|Huffman 合并|[中文思路与参考代码](problems/1161-stick-divisions/README.md)|
|398|3401|Stick Difference|两类贪心序列与扫描|[中文思路与参考代码](problems/3401-stick-difference/README.md)|
|399|1665|Coding Company|开放分组 DP|[中文思路与参考代码](problems/1665-coding-company/README.md)|
|400|2402|Two Stacks Sorting|栈冲突与二染色|[中文思路与参考代码](problems/2402-two-stacks-sorting/README.md)|
