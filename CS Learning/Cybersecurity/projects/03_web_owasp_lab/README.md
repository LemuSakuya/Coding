# 项目 03：OWASP Top 10 Web 打靶实战

> 对应章节：第 5 章《Web 应用安全》

## 目标

在本地搭建 **DVWA + OWASP Juice Shop** 两个靶场，完成 OWASP Top 10 (2021) 全量练习：

1. A01 失效的访问控制（IDOR / 目录遍历）
2. A02 加密失败（弱 JWT / 明文存储）
3. A03 注入（SQLi / NoSQLi / OS Command Injection）
4. A04 不安全设计
5. A05 安全配置错误
6. A06 组件漏洞（已知 CVE 利用）
7. A07 身份与认证缺陷（暴力破解、重置）
8. A08 软件与数据完整性（CI/CD 投毒）
9. A09 日志与监控缺失
10. A10 SSRF

## 靶场搭建

```bash
# DVWA
docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa

# Juice Shop
docker run -d --name juice -p 3000:3000 bkimminich/juice-shop
```

- DVWA：<http://localhost:8080>  默认账号 admin / password
- Juice Shop：<http://localhost:3000>

## 工具链

- **Burp Suite Community**：代理 + Repeater + Intruder
- **sqlmap**：自动化 SQL 注入
- **ffuf / dirsearch**：目录爆破
- **hydra**：弱口令
- **Postman / HTTPie**：API 调试

## 必做题清单

### A03 SQL 注入

- DVWA → Low/Medium/High 三档分别复现。
- 用 sqlmap 拿到 `manager` 库：
  ```bash
  sqlmap -u "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit" \
         --cookie="PHPSESSID=xxx; security=low" --batch --dbs --level=3
  ```

### A03 OS Command Injection

- DVWA → Command Injection，把 `127.0.0.1; id` 打出来；High 档用 `%0a`、`|`。

### XSS

- DVWA Reflected / Stored / DOM 各跑一遍。
- Juice Shop：完成 `Cross-Site Scripting` 系列挑战（至少 5 关）。

### A01 IDOR / BAC

- Juice Shop：`/#/administration` 未授权访问。
- 修改 JWT `role` 为 `admin`（需先搞定 A02 的 JWT 问题）。

### A02 加密失败

- Juice Shop：访问 `/ftp` 下载 `legal.md`、找隐藏的 backup 文件。
- 破解 MD5 / bcrypt 弱密码（结合项目 04）。

### A10 SSRF

- Juice Shop：用 `http://localhost:3000/solve/challenges/server-side?key=...` 之类的 endpoint 触发内部请求。

## 自动化（加分）

写 `run_burp_scan.py`（基于 Burp REST API / ZAP API），目标：

1. 自动爬虫 + 主动扫描。
2. 导出 HTML 报告。
3. 对发现的漏洞标注 OWASP Top 10 分类。

```bash
# ZAP Docker baseline
docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable \
  zap-full-scan.py -t http://host.docker.internal:3000 -r zap.html
```

## 交付物

- `writeup.md`：每类漏洞至少 1 个 payload + 截图 + 修复建议。
- `zap.html` / `burp-report.html`
- `scripts/` 目录：你写的自动化 Python 脚本

## 加分项

- 跑 **PortSwigger Web Security Academy** 前 20 个 Lab 并记录解题思路。
- 针对 Juice Shop 写一个 Nuclei 模板。
- 阅读 `juice-shop` 源码，对任选 3 个漏洞提修复 PR（白盒代码审计）。
