# 编排命令

用于复杂任务的顺序代理工作流。

## 用法

`/orchestrate [workflow-type] [task-description]`

## 工作流类型

### feature
完整功能实现工作流：
```
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

### bugfix
错误调查和修复工作流：
```
planner -> tdd-guide -> code-reviewer
```

### refactor
安全重构工作流：
```
architect -> code-reviewer -> tdd-guide
```

### security
安全聚焦审查：
```
security-reviewer -> code-reviewer -> architect
```

## 执行模式

对于工作流中的每个代理：

1. **调用代理** 并传递来自前一个代理的上下文
2. **收集输出** 作为结构化交接文档
3. **传递给下一个代理** 到链中
4. **汇总结果** 到最终报告

## 交接文档格式

在代理之间，创建交接文档：

```markdown
## 交接：[previous-agent] -> [next-agent]

### 上下文
[已完成工作的摘要]

### 发现
[关键发现或决策]

### 修改的文件
[触摸的文件列表]

### 未解决问题
[留给下一个代理的未解决项目]

### 建议
[建议的后续步骤]
```

## 示例：功能工作流

```
/orchestrate feature "添加用户认证"
```

执行：

1. **规划者代理**
   - 分析需求
   - 创建实现计划
   - 识别依赖项
   - 输出：`交接：planner -> tdd-guide`

2. **TDD 指导代理**
   - 读取规划者交接
   - 先写测试
   - 实现以通过测试
   - 输出：`交接：tdd-guide -> code-reviewer`

3. **代码审查者代理**
   - 审查实现
   - 检查问题
   - 建议改进
   - 输出：`交接：code-reviewer -> security-reviewer`

4. **安全审查者代理**
   - 安全审计
   - 漏洞检查
   - 最终批准
   - 输出：最终报告

## 最终报告格式

```
编排报告
====================
工作流：feature
任务：添加用户认证
代理：planner -> tdd-guide -> code-reviewer -> security-reviewer

摘要
-------
[一段摘要]

代理输出
-------------
规划者：[摘要]
TDD 指导：[摘要]
代码审查者：[摘要]
安全审查者：[摘要]

更改的文件
-------------
[列出所有修改的文件]

测试结果
------------
[测试通过/失败摘要]

安全状态
---------------
[安全发现]

建议
--------------
[SHIP / NEEDS WORK / BLOCKED]
```

## 并行执行

对于独立检查，并行运行代理：

```markdown
### 并行阶段
同时运行：
- code-reviewer（质量）
- security-reviewer（安全）
- architect（设计）

### 合并结果
将输出合并到单个报告中
```

## 参数

$ARGUMENTS:
- `feature <description>` - 完整功能工作流
- `bugfix <description>` - 错误修复工作流
- `refactor <description>` - 重构工作流
- `security <description>` - 安全审查工作流
- `custom <agents> <description>` - 自定义代理序列

## 自定义工作流示例

```
/orchestrate custom "architect,tdd-guide,code-reviewer" "重新设计缓存层"
```

## 提示

1. **从规划者开始** 处理复杂功能
2. **始终在合并前包含 code-reviewer**
3. **对认证/支付/PII 使用 security-reviewer**
4. **保持交接简洁** - 专注于下一个代理需要的内容
5. **在代理之间根据需要运行验证**
