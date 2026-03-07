---
paths:
  - "**/*.swift"
  - "**/Package.swift"
---
# Swift 钩子

> 此文件扩展 [common/hooks.md](../common/hooks.md) 添加 Swift 特定内容。

## PostToolUse 钩子

在 `~/.claude/settings.json` 中配置：

- **SwiftFormat**：编辑后自动格式化 `.swift` 文件
- **SwiftLint**：编辑 `.swift` 文件后运行 lint 检查
- **swift build**：编辑后类型检查修改的包

## 警告

标记 `print()` 语句 —— 对生产代码改用 `os.Logger` 或结构化日志。
