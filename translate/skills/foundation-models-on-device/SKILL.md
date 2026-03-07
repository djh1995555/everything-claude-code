---
name: foundation-models-on-device
description: Apple FoundationModels框架用于设备上LLM —— iOS 26+中的文本生成、使用@Generable的引导生成、工具调用和快照流。
---

# FoundationModels: 设备上LLM（iOS 26）

使用FoundationModels框架将Apple的设备上语言模型集成到应用程序中的模式。涵盖文本生成、使用`@Generable`的结构化输出、自定义工具调用和快照流 —— 所有操作都在设备上运行，以保护隐私和支持离线使用。

## 激活时机

- 使用Apple Intelligence设备上功能构建AI驱动的功能
- 无需云依赖即可生成或总结文本
- 从自然语言输入中提取结构化数据
- 为特定领域的AI操作实现自定义工具调用
- 流式传输结构化响应以进行实时UI更新
- 需要保护隐私的AI（数据不会离开设备）

## 核心模式 —— 可用性检查

在创建会话之前始终检查模型可用性：

```swift
struct GenerativeView: View {
    private var model = SystemLanguageModel.default

    var body: some View {
        switch model.availability {
        case .available:
            ContentView()
        case .unavailable(.deviceNotEligible):
            Text("设备不符合Apple Intelligence要求")
        case .unavailable(.appleIntelligenceNotEnabled):
            Text("请在设置中启用Apple Intelligence")
        case .unavailable(.modelNotReady):
            Text("模型正在下载或未准备好")
        case .unavailable(let other):
            Text("模型不可用：\(other)")
        }
    }
}
```

## 核心模式 —— 基本会话

```swift
// 单轮：每次创建新会话
let session = LanguageModelSession()
let response = try await session.respond(to: "What's a good month to visit Paris?")
print(response.content)

// 多轮：重用会话以保持对话上下文
let session = LanguageModelSession(instructions: """
    You are a cooking assistant.
    Provide recipe suggestions based on ingredients.
    Keep suggestions brief and practical.
    """)

let first = try await session.respond(to: "I have chicken and rice")
let followUp = try await session.respond(to: "What about a vegetarian option?")
```

指令的关键点：
- 定义模型的角色（"You are a mentor"）
- 指定要做什么（"Help extract calendar events"）
- 设置风格偏好（"Respond as briefly as possible"）
- 添加安全措施（"Respond with 'I can't help with that' for dangerous requests"）

## 核心模式 —— 使用@Generable的引导生成

生成结构化Swift类型而不是原始字符串：

### 1. 定义可生成类型

```swift
@Generable(description: "Basic profile information about a cat")
struct CatProfile {
    var name: String

    @Guide(description: "The age of the cat", .range(0...20))
    var age: Int

    @Guide(description: "A one sentence profile about the cat's personality")
    var profile: String
}
```

### 2. 请求结构化输出

```swift
let response = try await session.respond(
    to: "Generate a cute rescue cat",
    generating: CatProfile.self
)

// 直接访问结构化字段
print("Name: \(response.content.name)")
print("Age: \(response.content.age)")
print("Profile: \(response.content.profile)")
```

### 支持的@Guide约束

- `.range(0...20)` —— 数值范围
- `.count(3)` —— 数组元素计数
- `description:` —— 生成的语义指导

## 核心模式 —— 工具调用

让模型调用自定义代码以执行特定领域的任务：

### 1. 定义工具

```swift
struct RecipeSearchTool: Tool {
    let name = "recipe_search"
    let description = "Search for recipes matching a given term and return a list of results."

    @Generable
    struct Arguments {
        var searchTerm: String
        var numberOfResults: Int
    }

    func call(arguments: Arguments) async throws -> ToolOutput {
        let recipes = await searchRecipes(
            term: arguments.searchTerm,
            limit: arguments.numberOfResults
        )
        return .string(recipes.map { "- \($0.name): \($0.description)" }.joined(separator: "\n"))
    }
}
```

### 2. 使用工具创建会话

```swift
let session = LanguageModelSession(tools: [RecipeSearchTool()])
let response = try await session.respond(to: "Find me some pasta recipes")
```

### 3. 处理工具错误

```swift
do {
    let answer = try await session.respond(to: "Find a recipe for tomato soup.")
} catch let error as LanguageModelSession.ToolCallError {
    print(error.tool.name)
    if case .databaseIsEmpty = error.underlyingError as? RecipeSearchToolError {
        // 处理特定工具错误
    }
}
```

## 核心模式 —— 快照流

使用`PartiallyGenerated`类型流式传输结构化响应以进行实时UI更新：

```swift
@Generable
struct TripIdeas {
    @Guide(description: "Ideas for upcoming trips")
    var ideas: [String]
}

let stream = session.streamResponse(
    to: "What are some exciting trip ideas?",
    generating: TripIdeas.self
)

for try await partial in stream {
    // partial: TripIdeas.PartiallyGenerated (所有属性都是Optional)
    print(partial)
}
```

### SwiftUI集成

```swift
@State private var partialResult: TripIdeas.PartiallyGenerated?
@State private var errorMessage: String?

var body: some View {
    List {
        ForEach(partialResult?.ideas ?? [], id: \.self) { idea in
            Text(idea)
        }
    }
    .overlay {
        if let errorMessage { Text(errorMessage).foregroundStyle(.red) }
    }
    .task {
        do {
            let stream = session.streamResponse(to: prompt, generating: TripIdeas.self)
            for try await partial in stream {
                partialResult = partial
            }
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
```