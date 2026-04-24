# 第 6 章 信息收集与 OSINT（开源情报）

## 6.1 学习目标

1. 建立渗透测试 / 红队行动的**侦察（Reconnaissance）**思维：先地图，后攻击。
2. 掌握 **被动 / 主动侦察** 的分界、合规边界与工具链。
3. 能对一个目标域名 / 公司 / 个人做出结构化的 OSINT 画像。
4. 学会整理侦察成果（子域、资产、泄露、凭证），为漏洞评估阶段供料。

---

## 6.2 侦察分类

```
                    ┌──────────────┐
                    │   侦察目标     │
                    │ 域名/IP/人员/组织│
                    └──────┬───────┘
              ┌────────────┴────────────┐
              ▼                         ▼
     ┌────────────────┐         ┌────────────────┐
     │ 被动侦察 Passive │         │ 主动侦察 Active  │
     │ 不接触目标       │         │ 直接与目标交互    │
     │ 公开情报 / 缓存  │         │ 端口扫描 / 指纹  │
     └────────────────┘         └────────────────┘
```

| 维度 | 被动侦察 | 主动侦察 |
|------|----------|----------|
| 是否接触目标 | ❌ | ✅ |
| 是否留痕 | 几乎无 | 可被 IDS / WAF 记录 |
| 合规性 | 高 | 需授权 |
| 典型工具 | `Shodan`, `Censys`, `theHarvester`, `Google Dork` | `nmap`, `masscan`, `amass active`, `ffuf` |

> 未授权对真实目标发起主动侦察是违法的，务必在自有靶场或已签 SOW 的环境中练习。

---

## 6.3 OSINT 情报源

### 6.3.1 域名 / 资产

- **WHOIS**：`whois example.com`（注意 GDPR 后很多字段匿名化）
- **ASN / CIDR**：<https://bgp.he.net/>、`whois -h whois.radb.net -- '-i origin AS15169'`
- **证书透明度 (CT Logs)**：<https://crt.sh>、<https://censys.io/certificates>
- **DNS 历史**：`SecurityTrails`、`ViewDNS.info`、`DNSdumpster`
- **被动 DNS**：`VirusTotal Passive DNS`、`PassiveTotal`
- **互联网测绘**：`Shodan`、`Censys`、`ZoomEye`、`Fofa`、`Quake`

### 6.3.2 子域枚举

```bash
# 被动
amass enum -passive -d example.com -o subs_passive.txt
subfinder -d example.com -all -o subs_subfinder.txt
assetfinder --subs-only example.com >> subs_af.txt

# 主动（字典爆破）
puredns bruteforce bestdns.txt example.com -r resolvers.txt
ffuf -u https://FUZZ.example.com -w subdomains.txt -mc all -fs 0

# 聚合去重
cat subs_*.txt | sort -u > all_subs.txt
# 存活检测
httpx -l all_subs.txt -status-code -title -tech-detect -o live.txt
```

### 6.3.3 Google Dork / 搜索引擎语法

| 语法 | 作用 |
|------|------|
| `site:example.com` | 限定站点 |
| `inurl:admin` | URL 包含关键词 |
| `intitle:"index of"` | 标题包含关键词（常用于找列目录） |
| `filetype:pdf confidential` | 指定文件类型 |
| `ext:sql password` | 扩展名（同 filetype） |
| `"password" site:github.com` | GitHub 泄露 |
| `-site:example.com` | 排除 |

Dork 数据库：Google Hacking Database（GHDB）<https://www.exploit-db.com/google-hacking-database>

### 6.3.4 代码 / 凭证泄露

- **GitHub 搜索**：`"example.com" AWS_ACCESS_KEY_ID`
- **工具**：`trufflehog`、`gitleaks`、`gitGraber`
- **公开数据集**：HaveIBeenPwned、Dehashed、Intelx、Leak-Lookup

### 6.3.5 人员 OSINT

- 社媒：LinkedIn（公司架构）、微博、Twitter/X、BOSS、脉脉
- 图片：`Google Images`、`Yandex Images`、`TinEye`（反向搜图，经常能找到地理位置）
- 邮件推断：`hunter.io`、`phonebook.cz`、`EmailRep`
- 常见命名规则：`first.last@`、`flast@`、`first@` — 可配合 `theHarvester` 批量验证

### 6.3.6 文件元数据

- 工具：`exiftool`（图像 GPS、作者）、`FOCA`（PDF/DOC/PPT 内部路径、用户名、打印机）
- 关注：作者名、软件版本、内网路径（`C:\Users\zhangsan\...` 泄露域名或账号）

---

## 6.4 Recon 工具链示例

```
阶段 1：被动数据采集
  amass (passive) + subfinder + crt.sh + GitHub Dork
        ▼
阶段 2：聚合与去重
  anew / sort -u
        ▼
阶段 3：存活 + 指纹
  httpx + nuclei -t technologies/
        ▼
阶段 4：端口 + 服务
  nmap -sC -sV -p- live.txt
        ▼
阶段 5：内容发现
  ffuf / feroxbuster + waybackurls + gau
        ▼
阶段 6：漏洞扫描（交给 Ch07 / Ch08）
```

### 6.4.1 常用命令速查

```bash
# 子域枚举 + 存活
subfinder -d target.com -silent | httpx -silent > live.txt

# Wayback / GAU 历史 URL
gau target.com | tee urls.txt
waybackurls target.com | anew urls.txt

# 常见敏感文件
ffuf -u https://target.com/FUZZ -w raft-large-files.txt -mc 200,302

# JS 文件里找接口 / 凭证
gau target.com | grep -E '\.js(\?|$)' | httpx -silent | while read u; do
  curl -s "$u" | grep -Eo '(api|token|key|secret|password)["=: ]+[^"]+' ;
done
```

### 6.4.2 推荐的轻量 "all-in-one" 工作流

```bash
# reNgine / ProjectDiscovery 的 uncover + nuclei
uncover -q 'ssl:"target.com"' -silent | nuclei -t cves/ -severity high,critical
```

---

## 6.5 Shodan / Censys / FOFA 查询语法

### 6.5.1 Shodan

| 语法 | 说明 |
|------|------|
| `org:"Example Inc"` | 组织名 |
| `net:192.0.2.0/24` | IP 段 |
| `port:3389 country:CN` | 指定端口 + 地理位置 |
| `product:"nginx" version:"1.18.0"` | 软件版本 |
| `http.title:"Jenkins"` | HTTP 标题 |
| `ssl.cert.subject.CN:"example.com"` | 证书 CN |
| `vuln:CVE-2021-44228` | 已知漏洞 |

### 6.5.2 FOFA

```
domain="example.com" && port="443"
title="后台管理" && country="CN"
body="Apache Struts" && protocol="https"
header="X-Powered-By: PHP" && status_code="200"
```

### 6.5.3 Censys

```
services.tls.certificates.leaf_data.subject.common_name: example.com
services.http.response.headers.server: "nginx"
```

---

## 6.6 OSINT 实操案例：以 `example.com` 为目标

> 仅演示用法，实际执行前必须有书面授权。

1. **资产**：`crt.sh` → 100+ 历史证书 → 提取 SAN → 得到子域列表。
2. **归属**：`bgp.he.net` → ASN → CIDR → `nmap -sn` 快速存活扫描。
3. **泄露**：`github.com/search?q="example.com"+password` → 发现一个历史 commit 含 Slack Webhook。
4. **员工**：LinkedIn → 50+ 员工 → `theHarvester -d example.com -b all` → 生成 1000+ 邮箱 → `haveibeenpwned` 批量核验。
5. **文件**：`site:example.com filetype:pdf` → `exiftool` 提取元数据 → 得到内部作者名 + Office 版本。
6. **产出**：生成 `recon-<date>.md`，字段包括：资产、人员、凭证泄露、技术栈、敏感目录、低悬果（如 Jenkins 未授权）。

---

## 6.7 防守视角：如何减小自己的攻击面

| 控制项 | 建议 |
|--------|------|
| DNS | 敏感子域使用独立 DNS / 内部解析；删除历史记录 |
| 证书透明度 | 不可避免被公开；但要监控 CT 日志里出现的"假冒证书" |
| 员工 OSINT | 员工关闭 LinkedIn 的公司邮箱可见性；强制 2FA |
| GitHub | 启用组织级 Secret Scanning + Push Protection |
| 文档 | PDF / DOC 发布前用 `exiftool -all=` 清理元数据 |
| 互联网测绘 | Shodan Monitor 订阅，及时下线暴露面 |

---

## 6.8 工具速查卡

```bash
# 必装
brew install nmap amass jq
pipx install theHarvester shodan
# Go 系（ProjectDiscovery）
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/uncover/cmd/uncover@latest
go install -v github.com/tomnomnom/anew@latest
go install -v github.com/tomnomnom/waybackurls@latest
```

---

## 6.9 练习题

1. 写一个 Python 脚本：输入一个域名，输出子域、存活 HTTP 服务、技术指纹（基于 `subfinder` + `httpx` 的 JSON 输出聚合）。
2. 在 `crt.sh` 上检索你所在学校 / 公司的主域名，统计过去 12 个月申请了多少张证书。
3. 使用 `trufflehog github --org=<你自己的组织>` 扫描你自己的开源仓库，检查是否有 secret 泄露。
4. 学习如何在不访问目标网站的前提下（纯被动）还原其后端技术栈。

---

## 6.10 小结

侦察阶段的产出 = 后续所有渗透行为的 "数据底座"。做得越扎实，漏洞评估、漏洞利用阶段越省力。
**记住**：信息收集不是"多"，而是"准"与"结构化"。
