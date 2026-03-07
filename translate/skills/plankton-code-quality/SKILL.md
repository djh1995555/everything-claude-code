---
name: plankton-code-quality
description: "使用 Plankton 进行写入时代码质量强制执行 — 通过钩子在每次文件编辑时自动格式化、linting 和 Claude 驱动的修复。"
origin: community
---

# Plankton 代码质量技能

Plankton（致谢：@alxfazio）的集成参考，这是 Claude Code 的写入时代码质量强制执行系统。Plankton 通过 PostToolUse 钩子在每次文件编辑时运行格式化器和 linter，然后生成 Claude 子进程来修复代理未捕获的违规。

## 何时使用

- 您希望在每次文件编辑时自动格式化和 linting（而不仅仅是在提交时）
- 您需要防御代理修改 linter 配置以通过而不是修复代码
- 您需要针对修复的分层模型路由（Haiku 用于简单样式，Sonnet 用于逻辑，Opus 用于类型）
- 您使用多种语言（Python、TypeScript、Shell、YAML、JSON、TOML、Markdown、Dockerfile）

## 工作原理

### 三阶段架构

每次 Claude Code 编辑或写入文件时，Plankton 的 `multi_linter.sh` PostToolUse 钩子都会运行：

```
阶段 1：自动格式化（静默）
├─ 运行格式化器（ruff format、biome、shfmt、taplo、markdownlint）
├─ 静默修复 40-50% 的问题
└─ 不向主代理输出

阶段 2：收集违规（JSON）
├─ 运行 linter 并收集无法自动修复的违规
├─ 返回结构化 JSON：{line, column, code, message, linter}
└─ 仍然不向主代理输出

阶段 3：委托 + 验证
├─ 使用违规 JSON 生成 claude -p 子进程
├─ 根据违规复杂性路由到模型层：
│   ├─ Haiku：格式化、导入、样式（E/W/F 代码）— 120s 超时
│   ├─ Sonnet：复杂性、重构（C901、PLR 代码）— 300s 超时
│   └─ Opus：类型系统、深度推理（unresolved-attribute）— 600s 超时
├─ 重新运行阶段 1+2 以验证修复
└─ 如果干净则退出 0，如果仍有违规则退出 2（报告给主代理）
```

### 主代理看到的内容

| 场景 | 代理看到 | 钩子退出 |
|----------|-----------|-----------|
| 无违规 | 无 | 0 |
| 所有问题被子进程修复 | 无 | 0 |
| 子进程修复后仍有违规 | `[hook] N violation(s) remain` | 2 |
| 建议（重复、旧工具） | `[hook:advisory] ...` | 0 |

主代理只会看到子进程无法修复的问题。大多数质量问题会透明地解决。

### 配置保护（防御规则游戏）

LLM 会修改 `.ruff.toml` 或 `biome.json` 以禁用规则而不是修复代码。Plankton 通过三层保护阻止这种情况：

1. **PreToolUse 钩子** — `protect_linter_configs.sh` 在编辑发生前阻止对所有 linter 配置的编辑
2. **Stop 钩子** — `stop_config_guardian.sh` 在会话结束时通过 `git diff` 检测配置更改
3. **受保护文件列表** — `.ruff.toml`、`biome.json`、`.shellcheckrc`、`.yamllint`、`.hadolint.yaml` 等

### 包管理器强制执行

Bash 上的 PreToolUse 钩子阻止遗留包管理器：
- `pip`、`pip3`、`poetry`、`pipenv` → 被阻止（使用 `uv`）
- `npm`、`yarn`、`pnpm` → 被阻止（使用 `bun`）
- 允许的例外：`npm audit`、`npm view`、`npm publish`

## 设置

### 快速开始

```bash
# 将 Plankton 克隆到您的项目中（或共享位置）
# 注意：Plankton 由 @alxfazio 开发
git clone https://github.com/alexfazio/plankton.git
cd plankton

# 安装核心依赖
brew install jaq ruff uv

# 安装 Python linter
uv sync --all-extras

# 启动 Claude Code — 钩子自动激活
claude
```

无需安装命令，无需插件配置。当您在 Plankton 目录中运行 Claude Code 时，`.claude/settings.json` 中的钩子会自动被拾取。

### 每个项目的集成

要在您自己的项目中使用 Plankton 钩子：

1. 将 `.claude/hooks/` 目录复制到您的项目
2. 复制 `.claude/settings.json` 钩子配置
3. 复制 linter 配置文件（`.ruff.toml`、`biome.json` 等）
4. 安装您使用的语言的 linter

### 特定语言依赖

| 语言 | 必需 | 可选 |
|----------|----------|----------|
| Python | `ruff`、`uv` | `ty`（类型）、`vulture`（死代码）、`bandit`（安全） |
| TypeScript/JS | `biome` | `oxlint`、`semgrep`、`knip`（死导出） |
| Shell | `shellcheck`、`shfmt` | — |
| YAML | `yamllint` | — |
| Markdown | `markdownlint-cli2` | — |
| Dockerfile | `hadolint`（>= 2.12.0） | — |
| TOML | `taplo` | — |
| JSON | `jaq` | — |

## 与 ECC 配对

### 互补，不重叠

| 关注点 | ECC | Plankton |
|---------|-----|----------|
| 代码质量强制执行 | PostToolUse 钩子（Prettier、tsc） | PostToolUse 钩子（20+ linter + 子进程修复） |
| 安全扫描 | AgentShield、security-reviewer 代理 | Bandit（Python）、Semgrep（TypeScript） |
| 配置保护 | — | PreToolUse 阻止 + Stop 钩子检测 |
| 包管理器 | 检测 + 设置 | 强制执行（阻止遗留 PM） |
| CI 集成 | — | git 的 pre-commit 钩子 |
| 模型路由 | 手动（`/model opus`） | 自动（违规复杂性 → 层） |

### 推荐组合

1. 安装 ECC 作为您的插件（代理、技能、命令、规则）
2. 添加 Plankton 钩子以进行写入时质量强制执行
3. 使用 AgentShield 进行安全审计
4. 在 PR 前使用 ECC 的 verification-loop 作为最终关卡

### 避免钩子冲突

如果同时运行 ECC 和 Plankton 钩子：
- ECC 的 Prettier 钩子和 Plankton 的 biome 格式化器可能在 JS/TS 文件上冲突
- 解决方案：使用 Plankton 时禁用 ECC 的 Prettier PostToolUse 钩子（Plankton 的 biome 更全面）
- 两者可以在不同文件类型上共存（ECC 处理 Plankton 未覆盖的内容）

## 配置参考

Plankton 的 `.claude/hooks/config.json` 控制所有行为：

```json
{
  "languages": {
    "python": true,
    "shell": true,
    "yaml": true,
    "json": true,
    "toml": true,
    "dockerfile": true,
    "markdown": true,
    "typescript": {
      "enabled": true,
      "js_runtime": "auto",
      "biome_nursery": "warn",
      "semgrep": true
    }
  },
  "phases": {
    "auto_format": true,
    "subprocess_delegation": true
  },
  "subprocess": {
    "tiers": {
      "haiku":  { "timeout": 120, "max_turns": 10 },
      "sonnet": { "timeout": 300, "max_turns": 10 },
      "opus":   { "timeout": 600, "max_turns": 15 }
    },
    "volume_threshold": 5
  }
}
```

**关键设置：**
- 禁用您不使用的语言以加快钩子速度
- `volume_threshold` — 超过此计数的违规自动升级到更高模型层
- `subprocess_delegation: false` — 完全跳过阶段 3（仅报告违规）

## 环境覆盖

| 变量 | 用途 |
|----------|---------|
| `HOOK_SKIP_SUBPROCESS=1` | 跳过阶段 3，直接报告违规 |
| `HOOK_SUBPROCESS_TIMEOUT=N` | 覆盖层超时 |
| `HOOK_DEBUG_MODEL=1` | 记录模型选择决策 |
| `HOOK_SKIP_PM=1` | 绕过包管理器强制执行 |

## 参考

- Plankton（致谢：@alxfazio）
- Plankton REFERENCE.md — 完整架构文档（致谢：@alxfazio）
- Plankton SETUP.md — 详细安装指南（致谢：@alxfazio）

## ECC v1.8 添加

### 可复制的钩子配置文件

设置严格的质量行为：

```bash
export ECC_HOOK_PROFILE=strict
export ECC_QUALITY_GATE_FIX=true
export ECC_QUALITY_GATE_STRICT=true
```

### 语言门表

- TypeScript/JavaScript：首选 Biome，回退 Prettier
- Python：Ruff 格式/检查
- Go：gofmt

### 配置篡改防护

在质量强制执行期间，标记同一迭代中对配置文件的更改：

- `biome.json`、`.eslintrc*`、`prettier.config*`、`tsconfig.json`、`pyproject.toml`

如果配置被更改以抑制违规，需要在合并前进行显式审查。

### CI 集成模式

在 CI 中使用与本地钩子相同的命令：

1. 运行格式化器检查
2. 运行 lint/类型检查
3. 在严格模式下快速失败
4. 发布修复摘要

### 健康指标

跟踪：
- 门标记的编辑
- 平均修复时间
- 按类别划分的重复违规
- 由于门失败导致的合并阻塞