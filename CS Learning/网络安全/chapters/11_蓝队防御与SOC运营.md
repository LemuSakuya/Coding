# 第 11 章 蓝队防御与 SOC 运营

## 11.1 学习目标

1. 理解蓝队的职责地图：**SOC / IR / CTI / 红紫队演练 / 安全工程**。
2. 掌握一个现代 SOC 的技术栈：**日志采集 → SIEM → SOAR → EDR → 威胁情报**。
3. 能写出合格的 **Sigma 规则** 与 **检测工程（Detection Engineering）** 测试。
4. 熟悉 NIST / ISO 27035 的应急响应流程。

---

## 11.2 蓝队组织结构

```
CSO / CISO
   ├── 安全运营中心 (SOC)
   │   ├── L1 监控值班 (Monitor / Triage)
   │   ├── L2 事件响应 (Incident Response, IR)
   │   ├── L3 威胁狩猎 (Threat Hunting)
   │   └── 24/7 排班
   ├── 威胁情报 (CTI)
   ├── 检测工程 (Detection Engineering)
   ├── 安全工程 (DevSecOps / AppSec)
   ├── 红紫队演练 (Red/Purple Team)
   └── GRC（治理 / 风险 / 合规）
```

### 11.2.1 L1 / L2 / L3 SOC 分级

| 等级 | 职责 | 典型技能 |
|------|------|----------|
| L1 | 看告警、做一线 triage | 日志、SIEM 查询、脚本 |
| L2 | 深度调查、取证、闭环 | 动静分析、脚本、DFIR |
| L3 | 高阶狩猎、规则研发、事件主导 | 逆向、检测工程、ATT&CK 精通 |

---

## 11.3 SOC 技术栈

```
      ┌────────────────────────────────────────────┐
      │               情报层 Threat Intel           │
      │ MISP · OpenCTI · ThreatFox · 商业 TI        │
      └───────────────────┬────────────────────────┘
                          │
      ┌───────────────────▼────────────────────────┐
      │            分析层 SIEM / XDR / SOAR         │
      │ Splunk · ELK · Sentinel · Chronicle         │
      │ TheHive · Shuffle · Cortex                  │
      └───────────────────┬────────────────────────┘
                          │
      ┌───────────────────▼────────────────────────┐
      │        检测层 EDR / NDR / CWPP / EPP        │
      │ CrowdStrike · Elastic EDR · Wazuh · Velociraptor │
      │ Suricata · Zeek · 云 WAF                    │
      └───────────────────┬────────────────────────┘
                          │
      ┌───────────────────▼────────────────────────┐
      │         采集层 Sysmon / osquery / fluentd   │
      │ Filebeat · Winlogbeat · NXLog · Vector      │
      └────────────────────────────────────────────┘
```

---

## 11.4 日志采集（Log Source）

| 数据源 | 关注字段 |
|--------|----------|
| Windows Security Log | 4624, 4625, 4672, 4688, 4698, 4720, 1102 |
| Sysmon | 1/3/7/10/11/13/22 |
| Linux auditd | execve, connect, open |
| Firewall / Proxy | 源 IP / 目的 / URL / 威胁类别 |
| EDR | 进程、文件、注册表、网络 |
| 云审计 | AWS CloudTrail / Azure Activity / GCP Audit |
| 身份 | IdP 登录成功/失败 / MFA 挑战 / 可疑登录 |
| DNS / DHCP | 可疑子域 / NXDomain 激增 |
| VPN | 异地登录、同账号多会话 |

### 11.4.1 采集架构示例（ELK + Beats）

```
Winlogbeat / Filebeat  ─► Logstash  ─► Elasticsearch ─► Kibana
                                   \
                                    ─► Kafka（削峰）
```

### 11.4.2 采集优先级（Essential Log Sources）

1. 终端 EDR + Sysmon（进程链）
2. 身份（IdP、AD、Okta、飞书企业身份）
3. 网络出口（代理 + DNS）
4. 云控制面（CloudTrail / Activity）
5. Web 应用（Nginx access / 业务审计）

---

## 11.5 SIEM 建设

### 11.5.1 ELK（开源代表）

```bash
docker compose up -d       # 快速起一个 ELK
# 指标：_cat/indices，分片数 / 保留周期 / 热温冷架构
```

### 11.5.2 Splunk SPL 示例

```splunk
index=wineventlog EventCode=4625
| stats count by src_ip, user
| where count > 20
| sort - count
```

### 11.5.3 检测规则：Sigma（SIEM 中立语法）

```yaml
title: Suspicious PowerShell Download
id: 0b1f2e2d-xxx
status: experimental
description: PowerShell 调用 DownloadString 下载脚本
logsource:
  product: windows
  service: sysmon
detection:
  selection:
    EventID: 1
    Image|endswith: '\powershell.exe'
    CommandLine|contains:
      - 'DownloadString'
      - 'IEX '
      - 'Invoke-Expression'
  condition: selection
falsepositives:
  - 合法运维脚本
level: high
tags:
  - attack.execution
  - attack.t1059.001
```

用 `sigmac` 转换成 Splunk / ES / Chronicle 查询：

```bash
sigmac -t splunk -c splunk-windows rule.yml
```

---

## 11.6 EDR（Endpoint Detection & Response）

### 11.6.1 典型能力

- 进程创建链路（父子进程、命令行、Hash）
- 文件 / 注册表写入审计
- 网络连接关联
- 内存扫描 / Shellcode 检测
- 一键隔离、远程取证、反向 Shell

### 11.6.2 开源方案

- **Wazuh** = OSSEC + ELK：HIDS + 合规扫描 + Rootkit 检测
- **osquery** + **Fleet**：SQL 查询端点状态
- **Velociraptor**：高阶 DFIR / Hunt
- **Elastic EDR**：集成于 Elastic Security

### 11.6.3 示例：osquery 检测 "从 Temp 执行的未签名程序"

```sql
SELECT p.pid, p.name, p.path, s.authority, s.serial_number
FROM processes p
LEFT JOIN signature s ON p.path = s.path
WHERE p.path LIKE 'C:\\Users\\%\\AppData\\Local\\Temp\\%'
  AND (s.authority IS NULL OR s.result != 'trusted');
```

---

## 11.7 SOAR（编排与自动化）

### 11.7.1 核心能力

- Playbook：事件触发 → 自动收集证据 → 富化 → 决策 → 阻断 / 通知。
- 富化：VirusTotal / Shodan / 威胁情报 / CMDB 查询。
- 执行：防火墙封 IP、EDR 隔离主机、IdP 强制改密。

### 11.7.2 开源工具

- **TheHive** + **Cortex**：告警管理 + 富化分析
- **Shuffle**：可视化 Playbook，开源替代 Splunk SOAR
- **n8n / Elastalert 2**：轻量自动化

### 11.7.3 Playbook 样例：钓鱼邮件处置

```
Trigger: 邮件网关上报 phishing
  ├─ 提取 IOC（URL / 附件 Hash / 发件人）
  ├─ VirusTotal + URLScan 富化
  ├─ 若命中 KEV / 威胁情报 → 自动：
  │    ├─ 邮箱删信 (Graph API)
  │    ├─ 代理封 URL
  │    ├─ 给相关用户发 Teams / 飞书告警
  │    └─ 在 TheHive 创建 Case
  └─ 否则 → 人工复核
```

---

## 11.8 威胁狩猎（Threat Hunting）

### 11.8.1 假设驱动（Hypothesis-Driven）

```
1. 假设（Hypothesis）：攻击者利用 WMI 做横向移动
2. 数据：Sysmon Event 1 + 3 + 17/18, Security 4624
3. 查询：父进程=wmiprvse.exe / 远程登录后 5 分钟内出现 cmd.exe
4. 验证：是否是正常 SCCM / 监控软件
5. 产出：写成一条 Sigma 规则 + 通报
```

### 11.8.2 狩猎矩阵（示例）

| ATT&CK | 行为 | 关键信号 |
|--------|------|----------|
| T1003.001 | LSASS 内存转储 | procdump.exe 读 lsass；MiniDumpWriteDump |
| T1021.002 | SMB/Admin$ 横向 | 4624 Logon Type=3 + 4672 + 5140 |
| T1547.001 | Run 键持久化 | Sysmon 13: HKCU\...\Run |
| T1059.001 | PowerShell 下载 | DownloadString / IEX / -enc base64 |
| T1110.003 | 密码喷洒 | 4625 在多账号上重复失败 |
| T1566 | 钓鱼 | Outlook 启动 mshta / wscript |

---

## 11.9 应急响应（IR）

### 11.9.1 NIST 四阶段

```
Preparation → Detection & Analysis → Containment, Eradication & Recovery → Post-Incident Activity
准备       → 检测与分析            → 遏制 / 清除 / 恢复                → 事后复盘
```

### 11.9.2 关键动作（前 60 分钟）

1. 确认是真告警还是误报。
2. 评估影响：主机数量 / 数据外泄量。
3. 隔离：EDR 隔离、网络分段断开、改密钥。
4. 保留证据：内存、日志、流量。
5. 启动指挥部：作战室 / 事件记录（Who/When/What）。
6. 通知：内部 + 法务 + 监管（依据合规）。

### 11.9.3 事件分级（可按贵公司实际调整）

| 等级 | 触发条件 | SLA |
|------|----------|-----|
| P0 | 生产环境被控、数据外泄、勒索加密 | 立即集结 |
| P1 | 关键服务器被入侵、高危 0day 外网暴露 | < 1h |
| P2 | 受控失败的入侵尝试、内部违规 | < 4h |
| P3 | 异常但无实际影响 | 次日处理 |

---

## 11.10 检测工程（Detection Engineering）

### 11.10.1 规则生命周期

```
Hypothesis → Data Validation → Prototype → Test (Atomic Red Team / Purple Team)
         → Deploy → Monitor FP/TP → Tune → Retire
```

### 11.10.2 Purple Team 演练

- **Atomic Red Team**：<https://github.com/redcanaryco/atomic-red-team> — 基于 ATT&CK 的原子测试。
- **Caldera**：MITRE 的自动化红队平台。
- **Red Team Tools**：C2 模拟、横向移动、数据外带。
- **指标**：MTTD（发现时间）/ MTTR（响应时间）/ 覆盖率（ATT&CK 技术数）。

### 11.10.3 检测覆盖图

推荐工具：`attack-navigator`（<https://mitre-attack.github.io/attack-navigator/>）做可视化，标记每个 ATT&CK 技术当前检测能力：
- `green` 已覆盖 + 高置信
- `yellow` 部分覆盖
- `red` 盲区

---

## 11.11 合规基线

| 行业 | 主要标准 |
|------|----------|
| 国内 | 《网络安全等级保护 2.0》、《关键信息基础设施保护条例》、《数据安全法》、《个人信息保护法》 |
| 金融 | PCI-DSS、JR/T 0071 |
| 医疗 | HIPAA |
| 通用 | ISO 27001 / 27035 / 27701、NIST CSF、SOC 2 |

---

## 11.12 个人蓝队学习环境

```bash
# 1. ELK 一键起
git clone https://github.com/deviantony/docker-elk
cd docker-elk && docker compose up -d

# 2. Sysmon + Winlogbeat 靶机
choco install sysmon-bundle -y
# 配置文件：https://github.com/olafhartong/sysmon-modular

# 3. 下载 Atomic Red Team
IEX (IWR 'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1')
Invoke-AtomicTest T1059.001 -ShowDetails
```

搭好后：用 Atomic 触发某个 ATT&CK → 查 Kibana 看是否命中 → 写 Sigma → 迭代。

---

## 11.13 练习题

1. 用 Docker 搭一套 ELK + Winlogbeat + Sysmon 采集环境，让你的 Windows 10 虚拟机事件进入 Kibana。
2. 在 Kibana 里写出以下 3 条检测：
   - 从 `%AppData%\Roaming\` 启动的 PowerShell；
   - 5 分钟内 4625 失败 ≥ 10 次；
   - 新建的"Microsoft Edge"服务但签名者不是微软。
3. 用 Atomic Red Team 触发 `T1003.001`（LSASS dump），验证你的检测能否命中，并填补盲点。
4. 写一份事件响应手册（IR Playbook）模板，覆盖勒索 / 钓鱼 / 内网横向三种场景。

---

## 11.14 小结

蓝队的核心不是"用最贵的产品"，而是 **有可解释的检测逻辑 + 可验证的响应流程 + 持续演练**。
红队找 1 个洞就赢，蓝队每天要防 1 万次；所以 **工程化、流程化、自动化** 是唯一出路。
