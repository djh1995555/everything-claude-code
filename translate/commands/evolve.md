---
name: evolve
description: 分析本能并建议或生成进化的结构
command: true
---

# 进化命令

## 实现

使用插件根路径运行本能 CLI：

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" evolve [--generate]
```

或者如果 `CLAUDE_PLUGIN_ROOT` 未设置（手动安装）：

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py evolve [--generate]
```

分析本能并将相关的聚类为高级结构：
- **命令**：当本能描述用户调用的操作时
- **技能**：当本能描述自动触发的行为时
- **代理**：当本能描述复杂的、多步骤的过程时

## 用法

```
/evolve                    # 分析所有本能并建议进化
/evolve --generate         # 同时在 evolved/{skills,commands,agents} 下生成文件
```

## 进化规则

### → 命令（用户调用）
当本能描述用户会明确请求的操作时：
- 多个关于"当用户要求..."的本能
- 具有如"创建新的 X 时"等触发器的本能
- 遵循可重复序列的本能

示例：
- `new-table-step1`："添加数据库表时，创建迁移"
- `new-table-step2`："添加数据库表时，更新模式"
- `new-table-step3`："添加数据库表时，重新生成类型"

→ 创建：**new-table** 命令

### → 技能（自动触发）
当本能描述应自动发生的行为时：
- 模式匹配触发器
- 错误处理响应
- 代码样式执行

示例：
- `prefer-functional`："编写函数时，优先使用函数式风格"
- `use-immutable`："修改状态时，使用不可变模式"
- `avoid-classes`："设计模块时，避免基于类的设计"

→ 创建：`functional-patterns` 技能

### → 代理（需要深度/隔离）
当本能描述复杂的、多步骤的过程，受益于隔离时：
- 调试工作流
- 重构序列
- 研究任务

示例：
- `debug-step1`："调试时，首先检查日志"
- `debug-step2`："调试时，隔离失败的组件"
- `debug-step3`："调试时，创建最小复现"
- `debug-step4`："调试时，用测试验证修复"

→ 创建：**debugger** 代理

## 执行操作

1. 检测当前项目上下文
2. 读取项目 + 全局本能（项目在 ID 冲突时优先）
3. 按触发器/域模式对本能进行分组
4. 识别：
   - 技能候选（2+ 本能的触发器聚类）
   - 命令候选（高置信度工作流本能）
   - 代理候选（更大、高置信度聚类）
5. 在适用时显示推广候选（项目 → 全局）
6. 如果传递了 `--generate`，将文件写入：
   - 项目范围：`~/.claude/homunculus/projects/<project-id>/evolved/`
   - 全局回退：`~/.claude/homunculus/evolved/`

## 输出格式

```
============================================================
  进化分析 - 12 个本能
  项目：my-app (a1b2c3d4e5f6)
  项目范围：8 | 全局：4
============================================================

高置信度本能 (>=80%)：5

## 技能候选
1. 聚类："添加测试"
   本能：3
   平均置信度：82%
   域：testing
   范围：project

## 命令候选 (2)
  /adding-tests
    来源：test-first-workflow [project]
    置信度：84%

## 代理候选 (1)
  adding-tests-agent
    涵盖 3 个本能
    平均置信度：82%
```

## 标志

- `--generate`：除了分析输出外还生成进化文件

## 生成的文件格式

### 命令
```markdown
---
name: new-table
description: 创建带有迁移、模式更新和类型生成的新数据库表
command: /new-table
evolved_from:
  - new-table-migration
  - update-schema
  - regenerate-types
---

# New Table 命令

[基于聚类本能生成的内容]

## 步骤
1. ...
2. ...
```

### 技能
```markdown
---
name: functional-patterns
description: 强制执行函数式编程模式
evolved_from:
  - prefer-functional
  - use-immutable
  - avoid-classes
---

# Functional Patterns 技能

[基于聚类本能生成的内容]
```

### 代理
```markdown
---
name: debugger
description: 系统化调试代理
model: sonnet
evolved_from:
  - debug-check-logs
  - debug-isolate
  - debug-reproduce
---

# Debugger 代理

[基于聚类本能生成的内容]
```
