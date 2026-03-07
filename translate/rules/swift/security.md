---
paths:
  - "**/*.swift"
  - "**/Package.swift"
---
# Swift 安全

> 此文件扩展 [common/security.md](../common/security.md) 添加 Swift 特定内容。

## 密钥管理

- 对敏感数据（令牌、密码、密钥）使用 **Keychain Services** —— 绝不使用 `UserDefaults`
- 对构建时密钥使用环境变量或 `.xcconfig` 文件
- 绝不在源代码中硬编码密钥 —— 反编译工具可以轻易提取它们

```swift
let apiKey = ProcessInfo.processInfo.environment["API_KEY"]
guard let apiKey, !apiKey.isEmpty else {
    fatalError("API_KEY not configured")
}
```

## 传输安全

- 默认强制执行 App Transport Security (ATS) —— 不要禁用它
- 对关键端点使用证书固定
- 验证所有服务器证书

## 输入验证

- 在显示前清理所有用户输入以防止注入
- 使用带验证的 `URL(string:)` 而非强制解包
- 在处理前验证来自外部来源（API、深度链接、剪贴板）的数据
