# Rules 汇总表

本目录包含 Claude Code 的规则定义，用于强制执行编码标准、安全要求和开发工作流。

## 目录结构

```
rules/
├── common/          # 语言无关原则（始终安装）
├── typescript/      # TypeScript/JavaScript 特定
├── python/          # Python 特定
├── golang/          # Go 特定
└── swift/           # Swift 特定
```

- **common/** 包含适用于所有项目的通用默认值
- **语言目录** 扩展通用规则，包含框架特定模式、工具和代码示例
- 语言特定规则优先于通用规则（特定覆盖通用）

## 规则文件列表

### Common 目录（通用规则）

| 文件名 | 描述 | 主要内容 |
|--------|------|----------|
| [all.md](./common/all.md) | 索引文件 | 引用所有其他通用规则 |
| [coding-style.md](./common/coding-style.md) | 编码风格 | 不可变性、文件组织、错误处理、输入验证 |
| [security.md](./common/security.md) | 安全指南 | 安全检查清单、密钥管理、安全响应协议 |
| [testing.md](./common/testing.md) | 测试要求 | TDD 工作流、80% 覆盖率要求、测试类型 |
| [patterns.md](./common/patterns.md) | 通用模式 | 仓库模式、API 响应格式、骨架项目 |
| [agents.md](./common/agents.md) | 代理编排 | 可用代理、使用时机、并行执行策略 |
| [hooks.md](./common/hooks.md) | 钩子系统 | PreToolUse/PostToolUse/Stop 钩子类型 |
| [git-workflow.md](./common/git-workflow.md) | Git 工作流 | 提交消息格式、PR 工作流 |
| [development-workflow.md](./common/development-workflow.md) | 开发工作流 | 完整功能开发流程（研究→规划→TDD→审查→提交） |
| [performance.md](./common/performance.md) | 性能优化 | 模型选择策略、上下文管理、扩展思考模式 |

### TypeScript 目录

| 文件名 | 描述 | 主要内容 |
|--------|------|----------|
| [coding-style.md](./typescript/coding-style.md) | TypeScript 编码风格 | 不可变性、async/await、Zod 验证、无 console.log |
| [security.md](./typescript/security.md) | TypeScript 安全 | 类型安全最佳实践 |
| [testing.md](./typescript/testing.md) | TypeScript 测试 | Jest/Vitest/Playwright 框架 |
| [patterns.md](./typescript/patterns.md) | TypeScript 模式 | React/Next.js 模式 |
| [hooks.md](./typescript/hooks.md) | TypeScript 钩子 | ESLint/Prettier 自动格式化 |

### Python 目录

| 文件名 | 描述 | 主要内容 |
|--------|------|----------|
| [coding-style.md](./python/coding-style.md) | Python 编码风格 | PEP 8、类型注解、black/isort/ruff 格式化 |
| [security.md](./python/security.md) | Python 安全 | 安全扫描工具 |
| [testing.md](./python/testing.md) | Python 测试 | pytest、覆盖率工具 |
| [patterns.md](./python/patterns.md) | Python 模式 | Pythonic 惯用语、数据类 |
| [hooks.md](./python/hooks.md) | Python 钩子 | black/isort 自动格式化 |

### Golang 目录

| 文件名 | 描述 | 主要内容 |
|--------|------|----------|
| [coding-style.md](./golang/coding-style.md) | Go 编码风格 | gofmt/goimports、接口设计、错误包装 |
| [security.md](./golang/security.md) | Go 安全 | gosec、 Govulncheck 扫描 |
| [testing.md](./golang/testing.md) | Go 测试 | 表驱动测试、测试覆盖率 |
| [patterns.md](./golang/patterns.md) | Go 模式 | 惯用 Go、并发模式 |
| [hooks.md](./golang/hooks.md) | Go 钩子 | gofmt/goimports 格式化 |

### Swift 目录

| 文件名 | 描述 | 主要内容 |
|--------|------|----------|
| [coding-style.md](./swift/coding-style.md) | Swift 编码风格 | SwiftFormat、不可变性、命名规范、并发 |
| [security.md](./swift/security.md) | Swift 安全 | 安全最佳实践 |
| [testing.md](./swift/testing.md) | Swift 测试 | XCTest、测试组织 |
| [patterns.md](./swift/patterns.md) | Swift 模式 | SwiftUI 模式、结构化并发 |
| [hooks.md](./swift/hooks.md) | Swift 钩子 | SwiftFormat/SwiftLint 格式化 |

## 按主题分类

### 编码风格
| 文件 | 适用范围 |
|------|----------|
| [common/coding-style.md](./common/coding-style.md) | 所有语言 |
| [typescript/coding-style.md](./typescript/coding-style.md) | TypeScript/JavaScript |
| [python/coding-style.md](./python/coding-style.md) | Python |
| [golang/coding-style.md](./golang/coding-style.md) | Go |
| [swift/coding-style.md](./swift/coding-style.md) | Swift |

### 安全
| 文件 | 适用范围 |
|------|----------|
| [common/security.md](./common/security.md) | 所有语言 |
| [typescript/security.md](./typescript/security.md) | TypeScript/JavaScript |
| [python/security.md](./python/security.md) | Python |
| [golang/security.md](./golang/security.md) | Go |
| [swift/security.md](./swift/security.md) | Swift |

### 测试
| 文件 | 适用范围 |
|------|----------|
| [common/testing.md](./common/testing.md) | 所有语言 |
| [typescript/testing.md](./typescript/testing.md) | TypeScript/JavaScript |
| [python/testing.md](./python/testing.md) | Python |
| [golang/testing.md](./golang/testing.md) | Go |
| [swift/testing.md](./swift/testing.md) | Swift |

### 模式
| 文件 | 适用范围 |
|------|----------|
| [common/patterns.md](./common/patterns.md) | 所有语言 |
| [typescript/patterns.md](./typescript/patterns.md) | TypeScript/JavaScript |
| [python/patterns.md](./python/patterns.md) | Python |
| [golang/patterns.md](./golang/patterns.md) | Go |
| [swift/patterns.md](./swift/patterns.md) | Swift |

### 钩子
| 文件 | 适用范围 |
|------|----------|
| [common/hooks.md](./common/hooks.md) | 所有语言 |
| [typescript/hooks.md](./typescript/hooks.md) | TypeScript/JavaScript |
| [python/hooks.md](./python/hooks.md) | Python |
| [golang/hooks.md](./golang/hooks.md) | Go |
| [swift/hooks.md](./swift/hooks.md) | Swift |

## 总计

| 目录 | 文件数 |
|------|--------|
| common | 10 |
| typescript | 5 |
| python | 5 |
| golang | 5 |
| swift | 5 |
| **总计** | **30** |

## 安装说明

```bash
# 安装通用 + 语言特定规则
./install.sh typescript
./install.sh python
./install.sh golang
./install.sh swift

# 一次安装多个
./install.sh typescript python
```

> **重要**：复制整个目录 —— 不要扁平化使用 `/*`。通用和语言特定目录包含同名文件，扁平化会导致覆盖。

## 规则优先级

当语言特定规则和通用规则冲突时，**语言特定规则优先**。这遵循标准的分层配置模式（类似于 CSS 特异性或 `.gitignore` 优先级）。

## 规则 vs 技能

- **规则**（本目录）定义广泛适用的标准、约定和检查清单（例如，"80% 测试覆盖率"、"无硬编码密钥"） —— 告诉你要*做什么*
- **技能**（`skills/` 目录）为特定任务提供深入、可操作的参考资料（例如，`python-patterns`、`golang-testing`） —— 告诉你要*怎么做*
