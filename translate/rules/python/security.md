---
paths:
  - "**/*.py"
  - "**/*.pyi"
---
# Python 安全

> 此文件扩展 [common/security.md](../common/security.md) 添加 Python 特定内容。

## 密钥管理

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["OPENAI_API_KEY"]  # 如果缺失则引发 KeyError
```

## 安全扫描

- 使用 **bandit** 进行静态安全分析：
  ```bash
  bandit -r src/
  ```

## 参考

参见技能：`django-security` 获取 Django 特定安全指南（如果适用）。
