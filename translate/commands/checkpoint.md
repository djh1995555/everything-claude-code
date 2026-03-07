# 检查点命令

在您的工作流中创建或验证检查点。

## 用法

`/checkpoint [create|verify|list] [name]`

## 创建检查点

创建检查点时：

1. 运行 `/verify quick` 以确保当前状态干净
2. 创建 git stash 或使用检查点名称提交
3. 记录检查点到 `.claude/checkpoints.log`：

```bash
echo "$(date +%Y-%m-%d-%H:%M) | $CHECKPOINT_NAME | $(git rev-parse --short HEAD)" >> .claude/checkpoints.log
```

4. 报告检查点已创建

## 验证检查点

针对检查点进行验证时：

1. 从日志读取检查点
2. 将当前状态与检查点比较：
   - 自检查点以来添加的文件
   - 自检查点以来修改的文件
   - 现在与当时的测试通过率
   - 现在与当时的覆盖率

3. 报告：
```
检查点比较：$NAME
============================
文件更改：X
测试：+Y 通过 / -Z 失败
覆盖率：+X% / -Y%
构建：[PASS/FAIL]
```

## 列示检查点

显示所有检查点：
- 名称
- 时间戳
- Git SHA
- 状态（当前、落后、领先）

## 工作流

典型检查点流程：

```
[开始] --> /checkpoint create "功能开始"
   |
[实施] --> /checkpoint create "核心完成"
   |
[测试] --> /checkpoint verify "核心完成"
   |
[重构] --> /checkpoint create "重构完成"
   |
[PR] --> /checkpoint verify "功能开始"
```

## 参数

$ARGUMENTS:
- `create <name>` - 创建命名检查点
- `verify <name>` - 针对命名检查点验证
- `list` - 显示所有检查点
- `clear` - 删除旧检查点（保留最近 5 个）
