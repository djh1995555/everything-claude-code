# 线束审计命令

审计当前仓库的代理线束设置并返回优先评分卡。

## 用法

`/harness-audit [scope] [--format text|json]`

- `scope`（可选）：`repo`（默认）、`hooks`、`skills`、`commands`、`agents`
- `--format`：输出样式（`text` 默认，`json` 用于自动化）

## 评估内容

将每个类别评分从 `0` 到 `10`：

1. 工具覆盖
2. 上下文效率
3. 质量门
4. 内存持久化
5. 评估覆盖
6. 安全护栏
7. 成本效率

## 输出约定

返回：

1. `overall_score` 满分 70
2. 类别分数和具体发现
3. 带有确切文件路径的前 3 个操作
4. 建议接下来应用的 ECC 技能

## 检查清单

- 检查 `hooks/hooks.json`、`scripts/hooks/` 和钩子测试。
- 检查 `skills/`、命令覆盖和代理覆盖。
- 验证 `.cursor/`、`.opencode/`、`.codex/` 的跨线束一致性。
- 标记损坏或陈旧的引用。

## 示例结果

```text
线束审计（仓库）：52/70
- 质量门：9/10
- 评估覆盖：6/10
- 成本效率：4/10

前 3 个操作：
1) 在 scripts/hooks/cost-tracker.js 中添加成本跟踪钩子
2) 在 skills/eval-harness/SKILL.md 中添加 pass@k 文档和模板
3) 在 .opencode/commands/ 中添加 /harness-audit 的命令一致性
```

## 参数

$ARGUMENTS:
- `repo|hooks|skills|commands|agents`（可选范围）
- `--format text|json`（可选输出格式）
