---
name: continuous-learning
description: 自动从Claude Code会话中提取可重用模式，并将其保存为学习到的技能供将来使用。
origin: ECC
---

# 持续学习技能

自动评估Claude Code会话以提取可重用模式，这些模式可以保存为学习到的技能。

## 激活时机

- 设置从Claude Code会话自动提取模式
- 配置会话评估的Stop钩子
- 查看或管理`~/.claude/skills/learned/`中的学习到的技能
- 调整提取阈值或模式类别
- 比较v1（此版本）与v2（基于直觉）方法

## 工作原理

此技能作为**Stop钩子**在每个会话结束时运行：

1. **会话评估**：检查会话是否有足够的消息（默认：10+）
2. **模式检测**：从会话中识别可提取的模式
3. **技能提取**：将有用的模式保存到`~/.claude/skills/learned/`

## 配置

编辑`config.json`进行自定义：

```json
{
  "min_session_length": 10,
  "extraction_threshold": "medium",
  "auto_approve": false,
  "learned_skills_path": "~/.claude/skills/learned/",
  "patterns_to_detect": [
    "error_resolution",
    "user_corrections",
    "workarounds",
    "debugging_techniques",
    "project_specific"
  ],
  "ignore_patterns": [
    "simple_typos",
    "one_time_fixes",
    "external_api_issues"
  ]
}
```

## 模式类型

| 模式 | 描述 |
|---------|-------------|
| `error_resolution` | 特定错误的解决方法 |
| `user_corrections` | 用户更正中的模式 |
| `workarounds` | 框架/库 quirks 的解决方案 |
| `debugging_techniques` | 有效的调试方法 |
| `project_specific` | 项目特定的约定 |

## 钩子设置

添加到您的`~/.claude/settings.json`：

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning/evaluate-session.sh"
      }]
    }]
  }
}
```

## 为什么使用Stop钩子？

- **轻量级**：在会话结束时运行一次
- **非阻塞**：不会增加每条消息的延迟
- **完整上下文**：可以访问完整的会话记录

## 相关

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - 关于持续学习的章节
- `/learn`命令 - 会话中手动提取模式

---

## 比较笔记（研究：2025年1月）

### vs Homunculus

Homunculus v2采用更复杂的方法：

| 特性 | 我们的方法 | Homunculus v2 |
|---------|--------------|---------------|
| 观察 | Stop钩子（会话结束时） | PreToolUse/PostToolUse钩子（100%可靠） |
| 分析 | 主上下文 | 后台代理（Haiku） |
| 粒度 | 完整技能 | 原子"直觉" |
| 置信度 | 无 | 0.3-0.9加权 |
| 演化 | 直接到技能 | 直觉 → 聚类 → 技能/命令/代理 |
| 共享 | 无 | 导出/导入直觉 |

**来自homunculus的关键见解：**
> "v1依赖于技能进行观察。技能是概率性的——它们的触发率约为50-80%。v2使用钩子进行观察（100%可靠），并将直觉作为学习行为的原子单元。"

### 潜在的v2增强

1. **基于直觉的学习** - 更小的原子行为，带有置信度评分
2. **后台观察者** - Haiku代理并行分析
3. **置信度衰减** - 直觉如果被反驳会失去置信度
4. **领域标记** - 代码风格、测试、git、调试等
5. **演化路径** - 将相关直觉聚类为技能/命令

请参阅：`docs/continuous-learning-v2-spec.md`获取完整规范。