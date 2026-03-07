---
paths:
  - "**/*.go"
  - "**/go.mod"
  - "**/go.sum"
---
# Go 钩子

> 此文件扩展 [common/hooks.md](../common/hooks.md) 添加 Go 特定内容。

## PostToolUse 钩子

在 `~/.claude/settings.json` 中配置：

- **gofmt/goimports**：编辑后自动格式化 `.go` 文件
- **go vet**：编辑 `.go` 文件后运行静态分析
- **staticcheck**：在修改的包上运行扩展静态检查
