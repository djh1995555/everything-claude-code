---
paths:
  - "**/*.go"
  - "**/go.mod"
  - "**/go.sum"
---
# Go 模式

> 此文件扩展 [common/patterns.md](../common/patterns.md) 添加 Go 特定内容。

## 功能选项

```go
type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) { s.port = port }
}

func NewServer(opts ...Option) *Server {
    s := &Server{port: 8080}
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

## 小接口

在使用处定义接口，而非在实现处。

## 依赖注入

使用构造函数注入依赖：

```go
func NewUserService(repo UserRepository, logger Logger) *UserService {
    return &UserService{repo: repo, logger: logger}
}
```

## 参考

参见技能：`golang-patterns` 获取全面的 Go 模式，包括并发、错误处理和包组织。
