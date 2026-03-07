---
description: "在审计 Claude 技能和命令质量时使用。支持快速扫描（仅更改的技能）和完整盘点模式，通过子代理批量顺序评估。"
origin: ECC
---

# skill-stocktake

斜杠命令 (`/skill-stocktake`) 使用质量检查表 + AI 整体判断来审计所有 Claude 技能和命令。支持两种模式：用于最近更改技能的快速扫描，以及用于全面审查的完整盘点。

## 范围

该命令针对以下路径（相对于调用它的目录）：

| 路径 | 描述 |
|------|-------------|
| `~/.claude/skills/` | 全局技能（所有项目） |
| `{cwd}/.claude/skills/` | 项目级技能（如果目录存在） |

**在第 1 阶段开始时，命令会明确列出找到并扫描了哪些路径。**

### 针对特定项目

要包含项目级技能，请从该项目的根目录运行：

```bash
cd ~/path/to/my-project
/skill-stocktake
```

如果项目没有 `.claude/skills/` 目录，则仅评估全局技能和命令。

## 模式

| 模式 | 触发条件 | 持续时间 |
|------|---------|---------|
| 快速扫描 | `results.json` 存在（默认） | 5–10 分钟 |
| 完整盘点 | `results.json` 不存在，或 `/skill-stocktake full` | 20–30 分钟 |

**结果缓存：** `~/.claude/skills/skill-stocktake/results.json`

## 快速扫描流程

仅重新评估自上次运行以来已更改的技能（5–10 分钟）。

1. 读取 `~/.claude/skills/skill-stocktake/results.json`
2. 运行：`bash ~/.claude/skills/skill-stocktake/scripts/quick-diff.sh \
         ~/.claude/skills/skill-stocktake/results.json`
   （项目目录会从 `$PWD/.claude/skills` 自动检测；仅在需要时显式传递）
3. 如果输出为 `[]`：报告 "自上次运行以来没有更改。" 并停止
4. 使用相同的第 2 阶段标准仅重新评估那些更改的文件
5. 从之前的结果中保留未更改的技能
6. 仅输出差异
7. 运行：`bash ~/.claude/skills/skill-stocktake/scripts/save-results.sh \
         ~/.claude/skills/skill-stocktake/results.json <<< "$EVAL_RESULTS"`

## 完整盘点流程

### 第 1 阶段 — 清单

运行：`bash ~/.claude/skills/skill-stocktake/scripts/scan.sh`

该脚本枚举技能文件，提取前页内容，并收集 UTC 修改时间。
项目目录会从 `$PWD/.claude/skills` 自动检测；仅在需要时显式传递。
展示脚本输出的扫描摘要和清单表：

```
扫描：
  ✓ ~/.claude/skills/         (17 个文件)
  ✗ {cwd}/.claude/skills/    (未找到 — 仅全局技能)
```

| 技能 | 7d 使用 | 30d 使用 | 描述 |
|-------|--------|---------|-------------|

### 第 2 阶段 — 质量评估

启动任务工具子代理（**探索代理，模型：opus**），提供完整清单和检查表。
子代理读取每个技能，应用检查表，并返回每个技能的 JSON：

`{ "verdict": "Keep"|"Improve"|"Update"|"Retire"|"Merge into [X]", "reason": "..." }`

**分块指导：** 每个子代理调用处理约 20 个技能，以保持上下文可管理。在每个分块后将中间结果保存到 `results.json`（`status: "in_progress"`）。

所有技能评估完成后：设置 `status: "completed"`，进入第 3 阶段。

**恢复检测：** 如果启动时发现 `status: "in_progress"`，则从第一个未评估的技能恢复。

每个技能根据以下检查表进行评估：

```
- [ ] 检查与其他技能的内容重叠
- [ ] 检查与 MEMORY.md / CLAUDE.md 的重叠
- [ ] 验证技术参考的新鲜度（如果存在工具名称 / CLI 标志 / API，则使用 WebSearch）
- [ ] 考虑使用频率
```

裁决标准：

| 裁决 | 含义 |
|---------|---------|
| Keep | 有用且当前 |
| Improve | 值得保留，但需要特定改进 |
| Update | 引用的技术已过时（使用 WebSearch 验证） |
| Retire | 低质量、陈旧或成本不对称 |
| Merge into [X] | 与另一技能有大量重叠；指定合并目标 |

评估是**整体 AI 判断** — 不是数字评分。指导维度：
- **可操作性**：代码示例、命令或步骤，让您可以立即采取行动
- **范围契合**：名称、触发条件和内容对齐；不过于宽泛或狭窄
- **独特性**：价值不可被 MEMORY.md / CLAUDE.md / 另一技能替代
- **时效性**：技术参考在当前环境中有效

**原因质量要求** — `reason` 字段必须自包含且支持决策：
- 不要单独写 "未更改" — 始终重申核心证据
- 对于 **Retire**：说明 (1) 发现了什么具体缺陷，(2) 什么替代方案可以满足相同需求
  - 错误：`"Superseded"`
  - 正确：`"disable-model-invocation: true 已设置；被 continuous-learning-v2 取代，后者涵盖所有相同模式以及置信度评分。没有独特内容保留。"`
- 对于 **Merge**：指定目标并描述要整合的内容
  - 错误：`"与 X 重叠"`
  - 正确：`"42 行精简内容；chatlog-to-article 的第 4 步已经涵盖相同工作流。将 '文章角度' 提示作为注释整合到该技能中。"`
- 对于 **Improve**：描述需要的具体更改（什么部分，什么操作，相关的目标大小）
  - 错误：`"太长"`
  - 正确：`"276 行；'框架比较' 部分（L80–140）与 ai-era-architecture-principles 重复；删除它以达到约 150 行。"`
- 对于 **Keep**（快速扫描中仅修改时间更改）：重申原始裁决理由，不要写 "未更改"
  - 错误：`"未更改"`
  - 正确：`"修改时间已更新但内容未更改。规则/python/ 明确导入的唯一 Python 参考；未发现重叠。"`

### 第 3 阶段 — 摘要表

| 技能 | 7d 使用 | 裁决 | 原因 |
|-------|--------|---------|--------|

### 第 4 阶段 — 合并

1. **Retire / Merge**：在与用户确认之前，为每个文件提供详细理由：
   - 发现了什么具体问题（重叠、陈旧、损坏的引用等）
   - 什么替代方案涵盖相同功能（对于 Retire：哪个现有技能/规则；对于 Merge：目标文件和要整合的内容）
   - 删除的影响（任何受影响的依赖技能、MEMORY.md 引用或工作流）
2. **Improve**：提供带有理由的具体改进建议：
   - 要更改什么以及为什么（例如，"从 430→200 行，因为 X/Y 部分与 python-patterns 重复"）
   - 用户决定是否采取行动
3. **Update**：提供经过检查的更新内容
4. 检查 MEMORY.md 行数；如果超过 100 行，建议压缩

## 结果文件架构

`~/.claude/skills/skill-stocktake/results.json`：

**`evaluated_at`**：必须设置为评估完成的实际 UTC 时间。
通过 Bash 获取：`date -u +%Y-%m-%dT%H:%M:%SZ`。永远不要使用仅日期的近似值，如 `T00:00:00Z`。

```json
{
  "evaluated_at": "2026-02-21T10:00:00Z",
  "mode": "full",
  "batch_progress": {
    "total": 80,
    "evaluated": 80,
    "status": "completed"
  },
  "skills": {
    "skill-name": {
      "path": "~/.claude/skills/skill-name/SKILL.md",
      "verdict": "Keep",
      "reason": "具体、可操作、对 X 工作流的独特价值",
      "mtime": "2026-01-15T08:30:00Z"
    }
  }
}
```

## 注意事项

- 评估是盲目的：无论来源如何（ECC、自编写、自动提取），所有技能都应用相同的检查表
- 归档 / 删除操作始终需要明确的用户确认
- 不会根据技能来源进行裁决分支