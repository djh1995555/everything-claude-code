---
paths:
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
  - "**/*.jsx"
---
# TypeScript/JavaScript 编码风格

> 此文件扩展 [common/coding-style.md](../common/coding-style.md) 添加 TypeScript/JavaScript 特定内容。

## 不可变性

使用扩展运算符进行不可变更新：

```typescript
// 错误：修改
function updateUser(user, name) {
  user.name = name  // 修改！
  return user
}

// 正确：不可变性
function updateUser(user, name) {
  return {
    ...user,
    name
  }
}
```

## 错误处理

使用 async/await 配合 try-catch：

```typescript
try {
  const result = await riskyOperation()
  return result
} catch (error) {
  console.error('操作失败：', error)
  throw new Error('详细的用户友好消息')
}
```

## 输入验证

使用 Zod 进行基于模式的验证：

```typescript
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150)
})

const validated = schema.parse(input)
```

## Console.log

- 生产代码中不要有 `console.log` 语句
- 改用适当的日志库
- 参见钩子以进行自动检测
