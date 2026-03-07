---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
  - "**/*.jsx"
---
# TypeScript/JavaScript 安全

> 此文件扩展 [common/security.md](../common/security.md) 添加 TypeScript/JavaScript 特定内容。

## 密钥管理

```typescript
// 绝不：硬编码密钥
const apiKey = "sk-proj-xxxxx"

// 始终：环境变量
const apiKey = process.env.OPENAI_API_KEY

if (!apiKey) {
  throw new Error('OPENAI_API_KEY 未配置')
}
```

## 代理支持

- 使用 **security-reviewer** 技能进行全面安全审计
