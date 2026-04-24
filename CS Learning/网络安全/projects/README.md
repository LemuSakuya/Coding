# 网络安全实战项目总览

> 10 个可在本地复现、从入门到进阶的实战项目。
> 覆盖：基线加固 → 网络侦察 → Web 渗透 → 密码破解 → 流量分析 → 漏洞利用 → 蓝队 SIEM → 内存取证 → 二进制逆向 → 综合 CTF。

---

## 项目列表

| 编号 | 项目 | 对应章节 | 难度 |
|------|------|----------|------|
| [01](./01_linux_hardening/) | Linux 基线加固实验 | Ch03 | ⭐ |
| [02](./02_network_scanning/) | Nmap + Masscan 网络侦察 | Ch02、Ch06 | ⭐⭐ |
| [03](./03_web_owasp_lab/) | OWASP Top 10 Web 打靶 | Ch05 | ⭐⭐⭐ |
| [04](./04_password_cracking/) | John & Hashcat 密码破解 | Ch04 | ⭐⭐ |
| [05](./05_wireshark_traffic/) | Wireshark 流量分析 | Ch02、Ch10 | ⭐⭐ |
| [06](./06_metasploit_lab/) | Metasploit 漏洞利用靶场 | Ch08 | ⭐⭐⭐ |
| [07](./07_siem_elk/) | ELK SIEM 蓝队实验 | Ch11 | ⭐⭐⭐ |
| [08](./08_memory_forensics/) | Volatility 内存取证 | Ch10 | ⭐⭐⭐ |
| [09](./09_reverse_engineering/) | CrackMe 逆向 + Pwn 入门 | Ch09 | ⭐⭐⭐⭐ |
| [10](./10_ctf_capstone/) | 综合 CTF 挑战（毕业项目） | 全部 | ⭐⭐⭐⭐ |

---

## 环境准备

### 宿主机

- macOS / Windows / Linux 任选（Apple Silicon 推荐 UTM + Rosetta）
- Docker Desktop / Docker Engine
- VirtualBox / VMware / UTM
- Kali Linux 2024+ ISO

### Python 依赖

```bash
cd "CS Learning/网络安全/projects"
python -m venv .venv
source .venv/bin/activate            # macOS / Linux
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 靶机资源（合法 / 授权）

| 靶机 | 地址 |
|------|------|
| Metasploitable 2 | <https://sourceforge.net/projects/metasploitable/> |
| Metasploitable 3 | <https://github.com/rapid7/metasploitable3> |
| DVWA | <https://github.com/digininja/DVWA> |
| OWASP Juice Shop | <https://github.com/juice-shop/juice-shop> |
| HackTheBox / TryHackMe / VulnHub | 线上靶场 |
| PicoCTF | CTF 训练 |

---

## 通用安全约定

1. **所有实验仅在自己搭建或授权的环境中执行**。
2. 用单独的虚拟机网络，避免污染真机 / 公网。
3. 保留快照，每次实验后还原干净基线。
4. 写下笔记：`目标 → 命令 → 观察 → 结论 → 防御建议`。
5. **切勿** 在生产系统 / 真实陌生目标上做主动扫描、爆破、利用。

---

## 推荐节奏

- 一周一个项目，周末做 CTF。
- 每完成 1 个项目，写 1 篇复盘（放到 `assets/writeups/xx.md`）。
- 项目 10 是毕业项目：全流程独立完成，不查答案。
