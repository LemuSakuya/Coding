# 贡献指南

感谢你对本项目的关注！以下是参与贡献的流程。

## 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
  - [报告问题](#报告问题)
  - [提交代码](#提交代码)
  - [提交建议](#提交建议)
- [开发规范](#开发规范)
  - [分支命名](#分支命名)
  - [Commit 规范](#commit-规范)
  - [代码风格](#代码风格)

## 行为准则

- 尊重他人，保持友善
- 就事论事，不人身攻击
- 接受建设性批评

## 如何贡献

### 报告问题

在 Issues 中报告 Bug 时，请包含：

1. **问题描述** — 发生了什么，预期是什么
2. **复现步骤** — 如何触发这个问题
3. **环境信息** — Python 版本、操作系统等
4. **截图/日志** — 如果适用

### 提交代码

1. Fork 本仓库
2. 创建你的功能分支：`git checkout -b feature/your-feature`
3. 提交你的修改：`git commit -m 'Add: some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 提交 Pull Request

### 提交建议

欢迎通过 Issues 提出新功能建议，请说明：

- 这个功能解决什么问题
- 你期望的使用方式
- 是否有替代方案

## 开发规范

### 分支命名

| 前缀 | 用途 |
| ---- | ---- |
| `feature/` | 新功能 |
| `fix/` | Bug 修复 |
| `docs/` | 文档更新 |
| `refactor/` | 代码重构 |

### Commit 规范

遵循[约定式提交](https://www.conventionalcommits.org/zh-hans/)：

```
feat: 新增功能
fix: 修复 Bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试相关
chore: 构建/工具
```

### 代码风格

- Python 项目遵循 [PEP 8](https://pep8.org/)
- 适当添加注释，特别是数据分析和建模过程
- 文件名使用英文，避免特殊字符
