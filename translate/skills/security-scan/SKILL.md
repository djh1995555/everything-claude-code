---
name: security-scan
description: 使用 AgentShield 扫描你的 Claude Code 配置（.claude/ 目录）以查找安全漏洞、配置错误和注入风险。检查 CLAUDE.md、settings.json、MCP 服务器、钩子和代理定义。
origin: ECC
---

# 安全扫描技能

使用 [AgentShield](https://github.com/affaan-m/agentshield) 审计你的 Claude Code 配置以查找安全问题。

## 何时激活

- 设置新的 Claude Code 项目
- 修改 `.claude/settings.json`、`CLAUDE.md` 或 MCP 配置后
- 提交配置更改之前
- 加入带有现有 Claude Code 配置的新仓库时
- 定期安全卫生检查

## 扫描内容

| 文件 | 检查内容 |
|------|--------|
| `CLAUDE.md` | 硬编码密钥、自动运行指令、提示注入模式 |
| `settings.json` | 过于宽松的允许列表、缺失的拒绝列表、危险的绕过标志 |
| `mcp.json` | 高风险 MCP 服务器、硬编码环境密钥、npx 供应链风险 |
| `hooks/` | 通过插值的命令注入、数据泄露、静默错误抑制 |
| `agents/*.md` | 无限制的工具访问、提示注入表面、缺失的模型规范 |

## 前提条件

必须安装 AgentShield。检查并根据需要安装：

```bash
# 检查是否已安装
npx ecc-agentshield --version

# 全局安装（推荐）
npm install -g ecc-agentshield

# 或直接通过 npx 运行（无需安装）
npx ecc-agentshield scan .
```

## 使用方法

### 基本扫描

针对当前项目的 `.claude/` 目录运行：

```bash
# 扫描当前项目
npx ecc-agentshield scan

# 扫描特定路径
npx ecc-agentshield scan --path /path/to/.claude

# 扫描并设置最低严重程度过滤器
npx ecc-agentshield scan --min-severity medium
```

### 输出格式

```bash
# 终端输出（默认）——带颜色的报告和等级
npx ecc-agentshield scan

# JSON — 用于 CI/CD 集成
npx ecc-agentshield scan --format json

# Markdown — 用于文档
npx ecc-agentshield scan --format markdown

# HTML — 自包含的深色主题报告
npx ecc-agentshield scan --format html > security-report.html
```

### 自动修复

自动应用安全修复（仅修复标记为可自动修复的问题）：

```bash
npx ecc-agentshield scan --fix
```

这将：
- 用环境变量引用替换硬编码密钥
- 将通配符权限收紧为范围替代方案
- 从不修改仅手动的建议

### Opus 4.6 深度分析

运行对抗性三代理管道进行更深入的分析：

```bash
# 需要 ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY=your-key
npx ecc-agentshield scan --opus --stream
```

这将运行：
1. **攻击者（红队）** — 发现攻击向量
2. **防御者（蓝队）** — 推荐强化措施
3. **审计员（最终裁决）** — 综合双方观点

### 初始化安全配置

从头搭建新的安全 `.claude/` 配置：

```bash
npx ecc-agentshield init
```

创建：
- `settings.json` 带有范围权限和拒绝列表
- `CLAUDE.md` 带有安全最佳实践
- `mcp.json` 占位符

### GitHub Action

添加到你的 CI 管道：

```yaml
- uses: affaan-m/agentshield@v1
  with:
    path: '.'
    min-severity: 'medium'
    fail-on-findings: true
```

## 严重程度等级

| 等级 | 分数 | 含义 |
|-------|-------|---------|
| A | 90-100 | 安全配置 |
| B | 75-89 | 次要问题 |
| C | 60-74 | 需要注意 |
| D | 40-59 | 重大风险 |
| F | 0-39 | 严重漏洞 |

## 结果解释

### 严重发现（立即修复）
- 配置文件中的硬编码 API 密钥或令牌
- 允许列表中的 `Bash(*)`（无限制的 shell 访问）
- 钩子中通过 `${file}` 插值的命令注入
- 运行 shell 的 MCP 服务器

### 高风险发现（生产前修复）
- CLAUDE.md 中的自动运行指令（提示注入向量）
- 权限中缺失的拒绝列表
- 具有不必要 Bash 访问权限的代理

### 中等发现（推荐修复）
- 钩子中的静默错误抑制（`2>/dev/null`、`|| true`）
- 缺失的 PreToolUse 安全钩子
- MCP 服务器配置中的 `npx -y` 自动安装

### 信息发现（意识）
- MCP 服务器缺失描述
- 正确标记为良好实践的禁止指令

## 链接

- **GitHub**: [github.com/affaan-m/agentshield](https://github.com/affaan-m/agentshield)
- **npm**: [npmjs.com/package/ecc-agentshield](https://www.npmjs.com/package/ecc-agentshield)