---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
  - "**/*.jsx"
---
# TypeScript/JavaScript 钩子

> 此文件扩展 [common/hooks.md](../common/hooks.md) 添加 TypeScript/JavaScript 特定内容。

## PostToolUse 钩子

在 `~/.claude/settings.json` 中配置：

- **Prettier**：编辑后自动格式化 JS/TS 文件
- **TypeScript 检查**：编辑 `.ts`/`.tsx` 文件后运行 `tsc`
- **console.log 警告**：对编辑的文件中的 `console.log` 发出警告

## Stop 钩子

- **console.log 审计**：在会话结束前检查所有修改的文件中是否有 `console.log`
