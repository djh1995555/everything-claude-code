---
name: continuous-learning-v2
description: 基于直觉的学习系统，通过钩子观察会话，创建带有置信度评分的原子直觉，并将其演化为技能/命令/代理。v2.1添加了项目范围的直觉，以防止跨项目污染。
origin: ECC
version: 2.1.0
---

# 持续学习v2.1 - 基于直觉的架构

一个高级学习系统，通过原子"直觉" - 带有置信度评分的小型学习行为，将您的Claude Code会话转化为可重用的知识。

**v2.1** 添加了**项目范围的直觉** — React模式保留在您的React项目中，Python约定保留在您的Python项目中，而通用模式（如"始终验证输入"）则全局共享。

## 激活时机

- 设置从Claude Code会话自动学习
- 配置通过钩子提取基于直觉的行为
- 调整学习行为的置信度阈值
- 查看、导出或导入直觉库
- 将直觉演化为完整的技能、命令或代理
- 管理项目范围与全局直觉
- 将直觉从项目范围升级为全局范围

## v2.1中的新功能

| 特性 | v2.0 | v2.1 |
|---------|------|------|
| 存储 | 全局 (~/.claude/homunculus/) | 项目范围 (projects/<hash>/) |
| 范围 | 所有直觉适用于所有地方 | 项目范围 + 全局 |
| 检测 | 无 | git远程URL / 仓库路径 |
| 升级 | N/A | 在2+项目中看到时从项目→全局 |
| 命令 | 4个 (status/evolve/export/import) | 6个 (+promote/projects) |
| 跨项目 | 污染风险 | 默认隔离 |

## v2中的新功能（与v1相比）

| 特性 | v1 | v2 |
|---------|----|----|
| 观察 | Stop钩子（会话结束） | PreToolUse/PostToolUse（100%可靠） |
| 分析 | 主上下文 | 后台代理（Haiku） |
| 粒度 | 完整技能 | 原子"直觉" |
| 置信度 | 无 | 0.3-0.9加权 |
| 演化 | 直接到技能 | 直觉 -> 聚类 -> 技能/命令/代理 |
| 共享 | 无 | 导出/导入直觉 |

## 直觉模型

直觉是一种小型学习行为：

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project
project_id: "a1b2c3d4e5f6"
project_name: "my-react-app"
---

# 优先使用函数式风格

## 操作
在适当的时候使用函数式模式而不是类。

## 证据
- 观察到5次函数式模式偏好实例
- 用户在2025-01-15将基于类的方法更正为函数式
```

**属性：**
- **原子性** -- 一个触发条件，一个操作
- **置信度加权** -- 0.3 = 暂定，0.9 = 几乎确定
- **领域标记** -- 代码风格、测试、git、调试、工作流等
- **证据支持** -- 跟踪创建它的观察结果
- **范围感知** -- `project`（默认）或`global`

## 工作原理

```
会话活动（在git仓库中）
      |
      | 钩子捕获提示 + 工具使用（100%可靠）
      | + 检测项目上下文（git远程 / 仓库路径）
      v
+---------------------------------------------+
|  projects/<project-hash>/observations.jsonl  |
|   (提示、工具调用、结果、项目)               |
+---------------------------------------------+
      |
      | 观察者代理读取（后台，Haiku）
      v
+---------------------------------------------+
|          模式检测                            |
|   * 用户更正 -> 直觉                          |
|   * 错误解决 -> 直觉                          |
|   * 重复工作流 -> 直觉                        |
|   * 范围决策：项目还是全局？                  |
+---------------------------------------------+
      |
      | 创建/更新
      v
+---------------------------------------------+
|  projects/<project-hash>/instincts/personal/ |
|   * prefer-functional.yaml (0.7) [项目]       |
|   * use-react-hooks.yaml (0.9) [项目]         |
+---------------------------------------------+
|  instincts/personal/  (全局)                 |
|   * always-validate-input.yaml (0.85) [全局]  |
|   * grep-before-edit.yaml (0.6) [全局]        |
+---------------------------------------------+
      |
      | /evolve 聚类 + /promote 升级
      v
+---------------------------------------------+
|  projects/<hash>/evolved/ (项目范围)          |
|  evolved/ (全局)                             |
|   * commands/new-feature.md                  |
|   * skills/testing-workflow.md               |
|   * agents/refactor-specialist.md            |
+---------------------------------------------+
```

## 项目检测

系统自动检测您当前的项目：

1. **`CLAUDE_PROJECT_DIR`环境变量**（最高优先级）
2. **`git remote get-url origin`** -- 哈希以创建可移植的项目ID（不同机器上的相同仓库获得相同的ID）
3. **`git rev-parse --show-toplevel`** -- 使用仓库路径作为回退（机器特定）
4. **全局回退** -- 如果未检测到项目，直觉将进入全局范围

每个项目都有一个12字符的哈希ID（例如，`a1b2c3d4e5f6`）。`~/.claude/homunculus/projects.json`处的注册表文件将ID映射为人类可读的名称。

## 快速开始

### 1. 启用观察钩子

添加到您的`~/.claude/settings.json`。

**如果作为插件安装**（推荐）：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/hooks/observe.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/hooks/observe.sh"
      }]
    }]
  }
}
```

**如果手动安装到`~/.claude/skills`**：

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh"
      }]
    }]
  }
}
```

### 2. 初始化目录结构

系统在首次使用时自动创建目录，但您也可以手动创建：

```bash
# 全局目录
mkdir -p ~/.claude/homunculus/{instincts/{personal,inherited},evolved/{agents,skills,commands},projects}

# 项目目录在钩子首次在git仓库中运行时自动创建
```

### 3. 使用直觉命令