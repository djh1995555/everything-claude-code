---
name: swift-actor-persistence
description: 在 Swift 中使用 actors 实现线程安全的数据持久化 — 带有文件支持存储的内存缓存，从设计上消除数据竞争。
origin: ECC
---

# 使用 Swift Actors 实现线程安全持久化

使用 Swift actors 构建线程安全数据持久化层的模式。结合内存缓存和文件支持存储，利用 actor 模型在编译时消除数据竞争。

## 何时激活

- 在 Swift 5.5+ 中构建数据持久化层
- 需要对共享可变状态进行线程安全访问
- 希望消除手动同步（锁、DispatchQueues）
- 构建离线优先的本地存储应用

## 核心模式

### 基于 Actor 的存储库

Actor 模型保证序列化访问 — 无数据竞争，由编译器强制执行。

```swift
public actor LocalRepository<T: Codable & Identifiable> where T.ID == String {
    private var cache: [String: T] = [:]
    private let fileURL: URL

    public init(directory: URL = .documentsDirectory, filename: String = "data.json") {
        self.fileURL = directory.appendingPathComponent(filename)
        // 初始化期间同步加载（actor 隔离尚未激活）
        self.cache = Self.loadSynchronously(from: fileURL)
    }

    // MARK: - 公共 API

    public func save(_ item: T) throws {
        cache[item.id] = item
        try persistToFile()
    }

    public func delete(_ id: String) throws {
        cache[id] = nil
        try persistToFile()
    }

    public func find(by id: String) -> T? {
        cache[id]
    }

    public func loadAll() -> [T] {
        Array(cache.values)
    }

    // MARK: - 私有

    private func persistToFile() throws {
        let data = try JSONEncoder().encode(Array(cache.values))
        try data.write(to: fileURL, options: .atomic)
    }

    private static func loadSynchronously(from url: URL) -> [String: T] {
        guard let data = try? Data(contentsOf: url),
              let items = try? JSONDecoder().decode([T].self, from: data) else {
            return [:]
        }
        return Dictionary(uniqueKeysWithValues: items.map { ($0.id, $0) })
    }
}
```

### 使用

由于 actor 隔离，所有调用自动为 async：

```swift
let repository = LocalRepository<Question>()

// 读取 — 从内存缓存快速 O(1) 查找
let question = await repository.find(by: "q-001")
let allQuestions = await repository.loadAll()

// 写入 — 更新缓存并原子性持久化到文件
try await repository.save(newQuestion)
try await repository.delete("q-001")
```

### 与 @Observable ViewModel 结合

```swift
@Observable
final class QuestionListViewModel {
    private(set) var questions: [Question] = []
    private let repository: LocalRepository<Question>

    init(repository: LocalRepository<Question> = LocalRepository()) {
        self.repository = repository
    }

    func load() async {
        questions = await repository.loadAll()
    }

    func add(_ question: Question) async throws {
        try await repository.save(question)
        questions = await repository.loadAll()
    }
}
```

## 关键设计决策

| 决策 | 理由 |
|------|------|
| Actor（而非 class + lock） | 编译器强制执行线程安全，无手动同步 |
| 内存缓存 + 文件持久化 | 从缓存快速读取，写入磁盘持久化 |
| 同步初始化加载 | 避免异步初始化复杂性 |
| 按 ID 键控的字典 | O(1) 标识符查找 |
| 泛型于 `Codable & Identifiable` | 可重用于任何模型类型 |
| 原子文件写入（`.atomic`） | 崩溃时防止部分写入 |

## 最佳实践

- **使用 `Sendable` 类型** 用于跨 actor 边界的所有数据
- **保持 actor 的公共 API 最小化** — 仅暴露领域操作，而非持久化细节
- **使用 `.atomic` 写入** 以防止应用崩溃时数据损坏
- **在 `init` 中同步加载** — 异步初始化增加复杂性，对本地文件益处极小
- **与 `@Observable` 结合** ViewModels 用于响应式 UI 更新

## 避免的反模式

- 对新 Swift 并发代码使用 `DispatchQueue` 或 `NSLock` 而非 actors
- 向外部调用者暴露内部缓存字典
- 无验证地配置文件 URL
- 忘记所有 actor 方法调用都是 `await` — 调用者必须处理异步上下文
- 使用 `nonisolated` 绕过 actor 隔离（违背初衷）

## 何时使用

- iOS/macOS 应用中的本地数据存储（用户数据、设置、缓存内容）
- 稍后同步到服务器的离线优先架构
- 应用多个部分并发访问的任何共享可变状态
- 使用现代 Swift 并发替换传统 `DispatchQueue` 线程安全