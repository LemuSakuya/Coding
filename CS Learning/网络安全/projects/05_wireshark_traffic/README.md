# 项目 05：Wireshark 流量分析与协议还原

> 对应章节：第 2 章《网络基础与协议安全》、第 10 章《数字取证》

## 目标

1. 熟练使用 Wireshark / tshark 过滤器。
2. 会从 pcap 中还原：HTTP 文件、图片、TLS 指纹、DNS 异常。
3. 识别常见可疑流量（C2 Beacon、DNS Tunneling、端口扫描）。
4. 写 Python 脚本自动化分析 pcap。

## 环境

- Wireshark 4.x（macOS / Windows / Linux）
- `tshark` 命令行版本
- Python 3 + `scapy`、`pyshark`

## 素材

推荐 pcap 数据集：

- Malware Traffic Analysis：<https://malware-traffic-analysis.net/>
- NETRESEC：<https://www.netresec.com/?page=PcapFiles>
- Wireshark 官方示例：<https://wiki.wireshark.org/SampleCaptures>

本项目使用：
1. 一段 HTTP/FTP 登录的 pcap（可自己抓）
2. 一段 malware-traffic-analysis.net 提供的样本 pcap（含 C2）
3. 一段 DNS Tunneling pcap（iodine / dnscat2 生成）

## 实验任务

### 1. Wireshark 过滤器速查

| 目的 | 过滤器 |
|------|--------|
| 只看 HTTP | `http` |
| 只看 DNS | `dns` |
| 特定 IP | `ip.addr == 1.2.3.4` |
| 源端口 | `tcp.srcport == 443` |
| TLS 客户端 Hello | `tls.handshake.type == 1` |
| SYN 包（扫描特征） | `tcp.flags.syn == 1 and tcp.flags.ack == 0` |
| 大包 | `frame.len > 1500` |
| 指定 Host | `http.host contains "example"` |

### 2. HTTP 文件还原

- `File → Export Objects → HTTP`，把 png/zip/exe 导出。
- 对可疑 exe：`sha256sum` 后丢 VirusTotal。

### 3. 解密 TLS

- 浏览器设置 `SSLKEYLOGFILE`：

  ```bash
  export SSLKEYLOGFILE=/tmp/sslkeys.log
  firefox &
  ```

- Wireshark `Preferences → Protocols → TLS → (Pre)-Master-Secret log filename` 指定该文件。
- 重新打开 pcap，HTTPS 流量已被明文化。

### 4. 识别 C2 Beacon

- 特征：
  - 均匀心跳（每 30±10 秒一次小 POST）
  - TLS JA3/JA3S 指纹异常
  - 目标域名刚注册、DGA、CN 为 `localhost`
- 工具：
  - `Zeek` → `conn.log`、`ssl.log`
  - `rita`（Active Countermeasures）→ beacon 评分
  - `SilentSignal/honeyBadger`

### 5. DNS Tunneling 识别

- 特征：
  - TXT 记录大量、长度接近上限
  - 单域下子域数量爆炸（`aaa.tun.evil.com`、`bbb.tun.evil.com`）
  - 请求熵异常（Base32 / Base64 编码）

### 6. Python 自动化：`analyze_pcap.py`

```python
import pyshark
from collections import Counter

pcap = pyshark.FileCapture('sample.pcap', only_summaries=False)
hosts = Counter()
dns_names = Counter()

for pkt in pcap:
    if 'HTTP' in pkt:
        if hasattr(pkt.http, 'host'):
            hosts[pkt.http.host] += 1
    if 'DNS' in pkt and hasattr(pkt.dns, 'qry_name'):
        dns_names[pkt.dns.qry_name] += 1

print("Top 10 HTTP Hosts:")
for h, c in hosts.most_common(10):
    print(f"  {h}: {c}")

print("Top 10 DNS queries:")
for d, c in dns_names.most_common(10):
    print(f"  {d}: {c}")
```

## 交付物

- `writeup.md`：每个样本 pcap 的分析结论（含截图）
- `analyze_pcap.py`：通用分析脚本
- （如果抓了自己的包）`mycapture.pcap` + 注释

## 加分项

- 用 Zeek 跑 pcap：

  ```bash
  zeek -r malware.pcap
  ls *.log   # conn.log, dns.log, http.log, ssl.log
  ```

- 把 `conn.log` 导入 Elasticsearch，结合项目 07 做可视化。
- 研究 **JA3 / JA4** 指纹：用 `tshark -T ek -r pcap | jq .` 提取客户端指纹，并与已知恶意家族对比。
