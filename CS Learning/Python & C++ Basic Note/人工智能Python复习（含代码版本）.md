# 人工智能 Python 复习

> 同一套教材章节，按「第一次学也能跟上」重写。
> 每节固定节奏：**先记住一句话 → 为什么 → 怎么写 → 逐步看代码 → 常见坑**。
> 代码可直接在 Python 3.8+ 里跑。官方文档：
> [教程](https://docs.python.org/zh-cn/3/tutorial/index.html) ·
> [内置类型](https://docs.python.org/zh-cn/3/library/stdtypes.html) ·
> [标准库](https://docs.python.org/zh-cn/3/library/index.html)

**怎么用：** 先扫目录；每节先读「先记住一句话」再看代码；亲手改数字再跑；「坑」是考试最爱考的地方。章号保持教材习惯（2–10、13）。第 0 章是课前补脑。 

---

## 第 0 章　课前必须先通的 6 件事

后面所有「为什么报错」，几乎都能回到这里。

### 0.1 变量不是盒子，是便利贴

`a = 3` 更准确的说法是：**名字 `a` 被贴到了对象 `3` 上面。**

```python
a = [1, 2, 3]
b = a          # b 和 a 贴的是同一张列表，不是复印件
b.append(4)
print(a)       # [1, 2, 3, 4]  —— a 也变了

a = [1, 2, 3]
b = a.copy()   # 或 a[:] / list(a)
b.append(4)
print(a, b)    # [1, 2, 3]  [1, 2, 3, 4]
```

### 0.2 可变 vs 不可变

| 类型 | 改不改得了「这个对象自己」 | 代表 |
|------|---------------------------|------|
| 不可变 | 改不了，想改只能造新对象 | `int` `float` `str` `tuple` `frozenset` |
| 可变 | 可以原地改 | `list` `dict` `set` |

```python
s = "hi"
# s[0] = "H"     # TypeError：字符串不可变
s = "Hi"         # 这是让名字 s 改贴到一个新字符串上

lst = [1, 2]
lst[0] = 9       # 合法：列表可变，原地改第 0 格
```

### 0.3 下标从 0 开始，切片「含头不含尾」

```
元素:   A    B    C    D    E
下标:   0    1    2    3    4
负下标: -5  -4   -3   -2   -1
```

写法 `s[start:stop:step]`：`start` 含，`stop` 不含，`step` 默认 1（为负则倒着走）。

```python
s = ["A", "B", "C", "D", "E"]
print(s[1:4])     # ['B', 'C', 'D']
print(s[:3])      # ['A', 'B', 'C']
print(s[2:])      # ['C', 'D', 'E']
print(s[::2])     # ['A', 'C', 'E']
print(s[::-1])    # ['E', 'D', 'C', 'B', 'A']
```

### 0.4 缩进就是语法

Python 不用 `{}` 包代码块，用**同一层级的 4 个空格**表示从属。不要 Tab 和空格混用。

```python
x = 3
if x > 0:
    print("正数")           # 属于 if
print("这行已经离开 if")
```

### 0.5 `None`、真假、空容器

- `None` 表示「没有值」，不是 0，也不是 `""`。
- `if` 里当假：`None`、`False`、`0`、`0.0`、`""`、`[]`、`{}`、`set()`。
- 非空容器、非零数字、非空字符串都是真。`if [0]:` 为真（列表非空）。

### 0.6 不会就问解释器

```python
help(list.append)     # 看某个方法怎么用
print(dir([]))        # 列表有哪些方法
print(len([1, 2, 3])) # 几乎所有容器都用 len()
```

---

## 第二章　Python 序列

**先记住一句话：** 序列是「排好队的一串东西」，可用下标、切片、`len()`、`in`。

| 写法 | 类型 | 可变 | 有序 | 可重复 | 典型用途 |
|------|------|------|------|--------|----------|
| `[1, 2]` | list | 能 | 有 | 能 | 购物车、成绩表 |
| `(1, 2)` | tuple | 不能 | 有 | 能 | 坐标、多返回值 |
| `{"a": 1}` | dict | 能 | 键有插入序 | 键不重复 | 通讯录、配置 |
| `{1, 2}` | set | 能 | 无序 | 不能 | 去重、成员判断 |

官方：[5. 数据结构](https://docs.python.org/zh-cn/3/tutorial/datastructures.html) ·
[序列类型](https://docs.python.org/zh-cn/3/library/stdtypes.html#sequence-types-list-tuple-range)

---

### 2.1 列表：最常用的可变序列

**先记住一句话：** 方括号、逗号隔开、随时能增删改的队伍。

#### 创建

```python
a = [1, 2, 3, 4, 5]              # 字面量，最常用
b = list((1, 2, 3, 4, 5))        # 任何可迭代对象都能变列表
c = list("abc")                  # ['a', 'b', 'c']
d = list(range(3))               # [0, 1, 2]
e = [x * 2 for x in a]           # [2, 4, 6, 8, 10]
f = [x for x in a if x % 2 == 1] # [1, 3, 5]
```

推导式阅读顺序：**先看 `for`，再看 `if`，最后看前面要算什么。** 它等价于「建空列表 → 循环 → 满足条件就 append」。

> **坑：** `list(5)` 报错，整数不可迭代。要五个 0 写 `[0] * 5`。

#### 增：append / extend / insert / `+` / `*`

```python
a = [1, 2, 3]
a.append(4)          # 末尾加「一个」元素
a.extend([5, 6])     # 末尾拆开加「一串」
a.insert(0, 0)       # 在下标 0 插入，后面整体后移
print(a)             # [0, 1, 2, 3, 4, 5, 6]
print([1, 2] + [3])  # [1, 2, 3]   + 和 * 得到新列表
print([0] * 4)       # [0, 0, 0, 0]
```

`append([3, 4])` 把整坨当成一个元素；`extend([3, 4])` 拆开追加。
`append` 只收 1 个参数，`a.append(1, 2)` 非法。

#### 删：pop / remove / del / clear

```python
a = [10, 20, 30, 20, 40]
last = a.pop()        # 删并返回最后：40
mid = a.pop(1)        # 删并返回下标 1
a.remove(20)          # 只删「第一个值等于 20」的
del a[0]              # 按位置删，无返回值
a.clear()             # 清空
```

| 你知道什么 | 用谁 | 返回值 |
|------------|------|--------|
| 下标，还想要被删的值 | `pop(i)` | 有 |
| 值，不知道下标 | `remove(值)` | 无 |
| 下标或切片，不要返回值 | `del a[i]` | 无 |
| 全部清空 | `clear()` | 无 |

> **坑：** `remove` 找不到 → `ValueError`；`pop` 空列表 → `IndexError`。
> `remove` 只删第一次。删光所有 20：`a = [x for x in a if x != 20]`。

#### 改、查、切片赋值

```python
a = ["甲", "乙", "丙"]
a[1] = "改"
a[0:2] = ["A", "B"]    # 用切片替换一段
print(a[0], a[-1], len(a), a.index("B"), a.count("B"))

a = [0, 1, 2, 3, 4, 5]
print(a[1:4], a[::2], a[::-1])   # 切片得到新列表
a[1:4] = [8, 9]                  # 两个元素替换原来三段
del a[::2]                       # 删偶数下标
```

> **坑：** `b = a` 不是复制。`b = a[:]` 才是浅拷贝（只复制最外层；内层列表仍共享）。

#### 排序与成员判断

```python
a = [3, 1, 2]
a.sort()                       # 原地升序，返回 None
b = sorted([3, 1, 2])          # 新列表，原列表不动
a.sort(reverse=True)           # 降序
print(sorted(["pear", "apple", "banana"], key=len))

a = [1, 2, 3, 4, 5]
if 5 in a:
    print("5 is in the list")
if 6 not in a:
    print("6 is not in the list")
```

> **坑：** `a = a.sort()` 会把 `a` 变成 `None`。数字和字符串混排会 `TypeError`。
> 列表的 `in` 是线性扫描。大量「在不在」请先转 `set`。
> 原地倒转：`a.reverse()`；新列表倒序：`a[::-1]`。

---

### 2.2 元组：改不了的序列

**先记住一句话：** 长得像列表，造出来后不能增删改格子。适合打包一组值。

```python
t = (1, 2, 3, 4, 5)
u = tuple([1, 2, 3, 4, 5])
v = 1, 2, 3              # 真正打包的是逗号，括号常可省
only = (7,)              # 单元素：逗号不能省
not_tuple = (7)          # 这只是整数 7
empty = ()

print(t[1], t[0:2])      # 20  (10, 20) —— 先改成 t = (10, 20, 30) 再体会
# t[1] = 99              # TypeError
```

元组能下标、切片、`len`、`in`、`count`、`index`，不能 `append` / `pop`。

```python
def min_max(nums):
    return min(nums), max(nums)

lo, hi = min_max([3, 1, 4])    # 函数多返回值 = 返回元组再拆包
x, y = 1, 2
x, y = y, x                    # 交换，本质也是打包再拆
```

> **坑：** 「不可变」指格子不能换人。格子里若是列表，那个列表照样能改：
> `t = (1, [2, 3]); t[1].append(4)` 得到 `(1, [2, 3, 4])`。

---

### 2.3 字典：用键找值

**先记住一句话：** 不按 0、1、2 排队，用键当名字找值。键必须可哈希（通常是不可变对象）。
官方：[dict](https://docs.python.org/zh-cn/3/library/stdtypes.html#mapping-types-dict)

```python
d = {"a": 1, "b": 2, "c": 3}
e = dict(a=1, b=2, c=3)
f = dict([("a", 1), ("b", 2)])
g = dict.fromkeys(["a", "b", "c"], 0)   # 一批键，同一个初值
empty = {}                               # 空字典，不是空集合

print(d["a"])           # 键不存在 → KeyError
print(d.get("a"))       # 键不存在 → None
print(d.get("z", 0))    # 自己指定默认值

d["a"] = 100            # 键在就是改
d["d"] = 4              # 键不在就是增
d.update({"d": 4, "e": 5})
removed = d.pop("b")    # 删并返回值；键不在会 KeyError
print(d.pop("no", None))
del d["c"]
```

键必须存在、不存在就是写错了 → 用 `d[key]` 让它报错。
键可能没有 → 用 `d.get(key, 默认)`。

```python
d = {"a": 1, "b": 2}
print(list(d.keys()), list(d.values()), list(d.items()))
for key, value in d.items():
    print(key, "->", value)
print("a" in d)           # True   in 判断的是键
print(1 in d)             # False
print(1 in d.values())    # True
```

Python 3.7+ 字典记住插入顺序。

> **坑 1：** 遍历时不要增删键，会 `RuntimeError`。先 `list(d)` 拷一份键。
> **坑 2：** 列表 / 字典 / 集合不能当键。元组可以，但里面也必须全是可哈希对象。
> **坑 3：** `fromkeys(["a", "b"], [])` 两个键共享**同一个**空列表。

---

### 2.4 集合：只关心「有没有」

**先记住一句话：** 自动去重，不管第几个。元素必须可哈希。

```python
s = {1, 2, 3, 4, 5}
t = set([1, 2, 2, 3, 3])   # {1, 2, 3}
empty = set()              # 空集合。{} 是空字典！
unique = list(set([3, 1, 2, 1, 3]))  # 去重，顺序可能打乱

s = {1, 2}
s.add(3)
s.update([3, 4, 5])
s.discard(9)               # 没有也不报错
s.remove(1)                # 没有 → KeyError
s.pop()                    # 任意拿出一个，别依赖顺序
```

```python
s1, s2 = {1, 2, 3}, {3, 4, 5}
print(s1 | s2)    # {1, 2, 3, 4, 5}  并集
print(s1 & s2)    # {3}              交集
print(s1 - s2)    # {1, 2}           差集：在 s1 不在 s2
print(s1 ^ s2)    # {1, 2, 4, 5}     对称差
print({1, 2} <= {1, 2, 3})           # 子集
```

方法名：`union` / `intersection` / `difference` / `symmetric_difference`。
符号两边都必须是 set；方法名可接受任意可迭代对象（`s1 | [3, 4]` 会 `TypeError`）。

> **坑：** `{[]}` 非法。要放「一组东西」当元素，先变成元组。

**四种容器怎么选：** 按下标/要重复 → 列表；打包后不该改、当键、多返回值 → 元组；用名字找值 → 字典；去重/交并差 → 集合。

---

## 第三章　选择与循环

**先记住一句话：** `if` 选路；`for` 遍历已知的一串；`while` 条件还成立就重复。
官方：[4. 流程控制](https://docs.python.org/zh-cn/3/tutorial/controlflow.html)

### 3.1 if / elif / else

```python
x = 10
if x > 0:
    print("x is positive")
elif x == 0:
    print("x is zero")
else:
    print("x is negative")
```

从上往下找**第一个为真**的条件，只执行那一块。`elif` 可多个；`else` 最多一个，也可没有。

```python
print(0 or 5)          # 5   and/or 会短路，并返回最后求值的对象
print(3 and 4)         # 4
print(0 < x < 20)      # True，链式比较合法
label = "奇数" if x % 2 else "偶数"   # 条件表达式
```

比较：`== != < > <= >=`。和 `None` 比用 `is` / `is not`。逻辑：`and` `or` `not`。

> **坑 1：** `=` 赋值，`==` 比较。
> **坑 2：** `0.1 + 0.2 == 0.3` 为 `False`，用 `abs(a - b) < 1e-9`。
> **坑 3：** 写 `if x == 1 or x == 2`，不要写 `if x == 1 or 2`（`2` 恒真）。

### 3.2 for：本质是「一个一个拿出来」

```python
for i in range(5):
    print(i)
else:
    print("Loop completed")    # 0 1 2 3 4 然后这句
```

`range` 和切片一样含头不含尾：`range(5)` → 0..4；`range(2, 6)` → 2..5；`range(0, 10, 2)` → 偶数；`range(5, 0, -1)` → 5..1。

```python
names = ["Ann", "Bob", "Cara"]
for name in names:                         # 优先直接遍历
    print(name)
for i, name in enumerate(names, start=1):  # 既要下标又要值
    print(i, name)
for name, score in zip(names, [90, 80]):   # 并排走，以最短为准
    print(name, score)                     # Cara 被丢掉
```

### 3.3 while：事先不知道转几圈时用

```python
i = 0
while i < 5:
    print(i)
    i += 1                 # 漏了这行就是死循环
else:
    print("Loop completed")

while True:                # 常见写法：永远转，用 break 停
    text = "ok"
    if text == "ok":
        break
```

### 3.4 break / continue / 循环 else

```python
for i in range(10):
    if i == 5:
        break              # 整段立刻结束
    if i % 2 == 0:
        continue           # 结束本圈
    print(i)               # 只打印 1 3
```

**循环 `else` 极易记反：** 循环**正常走完**才执行；被 `break` 打断则**不执行**。适合「找遍了没找到」：

```python
def find(nums, target):
    for n in nums:
        if n == target:
            print("找到了")
            break
    else:
        print("没找到")

find([1, 2, 3], 2)    # 找到了
find([1, 2, 3], 9)    # 没找到
```

嵌套时，`break` 只跳出**最内层**。想一次跳两层：设标志位，或把内层抽成函数再 `return`。

---

## 第四章　字符串与正则表达式

**先记住一句话：** 字符串是不可变字符序列。「修改」其实都在造新串。复杂模式交给 `re`。
官方：[str](https://docs.python.org/zh-cn/3/library/stdtypes.html#text-sequence-type-str) ·
[re](https://docs.python.org/zh-cn/3/library/re.html)

### 4.1 字符串也是序列

```python
s = "Hello"
print(s[0], s[-1], s[1:4], len(s), "ell" in s)
# s[0] = "h"     # TypeError
```

单引号、双引号一样，选能少转义的。三引号可跨行。前缀 `r` 让反斜杠不再转义：`r"C:\new"` 里 `\n` 不是换行。

### 4.2 格式化：优先 f-string

```python
name, age = "Alice", 30
message = f"Hello, {name}. You are {age} years old."
print(message)
print(f"{3.14159:.2f}")    # 3.14
print(f"{42:05d}")         # 00042
print(f"{name:>10}")       # 右对齐宽度 10
print(f"{name = }")        # 调试：name = 'Alice'
# 老写法： "{} {}".format(name, age)   /   "%s %d" % (name, age)
```

### 4.3 常用方法（都不改原来的 s）

```python
s = "Hello, World!"
print(s.split(", "))                       # ['Hello', 'World!']
print("a,b,,c".split(","))                 # ['a', 'b', '', 'c']
print("  hi  \n".strip())                  # 'hi'
print(", ".join(["Hello", "World!"]))      # Hello, World!
print(s.replace("World", "Python"))
print(s.find("World"), s.index("World"))   # 7 7；find 找不到 -1，index 找不到会炸
print(s.startswith("Hello"), s.endswith("!"))
print("hello".upper(), "HELLO".lower(), "hello world".title())
print("banana".count("a"))                 # 3
```

`split` 和 `join` 是一对。**是分隔符去 join 列表**，不是列表去 join 分隔符。

> **坑 1：** `"".join([1, 2])` 报错，元素必须都是 str。
> **坑 2：** `if s.find("x")` 是错的——找到下标 0 时 `0` 为假。写 `if "x" in s`。
> **坑 3：** `replace` 默认换光；只换前 n 个：`s.replace("a", "b", n)`。

### 4.4 正则：用模式描述「长什么样」

普通 `find`/`replace` 只能死文字。正则描述一类文字。模式请写 `r"..."`，免得 `\b` 被 Python 先当成退格。

| 符号 | 意思 | 符号 | 意思 |
|------|------|------|------|
| `.` | 任意 1 字符（默认不含换行） | `^` `$` | 开头 / 结尾 |
| `*` `+` `?` | 前物 0+ / 1+ / 0 或 1 次 | `{m,n}` | m 到 n 次 |
| `[abc]` `[^0-9]` | 集合 / 取反 | `\|` `()` | 或者 / 分组 |
| `\d` `\w` `\s` | 数字 / 单词字符 / 空白 | `\b` | 单词边界 |

```python
import re
text = "The rain in Spain"

print(re.findall(r"\bS\w+", text))     # ['Spain']  所有匹配
m = re.search(r"\bS\w+", text)         # 任意位置第一个
if m:
    print(m.group(), m.span())         # Spain  (12, 17)
m = re.match(r"\bT\w+", text)          # 只从开头匹配
if m:
    print(m.group())                   # The
print(re.sub(r"\bS\w+", "Country", text))
print(re.split(r"\s+", text))          # ['The', 'rain', 'in', 'Spain']
```

`search` / `match` 找不到返回 `None`。对 `None` 调 `.group()` 会崩，**先 `if m:`**。
`match` 只看开头，所以 `re.match(r"Spain", text)` 是 `None`。

作业向例子——抽电话：

```python
import re
text = "Call me at 123-456-7890 or 987.654.3210"
pattern = r"\b\d{3}[-.]\d{3}[-.]\d{4}\b"
print(re.findall(pattern, text))
# ['123-456-7890', '987.654.3210']
# \d{3} 三位数字；[-.] 短横或点（[] 里的 . 是普通点）；\b 边界
```

分组可单独取某一截：`m.group(0)` 整段，`m.group(1)` 第一组，`m.groups()` 全部组。
同一模式多次用：`phone_re = re.compile(pattern)`，再 `phone_re.findall(text)`。

> **坑：** `findall` 若模式里有一组 `()`，返回的是**组**不是整段。既分组又拿整段用 `(?:...)`。
> `*` `+` 默认贪婪。`r"<.*>"` 会吞掉 `<a>b</a>` 整段；非贪婪写成 `.*?`。

---

## 第五章　函数的设计和使用

**先记住一句话：** 起了名字的可复用代码。值传进去，`return` 送出来。没写 `return` 就返回 `None`。
官方：[定义函数](https://docs.python.org/zh-cn/3/tutorial/controlflow.html#defining-functions)

### 5.1 最小函数与四种参数

```python
def greet(name, greeting="Hello"):
    """打印一句问候。greeting 有默认值。"""
    print(f"{greeting}, {name}!")

greet("Alice")                   # Hello, Alice!
greet("Bob", greeting="Hi")      # Hi, Bob!
greet(greeting="Hi", name="Bob") # 关键字参数可对调顺序
```

定义时顺序：**位置参数 → 默认值参数 → `*args` → 仅关键字 → `**kwargs`**。
有默认值的右边不能再出现没默认值的：`def f(a=1, b):` 非法。

```python
def sum_all(*args):              # args 是元组，装着多出来的位置参数
    return sum(args)
print(sum_all(1, 2, 3, 4, 5))    # 15

def print_config(**kwargs):      # kwargs 是字典，装着多出来的关键字参数
    for k, v in kwargs.items():
        print(k, "=", v)
print_config(host="localhost", port=8080)
```

调用时解包：序列用 `*`，字典用 `**`。

```python
def print_args(a, b, c):
    print(a, b, c)

print_args(*(1, 2, 3))
print_args(**{"a": 1, "b": 2, "c": 3})
```

`return` 一执行函数立刻结束。一次送多个值 = 返回元组，调用处拆包：`q, r = (17 // 5, 17 % 5)`。

### 5.2 作用域 LEGB 与 global

找名字四层：**局部 Local → 嵌套 Enclosing → 全局 Global → 内置 Built-in**。

```python
x = 10

def modify_x():
    global x                     # 声明：下面的 x 指全局那个
    x += 5

modify_x()
print(x)                         # 15
```

函数里对某名字一赋值，整个函数里它都算局部。于是：

```python
x = 10
def boom():
    print(x)     # UnboundLocalError：下面有赋值，这里的 x 已被当成局部
    x = x + 1
```

改外层函数的变量用 `nonlocal`。能不改全局就别改：当参数传入，`return` 传出。

### 5.3 lambda 与可变默认参数坑

```python
add_one = lambda x: x + 1        # 只能写一个表达式，等价 def add_one(x): return x + 1
print(add_one(5))                # 6
print(sorted([(1, "b"), (2, "a")], key=lambda p: p[1]))
```

默认值只在**定义函数时求值一次**：

```python
def add_item(item, bucket=[]):   # 错误示范：所有调用共享同一个 []
    bucket.append(item)
    return bucket
print(add_item(1))               # [1]
print(add_item(2))               # [1, 2]  不是 [2]
```

正确：默认用 `None`，函数里再造新列表。

```python
def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

---

## 第六章　面向对象程序设计

**先记住一句话：** 类是图纸，对象是实例。`self.属性` 记住自己的数据，方法描述自己会做的事。
官方：[9. 类](https://docs.python.org/zh-cn/3/tutorial/classes.html)

### 6.1 类、对象、`__init__`、`self`

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound")


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)     # 先让父类把 name 安顿好
        self.breed = breed

    def speak(self):
        print(f"{self.name} barks")


dog = Dog("Buddy", "Golden Retriever")
dog.speak()                        # Buddy barks
print(dog.name, dog.breed)
```

- `class Dog(Animal)`：狗是一种动物。
- `__init__` 不是你亲手调的。写 `Dog(...)` 时 Python 造空对象，再把它当 `self` 传进去。
- `self` 是当前对象。实例方法第一个参数必须是它（请永远叫 `self`）。
- 子类 `speak` 覆盖父类 `speak`，这就是最朴素的多态。

> **坑：** `dog.speak()` 才执行。`Dog.speak()` 缺 self；`dog.speak` 不带括号只是拿到函数对象。

### 6.2 访问约定与 @property

Python 没有真正的 private，靠命名提醒你：

| 写法 | 含义 | 外面直接碰 |
|------|------|------------|
| `self.public` | 公开 | 能 |
| `self._protected` | 内部实现，君子协定 | 能，但不该 |
| `self.__private` | 名称改写，防子类踩名 | 直接写会 AttributeError |

```python
class MyClass:
    def __init__(self):
        self.public_var = 10
        self._protected_var = 20
        self.__private_var = 30

    @property
    def private_var(self):
        return self.__private_var

obj = MyClass()
print(obj.public_var, obj._protected_var, obj.private_var)
# print(obj.__private_var)          # AttributeError
print(obj._MyClass__private_var)    # 真名被改写成这个，一般别用
```

`@property` 让外面仍写成 `obj.private_var`，里面却可以加计算、加校验。

### 6.3 实例方法 / 类方法 / 静态方法

```python
class MyClass:
    class_var = "I am a class variable"    # 属于类，实例默认共享

    def instance_method(self):
        print(f"Instance method: {self.class_var}")

    @classmethod
    def class_method(cls):
        print(f"Class method: {cls.class_var}")

    @staticmethod
    def static_method():
        print("Static method")

obj = MyClass()
obj.instance_method()      # 需要对象，才能拿到 self
MyClass.class_method()     # cls 指向类；常用来做备用构造器
MyClass.static_method()    # 普通函数，碰巧住在类下面
```

用到这个对象自己的数据 → 实例方法；用到类本身 → `@classmethod`；和状态无关只是好找 → `@staticmethod`。

> **坑：** `self.class_var = 1` 不会改类变量，只在这个实例上盖一个同名属性。改类变量写 `MyClass.class_var = ...`。

### 6.4 继承、super、多态

```python
class Animal:
    def speak(self):
        print("Some generic sound")

class Dog(Animal):
    def speak(self):
        super().speak()
        print("Woof!")

class Cat(Animal):
    def speak(self):
        super().speak()
        print("Meow!")

def animal_sound(animal):
    animal.speak()               # 调用方不关心你是狗还是猫

animal_sound(Dog())              # Some generic sound / Woof!
animal_sound(Cat())              # Some generic sound / Meow!
```

Python 的多态很宽松（鸭子类型）：只要对象有 `speak`，就能传进去。
`isinstance(obj, Animal)` 含子女；`type(obj) is Animal` 不含。一般用 `isinstance`。

常见双下方法：`__repr__` 给开发者看，`__eq__` 定义 `==`，`__len__` 让 `len(obj)` 能用。只实现一个字符串方法时优先 `__repr__`。

---

## 第七章　文件操作

**先记住一句话：** 用 `with open(...) as f`。离开缩进块（包括报错）都会自动关文件。
官方：[读写文件](https://docs.python.org/zh-cn/3/tutorial/inputoutput.html#reading-and-writing-files)

| 模式 | 含义 | 文件不存在 | 文件已存在 |
|------|------|------------|------------|
| `'r'` | 只读（默认） | 报错 | 从头读 |
| `'w'` | 只写 | 新建 | **清空后重写** |
| `'a'` | 追加 | 新建 | 末尾继续写 |
| `'x'` | 独占新建 | 新建 | FileExistsError |
| `'r+'` | 读写 | 报错 | 不清空，指针在开头 |
| `'w+'` / `'a+'` | 读写 | 新建 | 清空 / 写在末尾 |

再加 `b` 变二进制（读到 `bytes`，适合图片）；文本模式请写 `encoding="utf-8"`，否则 Windows 容易中文乱码。

```python
with open("example.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!")           # write 不自动加换行

with open("example.txt", "r", encoding="utf-8") as f:
    print(f.read())                    # Hello, World!

with open("example.txt", "w", encoding="utf-8") as f:
    f.writelines(["Line 1\n", "Line 2\n", "Line 3\n"])  # 也不会自动补 \n

with open("example.txt", "r", encoding="utf-8") as f:
    print(f.readlines())               # ['Line 1\n', 'Line 2\n', 'Line 3\n']

with open("example.txt", "r", encoding="utf-8") as f:
    for line in f:                     # 大文件首选：一行行读
        print(line.rstrip("\n"))
```

指针：`read()` 之后已经在末尾。`tell()` 看位置，`seek(0)` 回到开头。

```python
with open("example.txt", "r+", encoding="utf-8") as f:
    print(f.read(5))
    f.seek(0)
    print(f.read(5))
```

> **坑：** `'w'` 会清空。只想读再改用 `'r+'`。Windows 路径写成 `r"C:\new\a.txt"` 或正斜杠。
> 更稳：`from pathlib import Path`，然后 `p.write_text("你好\n", encoding="utf-8")`。

---

## 第八章　异常处理结构与程序调试

**先记住一句话：** 异常是可被接住的错误信号。`try` 放可能失败的事；`except` 对策；`else` 仅成功时走；`finally` 无论成败都走。
官方：[错误和异常](https://docs.python.org/zh-cn/3/tutorial/errors.html)

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")

try:
    result = 10 / 2
except ZeroDivisionError as e:
    print(f"Error: {e}")
else:
    print(f"Result is {result}")     # 没异常才走；成功路径里再炸，不会被上面 except 误伤

try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
finally:
    print("This will always execute")  # 成功、被接住、函数 return，都会走
```

顺序固定：**try → except（可多个）→ else → finally**。接异常尽量具体，不要裸 `except:` 把错误吞掉。

```python
def set_age(age):
    if age < 0:
        raise ValueError("年龄不能为负")
    return age
```

| 异常 | 典型触发 |
|------|----------|
| `ZeroDivisionError` | `1/0` |
| `ValueError` | `int("abc")` |
| `TypeError` | `"a" + 1` |
| `IndexError` / `KeyError` | 下标越界 / 键不在 |
| `AttributeError` / `NameError` | 没这属性 / 没这名字 |
| `FileNotFoundError` | 打开不存在的文件 |

调试：先读 traceback **最下面那一行**；`print` 关键变量；`assert 条件, "说明"`；不确定就 `print(type(x), repr(x))`。

---

## 第九章　GUI 编程（tkinter）

**先记住一句话：** 先造根窗口，再往上放控件，最后 `mainloop()` 进入事件循环等用户点、敲、关。
官方：[tkinter](https://docs.python.org/zh-cn/3/library/tkinter.html)

```python
import tkinter as tk

def on_button_click():
    print("Button was clicked!")

root = tk.Tk()
root.title("Tkinter Example")
root.geometry("320x160")

tk.Label(root, text="Hello, World!").pack()
tk.Button(root, text="Click Me", command=on_button_click).pack()
tk.Entry(root).pack()

root.mainloop()                    # 没有这行，窗口闪一下就结束
```

永远三步：`Tk()` → 造控件（第一个参数是父亲）→ 布局后 `mainloop()`。
`command=` 传**函数对象**，不要加括号——加了会在创建按钮时立刻调用。

三种布局：`pack` 上下左右挤；`grid` 行列（表单首选）；`place` 写死坐标。
**同一父亲下不要混用 pack 和 grid**，窗口会卡住。

```python
import tkinter as tk

root = tk.Tk()
tk.Label(root, text="用户名").grid(row=0, column=0, padx=5, pady=5)
user = tk.Entry(root)
user.grid(row=0, column=1)
tk.Label(root, text="密码").grid(row=1, column=0)
pwd = tk.Entry(root, show="*")
pwd.grid(row=1, column=1)

def login():
    print("尝试登录：", user.get())

tk.Button(root, text="登录", command=login).grid(row=2, column=0, columnspan=2)
root.mainloop()
```

`Entry.get()` 取输入。`mainloop()` 不是死卡住，是在问有没有鼠标键盘。
回调里不要 `time.sleep` 或长时间计算，窗口会假死。

---

## 第十章　网络程序设计（socket）

**先记住一句话：** TCP 像打电话。服务器装机等铃（`bind` + `listen` + `accept`）；客户端拨号（`connect`）；双方 `send` / `recv`，`close` 挂断。
官方：[socket](https://docs.python.org/zh-cn/3/library/socket.html)

- `AF_INET`：IPv4（`localhost` / `127.0.0.1` 是本机回环，适合自测）
- `SOCK_STREAM`：TCP，可靠有连接，作业几乎都用这个
- 网上走的是 **bytes**：字符串先 `.encode("utf-8")`，收到再 `.decode("utf-8")`

```python
# ===== 服务器：先启动这个 =====
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 8080))
server_socket.listen(5)            # 5 是等待队列长度，不是只能服务 5 人
print("Server is listening on port 8080")

while True:
    client_socket, addr = server_socket.accept()   # 阻塞等待下一个客户
    print(f"Connection from {addr} has been established")
    client_socket.send(b"Welcome to the server!")
    client_socket.close()
```

```python
# ===== 客户端：服务器起来之后再跑 =====
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8080))
message = client_socket.recv(1024)     # 1024 是上限，不保证一次读满
print(message.decode())                # Welcome to the server!
client_socket.close()
```

| 步骤 | 服务器 | 客户端 |
|------|--------|--------|
| 造 socket | 要 | 要 |
| bind / listen | 要 | 不要 |
| 等对方 | `accept` | `connect` |
| 收发 / 关闭 | `recv` `send` `close` | 同 |

> **坑：** 先开服务器再开客户端。没人听 → `ConnectionRefusedError`；端口占用 → `Address already in use`。
> `recv(n)` 可能只到一部分。作业「发一句收一句」通常够用；正经协议要定结束符或长度头，循环收。

---

## 第十三章　多线程与多进程编程

**先记住一句话：** 线程共享内存、切换便宜，但 CPython 有 GIL，纯计算往往快不起来；进程各有内存，能吃满多核，数据必须显式传递。
官方：[threading](https://docs.python.org/zh-cn/3/library/threading.html) ·
[multiprocessing](https://docs.python.org/zh-cn/3/library/multiprocessing.html)

| 场景 | 更合适 |
|------|--------|
| 等网络 / 磁盘 / 用户（I/O） | 线程 |
| 纯数字计算、要吃满 CPU | 进程 |
| 共享大字典、改同一列表 | 线程（加锁） |
| 怕互相踩内存、要隔离崩溃 | 进程 |

### 13.1 多线程

```python
import threading

def print_numbers():
    for i in range(5):
        print("num", i)

def print_letters():
    for letter in "abcde":
        print("let", letter)

t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)
t1.start()                 # 真正开始跑
t2.start()
t1.join()                  # 等到这条结束
t2.join()
print("both done")         # 数字和字母会交错，顺序每次可能不同
```

带参：`Thread(target=worker, args=(3,), kwargs={"prefix": "A"})`。`args` 必须是元组，一个参数也要写成 `(3,)`。

两线程改同一变量必须加锁，否则 `+=` 的「读-加-写」会丢更新：

```python
import threading
counter, lock = 0, threading.Lock()

def bump():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

ts = [threading.Thread(target=bump) for _ in range(4)]
for t in ts:
    t.start()
for t in ts:
    t.join()
print(counter)             # 应为 400000；去掉 lock 多半会少
```

> **坑：** tkinter 控件只能在主线程改。工作线程算完后，用 `root.after(0, 更新函数)` 把改 UI 的动作丢回去。

### 13.2 多进程

进程内存不共享，用 `Queue` 传话。Windows / macOS 下创建进程的代码必须放进 `if __name__ == "__main__":`，否则子进程重新导入模块会递归爆炸。

```python
from multiprocessing import Process, Queue

def worker(q):
    q.put("Hello from the worker process")

if __name__ == "__main__":
    q = Queue()
    p = Process(target=worker, args=(q,))
    p.start()
    print(q.get())         # Hello from the worker process
    p.join()
```

`join()` 两边含义一样：等到对方结束。不 join，主程序可能先退出，子任务被干掉。

| | 线程 | 进程 |
|--|------|------|
| 类 | `threading.Thread` | `multiprocessing.Process` |
| 启动 / 等待 | `start` / `join` | 同 |
| 传数据 | 共享变量 + 锁 | `Queue` / `Pipe` |
| 入口保护 | 一般不用 | 必须 `__main__` |

同类任务很多时可用池：`ThreadPoolExecutor`（I/O）或 `ProcessPoolExecutor`（CPU，同样要放 `__main__`）。

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(lambda x: x * x, range(5))))   # [0, 1, 4, 9, 16]
```

---

## 附录 A　一张纸对照

```
[]  list     可变有序可重复          ()  tuple   不可变；单元素必须 (1,)
{}  dict     键值对；{} 是空字典     set()      去重；空集合不能写成 {}
a[start:stop:step]   含 start 不含 stop
a.sort() 原地返回 None     sorted(a) 新列表
break 离开整段    continue 结束本圈    for-else：没被 break 才走 else
字符串不可变；", ".join(列表)  分隔符在左边
re.search 任意位置第一个   re.match 只从开头   re.findall 全部
模式写 r"..."     默认参数别用 []     *args 元组  **kwargs 字典
self 是当前实例    _ 别碰    __ 名称改写
@classmethod 收 cls    @staticmethod 谁都不收
with open(path, mode, encoding="utf-8")     'w' 清空  'a' 追加  'r+' 读写不清空
try / except / else / finally     else 仅成功；finally 一定走
服务器 bind+listen+accept     客户端 connect     收发的是 bytes
线程共享内存要加锁     进程用 Queue     进程入口护在 __main__
```

## 附录 B　跑不通时按这个查

1. 缩进是否 4 空格，有没有混 Tab；有没有用了中文标点 `：` `（`。
2. 字符串引号是否闭合；正则有没有写 `r`。
3. 有没有把 `sort` / `append` 的 `None` 赋回去。
4. 文件模式、编码、路径是否和设想一致。
5. 是否先开服务器再开客户端；多进程是否在 `__main__` 里。
6. 是否对可能为 `None` 的 match 直接 `.group()`。

## 附录 C　官方文档速查

| 主题 | 链接 |
|------|------|
| 教程总目录 | https://docs.python.org/zh-cn/3/tutorial/index.html |
| 数据结构 | https://docs.python.org/zh-cn/3/tutorial/datastructures.html |
| 流程控制与函数 | https://docs.python.org/zh-cn/3/tutorial/controlflow.html |
| 类 | https://docs.python.org/zh-cn/3/tutorial/classes.html |
| 文件 | https://docs.python.org/zh-cn/3/tutorial/inputoutput.html |
| 异常 | https://docs.python.org/zh-cn/3/tutorial/errors.html |
| 内置类型 / 内置函数 | https://docs.python.org/zh-cn/3/library/stdtypes.html · https://docs.python.org/zh-cn/3/library/functions.html |
| re / pathlib / tkinter | https://docs.python.org/zh-cn/3/library/re.html · pathlib.html · tkinter.html |
| socket / threading / multiprocessing | https://docs.python.org/zh-cn/3/library/socket.html · threading.html · multiprocessing.html |

**复习法：** 合上笔记，先默写附录 A；再挑一个「坑」用解释器亲手踩一遍。能讲清「为什么会这样」，比背方法列表有用得多。
