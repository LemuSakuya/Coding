# 项目 04：口令爆破与哈希破解（John + Hashcat）

> 对应章节：第 4 章《密码学基础与应用》、第 7 章《漏洞评估》

## 目标

1. 理解常见哈希格式（MD5 / SHA-256 / NTLM / bcrypt / PBKDF2 / Kerberos AS-REP / NetNTLMv2）。
2. 熟练使用 `John the Ripper` 与 `Hashcat` 的字典、掩码、规则攻击。
3. 掌握 **密码喷洒** 与 **字典生成**（CeWL、hashcat-rules）技巧。
4. 对比 GPU vs CPU 的破解速度差异。

## 环境

- Kali Linux（内置 John、Hashcat、rockyou.txt）
- 有 GPU 更佳（NVIDIA / Apple Silicon 的 Metal）

## 素材准备

```bash
# 1. 生成带标签的测试哈希
python gen_hashes.py
# 产出 hashes.txt：每行 <label>:<hash>

# 2. 下载字典
cp /usr/share/wordlists/rockyou.txt.gz .
gunzip rockyou.txt.gz
```

### `gen_hashes.py` 框架

```python
import hashlib, bcrypt, random, string

passwords = ['password', 'admin123', 'P@ssw0rd2024', 'tr0ub4dor&3']

with open('hashes.txt', 'w') as f:
    for p in passwords:
        f.write(f"MD5:{hashlib.md5(p.encode()).hexdigest()}\n")
        f.write(f"SHA1:{hashlib.sha1(p.encode()).hexdigest()}\n")
        f.write(f"SHA256:{hashlib.sha256(p.encode()).hexdigest()}\n")
        # bcrypt
        f.write(f"BCRYPT:{bcrypt.hashpw(p.encode(), bcrypt.gensalt(rounds=10)).decode()}\n")
```

## 实验任务

### 1. John 基础

```bash
# 单模式 (基于用户名变形)
john hashes.txt

# 字典
john --wordlist=rockyou.txt --format=raw-md5 hashes.txt

# 规则增强
john --wordlist=rockyou.txt --rules=Jumbo --format=raw-sha256 hashes.txt

# 查看已破解
john --show --format=raw-md5 hashes.txt
```

### 2. Hashcat 模式对照

| 模式 | Hashcat `-m` | 示例 |
|------|-------------|------|
| MD5 | 0 | `hashcat -m 0 md5.txt rockyou.txt` |
| SHA-1 | 100 | |
| SHA-256 | 1400 | |
| NTLM | 1000 | |
| bcrypt | 3200 | |
| NetNTLMv2 | 5600 | |
| Kerberos AS-REP | 18200 | |
| Kerberos TGS (Kerberoast) | 13100 | |

```bash
# 掩码攻击：8 位大小写 + 数字
hashcat -m 1000 ntlm.txt -a 3 ?u?l?l?l?l?l?d?d

# 组合攻击：字典 + 字典
hashcat -m 0 md5.txt -a 1 left.txt right.txt

# 规则攻击
hashcat -m 0 md5.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

### 3. 字典增强

```bash
# CeWL：从目标网站爬关键词
cewl https://example.com -w custom.txt -d 2 -m 5

# 合并自定义 + rockyou
cat custom.txt rockyou.txt | awk '!a[$0]++' > merged.txt

# hashcat utils：前缀 / 后缀
cat merged.txt | while read p; do echo "${p}2024!"; done > merged-2024.txt
```

### 4. 真实场景

- **NetNTLMv2 捕获 + 破解**：在 Responder / Inveigh 环境下获取 hash，Hashcat `-m 5600`。
- **Kerberoasting**：`impacket-GetUserSPNs -request -dc-ip <DC> <domain>/<user>`，离线 `-m 13100`。
- **NTDS.dit 转储**：`secretsdump.py` → `hashcat -m 1000 ntlm.txt`。

### 5. 性能对比

- 记录不同模式下 H/s 或 kH/s。
- 解释为什么 `bcrypt` 远慢于 `md5`（内存硬化 + cost factor）。

## 交付物

- `gen_hashes.py` + `hashes.txt`
- `writeup.md`：每类哈希的破解命令、耗时、结论。
- `benchmark.md`：3 种哈希在你的机器上的速度对比。

## 加分项

- 用 Python + `passlib` 写一个 **口令强度评估器**：输入密码 → 给出 bits 熵、是否在 HIBP、是否在 top 1000 common。
- 实现一个 **密码喷洒工具**：对 SMB / OWA / O365 IMAP，低速率、多账号尝试，避免锁定。
- 解读一篇学术论文：PBKDF2 vs Argon2 的抗 GPU/ASIC 能力。
