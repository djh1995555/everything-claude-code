# Skills 汇总表

本目录包含 Claude Code 的技能定义，为特定开发任务提供深入、可操作的参考指南。

## 技能与规则的区别

- **规则**（`rules/` 目录）告诉你**做什么** — 广泛适用的标准、约定和检查清单
- **技能**（本目录）告诉你**怎么做** — 特定任务的深入、可操作的参考资料

## 技能列表

### 核心开发技能

| 技能目录 | 名称 | 描述 | 主要内容 |
|----------|------|------|----------|
| [tdd-workflow](./tdd-workflow/SKILL.md) | TDD 工作流 | 测试驱动开发工作流 | 红-绿-重构周期、测试类型（单元/集成/E2E）、覆盖率要求 80%+、测试模式 |
| [e2e-testing](./e2e-testing/SKILL.md) | E2E 测试 | Playwright E2E 测试模式 | 页面对象模型 (POM)、配置模板、不稳定测试处理、工件管理 |
| [security-review](./security-review/SKILL.md) | 安全审查 | 安全漏洞检测和修复 | OWASP Top 10、密钥管理、输入验证、XSS/CSRF/SQL 注入防护、部署前检查清单 |
| [api-design](./api-design/SKILL.md) | API 设计 | REST API 设计模式 | 资源命名、HTTP 状态码、分页策略、错误响应格式、版本控制 |
| [backend-patterns](./backend-patterns/SKILL.md) | 后端模式 | 后端架构模式 | 仓库模式、服务层、中间件、数据库优化、N+1 查询预防 |

### 语言特定技能

#### Python
| 技能目录 | 名称 | 描述 | 主要内容 |
|----------|------|------|----------|
| [python-patterns](./python-patterns/SKILL.md) | Python 模式 | Python 惯用法和最佳实践 | PEP 8、类型提示、EAFP、上下文管理器、装饰器、并发（线程/多进程/async） |
| [python-testing](./python-testing/SKILL.md) | Python 测试 | Python 测试框架 | pytest、mock、测试夹具、参数化测试、覆盖率 |
| [django-patterns](./django-patterns/SKILL.md) | Django 模式 | Django 架构模式 | 项目结构、DRF、ORM、序列化器、权限、信号、中间件 |
| [django-tdd](./django-tdd/SKILL.md) | Django TDD | Django TDD 工作流 | Django 特定的测试驱动开发 |
| [django-security](./django-security/SKILL.md) | Django 安全 | Django 安全最佳实践 | Django 特定的安全配置 |
| [django-verification](./django-verification/SKILL.md) | Django 验证 | Django 验证模式 | Django 验证工作流 |

#### Go
| 技能目录 | 名称 | 描述 | 主要内容 |
|----------|------|------|----------|
| [golang-patterns](./golang-patterns/SKILL.md) | Go 模式 | Go 惯用法和最佳实践 | 错误处理、并发模式（Worker Pool、Context）、接口设计、函数式选项模式 |
| [golang-testing](./golang-testing/SKILL.md) | Go 测试 | Go 测试模式 | 表驱动测试、单元测试、基准测试、模糊测试、mock |

#### TypeScript/JavaScript
| 技能目录 | 名称 | 描述 | 主要内容 |
|----------|------|------|----------|
| [frontend-patterns](./frontend-patterns/SKILL.md) | 前端模式 | React/Next.js 前端模式 | 组件组合、自定义 Hook、状态管理、性能优化 |
| [frontend-slides](./frontend-slides/SKILL.md) | 前端幻灯片 | 前端幻灯片设计 | 幻灯片样式预设、演示模式 |

#### Java
| 技能目录 | 名称 | 描述 | 主要内容 |
|----------|------|------|----------|
| [springboot-patterns](./springboot-patterns/SKILL.md) | Spring Boot 模式 | Spring Boot 架构模式 | 分层架构、JPA 仓库、事务、缓存、异步处理、日志记录 |
| [springboot-security](./springboot-security/SKILL.md) | Spring Boot 安全 | Spring Boot 安全配置 | Spring Security、JWT、OAuth2 |
| [springboot-tdd](./springboot-tdd/SKILL.md) | Spring Boot TDD | Spring Boot TDD 工作流 | Spring Boot 测试驱动开发 |
| [springboot-verification](./springboot-verification/SKILL.md) | Spring Boot 验证 | Spring Boot 验证模式 | Spring Boot 验证工作流 |
| [jpa-patterns](./jpa-patterns/SKILL.md) | JPA 模式 | JPA 数据访问模式 | 实体设计、关联、查询优化、分页 |
| [java-coding-standards](./java-coding-standards/SKILL.md) | Java 编码标准 | Java 编码规范 | Java 代码风格、命名约定 |

#### Swift
| 技能目录 | 名称 | 描述 | 主要内容 |
|----------|------|------|----------|
| [swiftui-patterns](./swiftui-patterns/SKILL.md) | SwiftUI 模式 | SwiftUI 架构模式 | @Observable 状态管理、导航、视图组合、性能优化 |
| [swift-concurrency-6-2](./swift-concurrency-6-2/SKILL.md) | Swift 6 并发 | Swift 6 并发模式 | Swift 6 严格并发、Sendable、Actor |
| [swift-actor-persistence](./swift-actor-persistence/SKILL.md) | Swift Actor 持久化 | Actor 持久化模式 | 基于 Actor 的数据持久化 |
| [swift-protocol-di-testing](./swift-protocol-di-testing/SKILL.md) | Swift 协议 DI 测试 | 依赖注入和测试 | 协议导向的依赖注入、Swift Testing |

#### C++
| 技能目录 | 名称 | 描述 | 主要内容 |
|----------|------|------|----------|
| [cpp-testing](./cpp-testing/SKILL.md) | C++ 测试 | C++ 测试框架 | Google Test、Catch2、测试模式 |
| [cpp-coding-standards](./cpp-coding-standards/SKILL.md) | C++ 编码标准 | C++ 编码规范 | C++ 代码风格、最佳实践 |

### 数据库和基础设施

| 技能目录 | 名称 | 描述 | 主要内容 |
|----------|------|------|----------|
| [postgres-patterns](./postgres-patterns/SKILL.md) | PostgreSQL 模式 | PostgreSQL 最佳实践 | 索引策略、查询优化、RLS、数据类型、连接池、分区 |
| [database-migrations](./database-migrations/SKILL.md) | 数据库迁移 | 迁移管理策略 | 版本控制、回滚策略、种子数据 |
| [clickhouse-io](./clickhouse-io/SKILL.md) | ClickHouse | ClickHouse 分析模式 | 列式存储、优化策略 |
| [docker-patterns](./docker-patterns/SKILL.md) | Docker 模式 | Docker 和 Compose 模式 | 多阶段构建、开发环境、网络、卷策略、安全 |
| [deployment-patterns](./deployment-patterns/SKILL.md) | 部署模式 | 部署策略 | CI/CD、蓝绿部署、金丝雀发布 |

### AI/代理工程

| 技能目录 | 名称 | 描述 | 主要内容 |
|----------|------|------|----------|
| [agentic-engineering](./agentic-engineering/SKILL.md) | 代理工程 | AI 代理工作流 | 先评估后执行、任务分解、模型路由、成本纪律 |
| [agent-harness-construction](./agent-harness-construction/SKILL.md) | 代理线束构建 | 代理线束配置 | 代理系统配置模式 |
| [autonomous-loops](./autonomous-loops/SKILL.md) | 自主循环 | 自主代理循环 | 循环工作流、进度监控、停顿检测 |
| [continuous-learning](./continuous-learning/SKILL.md) | 持续学习 | 持续学习工作流 | 从会话中提取模式 |
| [continuous-learning-v2](./continuous-learning-v2/SKILL.md) | 持续学习 V2 | 改进的持续学习 | 增强的持续学习模式 |
| [eval-harness](./eval-harness/SKILL.md) | 评估线束 | 评估驱动开发 | 能力评估、回归检查 |
| [cost-aware-llm-pipeline](./cost-aware-llm-pipeline/SKILL.md) | 成本感知 LLM 管道 | 成本优化 | 模型选择、成本追踪 |
| [ai-first-engineering](./ai-first-engineering/SKILL.md) | AI 优先工程 | AI 优先开发 | AI 驱动的开发工作流 |

### 内容创作

| 技能目录 | 名称 | 描述 | 主要内容 |
|----------|------|------|----------|
| [content-engine](./content-engine/SKILL.md) | 内容引擎 | 内容创作工作流 | 系统化内容创作 |
| [article-writing](./article-writing/SKILL.md) | 文章写作 | 技术文章写作 | 文章结构、写作风格 |
| [market-research](./market-research/SKILL.md) | 市场研究 | 市场研究方法 | 研究框架、数据收集 |
| [investor-materials](./investor-materials/SKILL.md) | 投资者材料 | 投资者文档 | Pitch deck、投资备忘录 |
| [investor-outreach](./investor-outreach/SKILL.md) | 投资者外联 | 投资者沟通 | 外联策略、邮件模板 |

### 其他技能

| 技能目录 | 名称 | 描述 | 主要内容 |
|----------|------|------|----------|
| [coding-standards](./coding-standards/SKILL.md) | 编码标准 | 通用编码标准 | 跨语言编码最佳实践 |
| [search-first](./search-first/SKILL.md) | 搜索优先 | 搜索优先开发 | 先搜索后实现 |
| [verification-loop](./verification-loop/SKILL.md) | 验证循环 | 验证工作流 | 迭代验证模式 |
| [iterative-retrieval](./iterative-retrieval/SKILL.md) | 迭代检索 | 迭代信息检索 | 渐进式信息收集 |
| [content-hash-cache-pattern](./content-hash-cache-pattern/SKILL.md) | 内容哈希缓存 | 缓存模式 | 基于内容哈希的缓存 |
| [nanoclaw-repl](./nanoclaw-repl/SKILL.md) | Nanoclaw REPL | REPL 工具 | 交互式开发工具 |
| [configure-ecc](./configure-ecc/SKILL.md) | 配置 ECC | Claude Code 配置 | ECC 配置指南 |
| [project-guidelines-example](./project-guidelines-example/SKILL.md) | 项目指南示例 | 项目指南模板 | 项目特定指南示例 |
| [visa-doc-translate](./visa-doc-translate/SKILL.md) | 签证文档翻译 | 签证文档处理 | 签证申请文档翻译 |
| [nutrient-document-processing](./nutrient-document-processing/SKILL.md) | 营养文档处理 | 营养数据处理 | 营养信息提取和处理 |
| [liquid-glass-design](./liquid-glass-design/SKILL.md) | Liquid Glass 设计 | 设计语言 | Apple Liquid Glass 设计模式 |
| [regex-vs-llm-structured-text](./regex-vs-llm-structured-text/SKILL.md) | Regex vs LLM | 结构化文本处理 | 何时使用 Regex vs LLM |
| [strategic-compact](./strategic-compact/SKILL.md) | 战略契约 | 战略文档 | 战略规划框架 |
| [enterprise-agent-ops](./enterprise-agent-ops/SKILL.md) | 企业代理运维 | 企业级 AI 运维 | 大规模 AI 代理部署 |
| [ralphinho-rfc-pipeline](./ralphinho-rfc-pipeline/SKILL.md) | Ralphinho RFC 管道 | RFC 流程 | RFC 创建和审查流程 |
| [skill-stocktake](./skill-stocktake/SKILL.md) | 技能盘点 | 技能清单 | 技能评估和管理 |
| [plankton-code-quality](./plankton-code-quality/SKILL.md) | Plankton 代码质量 | 代码质量工具 | 代码质量自动化 |
| [foundation-models-on-device](./foundation-models-on-device/SKILL.md) | 设备端基础模型 | 边缘 AI | 设备端模型部署 |

## 按类别分类

### 编程语言和框架
- **Python**: `python-patterns`, `python-testing`, `django-patterns`, `django-tdd`, `django-security`, `django-verification`
- **Go**: `golang-patterns`, `golang-testing`
- **Java**: `springboot-patterns`, `springboot-security`, `springboot-tdd`, `springboot-verification`, `jpa-patterns`, `java-coding-standards`
- **Swift**: `swiftui-patterns`, `swift-concurrency-6-2`, `swift-actor-persistence`, `swift-protocol-di-testing`
- **TypeScript/JavaScript**: `frontend-patterns`, `frontend-slides`
- **C++**: `cpp-testing`, `cpp-coding-standards`

### 测试
- `tdd-workflow`, `e2e-testing`, `python-testing`, `golang-testing`, `django-tdd`, `springboot-tdd`, `cpp-testing`

### 安全
- `security-review`, `django-security`, `springboot-security`

### 数据库
- `postgres-patterns`, `database-migrations`, `clickhouse-io`

### 基础设施和 DevOps
- `docker-patterns`, `deployment-patterns`, `api-design`, `backend-patterns`

### AI/代理工程
- `agentic-engineering`, `agent-harness-construction`, `autonomous-loops`, `continuous-learning`, `continuous-learning-v2`, `eval-harness`, `cost-aware-llm-pipeline`, `ai-first-engineering`, `search-first`, `verification-loop`

## 技能文件格式

所有技能文件使用 Markdown 格式，并在开头包含 YAML frontmatter：

```yaml
---
name: skill-name
description: 简短描述
origin: ECC  # 可选
---
```

## 使用说明

1. 技能包含详细的代码示例、模式说明和最佳实践
2. 根据需要引用相应的技能，而不是每次都重复解释
3. 语言特定的技能通常引用相关的 rules 文件
4. 技能可以包含完整的工作流程和分步指南

## 总计

| 类别 | 数量 |
|------|------|
| Python 相关 | 6 |
| Go 相关 | 2 |
| Java/Spring 相关 | 6 |
| Swift 相关 | 4 |
| TypeScript/前端 | 2 |
| C++ 相关 | 2 |
| 数据库/基础设施 | 4 |
| AI/代理工程 | 8 |
| 内容创作 | 5 |
| 其他 | 16 |
| **总计** | **55+** |
