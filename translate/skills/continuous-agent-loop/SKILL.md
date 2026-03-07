---
name: continuous-agent-loop
description: 具有质量门、评估和恢复控制的持续自主代理循环模式。
origin: ECC
---

# 持续代理循环

这是v1.8+的规范循环技能名称。它取代了`autonomous-loops`，同时在一个版本内保持兼容性。

## 循环选择流程

```text
开始
  |
  +-- 需要严格的CI/PR控制？ -- 是 --> continuous-pr
  |                                    
  +-- 需要RFC分解？ -- 是 --> rfc-dag
  |
  +-- 需要探索性并行生成？ -- 是 --> infinite
  |
  +-- 默认 --> sequential
```

## 组合模式

推荐的生产堆栈：
1. RFC分解 (`ralphinho-rfc-pipeline`)
2. 质量门 (`plankton-code-quality` + `/quality-gate`)
3. 评估循环 (`eval-harness`)
4. 会话持久化 (`nanoclaw-repl`)

## 故障模式

- 循环 churn 没有可衡量的进展
- 重复重试相同的根本原因
- 合并队列停滞
- 无边界升级导致的成本漂移

## 恢复

- 冻结循环
- 运行 `/harness-audit`
- 将范围缩小到失败单元
- 使用明确的验收标准重放