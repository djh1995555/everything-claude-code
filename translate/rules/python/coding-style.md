---
paths:
  - "**/*.py"
  - "**/*.pyi"
---
# Python 编码风格

> 此文件扩展 [common/coding-style.md](../common/coding-style.md) 添加 Python 特定内容。

## 标准

- 遵循 **PEP 8** 约定
- 在所有函数签名上使用**类型注解**

## 不可变性

优先使用不可变数据结构：

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    email: str

from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
```

## 格式化

- **black** 用于代码格式化
- **isort** 用于导入排序
- **ruff** 用于 linting

## 参考

参见技能：`python-patterns` 获取全面的 Python 习语和模式。
