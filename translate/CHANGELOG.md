# 变更日志

## 1.8.0 - 2026-03-04

### 亮点

- 以 harness 为重点的版本，专注于可靠性、评估纪律和自主循环操作。
- Hook 运行时现在支持基于配置文件的控制和目标化 Hook 禁用。
- NanoClaw v2 增加了模型路由、技能热加载、分支、搜索、压缩、导出和指标。

### 核心

- 新增命令：`/harness-audit`、`/loop-start`、`/loop-status`、`/quality-gate`、`/model-route`。
- 新增技能：
  - `agent-harness-construction`
  - `agentic-engineering`
  - `ralphinho-rfc-pipeline`
  - `ai-first-engineering`
  - `enterprise-agent-ops`
  - `nanoclaw-repl`
  - `continuous-agent-loop`
- 新增代理：
  - `harness-optimizer`
  - `loop-operator`

### Hook 可靠性

- 修复了 SessionStart 根解析，增加了强大的回退搜索。
- 将会话摘要持久化移至 `Stop`，此时转录 payload 可用。
- 增加了质量门和成本跟踪器 hooks。
- 用专用脚本文件替换了脆弱的内联 hook 单行代码。
- 增加了 `ECC_HOOK_PROFILE` 和 `ECC_DISABLED_HOOKS` 控制。

### 跨平台

- 改进了文档警告逻辑中的 Windows 安全路径处理。
- 强化了观察者循环行为，避免非交互式挂起。

### 说明

- `autonomous-loops` 作为兼容性别名保留一个版本；`continuous-agent-loop` 是规范名称。

### 鸣谢

- 灵感来自 [zarazhangrui](https://github.com/zarazhangrui)
- homunculus 灵感来自 [humanplane](https://github.com/humanplane)