# Agents 汇总表

本目录包含所有可用的 Claude Code 代理（Agents）定义文件，用于专门的代码审查、构建修复、安全检测等任务。

## 代理列表

| 文件名 | 名称 | 描述 | 工具 | 模型 |
|--------|------|------|------|------|
| [go-reviewer.md](./go-reviewer.md) | go-reviewer | 专家级 Go 代码审查者，专注于惯用的 Go、并发模式、错误处理和性能。用于所有 Go 代码更改。必须用于 Go 项目。 | Read, Grep, Glob, Bash | sonnet |
| [architect.md](./architect.md) | architect | 系统设计、可扩展性和技术决策的软件架构专家。在规划新功能、重构大型系统或做出架构决策时主动使用。 | Read, Grep, Glob | opus |
| [harness-optimizer.md](./harness-optimizer.md) | harness-optimizer | 分析和改进本地代理线束配置，以提高可靠性、成本和吞吐量。 | Read, Grep, Glob, Bash, Edit | sonnet |
| [python-reviewer.md](./python-reviewer.md) | python-reviewer | 专家级 Python 代码审查者，专注于 PEP 8 合规性、Pythonic 惯用语、类型提示、安全性和性能。用于所有 Python 代码更改。必须用于 Python 项目。 | Read, Grep, Glob, Bash | sonnet |
| [e2e-runner.md](./e2e-runner.md) | e2e-runner | 使用 Vercel Agent Browser（首选）和 Playwright 后备的端到端测试专家。主动用于生成、维护和运行 E2E 测试。管理测试旅程、隔离不稳定的测试、上传工件（截图、视频、跟踪），并确保关键用户流程正常工作。 | Read, Write, Edit, Bash, Grep, Glob | sonnet |
| [doc-updater.md](./doc-updater.md) | doc-updater | 文档和代码地图专家。主动用于更新代码地图和文档。运行 /update-codemaps 和 /update-docs，生成 docs/CODEMAPS/*，更新 README 和指南。 | Read, Write, Edit, Bash, Grep, Glob | haiku |
| [database-reviewer.md](./database-reviewer.md) | database-reviewer | PostgreSQL 数据库专家，负责查询优化、模式设计、安全和性能。在编写 SQL、创建迁移、设计模式或排查数据库性能问题时主动使用。结合了 Supabase 最佳实践。 | Read, Write, Edit, Bash, Grep, Glob | sonnet |
| [tdd-guide.md](./tdd-guide.md) | tdd-guide | 测试驱动开发专家，执行先写测试的方法论。在编写新功能、修复 bug 或重构代码时主动使用。确保 80%+ 的测试覆盖率。 | Read, Write, Edit, Bash, Grep | sonnet |
| [loop-operator.md](./loop-operator.md) | loop-operator | 操作自主代理循环、监控进度，并在循环停顿时安全干预。 | Read, Grep, Glob, Bash, Edit | sonnet |
| [build-error-resolver.md](./build-error-resolver.md) | build-error-resolver | 构建和 TypeScript 错误解决专家。在构建失败或出现类型错误时主动使用。仅用最小差异修复构建/类型错误，不进行架构编辑。专注于快速让构建变绿。 | Read, Write, Edit, Bash, Grep, Glob | sonnet |
| [chief-of-staff.md](./chief-of-staff.md) | chief-of-staff | 个人沟通参谋长，分类电子邮件、Slack、LINE 和 Messenger。将消息分类为 4 个层级（跳过/仅信息/会议信息/需要操作），生成草稿回复，并通过钩子强制发送后跟进。在管理多渠道沟通工作流时使用。 | Read, Grep, Glob, Bash, Edit, Write | opus |
| [security-reviewer.md](./security-reviewer.md) | security-reviewer | 安全漏洞检测和修复专家。在编写处理用户输入、身份验证、API 端点或敏感数据的代码后主动使用。标记密钥、SSRF、注入、不安全加密和 OWASP Top 10 漏洞。 | Read, Write, Edit, Bash, Grep, Glob | sonnet |
| [go-build-resolver.md](./go-build-resolver.md) | go-build-resolver | Go 构建、vet 和编译错误解决专家。用最小的更改修复构建错误、go vet 问题和 linter 警告。在 Go 构建失败时使用。 | Read, Write, Edit, Bash, Grep, Glob | sonnet |
| [refactor-cleaner.md](./refactor-cleaner.md) | refactor-cleaner | 死代码清理和合并专家。主动用于删除未使用的代码、重复项和重构。运行分析工具（knip、depcheck、ts-prune）来识别死代码并安全删除。 | Read, Write, Edit, Bash, Grep, Glob | sonnet |
| [code-reviewer.md](./code-reviewer.md) | code-reviewer | 专家代码审查专家。主动审查代码的质量、安全性和可维护性。在编写或修改代码后立即使用。必须用于所有代码更改。 | Read, Grep, Glob, Bash | sonnet |
| [planner.md](./planner.md) | planner | 复杂功能和重构的专家规划专家。当用户请求功能实现、架构更改或复杂重构时，主动使用。自动激活用于规划任务。 | Read, Grep, Glob | opus |

## 按类别分类

### 代码审查类
| 代理 | 用途 |
|------|------|
| [code-reviewer](./code-reviewer.md) | 通用代码审查（质量、安全、可维护性） |
| [go-reviewer](./go-reviewer.md) | Go 代码审查 |
| [python-reviewer](./python-reviewer.md) | Python 代码审查 |
| [security-reviewer](./security-reviewer.md) | 安全漏洞检测和修复 |
| [database-reviewer](./database-reviewer.md) | SQL/数据库查询审查 |

### 构建修复类
| 代理 | 用途 |
|------|------|
| [build-error-resolver](./build-error-resolver.md) | TypeScript/构建错误修复 |
| [go-build-resolver](./go-build-resolver.md) | Go 构建错误修复 |

### 架构规划类
| 代理 | 用途 |
|------|------|
| [planner](./planner.md) | 功能实现规划 |
| [architect](./architect.md) | 系统架构设计 |
| [refactor-cleaner](./refactor-cleaner.md) | 死代码清理和重构 |

### 测试类
| 代理 | 用途 |
|------|------|
| [tdd-guide](./tdd-guide.md) | 测试驱动开发指导 |
| [e2e-runner](./e2e-runner.md) | 端到端测试执行 |

### 运维/工具类
| 代理 | 用途 |
|------|------|
| [doc-updater](./doc-updater.md) | 文档和代码地图更新 |
| [harness-optimizer](./harness-optimizer.md) | 代理线束配置优化 |
| [loop-operator](./loop-operator.md) | 自主代理循环管理 |
| [chief-of-staff](./chief-of-staff.md) | 沟通工作流管理 |

## 代理文件格式

所有代理文件使用 Markdown 格式，并在开头包含 YAML frontmatter：

```yaml
---
name: agent-name
description: 简短描述
tools: ["Tool1", "Tool2", "Tool3"]
model: sonnet  # 或 opus, haiku
color: orange  # 可选
---
```

## 使用说明

1. 这些代理通过 Agent 工具调用，由主代理根据任务类型自动选择
2. 每个代理都有特定的 `tools` 列表，限制其可操作范围
3. `model` 字段指定使用的 Claude 模型（sonnet/opus/haiku）
4. 详细的工作流程和指令在每个代理文件的正文部分
