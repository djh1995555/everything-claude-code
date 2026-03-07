---
name: regex-vs-llm-structured-text
description: 解析结构化文本时在正则表达式和 LLM 之间选择的决策框架——从正则表达式开始，仅在低置信度边缘情况下使用 LLM。
origin: ECC
---

# 结构化文本解析的正则表达式 vs LLM

解析结构化文本（测验、表单、发票、文档）的实用决策框架。关键见解：正则表达式可以廉价且确定地处理 95-98% 的情况。将昂贵的 LLM 调用保留给剩余的边缘情况。

## 何时激活

- 解析具有重复模式的结构化文本（问题、表单、表格）
- 为文本提取在正则表达式和 LLM 之间做出选择
- 构建结合两种方法的混合管道
- 优化文本处理中的成本/准确性权衡

## 决策框架

```
文本格式是否一致且重复？
├── 是（>90% 遵循模式）→ 从正则表达式开始
│   ├── 正则表达式处理 95%+ → 完成，无需 LLM
│   └── 正则表达式处理 <95% → 仅为边缘情况添加 LLM
└── 否（自由格式、高度可变）→ 直接使用 LLM
```

## 架构模式

```
源文本
    │
    ▼
[正则表达式解析器] ─── 提取结构（95-98% 准确率）
    │
    ▼
[文本清理器] ─── 去除噪声（标记、页码、 artifacts）
    │
    ▼
[置信度评分器] ─── 标记低置信度提取结果
    │
    ├── 高置信度（≥0.95）→ 直接输出
    │
    └── 低置信度（<0.95）→ [LLM 验证器] → 输出
```

## 实现

### 1. 正则表达式解析器（处理大多数情况）

```python
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class ParsedItem:
    id: str
    text: str
    choices: tuple[str, ...]
    answer: str
    confidence: float = 1.0

def parse_structured_text(content: str) -> list[ParsedItem]:
    """使用正则表达式模式解析结构化文本。"""
    pattern = re.compile(
        r"(?P<id>\d+)\.\s*(?P<text>.+?)\n"
        r"(?P<choices>(?:[A-D]\..+?\n)+)"
        r"Answer:\s*(?P<answer>[A-D])",
        re.MULTILINE | re.DOTALL,
    )
    items = []
    for match in pattern.finditer(content):
        choices = tuple(
            c.strip() for c in re.findall(r"[A-D]\.\s*(.+)", match.group("choices"))
        )
        items.append(ParsedItem(
            id=match.group("id"),
            text=match.group("text").strip(),
            choices=choices,
            answer=match.group("answer"),
        ))
    return items
```

### 2. 置信度评分

标记可能需要 LLM 审查的项目：

```python
@dataclass(frozen=True)
class ConfidenceFlag:
    item_id: str
    score: float
    reasons: tuple[str, ...]

def score_confidence(item: ParsedItem) -> ConfidenceFlag:
    """评分提取置信度并标记问题。"""
    reasons = []
    score = 1.0

    if len(item.choices) < 3:
        reasons.append("few_choices")
        score -= 0.3

    if not item.answer:
        reasons.append("missing_answer")
        score -= 0.5

    if len(item.text) < 10:
        reasons.append("short_text")
        score -= 0.2

    return ConfidenceFlag(
        item_id=item.id,
        score=max(0.0, score),
        reasons=tuple(reasons),
    )

def identify_low_confidence(
    items: list[ParsedItem],
    threshold: float = 0.95,
) -> list[ConfidenceFlag]:
    """返回低于置信度阈值的项目。"""
    flags = [score_confidence(item) for item in items]
    return [f for f in flags if f.score < threshold]
```

### 3. LLM 验证器（仅用于边缘情况）

```python
def validate_with_llm(
    item: ParsedItem,
    original_text: str,
    client,
) -> ParsedItem:
    """使用 LLM 修复低置信度提取结果。"""
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # 用于验证的最便宜模型
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": (
                f"从此文本中提取问题、选项和答案。\n\n"
                f"文本：{original_text}\n\n"
                f"当前提取结果：{item}\n\n"
                f"如果需要返回修正后的 JSON，如果准确则返回 'CORRECT'。"
            ),
        }],
    )
    # 解析 LLM 响应并返回修正后的项目...
    return corrected_item
```

### 4. 混合管道

```python
def process_document(
    content: str,
    *,
    llm_client=None,
    confidence_threshold: float = 0.95,
) -> list[ParsedItem]:
    """完整管道：正则表达式 -> 置信度检查 -> LLM 处理边缘情况。"""
    # 步骤 1：正则表达式提取（处理 95-98%）
    items = parse_structured_text(content)

    # 步骤 2：置信度评分
    low_confidence = identify_low_confidence(items, confidence_threshold)

    if not low_confidence or llm_client is None:
        return items

    # 步骤 3：LLM 验证（仅用于标记的项目）
    low_conf_ids = {f.item_id for f in low_confidence}
    result = []
    for item in items:
        if item.id in low_conf_ids:
            result.append(validate_with_llm(item, content, llm_client))
        else:
            result.append(item)

    return result
```

## 实际指标

来自生产测验解析管道（410 个项目）：

| 指标 | 值 |
|--------|-------|
| 正则表达式成功率 | 98.0% |
| 低置信度项目 | 8（2.0%） |
| 需要的 LLM 调用 | ~5 |
| 与全 LLM 相比的成本节省 | ~95% |
| 测试覆盖率 | 93% |

## 最佳实践

- **从正则表达式开始** — 即使不完美的正则表达式也能为你提供改进的基线
- **使用置信度评分** 以编程方式确定哪些需要 LLM 帮助
- **使用最便宜的 LLM** 进行验证（Haiku 级模型足够）
- **永远不要改变** 解析的项目 — 从清理/验证步骤返回新实例
- **TDD 对解析器效果很好** — 先为已知模式编写测试，然后处理边缘情况
- **记录指标**（正则表达式成功率、LLM 调用次数）以跟踪管道健康状况

## 应避免的反模式

- 当正则表达式处理 95%+ 的情况时，将所有文本发送到 LLM（昂贵且缓慢）
- 对自由格式、高度可变的文本使用正则表达式（LLM 更适合）
- 跳过置信度评分，希望正则表达式“正常工作”
- 在清理/验证步骤中改变解析的对象
- 不测试边缘情况（格式错误的输入、缺失字段、编码问题）

## 何时使用

- 测验/考试问题解析
- 表单数据提取
- 发票/收据处理
- 文档结构解析（标题、章节、表格）
- 任何具有重复模式且成本重要的结构化文本