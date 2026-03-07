---
name: autonomous-loops
description: "自主Claude Code循环的模式和架构——从简单的顺序管道到RFC驱动的多代理DAG系统。"
origin: ECC
---

# 自主循环技能

> 兼容性说明（v1.8.0）：`autonomous-loops` 将保留一个版本。
> 标准技能名称现在是 `continuous-agent-loop`。新的循环指南
> 应在那里编写，而此技能仍可用以避免
> 破坏现有工作流。

用于自主运行Claude Code循环的模式、架构和参考实现。涵盖从简单的`claude -p`管道到完整的RFC驱动的多代理DAG编排的所有内容。

## 使用时机

- 设置无需人工干预的自主开发工作流
- 为您的问题选择合适的循环架构（简单vs复杂）
- 构建CI/CD风格的持续开发管道
- 运行带合并协调的并行代理
- 实现跨循环迭代的上下文持久化
- 为自主工作流添加质量门和清理步骤

## 循环模式谱

从最简单到最复杂：

| 模式 | 复杂度 | 最佳用途 |
|---------|-----------|----------|
| [顺序管道](#1-顺序管道-claude--p) | 低 | 日常开发步骤、脚本化工作流 |
| [NanoClaw REPL](#2-nanoclaw-repl) | 低 | 交互式持久会话 |
| [无限代理循环](#3-无限代理循环) | 中 | 并行内容生成、规范驱动工作 |
| [持续Claude PR循环](#4-持续claude-pr循环) | 中 | 带CI门控的多天迭代项目 |
| [去杂乱模式](#5-去杂乱模式) | 附加 | 任何实现步骤后的质量清理 |
| [Ralphinho / RFC驱动的DAG](#6-ralphinho--rfc驱动的dag编排) | 高 | 大型功能、带合并队列的多单元并行工作 |

---

## 1. 顺序管道 (`claude -p`)

**最简单的循环。** 将日常开发分解为一系列非交互式的`claude -p`调用。每个调用都是一个有明确提示的聚焦步骤。

### 核心见解

> 如果你无法理解这样的循环，这意味着你甚至无法在交互模式下驱动LLM来修复你的代码。

`claude -p`标志以非交互方式运行Claude Code，完成后退出。链式调用以构建管道：

```bash
#!/bin/bash
# daily-dev.sh — 功能分支的顺序管道

set -e

# 步骤1：实现功能
claude -p "Read the spec in docs/auth-spec.md. Implement OAuth2 login in src/auth/. Write tests first (TDD). Do NOT create any new documentation files."

# 步骤2：去杂乱（清理步骤）
claude -p "Review all files changed by the previous commit. Remove any unnecessary type tests, overly defensive checks, or testing of language features (e.g., testing that TypeScript generics work). Keep real business logic tests. Run the test suite after cleanup."

# 步骤3：验证
claude -p "Run the full build, lint, type check, and test suite. Fix any failures. Do not add new features."

# 步骤4：提交
claude -p "Create a conventional commit for all staged changes. Use 'feat: add OAuth2 login flow' as the message."
```

### 关键设计原则

1. **每个步骤都是隔离的** — 每个`claude -p`调用都有一个全新的上下文窗口，意味着步骤之间没有上下文泄露。
2. **顺序很重要** — 步骤按顺序执行。每个步骤都建立在前一个步骤留下的文件系统状态之上。
3. **否定指令很危险** — 不要说“不要测试类型系统”。相反，添加一个单独的清理步骤（参见[去杂乱模式](#5-去杂乱模式)）。
4. **退出码传播** — `set -e`在失败时停止管道。

### 变体

**带模型路由：**
```bash
# 使用Opus进行研究（深度推理）
claude -p --model opus "Analyze the codebase architecture and write a plan for adding caching..."

# 使用Sonnet进行实现（快速、高效）
claude -p "Implement the caching layer according to the plan in docs/caching-plan.md..."

# 使用Opus进行审查（彻底）
claude -p --model opus "Review all changes for security issues, race conditions, and edge cases..."
```

**带环境上下文：**
```bash
# 通过文件传递上下文，而非提示长度
echo "Focus areas: auth module, API rate limiting" > .claude-context.md
claude -p "Read .claude-context.md for priorities. Work through them in order."
rm .claude-context.md
```

**带`--allowedTools`限制：**
```bash
# 只读分析步骤
claude -p --allowedTools "Read,Grep,Glob" "Audit this codebase for security vulnerabilities..."

# 只写实现步骤
claude -p --allowedTools "Read,Write,Edit,Bash" "Implement the fixes from security-audit.md..."
```

---

## 2. NanoClaw REPL

**ECC的内置持久循环。** 一个会话感知的REPL，以完整的对话历史同步调用`claude -p`。

```bash
# 启动默认会话
node scripts/claw.js

# 带技能上下文的命名会话
CLAW_SESSION=my-project CLAW_SKILLS=tdd-workflow,security-review node scripts/claw.js
```

### 工作原理

1. 从`~/.claude/claw/{session}.md`加载对话历史
2. 每个用户消息都以完整历史作为上下文发送给`claude -p`
3. 响应被追加到会话文件（Markdown作为数据库）
4. 会话在重启之间保持

### NanoClaw vs 顺序管道

| 用例 | NanoClaw | 顺序管道 |
|----------|----------|-------------------|
| 交互式探索 | 是 | 否 |
| 脚本化自动化 | 否 | 是 |
| 会话持久化 | 内置 | 手动 |
| 上下文累积 | 每轮增长 | 每个步骤全新 |
| CI/CD集成 | 差 | 优 |

有关完整详细信息，请参阅`/claw`命令文档。

---

## 3. 无限代理循环

**双提示系统**，编排并行子代理以进行规范驱动的生成。由disler开发（致谢：@disler）。

### 架构：双提示系统

```
提示1（编排器）              提示2（子代理）
┌─────────────────────┐             ┌──────────────────────┐
│ 解析规范文件        │             │ 接收完整上下文        │
│ 扫描输出目录        │  部署      │ 读取分配的编号        │
│ 规划迭代            │────────────│ 严格遵循规范          │
│ 分配创意目录        │  N个代理   │ 生成唯一输出          │
│ 管理波浪            │             │ 保存到输出目录        │
└─────────────────────┘             └──────────────────────┘
```

### 模式

1. **规范分析** — 编排器读取定义要生成内容的规范文件（Markdown）
2. **目录侦察** — 扫描现有输出以找到最高迭代编号
3. **并行部署** — 启动N个子代理，每个代理都有：
   - 完整规范
   - 唯一的创意方向
   - 特定的迭代编号（无冲突）
   - 现有迭代的快照（用于唯一性）
4. **波浪管理** — 对于无限模式，部署3-5个代理的波浪，直到上下文耗尽

### 通过Claude Code命令实现

创建`.claude/commands/infinite.md`：

```markdown
从$ARGUMENTS解析以下参数：
1. spec_file — 规范markdown的路径
2. output_dir — 迭代保存的位置
3. count — 整数1-N或"infinite"

阶段1：读取并深入理解规范。
阶段2：列出output_dir，找到最高迭代编号。从N+1开始。
阶段3：规划创意方向——每个代理获得一个不同的主题/方法。
阶段4：并行部署子代理（任务工具）。每个代理接收：
  - 完整规范文本
  - 当前目录快照
  - 分配的迭代编号
  - 唯一的创意方向
阶段5（无限模式）：以3-5个的波浪循环，直到上下文不足。
```

**调用：**
```bash
/project:infinite specs/component-spec.md src/ 5
/project:infinite specs/component-spec.md src/ infinite
```

### 批处理策略

| 数量 | 策略 |