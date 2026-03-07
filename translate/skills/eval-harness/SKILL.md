---
name: eval-harness
description: 用于Claude Code会话的正式评估框架，实现评估驱动开发（EDD）原则
tools: Read, Write, Edit, Bash, Grep, Glob
---

# 评估框架技能

用于Claude Code会话的正式评估框架，实现评估驱动开发（EDD）原则。

## 激活时机

- 为AI辅助工作流设置评估驱动开发（EDD）
- 为Claude Code任务完成定义通过/失败标准
- 使用pass@k指标衡量代理可靠性
- 为提示或代理变更创建回归测试套件
- 跨模型版本对代理性能进行基准测试

## 理念

评估驱动开发将评估视为"AI开发的单元测试"：
- 在实现之前定义预期行为
- 在开发期间持续运行评估
- 跟踪每次变更的回归
- 使用pass@k指标进行可靠性测量

## 评估类型

### 能力评估
测试Claude是否能够完成以前无法完成的任务：
```markdown
[CAPABILITY EVAL: feature-name]
Task: Claude应完成的任务描述
Success Criteria:
  - [ ] 标准1
  - [ ] 标准2
  - [ ] 标准3
Expected Output: 预期结果描述
```

### 回归评估
确保变更不会破坏现有功能：
```markdown
[REGRESSION EVAL: feature-name]
Baseline: SHA或检查点名称
Tests:
  - existing-test-1: PASS/FAIL
  - existing-test-2: PASS/FAIL
  - existing-test-3: PASS/FAIL
Result: X/Y通过（之前为Y/Y）
```

## 评分器类型

### 1. 基于代码的评分器
使用代码进行确定性检查：
```bash
# 检查文件是否包含预期模式
grep -q "export function handleAuth" src/auth.ts && echo "PASS" || echo "FAIL"

# 检查测试是否通过
npm test -- --testPathPattern="auth" && echo "PASS" || echo "FAIL"

# 检查构建是否成功
npm run build && echo "PASS" || echo "FAIL"
```

### 2. 基于模型的评分器
使用Claude评估开放式输出：
```markdown
[MODEL GRADER PROMPT]
评估以下代码变更：
1. 是否解决了所述问题？
2. 结构是否良好？
3. 是否处理了边缘情况？
4. 错误处理是否适当？

Score: 1-5（1=差，5=优）
Reasoning: [解释]
```

### 3. 人工评分器
标记需要手动审查：
```markdown
[HUMAN REVIEW REQUIRED]
Change: 变更描述
Reason: 为什么需要人工审查
Risk Level: LOW/MEDIUM/HIGH
```

## 指标

### pass@k
"k次尝试中至少一次成功"
- pass@1: 首次尝试成功率
- pass@3: 3次尝试内成功
- 典型目标：pass@3 > 90%

### pass^k
"所有k次试验都成功"
- 更高的可靠性标准
- pass^3: 连续3次成功
- 用于关键路径

## 评估工作流

### 1. 定义（编码前）
```markdown
## EVAL DEFINITION: feature-xyz

### Capability Evals
1. 可以创建新用户账户
2. 可以验证电子邮件格式
3. 可以安全地哈希密码

### Regression Evals
1. 现有登录仍然有效
2. 会话管理未改变
3. 登出流程完好

### Success Metrics
- 能力评估的pass@3 > 90%
- 回归评估的pass^3 = 100%
```

### 2. 实现
编写代码以通过定义的评估。

### 3. 评估
```bash
# 运行能力评估
[运行每个能力评估，记录PASS/FAIL]

# 运行回归评估
npm test -- --testPathPattern="existing"

# 生成报告
```

### 4. 报告
```markdown
EVAL REPORT: feature-xyz
========================

Capability Evals:
  create-user:     PASS (pass@1)
  validate-email:  PASS (pass@2)
  hash-password:   PASS (pass@1)
  Overall:         3/3 passed

Regression Evals:
  login-flow:      PASS
  session-mgmt:    PASS
  logout-flow:     PASS
  Overall:         3/3 passed

Metrics:
  pass@1: 67% (2/3)
  pass@3: 100% (3/3)

Status: READY FOR REVIEW
```

## 集成模式

### 预实现
```
/eval define feature-name
```
在`.claude/evals/feature-name.md`创建评估定义文件

### 实现期间
```
/eval check feature-name
```
运行当前评估并报告状态

### 后实现
```
/eval report feature-name
```
生成完整评估报告

## 评估存储

在项目中存储评估：
```
.claude/
  evals/
    feature-xyz.md      # 评估定义
    feature-xyz.log     # 评估运行历史
    baseline.json       # 回归基线
```

## 最佳实践

1. **在编码前定义评估** - 促使清晰思考成功标准
2. **频繁运行评估** - 及早发现回归
3. **随时间跟踪pass@k** - 监控可靠性趋势