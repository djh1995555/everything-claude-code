---
paths:
  - "**/*.py"
  - "**/*.pyi"
---
# Python 钩子

> 此文件扩展 [common/hooks.md](../common/hooks.md) 添加 Python 特定内容。

## PostToolUse 钩子

在 `~/.claude/settings.json` 中配置：

- **black/ruff**：编辑后自动格式化 `.py` 文件
- **mypy/pyright**：编辑 `.py` 文件后运行类型检查

## 警告

- 对编辑的文件中的 `print()` 语句发出警告（改用 `logging` 模块）
