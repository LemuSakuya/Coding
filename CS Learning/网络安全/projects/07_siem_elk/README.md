# 项目 07：基于 ELK 搭建轻量 SIEM

> 对应章节：第 11 章《蓝队防御与 SOC 运营》

## 目标

1. 用 Docker Compose 搭起 **Elasticsearch + Kibana + Logstash + Filebeat/Winlogbeat**。
2. 把 **Sysmon + Windows Security Log** 送到 ELK。
3. 写 3~5 条检测规则（Kibana Alerts 或 Sigma 转换）。
4. 用 Atomic Red Team 触发攻击，验证告警是否命中。

## 架构

```
[Win10 VM]               [Kali / Docker Host]
  Sysmon ──┐
           ├─► Winlogbeat ─► Logstash ─► Elasticsearch ─► Kibana
  Security ┘                                        ▲
                                                    │
                                        [Atomic Red Team 攻击]
```

## 步骤

### 1. ELK 一键起

```bash
git clone https://github.com/deviantony/docker-elk
cd docker-elk
cp .env.example .env
docker compose up -d
# 访问 Kibana: http://localhost:5601  (elastic / changeme)
```

### 2. Win10 靶机配置

#### 安装 Sysmon（使用 SwiftOnSecurity 配置）

```powershell
# 管理员 PowerShell
Invoke-WebRequest https://download.sysinternals.com/files/Sysmon.zip -OutFile Sysmon.zip
Expand-Archive Sysmon.zip -Force
Invoke-WebRequest https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/master/sysmonconfig-export.xml -OutFile sysmon.xml
.\Sysmon\Sysmon64.exe -accepteula -i sysmon.xml
```

#### 启用审计

```powershell
auditpol /set /category:"Logon/Logoff" /success:enable /failure:enable
auditpol /set /subcategory:"Process Creation" /success:enable
# 开启命令行审计
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\Audit" /v ProcessCreationIncludeCmdLine_Enabled /t REG_DWORD /d 1 /f
```

#### 安装 Winlogbeat

```yaml
# winlogbeat.yml 摘要
winlogbeat.event_logs:
  - name: Security
  - name: System
  - name: Microsoft-Windows-Sysmon/Operational
  - name: Microsoft-Windows-PowerShell/Operational

output.logstash:
  hosts: ["<DockerHostIP>:5044"]
```

启动：
```powershell
.\winlogbeat.exe setup -e
Start-Service winlogbeat
```

### 3. Kibana 索引与视图

- 创建 Data View：`winlogbeat-*`
- Discover：确认能看到 `event.code = 4688` / Sysmon `event_id = 1`。
- 建好常用 Dashboard：
  - 新进程 Top 10（命令行）
  - 失败登录（4625）
  - 网络出站 IP Top 20（Sysmon ID=3）
  - PowerShell 脚本块（4104）

### 4. 写 3 条检测

#### 4.1 PowerShell 下载并执行

```
event.code:1 AND process.name:"powershell.exe"
  AND (process.command_line:*DownloadString* OR process.command_line:*IEX* OR process.command_line:*Invoke-Expression*)
```

#### 4.2 5 分钟内 Windows 登录失败 ≥ 10

使用 Kibana Rule：`event.code:4625`，按 `user.name` 聚合，Threshold 10/5m。

#### 4.3 Sysmon ID=11：新建可疑扩展的文件

```
event.code:11 AND file.path:*\\Temp\\* AND (file.extension:"exe" OR file.extension:"dll" OR file.extension:"ps1")
```

### 5. Atomic Red Team 验证

```powershell
IEX (IWR 'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1' -UseBasicParsing)
Install-AtomicRedTeam -getAtomics

# 触发 T1059.001 (PowerShell)
Invoke-AtomicTest T1059.001 -TestNumbers 1

# 触发 T1003.001 (LSASS dump 模拟)
Invoke-AtomicTest T1003.001 -TestNumbers 1 -CheckPrereqs
Invoke-AtomicTest T1003.001 -TestNumbers 1

# 完成后清理
Invoke-AtomicTest T1059.001 -Cleanup
```

然后回 Kibana 观察是否命中、时间差多少、误报情况。

### 6. 写 Sigma 并转换

```bash
pip install sigma-cli
sigma convert -t elasticsearch -p windows-logsources rule.yml
```

## 交付物

- `docker-compose.yml`（或链接）+ 你的自定义 pipeline / ingest
- `sysmon-config.xml` 修改版
- `detections/*.yml`（Sigma）+ Kibana 导出的 `.ndjson`
- `writeup.md`：记录每条检测的原理 / 验证结果 / 调优过程

## 加分项

- 引入 **Fleet + Elastic Agent**，替代 Beats，做统一管理。
- 接入 **Zeek / Suricata** 的 NDR 日志，打通"主机 + 网络"两侧。
- 搭 **Wazuh**（开源 EDR + HIDS）并和 ELK 对比告警质量。
- 用 `TheHive + Cortex` 把告警升级为 Case，演示完整 SOC 流程。
