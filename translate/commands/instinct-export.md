---
name: instinct-export
description: 将本能从项目/全局范围导出到文件
command: /instinct-export
---

# 本能导出命令

将本能导出为可共享格式。适用于：
- 与队友共享
- 传输到新机器
- 为项目约定做出贡献

## 用法

```
/instinct-export                           # 导出所有个人本能
/instinct-export --domain testing          # 仅导出测试本能
/instinct-export --min-confidence 0.7      # 仅导出高置信度本能
/instinct-export --output team-instincts.yaml
/instinct-export --scope project --output project-instincts.yaml
```

## 执行操作

1. 检测当前项目上下文
2. 按选定范围加载本能：
   - `project`：仅当前项目
   - `global`：仅全局
   - `all`：项目 + 全局合并（默认）
3. 应用过滤器（`--domain`、`--min-confidence`）
4. 写入文件 YAML 样式导出（如果未提供输出路径则输出到 stdout）

## 输出格式

创建 YAML 文件：

```yaml
# 本能导出
# 生成：2025-01-22
# 来源：personal
# 计数：12 个本能

---
id: prefer-functional-style
trigger: "编写新函数时"
confidence: 0.8
domain: code-style
source: session-observation
scope: project
project_id: a1b2c3d4e5f6
project_name: my-app
---

# 优先使用函数式风格

## 操作
使用函数式模式而非类。
```

## 标志

- `--domain <name>`：仅导出指定域
- `--min-confidence <n>`：最低置信度阈值
- `--output <file>`：输出文件路径（省略时输出到 stdout）
- `--scope <project|global|all>`：导出范围（默认：`all`）
