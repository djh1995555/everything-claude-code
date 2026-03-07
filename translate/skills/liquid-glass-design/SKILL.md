---
name: liquid-glass-design
description: iOS 26 Liquid Glass 设计系统 — 具有模糊、反射和交互式变形功能的动态玻璃材质，适用于 SwiftUI、UIKit 和 WidgetKit。
---

# Liquid Glass 设计系统（iOS 26）

实现 Apple Liquid Glass 的模式 — 一种动态材质，可模糊其后方的内容，反射周围内容的颜色和光线，并对触摸和指针交互做出反应。涵盖 SwiftUI、UIKit 和 WidgetKit 集成。

## 何时激活

- 为 iOS 26+ 构建或更新应用，采用新设计语言
- 实现玻璃风格的按钮、卡片、工具栏或容器
- 创建玻璃元素之间的变形过渡
- 为小部件应用 Liquid Glass 效果
- 将现有的模糊/材质效果迁移到新的 Liquid Glass API

## 核心模式 — SwiftUI

### 基本玻璃效果

为任何视图添加 Liquid Glass 的最简单方法：

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect()  // 默认：常规变体，胶囊形状
```

### 自定义形状和色调

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(.regular.tint(.orange).interactive(), in: .rect(cornerRadius: 16.0))
```

关键自定义选项：
- `.regular` — 标准玻璃效果
- `.tint(Color)` — 添加颜色色调以突出显示
- `.interactive()` — 响应触摸和指针交互
- 形状：`.capsule`（默认）、`.rect(cornerRadius:)`、`.circle`

### 玻璃按钮样式

```swift
Button("Click Me") { /* 动作 */ }
    .buttonStyle(.glass)

Button("Important") { /* 动作 */ }
    .buttonStyle(.glassProminent)
```

### 用于多个元素的 GlassEffectContainer

始终将多个玻璃视图包装在容器中，以提高性能和启用变形：

```swift
GlassEffectContainer(spacing: 40.0) {
    HStack(spacing: 40.0) {
        Image(systemName: "scribble.variable")
            .frame(width: 80.0, height: 80.0)
            .font(.system(size: 36))
            .glassEffect()

        Image(systemName: "eraser.fill")
            .frame(width: 80.0, height: 80.0)
            .font(.system(size: 36))
            .glassEffect()
    }
}
```

`spacing` 参数控制合并距离 — 元素越近，玻璃形状越会融合在一起。

### 合并玻璃效果

使用 `glassEffectUnion` 将多个视图合并为单个玻璃形状：

```swift
@Namespace private var namespace

GlassEffectContainer(spacing: 20.0) {
    HStack(spacing: 20.0) {
        ForEach(symbolSet.indices, id: \.self) { item in
            Image(systemName: symbolSet[item])
                .frame(width: 80.0, height: 80.0)
                .glassEffect()
                .glassEffectUnion(id: item < 2 ? "group1" : "group2", namespace: namespace)
        }
    }
}
```

### 变形过渡

在玻璃元素出现/消失时创建平滑变形：

```swift
@State private var isExpanded = false
@Namespace private var namespace

GlassEffectContainer(spacing: 40.0) {
    HStack(spacing: 40.0) {
        Image(systemName: "scribble.variable")
            .frame(width: 80.0, height: 80.0)
            .glassEffect()
            .glassEffectID("pencil", in: namespace)

        if isExpanded {
            Image(systemName: "eraser.fill")
                .frame(width: 80.0, height: 80.0)
                .glassEffect()
                .glassEffectID("eraser", in: namespace)
        }
    }
}

Button("Toggle") {
    withAnimation { isExpanded.toggle() }
}
.buttonStyle(.glass)
```

### 扩展水平滚动到侧边栏下方

要允许水平滚动内容延伸到侧边栏或检查器下方，请确保 `ScrollView` 内容到达容器的前导/尾随边缘。当布局延伸到边缘时，系统会自动处理侧边栏下方的滚动行为 — 不需要额外的修饰符。

## 核心模式 — UIKit

### 基本 UIGlassEffect

```swift
let glassEffect = UIGlassEffect()
glassEffect.tintColor = UIColor.systemBlue.withAlphaComponent(0.3)
glassEffect.isInteractive = true

let visualEffectView = UIVisualEffectView(effect: glassEffect)
visualEffectView.translatesAutoresizingMaskIntoConstraints = false
visualEffectView.layer.cornerRadius = 20
visualEffectView.clipsToBounds = true

view.addSubview(visualEffectView)
NSLayoutConstraint.activate([
    visualEffectView.centerXAnchor.constraint(equalTo: view.centerXAnchor),
    visualEffectView.centerYAnchor.constraint(equalTo: view.centerYAnchor),
    visualEffectView.widthAnchor.constraint(equalToConstant: 200),
    visualEffectView.heightAnchor.constraint(equalToConstant: 120)
])

// 向 contentView 添加内容
let label = UILabel()
label.text = "Liquid Glass"
label.translatesAutoresizingMaskIntoConstraints = false
visualEffectView.contentView.addSubview(label)
NSLayoutConstraint.activate([
    label.centerXAnchor.constraint(equalTo: visualEffectView.contentView.centerXAnchor),
    label.centerYAnchor.constraint(equalTo: visualEffectView.contentView.centerYAnchor)
])
```

### 用于多个元素的 UIGlassContainerEffect

```swift
let containerEffect = UIGlassContainerEffect()
containerEffect.spacing = 40.0

let containerView = UIVisualEffectView(effect: containerEffect)

let firstGlass = UIVisualEffectView(effect: UIGlassEffect())
let secondGlass = UIVisualEffectView(effect: UIGlassEffect())

containerView.contentView.addSubview(firstGlass)
containerView.contentView.addSubview(secondGlass)
```

### 滚动边缘效果

```swift
scrollView.topEdgeEffect.style = .automatic
scrollView.bottomEdgeEffect.style = .hard
scrollView.leftEdgeEffect.isHidden = true
```

### 工具栏玻璃集成

```swift
let favoriteButton = UIBarButtonItem(image: UIImage(systemName: "heart"), style: .plain, target: self, action: #selector(favoriteAction))
favoriteButton.hidesSharedBackground = true  // 选择退出共享玻璃背景
```

## 核心模式 — WidgetKit

### 渲染模式检测

```swift
struct MyWidgetView: View {
    @Environment(\.widgetRenderingMode) var renderingMode

    var body: some View {
        if renderingMode == .accented {
            // 色调模式：白色色调、主题玻璃背景
        } else {
            // 全彩色模式：标准外观
        }
    }
}
```

### 用于视觉层次结构的强调组

```swift
HStack {
    VStack(alignment: .leading) {
        Text("Title")
            .widgetAccentable()  // 强调组
        Text("Subtitle")
            // 主要组（默认）
    }
    Image(systemName: "star.fill")
        .widgetAccentable()  // 强调组
}
```

### 强调模式下的图像渲染

```swift
Image("myImage")
    .widgetAccentedRenderingMode(.monochrome)
```

### 容器背景

```swift
VStack { /* 内容 */ }
    .containerBackground(for: .widget) {
        Color.blue.opacity(0.2)
    }
```

## 关键设计决策

| 决策 | 理由 |
|----------|-----------|
| GlassEffectContainer 包装 | 性能优化，启用玻璃元素之间的变形 |
| `spacing` 参数 | 控制合并距离 — 微调元素必须多近才能融合 |
| `@Namespace` + `glassEffectID` | 在视图层次结构变化时启用平滑变形过渡 |
| `interactive()` 修饰符 | 显式选择加入触摸/指针反应 — 并非所有玻璃都应响应 |
| UIKit 中的 UIGlassContainerEffect | 与 SwiftUI 相同的容器模式以保持一致性 |
| 小部件中的强调渲染模式 | 当用户选择色调主屏幕时，系统应用色调玻璃 |

## 最佳实践

- **始终使用 GlassEffectContainer** 当对多个兄弟视图应用玻璃效果时 — 它启用变形并提高渲染性能
- **在其他外观修饰符之后应用 `.glassEffect()`**（frame、font、padding）
- **仅在响应用户交互的元素上使用 `.interactive()`**（按钮、可切换项目）
- **仔细选择容器中的间距** 以控制玻璃效果何时合并
- **在更改视图层次结构时使用 `withAnimation`** 以启用平滑变形过渡
- **在各种外观下测试** — 浅色模式、深色模式和强调/色调模式
- **确保可访问性对比度** — 玻璃上的文本必须保持可读

## 应避免的反模式

- 在没有 GlassEffectContainer 的情况下使用多个独立的 `.glassEffect()` 视图
- 嵌套过多玻璃效果 — 降低性能和视觉清晰度
- 为每个视图应用玻璃效果 — 保留用于交互式元素、工具栏和卡片
- 在 UIKit 中使用圆角半径时忘记 `clipsToBounds = true`
- 在小部件中忽略强调渲染模式 — 破坏色调主屏幕外观
- 在玻璃后面使用不透明背景 — 破坏半透明效果

## 使用场景

- 采用新 iOS 26 设计的导航栏、工具栏和标签栏
- 浮动操作按钮和卡片式容器
- 需要视觉深度和触摸反馈的交互式控件
- 应与系统 Liquid Glass 外观集成的小部件
- 相关 UI 状态之间的变形过渡