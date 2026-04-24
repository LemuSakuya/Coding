# 第 3 章 操作系统安全（Linux & Windows）

## 3.1 学习目标

1. 掌握 Linux / Windows 权限模型。
2. 熟练进行基线加固、日志审计、权限最小化。
3. 理解典型提权路径（SUID、Kernel、DLL 劫持、Token 窃取）。
4. 会做主机层入侵排查。

---

## 3.2 Linux 安全基础

### 3.2.1 权限体系

```
  -rwxr-xr--  1  alice  dev  4096  Apr 24 12:00  app
  │└┬┘└┬┘└┬┘     └─┬─┘ └┬┘
  │ │  │  │        │    └── 所属组 dev
  │ │  │  │        └── 所有者 alice
  │ │  │  └── other 权限 r--
  │ │  └── group 权限 r-x
  │ └── owner 权限 rwx
  └── 文件类型：- 普通、d 目录、l 链接、b/c 设备
```

### 3.2.2 特殊位

| 位 | 数字 | 含义 |
|----|------|------|
| SUID | 4000 | 以文件所有者身份执行（`s` 替换 `x`） |
| SGID | 2000 | 以所属组身份执行 |
| Sticky | 1000 | 仅所有者可删除（`/tmp`） |

```bash
find / -perm -4000 -type f 2>/dev/null   # 查找所有 SUID 程序 → 提权关注点
```

### 3.2.3 Capabilities

比 root 细粒度，如 `CAP_NET_ADMIN` / `CAP_SYS_ADMIN`。

```bash
getcap -r / 2>/dev/null
setcap cap_net_raw+ep ./my_tool
```

### 3.2.4 PAM & Login

- `/etc/pam.d/` 控制密码策略、登录限制
- `/etc/security/limits.conf` 资源限制
- `faillock` 防爆破

---

## 3.3 Linux 加固清单（Hardening Checklist）

### 账户

- [ ] 禁用 root SSH 登录：`PermitRootLogin no`
- [ ] 禁用空口令 / 不用账号：`passwd -l username`
- [ ] 强制密码复杂度（`pam_pwquality`）
- [ ] 口令过期策略（`chage`）

### 网络

- [ ] 关闭 IPv6（若不用）
- [ ] `iptables` / `nftables` 入出站策略默认 DROP
- [ ] 禁用 `source routing`、`icmp redirect`
- [ ] 启用 SYN Cookie：`net.ipv4.tcp_syncookies=1`

### 文件系统

- [ ] `/tmp` `/var/tmp` 独立挂载 + `noexec,nosuid,nodev`
- [ ] 启用 `auditd`、记录关键文件（`/etc/passwd` `/etc/shadow`）

### 服务

- [ ] 最小化安装：移除 `telnet` `rsh` `rlogin` `ftp`
- [ ] 关闭未使用端口：`ss -tunlp`
- [ ] 启用 `fail2ban`

### 内核

- [ ] 启用 SELinux / AppArmor
- [ ] `kernel.kptr_restrict=2`、`kernel.dmesg_restrict=1`
- [ ] `systemd-resolved` + DoH

---

## 3.4 Linux 提权常见路径

| 路径 | 关键命令 / 工具 |
|------|-----------------|
| 配置错误的 SUID | `find / -perm -4000` → GTFOBins |
| sudo 配置漏洞 | `sudo -l`，检索 GTFOBins |
| cron / systemd timer 可写脚本 | `ls -la /etc/cron*` |
| LD_PRELOAD / LD_LIBRARY_PATH | 环境变量劫持 |
| 内核漏洞 | Dirty COW、Dirty Pipe、OverlayFS |
| Docker / Kubernetes 逃逸 | 特权容器、挂载 `/var/run/docker.sock` |
| 可写的 `/etc/passwd` | 写入新的 root 行 |

**自动化工具**：`LinPEAS` / `LinEnum` / `pspy`。

GTFOBins：<https://gtfobins.github.io/>

---

## 3.5 Windows 安全基础

### 3.5.1 账户类型

- 本地账户（SAM 数据库，`C:\Windows\System32\config\SAM`）
- 域账户（存于域控 AD 数据库 `ntds.dit`）
- 组：Administrators / Domain Admins / Enterprise Admins

### 3.5.2 访问令牌与 SID

- **Token** 包含身份 + 权限 + 会话
- SID：`S-1-5-21-<domain>-<rid>`，`500` = 管理员、`501` = 来宾

### 3.5.3 UAC & 完整性级别

| 级别 | 含义 |
|------|------|
| Low | 浏览器沙箱 |
| Medium | 普通用户默认 |
| High | 管理员点击"提升权限"后 |
| System | 内核、服务 |

---

## 3.6 Windows 提权路径

| 路径 | 工具 |
|------|------|
| 未加引号的服务路径 | `wmic service get name,pathname` |
| AlwaysInstallElevated 注册表 | 生成 MSI + `msiexec` |
| 不安全的服务权限 | `accesschk.exe` |
| DLL 劫持 | `Procmon` 找加载失败 DLL |
| Token Impersonation | `Incognito`、`JuicyPotato` / `PrintSpoofer` / `RoguePotato` |
| 凭据抓取 | `mimikatz sekurlsa::logonpasswords` |
| SeDebugPrivilege / SeImpersonatePrivilege 滥用 | `whoami /priv` |

**自动化工具**：`WinPEAS`、`PowerUp.ps1`、`Seatbelt`。

---

## 3.7 Active Directory 安全

### 3.7.1 攻击链

```
外网 → 初访 → 域用户 → 枚举 AD → 横向移动 → 域管 → 域内所有资产
```

### 3.7.2 经典攻击

| 攻击 | 原理 |
|------|------|
| **Kerberoasting** | 请求 SPN 服务票据后离线爆破 |
| **AS-REP Roasting** | 对关闭预认证的账户抓取 AS-REP |
| **Pass-the-Hash (PtH)** | 用 NTLM 哈希直接认证 |
| **Pass-the-Ticket (PtT)** | 用 Kerberos TGT/TGS 直接认证 |
| **Golden Ticket** | 用 krbtgt 哈希伪造万能 TGT |
| **Silver Ticket** | 用服务账户哈希伪造单服务 TGS |
| **DCSync** | 具备复制权限即可同步所有域账户哈希 |
| **Zerologon (CVE-2020-1472)** | Netlogon 加密漏洞直接拿域控 |
| **NoPAC / sAMAccountName 欺骗** | CVE-2021-42278/42287 |
| **PetitPotam + AD CS** | 强制认证 + 证书滥用 |

### 3.7.3 关键工具

- **BloodHound** - 可视化攻击路径（Cypher 查询）
- **Impacket** - Python 套件（`secretsdump.py`、`GetNPUsers.py`、`wmiexec.py`）
- **Rubeus** - Kerberos 工具
- **CrackMapExec / NetExec** - 内网瑞士军刀
- **PowerView** / **AD Module** - 枚举

---

## 3.8 日志与审计

### Linux

| 路径 | 内容 |
|------|------|
| `/var/log/auth.log` `/var/log/secure` | 登录 / sudo |
| `/var/log/syslog` `/var/log/messages` | 系统 |
| `/var/log/audit/audit.log` | `auditd` |
| `~/.bash_history` | 历史命令（易被清空） |
| `last` `lastb` `w` | 登录记录 |

### Windows 事件 ID 速查

| ID | 含义 |
|----|------|
| 4624 | 成功登录 |
| 4625 | 登录失败 |
| 4672 | 特权登录 |
| 4688 | 新进程创建 |
| 4697 | 新服务安装 |
| 4698 | 计划任务创建 |
| 4720 | 新账户 |
| 1102 | 安全日志被清空 |
| 7045 | 服务安装（System） |

推荐 **Sysmon**：更细粒度日志（进程树、网络连接、文件哈希）。

---

## 3.9 主机入侵排查思路

```
1. 账户：last / w / /etc/passwd、shadow、Administrators 组
2. 进程：ps -ef / ss -tunlp / Tasklist / Procmon
3. 网络连接：netstat / ss，看异常外联
4. 启动项：crontab -l / systemd timer / 注册表 Run / 计划任务
5. 文件：近期修改的文件、SUID、临时目录
6. 日志：auth.log、事件日志、Web 服务器日志
7. 后门：SSH authorized_keys、PAM 后门、LKM rootkit、Web shell
```

常用工具：`chkrootkit` / `rkhunter` / `ClamAV` / `osquery` / Sysmon。

---

## 3.10 高频考点

1. Linux 文件权限 `0755` 的含义？
2. 如何快速排查一台 Linux 机器是否被植入持久化后门？
3. Windows 中 NTLM 与 Kerberos 的区别？
4. 简述 Kerberos 认证 AS-REQ / AS-REP / TGS-REQ / TGS-REP 四步。
5. 什么是 Pass-the-Hash？LM/NTLM 哈希的弱点？
6. SeImpersonatePrivilege 为什么危险？
7. Golden Ticket 和 Silver Ticket 的区别？
8. 如何检测 Mimikatz 在主机上的执行？

---

## 3.11 延伸阅读

- 《Windows Internals (7th Ed.)》Mark Russinovich
- 《The Linux Programming Interface》Michael Kerrisk
- 《Active Directory Security》Sean Metcalf - adsecurity.org
- CIS Benchmarks：<https://www.cisecurity.org/cis-benchmarks/>
- HackTricks：<https://book.hacktricks.xyz/>
