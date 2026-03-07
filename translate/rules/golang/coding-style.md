---
paths:
  - "**/*.go"
  - "**/go.mod"
  - "**/go.sum"
---
# Go 编码风格

> 此文件扩展 [common/coding-style.md](../common/coding-style.md) 添加 Go 特定内容。

## 格式化

- **gofmt** 和 **goimports** 是强制的 —— 无风格争论

## 设计原则

- 接受接口，返回结构体
- 保持接口小（1-3 个方法）

## 错误处理

始终用上下文包装错误：

```go
if err != nil {
    return fmt.Errorf("failed to create user: %w", err)
}
```

## 参考

参见技能：`golang-patterns` 获取全面的 Go 习语和模式。
