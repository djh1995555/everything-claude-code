---
name: instinct-status
description: 显示已学习的本能（项目 + 全局）及其置信度
command: true
---

# 本能状态命令

显示当前项目的已学习本能加上全局本能，按域分组。

## 实现

使用插件根路径运行本能 CLI：

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" status
```

或者如果 `CLAUDE_PLUGIN_ROOT` 未设置（手动安装），使用：

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py status
```

## 用法

```
/instinct-status
```

## 执行操作

1. 检测当前项目上下文（git 远程/路径哈希）
2. 从 `~/.claude/homunculus/projects/<project-id>/instincts/` 读取项目本能
3. 从 `~/.claude/homunculus/instincts/` 读取全局本能
4. 使用优先规则合并（项目在 ID 冲突时覆盖全局）
5. 按域显示，带置信度条和观察统计

## 输出格式

```
============================================================
  本能状态 - 总共 12 个
============================================================

  项目：my-app (a1b2c3d4e5f6)
  项目本能：8
  全局本能：  4

## 项目范围 (my-app)
  ### 工作流 (3)
    ███████░░░  70%  编辑前搜索 [项目]
              触发器：修改代码时

## 全局（应用于所有项目）
  ### 安全 (2)
    █████████░  85%  验证用户输入 [全局]
              触发器：处理用户输入时
```
