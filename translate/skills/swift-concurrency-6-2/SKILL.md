---
name: swift-concurrency-6-2
description: Swift 6.2 可接近并发 — 默认单线程，@concurrent 用于显式后台卸载，隔离一致性用于主 actor 类型。
---

# Swift 6.2 可接近并发

采用 Swift 6.2 并发模型的模式，其中代码默认单线程运行，并发显式引入。在不牺牲性能的情况下消除常见数据竞争错误。

## 何时激活

- 将 Swift 5.x 或 6.0/6.1 项目迁移到 Swift 6.2
- 解决数据竞争安全编译器错误
- 设计基于 MainActor 的应用架构
- 将 CPU 密集型工作卸载到后台线程
- 在 MainActor 隔离类型上实现协议一致性
- 在 Xcode 26 中启用可接近并发构建设置

## 核心问题：隐式后台卸载

在 Swift 6.1 及更早版本中，async 函数可能被隐式卸载到后台线程，即使在看似安全的代码中也会导致数据竞争错误：

```swift
// Swift 6.1：错误
@MainActor
final class StickerModel {
    let photoProcessor = PhotoProcessor()

    func extractSticker(_ item: PhotosPickerItem) async throws -> Sticker? {
        guard let data = try await item.loadTransferable(type: Data.self) else { return nil }

        // 错误：发送 'self.photoProcessor' 可能导致数据竞争
        return await photoProcessor.extractSticker(data: data, with: item.itemIdentifier)
    }
}
```

Swift 6.2 修复了此问题：async 函数默认保持在调用 actor 上。

```swift
// Swift 6.2：正常 — async 保持在 MainActor，无数据竞争
@MainActor
final class StickerModel {
    let photoProcessor = PhotoProcessor()

    func extractSticker(_ item: PhotosPickerItem) async throws -> Sticker? {
        guard let data = try await item.loadTransferable(type: Data.self) else { return nil }
        return await photoProcessor.extractSticker(data: data, with: item.itemIdentifier)
    }
}
```

## 核心模式 — 隔离一致性

MainActor 类型现在可以安全地符合非隔离协议：

```swift
protocol Exportable {
    func export()
}

// Swift 6.1：错误 — 进入主 actor 隔离代码
// Swift 6.2：使用隔离一致性正常
extension StickerModel: @MainActor Exportable {
    func export() {
        photoProcessor.exportAsPNG()
    }
}
```

编译器确保一致性仅在主 actor 上使用：

```swift
// 正常 — ImageExporter 也是 @MainActor
@MainActor
struct ImageExporter {
    var items: [any Exportable]

    mutating func add(_ item: StickerModel) {
        items.append(item)  // 安全：相同 actor 隔离
    }
}

// 错误 — 非隔离上下文无法使用 MainActor 一致性
nonisolated struct ImageExporter {
    var items: [any Exportable]

    mutating func add(_ item: StickerModel) {
        items.append(item)  // 错误：此处无法使用主 actor 隔离一致性
    }
}
```

## 核心模式 — 全局和静态变量

使用 MainActor 保护全局/静态状态：

```swift
// Swift 6.1：错误 — 非 Sendable 类型可能有共享可变状态
final class StickerLibrary {
    static let shared: StickerLibrary = .init()  // 错误
}

// 修复：使用 @MainActor 注释
@MainActor
final class StickerLibrary {
    static let shared: StickerLibrary = .init()  // 正常
}
```

### MainActor 默认推断模式

Swift 6.2 引入了一种模式，默认推断 MainActor — 无需手动注释：

```swift
// 启用 MainActor 默认推断后：
final class StickerLibrary {
    static let shared: StickerLibrary = .init()  // 隐式 @MainActor
}

final class StickerModel {
    let photoProcessor: PhotoProcessor
    var selection: [PhotosPickerItem]  // 隐式 @MainActor
}

extension StickerModel: Exportable {  // 隐式 @MainActor 一致性
    func export() {
        photoProcessor.exportAsPNG()
    }
}
```

此模式为可选，推荐用于应用、脚本和其他可执行目标。

## 核心模式 — @concurrent 用于后台工作

当您需要实际并行时，使用 `@concurrent` 显式卸载：

> **重要提示：** 此示例需要可接近并发构建设置 — SE-0466（MainActor 默认隔离）和 SE-0461（默认非隔离非发送）。启用这些后，`extractSticker` 保持在调用者的 actor 上，使可变状态访问安全。**没有这些设置，此代码存在数据竞争** — 编译器将标记它。

```swift
nonisolated final class PhotoProcessor {
    private var cachedStickers: [String: Sticker] = [:]

    func extractSticker(data: Data, with id: String) async -> Sticker {
        if let sticker = cachedStickers[id] {
            return sticker
        }

        let sticker = await Self.extractSubject(from: data)
        cachedStickers[id] = sticker
        return sticker
    }

    // 将昂贵的工作卸载到并发线程池
    @concurrent
    static func extractSubject(from data: Data) async -> Sticker { /* ... */ }
}

// 调用者必须 await
let processor = PhotoProcessor()
processedPhotos[item.id] = await processor.extractSticker(data: data, with: item.id)
```

要使用 `@concurrent`：
1. 将包含类型标记为 `nonisolated`
2. 向函数添加 `@concurrent`
3. 如果尚未异步，添加 `async`
4. 在调用点添加 `await`

## 关键设计决策

| 决策 | 理由 |
|------|------|
| 默认单线程 | 最自然的代码无数据竞争；并发是可选的 |
| Async 保持在调用 actor | 消除导致数据竞争错误的隐式卸载 |
| 隔离一致性 | MainActor 类型可以符合协议而无需不安全的解决方法 |
| `@concurrent` 显式可选 | 后台执行是深思熟虑的性能选择，而非意外 |
| MainActor 默认推断 | 减少应用目标的样板 `@MainActor` 注释 |
| 可选采用 | 非破坏性迁移路径 — 逐步启用功能 |

## 迁移步骤

1. **在 Xcode 中启用**：构建设置中的 Swift 编译器 > 并发部分
2. **在 SPM 中启用**：在包清单中使用 `SwiftSettings` API
3. **使用迁移工具**：通过 swift.org/migration 自动代码更改
4. **从 MainActor 默认开始**：为应用目标启用推断模式
5. **在需要的地方添加 `@concurrent`**：先分析，然后卸载热点路径
6. **彻底测试**：数据竞争问题成为编译时错误

## 最佳实践

- **从 MainActor 开始** — 先编写单线程代码，稍后优化
- **仅对 CPU 密集型工作使用 `@concurrent`** — 图像处理、压缩、复杂计算
- **为主要单线程的应用目标启用 MainActor 推断模式**
- **卸载前分析** — 使用 Instruments 查找实际瓶颈
- **使用 MainActor 保护全局** — 全局/静态可变状态需要 actor 隔离
- **使用隔离一致性** 而非 `nonisolated` 解决方法或 `@Sendable` 包装器
- **逐步迁移** — 在构建设置中一次启用一个功能

## 避免的反模式

- 对每个 async 函数应用 `@concurrent`（大多数不需要后台执行）
- 使用 `nonisolated` 抑制编译器错误而不理解隔离
- 当 actors 提供相同安全性时保留传统 `DispatchQueue` 模式
- 在并发相关的 Foundation Models 代码中跳过 `model.availability` 检查
- 与编译器对抗 — 如果它报告数据竞争，代码存在真正的并发问题
- 假设所有 async 代码在后台运行（Swift 6.2 默认：保持在调用 actor）

## 何时使用

- 所有新 Swift 6.2+ 项目（可接近并发是推荐的默认）
- 将现有应用从 Swift 5.x 或 6.0/6.1 并发迁移
- 在 Xcode 26 采用期间解决数据竞争安全编译器错误
- 构建以 MainActor 为中心的应用架构（大多数 UI 应用）
- 性能优化 — 将特定繁重计算卸载到后台