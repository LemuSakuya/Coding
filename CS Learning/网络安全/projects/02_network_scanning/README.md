# 项目 02：网络侦察（Nmap + Masscan + 自动化脚本）

> 对应章节：第 2 章《网络基础与协议安全》、第 6 章《信息收集与 OSINT》

## 目标

1. 在自有 Home-Only 网络里，使用 Nmap / Masscan 完成：
   - 存活主机发现
   - 全端口扫描
   - 服务识别
   - 漏洞脚本扫描
2. 用 Python (`python-nmap`) 写一个自动化脚本，输出结构化 JSON / Markdown 报告。

## 实验环境

- 宿主机 + 1 台 Metasploitable 2 靶机（192.168.56.101）
- Kali Linux 作为扫描机（192.168.56.102）
- 网络模式：Host-Only（**请勿** 在公网 IP 上执行）

## 手工步骤

### 1. 存活发现

```bash
sudo nmap -sn 192.168.56.0/24 -oA alive
```

### 2. 全端口扫描（两阶段）

```bash
# 阶段 1：快速找开放端口
sudo masscan -p1-65535 192.168.56.101 --rate 5000 -oL open.masscan
awk '/open/ {print $3}' open.masscan | sort -nu | paste -sd, > ports.txt

# 阶段 2：Nmap 做服务识别 + NSE
sudo nmap -sS -sV -sC -O -p"$(cat ports.txt)" 192.168.56.101 -oA deep
```

### 3. 漏洞脚本扫描

```bash
sudo nmap --script vuln -p"$(cat ports.txt)" 192.168.56.101 -oA vuln
```

### 4. 提炼指纹

```bash
xsltproc deep.xml -o deep.html   # 打开看
grep -E "open" deep.gnmap | head
```

## 自动化脚本

参考 `scan_and_report.py`（你需要自己实现），功能：

- 输入：IP / CIDR
- 流程：存活 → 端口 → 服务 → 漏洞
- 输出：`report.md`（按端口分段，含风险评分）+ `result.json`

```python
# 框架示意（自行补全）
import nmap, json, datetime

nm = nmap.PortScanner()
nm.scan(hosts='192.168.56.101', arguments='-sS -sV -sC -p 1-1000')

data = {
    'scanned_at': datetime.datetime.utcnow().isoformat(),
    'hosts': []
}
for host in nm.all_hosts():
    host_data = {'ip': host, 'ports': []}
    for proto in nm[host].all_protocols():
        for port, info in nm[host][proto].items():
            host_data['ports'].append({
                'port': port, 'protocol': proto,
                'state': info['state'],
                'service': info.get('name'),
                'product': info.get('product'),
                'version': info.get('version'),
            })
    data['hosts'].append(host_data)

with open('result.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

## 交付物

- `scan_and_report.py`
- `alive.nmap` / `deep.nmap` / `vuln.nmap` 原始结果
- `report.md`：中文扫描报告（含风险分级与修复建议）

## 加分项

- 加入 **Nuclei** 做模板化 CVE 扫描，合并结果。
- 支持断点续扫（根据 IP 去重）。
- 用 `argparse` 提供 CLI；`rich` 输出彩色进度。
- 把扫描写入 Elasticsearch，配合项目 07 做可视化。
