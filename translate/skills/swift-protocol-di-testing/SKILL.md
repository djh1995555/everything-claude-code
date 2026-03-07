---
name: swift-protocol-di-testing
description: 基于协议的依赖注入，用于可测试 Swift 代码 — 使用聚焦协议和 Swift Testing 模拟文件系统、网络和外部 API。
origin: ECC
---

# 用于测试的 Swift 基于协议依赖注入

通过将外部依赖（文件系统、网络、iCloud）抽象到小型、聚焦协议后使 Swift 代码可测试的模式。无需 I/O 即可实现确定性测试。

## 何时激活

- 编写访问文件系统、网络或外部 API 的 Swift 代码
- 需要测试错误处理路径而不触发实际失败
- 构建跨环境（应用、测试、SwiftUI 预览）工作的模块
- 使用 Swift 并发（actors、Sendable）设计可测试架构

## 核心模式

### 1. 定义小型、聚焦协议

每个协议恰好处理一个外部关注点。

```swift
// 文件系统访问
public protocol FileSystemProviding: Sendable {
    func containerURL(for purpose: Purpose) -> URL?
}

// 文件读/写操作
public protocol FileAccessorProviding: Sendable {
    func read(from url: URL) throws -> Data
    func write(_ data: Data, to url: URL) throws
    func fileExists(at url: URL) -> Bool
}

// 书签存储（例如，用于沙盒应用）
public protocol BookmarkStorageProviding: Sendable {
    func saveBookmark(_ data: Data, for key: String) throws
    func loadBookmark(for key: String) throws -> Data?
}
```

### 2. 创建默认（生产）实现

```swift
public struct DefaultFileSystemProvider: FileSystemProviding {
    public init() {}

    public func containerURL(for purpose: Purpose) -> URL? {
        FileManager.default.url(forUbiquityContainerIdentifier: nil)
    }
}

public struct DefaultFileAccessor: FileAccessorProviding {
    public init() {}

    public func read(from url: URL) throws -> Data {
        try Data(contentsOf: url)
    }

    public func write(_ data: Data, to url: URL) throws {
        try data.write(to: url, options: .atomic)
    }

    public func fileExists(at url: URL) -> Bool {
        FileManager.default.fileExists(atPath: url.path)
    }
}
```

### 3. 为测试创建模拟实现

```swift
public final class MockFileAccessor: FileAccessorProviding, @unchecked Sendable {
    public var files: [URL: Data] = [:]
    public var readError: Error?
    public var writeError: Error?

    public init() {}

    public func read(from url: URL) throws -> Data {
        if let error = readError { throw error }
        guard let data = files[url] else {
            throw CocoaError(.fileReadNoSuchFile)
        }
        return data
    }

    public func write(_ data: Data, to url: URL) throws {
        if let error = writeError { throw error }
        files[url] = data
    }

    public func fileExists(at url: URL) -> Bool {
        files[url] != nil
    }
}
```

### 4. 使用默认参数注入依赖

生产代码使用默认值；测试注入模拟。

```swift
public actor SyncManager {
    private let fileSystem: FileSystemProviding
    private let fileAccessor: FileAccessorProviding

    public init(
        fileSystem: FileSystemProviding = DefaultFileSystemProvider(),
        fileAccessor: FileAccessorProviding = DefaultFileAccessor()
    ) {
        self.fileSystem = fileSystem
        self.fileAccessor = fileAccessor
    }

    public func sync() async throws {
        guard let containerURL = fileSystem.containerURL(for: .sync) else {
            throw SyncError.containerNotAvailable
        }
        let data = try fileAccessor.read(
            from: containerURL.appendingPathComponent("data.json")
        )
        // 处理数据...
    }
}
```

### 5. 使用 Swift Testing 编写测试

```swift
import Testing

@Test("同步管理器处理缺失容器")
func testMissingContainer() async {
    let mockFileSystem = MockFileSystemProvider(containerURL: nil)
    let manager = SyncManager(fileSystem: mockFileSystem)

    await #expect(throws: SyncError.containerNotAvailable) {
        try await manager.sync()
    }
}

@Test("同步管理器正确读取数据")
func testReadData() async throws {
    let mockFileAccessor = MockFileAccessor()
    mockFileAccessor.files[testURL] = testData

    let manager = SyncManager(fileAccessor: mockFileAccessor)
    let result = try await manager.loadData()

    #expect(result == expectedData)
}

@Test("同步管理器优雅处理读取错误")
func testReadError() async {
    let mockFileAccessor = MockFileAccessor()
    mockFileAccessor.readError = CocoaError(.fileReadCorruptFile)

    let manager = SyncManager(fileAccessor: mockFileAccessor)

    await #expect(throws: SyncError.self) {
        try await manager.sync()
    }
}
```

## 最佳实践

- **单一职责**：每个协议应处理一个关注点 — 不要创建包含许多方法的"上帝协议"
- **Sendable 一致性**：跨 actor 边界使用协议时必需
- **默认参数**：让生产代码默认使用真实实现；只有测试需要指定模拟
- **错误模拟**：使用可配置错误属性设计模拟以测试失败路径
- **仅模拟边界**：模拟外部依赖（文件系统、网络、API），而非内部类型

## 避免的反模式

- 创建涵盖所有外部访问的单个大型协议
- 模拟无外部依赖的内部类型
- 使用 `#if DEBUG` 条件而非适当的依赖注入
- 与 actors 一起使用时忘记 `Sendable` 一致性
- 过度设计：如果类型无外部依赖，它不需要协议

## 何时使用

- 任何接触文件系统、网络或外部 API 的 Swift 代码
- 测试在真实环境中难以触发的错误处理路径
- 构建需要在应用、测试和 SwiftUI 预览上下文中工作的模块
- 使用 Swift 并发（actors、结构化并发）且需要可测试架构的应用