---
paths:
  - "**/*.swift"
  - "**/Package.swift"
---
# Swift 模式

> 此文件扩展 [common/patterns.md](../common/patterns.md) 添加 Swift 特定内容。

## 面向协议的设计

定义小而专注的协议。使用协议扩展共享默认值：

```swift
protocol Repository: Sendable {
    associatedtype Item: Identifiable & Sendable
    func find(by id: Item.ID) async throws -> Item?
    func save(_ item: Item) async throws
}
```

## 值类型

- 对数据传输对象和模型使用结构体
- 使用带有关联值的枚举建模不同状态：

```swift
enum LoadState<T: Sendable>: Sendable {
    case idle
    case loading
    case loaded(T)
    case failed(Error)
}
```

## Actor 模式

使用 actor 处理共享可变状态，而非锁或调度队列：

```swift
actor Cache<Key: Hashable & Sendable, Value: Sendable> {
    private var storage: [Key: Value] = [:]

    func get(_ key: Key) -> Value? { storage[key] }
    func set(_ key: Key, value: Value) { storage[key] = value }
}
```

## 依赖注入

使用默认参数注入协议 —— 生产使用默认值，测试注入 mock：

```swift
struct UserService {
    private let repository: any UserRepository

    init(repository: any UserRepository = DefaultUserRepository()) {
        self.repository = repository
    }
}
```

## 参考

参见技能：`swift-actor-persistence` 获取基于 actor 的持久化模式。
参见技能：`swift-protocol-di-testing` 获取基于协议的 DI 和测试。
