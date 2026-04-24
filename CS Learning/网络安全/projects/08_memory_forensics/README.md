# 项目 08：Volatility 内存取证实战

> 对应章节：第 10 章《恶意代码分析与数字取证》

## 目标

1. 掌握内存取证的基本流程与常用 Volatility 3 插件。
2. 对样本内存镜像完成：进程分析、网络连接、注入检测、凭证提取、历史命令还原。
3. 产出一份结构化的 DFIR 报告。

## 环境

```bash
python -m venv .venv && source .venv/bin/activate
pip install volatility3 yara-python
```

## 样本来源

公开的练习用内存镜像（合法获取）：

- CFReDS（NIST）：<https://www.cfreds.nist.gov/>
- Volatility Training Images（作者原始仓库的 wiki / README）
- SANS Holiday Hack / DFIR Challenges 过往题
- MemLabs：<https://github.com/stuxnet999/MemLabs>（推荐，共 6 个 Lab，由易到难）

本项目以 **MemLabs Lab1–Lab3** 为主。

## 基础命令

```bash
vol -f lab1.raw windows.info
vol -f lab1.raw windows.pslist
vol -f lab1.raw windows.pstree
vol -f lab1.raw windows.cmdline
vol -f lab1.raw windows.netscan
vol -f lab1.raw windows.netstat
vol -f lab1.raw windows.malfind
vol -f lab1.raw windows.filescan | grep -i pass
vol -f lab1.raw windows.dumpfiles --virtaddr <addr>
vol -f lab1.raw windows.registry.printkey --key 'Software\Microsoft\Windows\CurrentVersion\Run'
vol -f lab1.raw windows.registry.hivelist
vol -f lab1.raw windows.hashdump
vol -f lab1.raw windows.lsadump
vol -f lab1.raw windows.clipboard
vol -f lab1.raw windows.screenshots
```

## 调查清单（每个样本都做一次）

1. **系统信息**：OS 版本 / 服务包 / KDBG。
2. **进程树**：找不寻常的父子关系（`mshta` 由 `winword` 启动？）。
3. **命令行参数**：`cmdline` 出现 `powershell -enc`、`rundll32 ... ,EntryPoint`？
4. **网络连接**：`netscan` 里可疑外联（非常规端口、奇怪域名）。
5. **注入**：`malfind` 输出的 PE/MZ 片段 + RWX 内存。
6. **持久化**：`Run / RunOnce`、`Services`、`Scheduled Tasks`（通过 `registry.printkey` 或 `filescan`）。
7. **凭证**：`hashdump` / `lsadump` / `cachedump`。
8. **文件句柄**：`handles --object File` 找可疑路径。
9. **网页历史**：`iehistory`（如适用）。
10. **证据保存**：用 `dumpfiles` / `memmap` 把可疑内容转储到磁盘做二次分析。

## 使用 YARA 扫内存

```bash
pip install yara-python
vol -f lab.raw yarascan.YaraScan --yara-rules '/Mimikatz/'
vol -f lab.raw yarascan.YaraScan --yara-file my-rules.yar
```

## 自动化：`memprobe.py`

写一个 Python 工具，顺序跑上面的插件并把结果合成一份 Markdown 表格。

```python
import subprocess, json

PLUGINS = [
    "windows.info",
    "windows.pslist",
    "windows.pstree",
    "windows.cmdline",
    "windows.netscan",
    "windows.malfind",
]

def run(img, plugin):
    cmd = ["vol", "-r", "json", "-f", img, plugin]
    out = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(out.stdout)
    except Exception:
        return out.stdout

if __name__ == "__main__":
    import sys
    img = sys.argv[1]
    for p in PLUGINS:
        data = run(img, p)
        print(f"## {p}\n")
        print(data if isinstance(data, str) else json.dumps(data, indent=2)[:2000])
```

## 交付物

- `writeup.md`：每个 Lab 的分析过程 + flag（如有）+ 攻击链还原
- `memprobe.py` + `output/` 目录（插件原始输出）
- `timeline.md`：按时间顺序还原攻击者行为

## 加分项

- 对 Linux 镜像使用 `linux.*` 插件做一次分析。
- 把结果导入 **Plaso / log2timeline** 做跨源时间线。
- 用 BloodHound 数据（若存在）还原域内攻击路径。
- 写一篇中文博客文章，在 `writeup.md` 基础上图文排版，发布到自己的博客。
