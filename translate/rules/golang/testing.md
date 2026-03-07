---
paths:
  - "**/*.go"
  - "**/go.mod"
  - "**/go.sum"
---
# Go 测试

> 此文件扩展 [common/testing.md](../common/testing.md) 添加 Go 特定内容。

## 框架

使用标准 `go test` 配合**表驱动测试**。

## 竞争检测

始终使用 `-race` 标志运行：

```bash
go test -race ./...
```

## 覆盖率

```bash
go test -cover ./...
```

## 参考

参见技能：`golang-testing` 获取详细的 Go 测试模式和辅助函数。
