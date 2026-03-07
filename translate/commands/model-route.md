# 模型路由命令

根据任务复杂度和预算推荐最佳模型层级。

## 用法

`/model-route [task-description] [--budget low|med|high]`

## 路由启发式规则

- `haiku`：确定性、低风险的机械性更改
- `sonnet`：实现和重构的默认值
- `opus`：架构、深度审查、模糊需求

## 必需输出

- 推荐的模型
- 置信度水平
- 为什么这个模型适合
- 如果首次尝试失败，提供备用模型

## 参数

$ARGUMENTS:
- `[task-description]` 可选自由文本
- `--budget low|med|high` 可选
