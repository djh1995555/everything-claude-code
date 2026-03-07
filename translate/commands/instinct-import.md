---
name: instinct-import
description: 将本能从文件或 URL 导入到项目/全局范围
command: true
---

# 本能导入命令

## 实现

使用插件根路径运行本能 CLI：

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/scripts/instinct-cli.py" import <file-or-url> [--dry-run] [--force] [--min-confidence 0.7] [--scope project|global]
```

或者如果 `CLAUDE_PLUGIN_ROOT` 未设置（手动安装）：

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py import <file-or-url>
```

从本地文件路径或 HTTP(S) URL 导入本能。

## 用法

```
/instinct-import team-instincts.yaml
/instinct-import https://github.com/org/repo/instincts.yaml
/instinct-import team-instincts.yaml --dry-run
/instinct-import team-instincts.yaml --scope global --force
```

## 执行操作

1. 获取本能文件（本地路径或 URL）
2. 解析并验证格式
3. 检查与现有本能的重复项
4. 合并或添加新本能
5. 保存到继承的本能目录：
   - 项目范围：`~/.claude/homunculus/projects/<project-id>/instincts/inherited/`
   - 全局范围：`~/.claude/homunculus/instincts/inherited/`

## 导入流程

```
📥 从以下位置导入本能：team-instincts.yaml
================================================

找到 12 个要导入的本能。

分析冲突...

## 新本能 (8)
将添加以下内容：
  ✓ use-zod-validation (置信度: 0.7)
  ✓ prefer-named-exports (置信度: 0.65)
  ✓ test-async-functions (置信度: 0.8)
  ...

## 重复本能 (3)
已有类似本能：
  ⚠️ prefer-functional-style
     本地：0.8 置信度, 12 次观察
     导入：0.7 置信度
     → 保留本地（更高置信度）

  ⚠️ test-first-workflow
     本地：0.75 置信度
     导入：0.9 置信度
     → 更新为导入项（更高置信度）

导入 8 个新的，更新 1 个？
```

## 合并行为

当导入与现有 ID 相同的本能时：
- 置信度更高的导入成为更新候选
- 置信度相等/更低的导入被跳过
- 除非使用 `--force`，否则需要用户确认

## 源跟踪

导入的本能用以下内容标记：
```yaml
source: inherited
scope: project
imported_from: "team-instincts.yaml"
project_id: "a1b2c3d4e5f6"
project_name: "my-project"
```

## 标志

- `--dry-run`：预览而不导入
- `--force`：跳过确认提示
- `--min-confidence <n>`：仅导入高于阈值的本能
- `--scope <project|global>`：选择目标范围（默认值：`project`）

## 输出

导入后：
```
✅ 导入完成！

新增：8 个本能
更新：1 个本能
跳过：3 个本能（已存在相等/更高置信度）

新本能保存到：~/.claude/homunculus/instincts/inherited/

运行 /instinct-status 查看所有本能。
```
