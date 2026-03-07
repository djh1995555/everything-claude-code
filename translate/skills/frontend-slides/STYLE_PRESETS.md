# 样式预设参考

为`frontend-slides`精心策划的视觉样式。

使用此文件获取：
- 强制适配视口的CSS基础
- 预设选择和情绪映射
- CSS注意事项和验证规则

仅使用抽象形状。除非用户明确要求，否则避免使用插图。

## 视口适配是强制性的

每张幻灯片必须完全适配单个视口。

### 黄金法则

```text
每张幻灯片 = 恰好一个视口高度。
内容过多 = 拆分为更多幻灯片。
绝不允许幻灯片内部滚动。
```

### 密度限制

| 幻灯片类型 | 最大内容 |
|------------|-----------------|
| 标题幻灯片 | 1个标题 + 1个副标题 + 可选标语 |
| 内容幻灯片 | 1个标题 + 4-6个项目符号或2个段落 |
| 功能网格 | 最多6个卡片 |
| 代码幻灯片 | 最多8-10行 |
| 引用幻灯片 | 1个引用 + 出处 |
| 图像幻灯片 | 1个图像，理想情况下高度不超过60vh |

## 强制基础CSS

将此块复制到每个生成的演示文稿中，然后在其基础上设置主题。

```css
/* ===========================================
   VIEWPORT FITTING: MANDATORY BASE STYLES
   =========================================== */

html, body {
    height: 100%;
    overflow-x: hidden;
}

html {
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}

.slide {
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    position: relative;
}

.slide-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-height: 100%;
    overflow: hidden;
    padding: var(--slide-padding);
}

:root {
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --h3-size: clamp(1rem, 2.5vw, 1.75rem);
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.65rem, 1vw, 0.875rem);

    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
    --element-gap: clamp(0.25rem, 1vw, 1rem);
}

.card, .container, .content-box {
    max-width: min(90vw, 1000px);
    max-height: min(80vh, 700px);
}

.feature-list, .bullet-list {
    gap: clamp(0.4rem, 1vh, 1rem);
}

.feature-list li, .bullet-list li {
    font-size: var(--body-size);
    line-height: 1.4;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: clamp(0.5rem, 1.5vw, 1rem);
}

img, .image-container {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
}

@media (max-height: 700px) {
    :root {
        --slide-padding: clamp(0.75rem, 3vw, 2rem);
        --content-gap: clamp(0.4rem, 1.5vw, 1rem);
        --title-size: clamp(1.25rem, 4.5vw, 2.5rem);
        --h2-size: clamp(1rem, 3vw, 1.75rem);
    }
}

@media (max-height: 600px) {
    :root {
        --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem);
        --content-gap: clamp(0.3rem, 1vw, 0.75rem);
        --title-size: clamp(1.1rem, 4vw, 2rem);
        --body-size: clamp(0.7rem, 1.2vw, 0.95rem);
    }

    .nav-dots, .keyboard-hint, .decorative {
        display: none;
    }
}

@media (max-height: 500px) {
    :root {
        --slide-padding: clamp(0.4rem, 2vw, 1rem);
        --title-size: clamp(1rem, 3.5vw, 1.5rem);
        --h2-size: clamp(0.9rem, 2.5vw, 1.25rem);
        --body-size: clamp(0.65rem, 1vw, 0.85rem);
    }
}

@media (max-width: 600px) {
    :root {
        --title-size: clamp(1.25rem, 7vw, 2.5rem);
    }

    .grid {
        grid-template-columns: 1fr;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }

    html {
        scroll-behavior: auto;
    }
}
```

## 视口检查清单

- 每个`.slide`都有`height: 100vh`、`height: 100dvh`和`overflow: hidden`
- 所有排版使用`clamp()`
- 所有间距使用`clamp()`或视口单位
- 图像有`max-height`约束
- 网格使用`auto-fit` + `minmax()`自适应
- 短高度断点存在于`700px`、`600px`和`500px`
- 如果任何内容感觉拥挤，拆分幻灯片

## 情绪到预设映射

| 情绪 | 推荐预设 |
|------|--------------|
| 印象深刻 / 自信 | Bold Signal, Electric Studio, Dark Botanical |
| 兴奋 / 充满活力 | Creative Voltage, Neon Cyber, Split Pastel |
| 平静 / 专注 | Notebook Tabs, Paper & Ink, Swiss Modern |
| 启发 / 感动 | Dark Botanical, Vintage Editorial, Pastel Geometry |

## 预设目录

### 1. Bold Signal

- 氛围：自信、高冲击力、适合主题演讲
- 最佳用途：推销文稿、发布会、声明
- 字体：Archivo Black + Space Grotesk
- 调色板：炭灰色背景、热橙色焦点卡片、纯白色文本
- 特色：超大章节编号、深色背景上的高对比度卡片

### 2. Electric Studio

- 氛围：干净、大胆、代理级抛光
- 最佳用途：客户演示、战略回顾
- 字体：仅使用Manrope
- 调色板：黑色、白色、饱和钴蓝色强调色