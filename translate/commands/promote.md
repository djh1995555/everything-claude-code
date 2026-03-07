---
name: promote
description: 将项目范围的本能提升到全局范围
command: true
---

# 提升命令

将本能从项目范围提升到 continuous-learning-v2 中的全局范围。

## 实现

使用插件根路径运行本能 CLI：

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" promote [instinct-id] [--force] [--dry-run]
```

或者如果 `CLAUDE_PLUGIN_ROOT` 未设置（手动安装）：

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py promote [instinct-id] [--force] [--dry-run]
```

## 用法

```bash
/promote                      # 自动检测提升候选
/promote --dry-run            # 预览自动提升候选
/promote --force              # 无需提示提升所有合格候选
/promote grep-before-edit     # 从当前项目提升一个特定本能
```

## 执行操作

1. 检测当前项目
2. 如果提供了 `instinct-id`，仅提升该本能（如果存在于当前项目中）
3. 否则，找到满足以下条件的跨项目候选：
   - 出现在至少 2 个项目中
   - 满足置信度阈值
4. 将提升的本能写入 `~/.claude/homunculus/instincts/personal/`，设置 `scope: global`
