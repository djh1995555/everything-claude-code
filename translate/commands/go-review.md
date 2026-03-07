---
description: 全面的 Go 代码审查，检查惯用模式、并发安全性、错误处理和安全性。调用 go-reviewer 代理。
---

# Go 代码审查

此命令调用 **go-reviewer** 代理进行全面的 Go 特定代码审查。

## 此命令的作用

1. **识别 Go 更改**：通过 `git diff` 查找修改的 `.go` 文件
2. **运行静态分析**：执行 `go vet`、`staticcheck` 和 `golangci-lint`
3. **安全扫描**：检查 SQL 注入、命令注入、竞争条件
4. **并发审查**：分析 goroutine 安全性、通道使用、互斥锁模式
5. **惯用 Go 检查**：验证代码遵循 Go 约定和最佳实践
6. **生成报告**：按严重性对问题进行分类

## 何时使用

在以下情况使用 `/go-review`：
- 编写或修改 Go 代码后
- 提交 Go 更改之前
- 审查带有 Go 代码的拉取请求
- 加入新的 Go 代码库
- 学习惯用 Go 模式

## 审查类别

### 严重（必须修复）
- SQL/命令注入漏洞
- 没有同步的竞争条件
- Goroutine 泄漏
- 硬编码凭证
- 不安全指针使用
- 关键路径中的错误被忽略

### 高（应该修复）
- 缺少带有上下文的错误包装
- panic 而非错误返回
- 上下文未传播
- 无缓冲通道导致死锁
- 接口未满足错误
- 缺少互斥锁保护

### 中（考虑）
- 非惯用代码模式
- 导出缺少 godoc 注释
- 低效的字符串连接
- 切片未预分配
- 未使用表驱动测试

## 运行的自动检查

```bash
# 静态分析
go vet ./...

# 高级检查（如果已安装）
staticcheck ./...
golangci-lint run

# 竞争检测
go build -race ./...

# 安全漏洞
govulncheck ./...
```

## 示例用法

```text
用户：/go-review

代理：
# Go 代码审查报告

## 审查的文件
- internal/handler/user.go（已修改）
- internal/service/auth.go（已修改）

## 静态分析结果
✓ go vet：没有问题
✓ staticcheck：没有问题

## 发现的问题

[严重] 竞争条件
文件：internal/service/auth.go:45
问题：在没有同步的情况下访问共享映射
```go
var cache = map[string]*Session{}  // 并发访问！

func GetSession(id string) *Session {
    return cache[id]  // 竞争条件
}
```
修复：使用 sync.RWMutex 或 sync.Map
```go
var (
    cache   = map[string]*Session{}
    cacheMu sync.RWMutex
)

func GetSession(id string) *Session {
    cacheMu.RLock()
    defer cacheMu.RUnlock()
    return cache[id]
}
```

[高] 缺少错误上下文
文件：internal/handler/user.go:28
问题：在没有上下文的情况下返回错误
```go
return err  // 没有上下文
```
修复：用上下文包装
```go
return fmt.Errorf("get user %s: %w", userID, err)
```

## 摘要
- 严重：1
- 高：1
- 中：0

建议：❌ 在修复严重问题之前阻止合并
```

## 批准标准

| 状态 | 条件 |
|--------|-----------|
| ✅ 批准 | 没有严重或高问题 |
| ⚠️ 警告 | 只有中等问题（谨慎合并） |
| ❌ 阻止 | 发现严重或高问题 |

## 与其他命令的集成

- 首先使用 `/go-test` 确保测试通过
- 如果出现构建错误使用 `/go-build`
- 在提交前使用 `/go-review`
- 对非 Go 特定问题使用 `/code-review`

## 相关

- 代理：`agents/go-reviewer.md`
- 技能：`skills/golang-patterns/`、`skills/golang-testing/`
