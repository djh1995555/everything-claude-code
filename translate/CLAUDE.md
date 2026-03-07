# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在处理此仓库代码时提供指导。

## 项目概述

这是一个 **Claude Code 插件** - 一套生产级的代理、技能、钩子、命令、规则和 MCP 配置的集合。本项目为使用 Claude Code 进行软件开发提供经过实战检验的工作流。

## 运行测试

```bash
# 运行所有测试
node tests/run-all.js

# 运行单个测试文件
node tests/lib/utils.test.js
node tests/lib/package-manager.test.js
node tests/hooks/hooks.test.js
```

## 架构

项目组织为几个核心组件：

- **agents/** - 用于委派的专门子代理（规划者、代码审查者、TDD 指导者等）
- **skills/** - 工作流定义和领域知识（编码标准、模式、测试）
- **commands/** - 用户调用的斜杠命令（/tdd、/plan、/e2e 等）
- **hooks/** - 基于触发器的自动化（会话持久化、工具前后钩子）
- **rules/** - 始终遵循的准则（安全、编码风格、测试要求）
- **mcp-configs/** - 用于外部集成的 MCP 服务器配置
- **scripts/** - 用于钩子和设置的跨平台 Node.js 工具
- **tests/** - 脚本和工具的测试套件

## 主要命令

- `/tdd` - 测试驱动开发工作流
- `/plan` - 实现规划
- `/e2e` - 生成并运行端到端测试
- `/code-review` - 质量审查
- `/build-fix` - 修复构建错误
- `/learn` - 从会话中提取模式
- `/skill-create` - 从 git 历史生成技能

## 开发说明

- 包管理器检测：npm、pnpm、yarn、bun（可通过 `CLAUDE_PACKAGE_MANAGER` 环境变量或项目配置进行配置）
- 跨平台：通过 Node.js 脚本支持 Windows、macOS、Linux
- 代理格式：带有 YAML 前端的 Markdown（名称、描述、工具、模型）
- 技能格式：带有清晰章节的 Markdown，说明何时使用、工作原理、示例
- 钩子格式：带有匹配条件和命令/通知钩子的 JSON

## 贡献

遵循 CONTRIBUTING.md 中的格式：
- 代理：带有前端的 Markdown（名称、描述、工具、模型）
- 技能：清晰的章节（何时使用、工作原理、示例）
- 命令：带有描述前端的 Markdown
- 钩子：带有匹配器和钩子数组的 JSON

文件命名：小写连字符（例如 `python-reviewer.md`、`tdd-workflow.md`）
