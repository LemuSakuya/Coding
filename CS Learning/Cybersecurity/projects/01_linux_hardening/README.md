# 项目 01：Linux 基线加固实验

> 对应章节：第 3 章《操作系统安全》

## 目标

在一台干净的 Ubuntu Server 22.04 虚拟机上：

1. 完成 CIS Benchmark L1 基线加固。
2. 用 `lynis` / `openscap` 前后对比分数。
3. 产出一份中文加固报告 `report.md`。

## 实验环境

- VirtualBox / UTM / VMware
- Ubuntu Server 22.04 LTS
- 4 GB 内存 / 20 GB 磁盘
- 用户：`student`（sudo）

## 步骤

### 1. 基线扫描（加固前）

```bash
sudo apt update && sudo apt install -y lynis
sudo lynis audit system --quick | tee lynis-before.log
```

记录 **Hardening Index** 与主要 WARNING。

### 2. 基线加固清单

> 每项在 `fix.sh` 里以可回滚的方式写入。

#### 用户与认证

```bash
# 禁用 root 直接 SSH
sudo sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

# 强密码策略
sudo apt install -y libpam-pwquality
echo "minlen=12 minclass=3 retry=3" | sudo tee /etc/security/pwquality.conf

# 失败锁定
sudo tee -a /etc/pam.d/common-auth <<'EOF'
auth required pam_faillock.so preauth silent audit deny=5 unlock_time=1800
EOF
```

#### 文件权限

```bash
sudo chmod 600 /etc/shadow /etc/gshadow
sudo chmod 644 /etc/passwd /etc/group
sudo find / -perm -4000 -type f 2>/dev/null > suid-before.txt
```

#### 服务最小化

```bash
sudo systemctl disable --now cups avahi-daemon bluetooth nfs-client.target
```

#### 网络与防火墙

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw enable
```

#### 内核加固 (`/etc/sysctl.d/99-hardening.conf`)

```
net.ipv4.tcp_syncookies = 1
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
kernel.randomize_va_space = 2
fs.suid_dumpable = 0
```

```bash
sudo sysctl --system
```

#### 日志与审计

```bash
sudo apt install -y auditd
sudo systemctl enable --now auditd
# 关键监控
echo '-w /etc/passwd -p wa -k passwd_changes' | sudo tee -a /etc/audit/rules.d/hardening.rules
sudo augenrules --load
```

### 3. 加固后扫描

```bash
sudo lynis audit system --quick | tee lynis-after.log
```

对比 `Hardening Index` 是否从 ~55 提升到 ~80+。

### 4. 报告模板

在 `report.md` 中填写：

```
# Linux 基线加固报告

## 1. 环境
## 2. 加固前分数
## 3. 执行的加固项（分类 / 命令 / 原理）
## 4. 加固后分数（前后截图）
## 5. 剩余风险与后续计划
```

## 交付物

- `fix.sh`：可回滚的加固脚本
- `lynis-before.log` / `lynis-after.log`
- `report.md`：中文加固报告

## 加分项

- 用 Ansible Playbook 把加固项自动化。
- 跑 OpenSCAP `ssg-ubuntu2204-ds.xml` 的 CIS profile 并解读 HTML 报告。
- 写一份对比 **CIS L1 vs CIS L2** 的差异分析。
