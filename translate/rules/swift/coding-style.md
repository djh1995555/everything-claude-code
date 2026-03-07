---
paths:
  - "**/*.swift"
  - "**/Package.swift"
---
# Swift 编码风格

> 此文件扩展 [common/coding-style.md](../common/coding-style.md) 添加 Swift 特定内容。

## 格式化

- **SwiftFormat** 用于自动格式化，**SwiftLint** 用于风格强制
- `swift-format` 作为替代方案与 Xcode 16+ 捆绑

## 不可变性

- 优先使用 `let` 而非 `var` —— 将所有内容定义为 `let`，仅在编译器要求时才更改为 `var`
- 默认使用带有值语义的 `struct`；仅在需要身份或引用语义时使用 `class`

## 命名

遵循 [Apple API 设计指南](https://www.swift.org/documentation/api-design-guidelines/)：

- 在使用点清晰 —— 省略不必要的词
- 根据角色而非类型命名方法和属性
- 对常量使用 `static let` 而非全局常量

## 错误处理

使用类型化抛出（Swift 6+）和模式匹配：

```swift
func load(id: String) throws(LoadError) -> Item {
    guard let data = try? read(from: path) else {
        throw .fileNotFound(id)
    }
    return try decode(data)
}
```

## 并发

启用 Swift 6 严格并发检查。优先：

- 用于跨隔离边界数据传递的 `Sendable` 值类型
- 用于共享可变状态的 Actor
- 结构化并发（`async let`、`TaskGroup`）而非非结构化 `Task {}`
