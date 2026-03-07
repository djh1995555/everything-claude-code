---
name: configure-ecc
description: Everything Claude Code的交互式安装程序——引导用户选择并安装技能和规则到用户级或项目级目录，验证路径，并可选优化安装文件。
origin: ECC
---

# 配置Everything Claude Code (ECC)

Everything Claude Code项目的交互式、分步安装向导。使用`AskUserQuestion`引导用户选择性安装技能和规则，然后验证正确性并提供优化选项。

## 激活时机

- 用户说"configure ecc"、"install ecc"、"setup everything claude code"或类似内容
- 用户想要选择性安装此项目的技能或规则
- 用户想要验证或修复现有的ECC安装
- 用户想要为其项目优化已安装的技能或规则

## 先决条件

此技能必须在激活前可供Claude Code访问。两种引导方式：
1. **通过插件**：`/plugin install everything-claude-code` — 插件自动加载此技能
2. **手动**：仅将此技能复制到`~/.claude/skills/configure-ecc/SKILL.md`，然后通过说"configure ecc"激活

---

## 步骤0：克隆ECC仓库

在任何安装之前，将最新的ECC源代码克隆到`/tmp`：

```bash
rm -rf /tmp/everything-claude-code
git clone https://github.com/affaan-m/everything-claude-code.git /tmp/everything-claude-code
```

设置`ECC_ROOT=/tmp/everything-claude-code`作为所有后续复制操作的源。

如果克隆失败（网络问题等），使用`AskUserQuestion`要求用户提供现有ECC克隆的本地路径。

---

## 步骤1：选择安装级别

使用`AskUserQuestion`询问用户安装位置：

```
问题："ECC组件应安装在哪里？"
选项：
  - "用户级别 (~/.claude/)" — "适用于您的所有Claude Code项目"
  - "项目级别 (.claude/)" — "仅适用于当前项目"
  - "两者都" — "通用/共享项在用户级别，项目特定项在项目级别"
```

将选择存储为`INSTALL_LEVEL`。设置目标目录：
- 用户级别：`TARGET=~/.claude`
- 项目级别：`TARGET=.claude`（相对于当前项目根目录）
- 两者都：`TARGET_USER=~/.claude`，`TARGET_PROJECT=.claude`

如果目标目录不存在，则创建：
```bash
mkdir -p $TARGET/skills $TARGET/rules
```

---

## 步骤2：选择并安装技能

### 2a：选择范围（核心 vs  niche）

默认**核心（推荐新用户使用）** — 复制`.agents/skills/*`以及`skills/search-first/`用于研究优先工作流。此捆绑包涵盖工程、评估、验证、安全、战略压缩、前端设计和Anthropic跨职能技能（文章写作、内容引擎、市场研究、前端幻灯片）。

使用`AskUserQuestion`（单选）：
```
问题："仅安装核心技能，还是包括 niche/框架包？"
选项：
  - "仅核心（推荐）" — "tdd、e2e、评估、验证、研究优先、安全、前端模式、压缩、跨职能Anthropic技能"
  - "核心 + 选定的 niche" — "在核心之后添加框架/领域特定技能"
  - "仅 niche" — "跳过核心，安装特定框架/领域技能"
默认：仅核心
```

如果用户选择niche或核心 + niche，继续下面的类别选择，仅包括他们选择的那些niche技能。

### 2b：选择技能类别

有27个技能分为4个类别。使用`AskUserQuestion`并设置`multiSelect: true`：

```
问题："您要安装哪些技能类别？"
选项：
  - "框架与语言" — "Django、Spring Boot、Go、Python、Java、前端、后端模式"
  - "数据库" — "PostgreSQL、ClickHouse、JPA/Hibernate模式"
  - "工作流与质量" — "TDD、验证、学习、安全审查、压缩"
  - "所有技能" — "安装所有可用技能"
```

### 2c：确认单个技能

对于每个选定的类别，打印下面的完整技能列表，并要求用户确认或取消选择特定技能。如果列表超过4项，将列表打印为文本，并使用`AskUserQuestion`提供"安装所有列出的"选项以及"其他"供用户粘贴特定名称。

**类别：框架与语言（17个技能）**

| 技能 | 描述 |
|-------|-------------|
| `backend-patterns` | 后端架构、API设计、Node.js/Express/Next.js的服务器端最佳实践 |
| `coding-standards` | TypeScript、JavaScript、React、Node.js的通用编码标准 |
| `django-patterns` | Django架构、使用DRF的REST API、ORM、缓存、信号、中间件 |
| `django-security` | Django安全：认证、CSRF、SQL注入、XSS预防 |
| `django-tdd` | 使用pytest-django、factory_boy、mock、覆盖率的Django测试 |
| `django-verification` | Django验证循环：迁移、linting、测试、安全扫描 |
| `frontend-patterns` | React、Next.js、状态管理、性能、UI模式 |
| `frontend-slides` | 零依赖HTML演示、样式预览和PPTX到Web转换 |
| `golang-patterns` | 惯用Go模式、健壮Go应用程序的约定 |
| `golang-testing` | Go测试：表驱动测试、子测试、基准测试、模糊测试 |
| `java-coding-standards` | Spring Boot的Java编码标准：命名、不可变性、Optional、流 |
| `python-patterns` | Pythonic习惯用法、PEP 8、类型提示、最佳实践 |
| `python-testing` | 使用pytest、TDD、fixtures、mock、参数化的Python测试 |
| `springboot-patterns` | Spring Boot架构、REST API、分层服务、缓存、异步 |
| `springboot-security` | Spring Security：认证/授权、验证、CSRF、机密、速率限制 |
| `springboot-tdd` | 使用JUnit 5、Mockito、MockMvc、Testcontainers的Spring Boot TDD |
| `springboot-verification` | Spring Boot验证：构建、静态分析、测试、安全扫描 |

**类别：数据库（3个技能）**

| 技能 | 描述 |
|-------|-------------|
| `clickhouse-io` | ClickHouse模式、查询优化、分析、数据工程 |
| `jpa-patterns` | JPA/Hibernate实体设计、关系、查询优化、事务 |
| `postgres-patterns` | PostgreSQL查询优化、模式设计、索引、安全 |

**类别：工作流与质量（8个技能）**

| 技能 | 描述 |
|-------|-------------|
| `continuous-learning` | 从会话中自动提取可重用模式作为学习到的技能 |
| `continuous-learning-v2` | 基于直觉的学习，带有置信度评分，演变为技能/命令/代理 |
| `eval-harness` | 用于评估驱动开发（EDD）的正式评估框架 |
| `iterative-retrieval` | 渐进式上下文细化，解决子代理上下文问题 |
| `security-review` | 安全检查表：认证、输入、机密、API、支付功能 |
| `strategic-compact` | 在逻辑间隔建议手动上下文压缩 |
| `tdd-workflow` | 强制执行80%+覆盖率的TDD：单元、集成、E2E |
| `verification-loop` | 验证和质量循环模式 |

**类别：业务与内容（5个技能）**

| 技能 | 描述 |
|-------|-------------|
| `article-writing` | 使用提供的语音、笔记、示例或源文档进行长篇写作 |
| `content-engine` | 多平台社交内容、脚本和再利用工作流 |
| `market-research` | 有来源的市场、竞争对手、资金和技术研究 |
| `investor-materials` | 推介幻灯片、单页文档、投资者备忘录和财务模型 |
| `investor-outreach` | 个性化投资者冷邮件、暖介绍和跟进 |

**独立**

| 技能 | 描述 |
|-------|-------------|
| `project-guidelines-example` | 创建项目特定技能的模板 |

### 2d：执行安装

对于每个选定的技能，复制整个技能目录：
```bash
cp -r $ECC_ROOT/skills/<skill-name> $TARGET/skills/
```

注意：`continuous-learning`和`continuous-learning-v2`有额外文件（config.json、hooks、scripts）——确保复制整个目录，而不仅仅是SKILL.md。

---

## 步骤3：选择并安装规则

使用`AskUserQuestion`并设置`multiSelect: true`：

```
问题："您要安装哪些规则集？"
选项：
  - "通用规则（推荐）" — "语言无关原则：编码风格、git工作流、测试、安全等（8个文件）"
  - "TypeScript/JavaScript" — "TS/JS模式、钩子、使用Playwright测试（5个文件）"
  - "Python" — "Python模式、pytest、black/ruff格式化（5个文件）"
  - "Go" — "Go模式、表驱动测试、gofmt/staticcheck（5个文件）"
```

执行安装：
```bash
# 通用规则（平级复制到rules/）
cp -r $ECC_ROOT/rules/common/* $TARGET/rules/

# 语言特定规则（平级复制到rules/）
cp -r $ECC_ROOT/rules/typescript/* $TARGET/rules/   # 如果选定
cp -r $ECC_ROOT/rules/python/* $TARGET/rules/        # 如果选定
cp -r $ECC_ROOT/rules/golang/* $TARGET/rules/        # 如果选定
```

**重要**：如果用户选择任何语言特定规则但**未**选择通用规则，警告他们：
> "语言特定规则扩展通用规则。不安装通用规则可能导致覆盖不完整。也要安装通用规则吗？"

---

## 步骤4：安装后验证