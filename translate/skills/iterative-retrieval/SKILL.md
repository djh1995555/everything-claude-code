---
name: iterative-retrieval
description: 逐步优化上下文检索以解决子代理上下文问题的模式
origin: ECC
---

# 迭代检索模式

解决多代理工作流中的“上下文问题”，其中子代理在开始工作前不知道自己需要什么上下文。

## 何时激活

- 生成需要代码库上下文但无法预先预测的子代理
- 构建上下文逐步优化的多代理工作流
- 在代理任务中遇到“上下文过大”或“缺少上下文”失败
- 为代码探索设计类似 RAG 的检索管道
- 优化代理编排中的令牌使用

## 问题

子代理生成时上下文有限。它们不知道：
- 哪些文件包含相关代码
- 代码库中存在哪些模式
- 项目使用什么术语

标准方法失败的原因：
- **发送所有内容**：超出上下文限制
- **不发送任何内容**：代理缺乏关键信息
- **猜测需要什么**：通常是错误的

## 解决方案：迭代检索

一个 4 阶段循环，逐步优化上下文：

```
┌─────────────────────────────────────────────┐
│                                             │
│   ┌──────────┐      ┌──────────┐            │
│   │ DISPATCH │─────▶│ EVALUATE │            │
│   └──────────┘      └──────────┘            │
│        ▲                  │                 │
│        │                  ▼                 │
│   ┌──────────┐      ┌──────────┐            │
│   │   LOOP   │◀─────│  REFINE  │            │
│   └──────────┘      └──────────┘            │
│                                             │
│        Max 3 cycles, then proceed           │
└─────────────────────────────────────────────┘
```

### 阶段 1：DISPATCH（调度）

初始广泛查询以收集候选文件：

```javascript
// 从高级别意图开始
const initialQuery = {
  patterns: ['src/**/*.ts', 'lib/**/*.ts'],
  keywords: ['authentication', 'user', 'session'],
  excludes: ['*.test.ts', '*.spec.ts']
};

// 调度到检索代理
const candidates = await retrieveFiles(initialQuery);
```

### 阶段 2：EVALUATE（评估）

评估检索到的内容的相关性：

```javascript
function evaluateRelevance(files, task) {
  return files.map(file => ({
    path: file.path,
    relevance: scoreRelevance(file.content, task),
    reason: explainRelevance(file.content, task),
    missingContext: identifyGaps(file.content, task)
  }));
}
```

评分标准：
- **高 (0.8-1.0)**：直接实现目标功能
- **中 (0.5-0.7)**：包含相关模式或类型
- **低 (0.2-0.4)**：间接相关
- **无 (0-0.2)**：不相关，排除

### 阶段 3：REFINE（优化）

根据评估更新搜索标准：

```javascript
function refineQuery(evaluation, previousQuery) {
  return {
    // 添加在高相关性文件中发现的新模式
    patterns: [...previousQuery.patterns, ...extractPatterns(evaluation)],

    // 添加在代码库中发现的术语
    keywords: [...previousQuery.keywords, ...extractKeywords(evaluation)],

    // 排除已确认不相关的路径
    excludes: [...previousQuery.excludes, ...evaluation
      .filter(e => e.relevance < 0.2)
      .map(e => e.path)
    ],

    // 针对特定差距
    focusAreas: evaluation
      .flatMap(e => e.missingContext)
      .filter(unique)
  };
}
```

### 阶段 4：LOOP（循环）

使用优化后的标准重复（最多 3 个周期）：

```javascript
async function iterativeRetrieve(task, maxCycles = 3) {
  let query = createInitialQuery(task);
  let bestContext = [];

  for (let cycle = 0; cycle < maxCycles; cycle++) {
    const candidates = await retrieveFiles(query);
    const evaluation = evaluateRelevance(candidates, task);

    // 检查是否有足够的上下文
    const highRelevance = evaluation.filter(e => e.relevance >= 0.7);
    if (highRelevance.length >= 3 && !hasCriticalGaps(evaluation)) {
      return highRelevance;
    }

    // 优化并继续
    query = refineQuery(evaluation, query);
    bestContext = mergeContext(bestContext, highRelevance);
  }

  return bestContext;
}
```

## 实际示例

### 示例 1：Bug 修复上下文

```
任务："修复身份验证令牌过期 bug"

周期 1：
  DISPATCH：在 src/** 中搜索 "token", "auth", "expiry"
  EVALUATE：找到 auth.ts (0.9), tokens.ts (0.8), user.ts (0.3)
  REFINE：添加 "refresh", "jwt" 关键词；排除 user.ts

周期 2：
  DISPATCH：搜索优化后的术语
  EVALUATE：找到 session-manager.ts (0.95), jwt-utils.ts (0.85)
  REFINE：上下文足够（2 个高相关性文件）

结果：auth.ts, tokens.ts, session-manager.ts, jwt-utils.ts
```

### 示例 2：功能实现

```
任务："为 API 端点添加速率限制"

周期 1：
  DISPATCH：在 routes/** 中搜索 "rate", "limit", "api"
  EVALUATE：无匹配 - 代码库使用 "throttle" 术语
  REFINE：添加 "throttle", "middleware" 关键词

周期 2：
  DISPATCH：搜索优化后的术语
  EVALUATE：找到 throttle.ts (0.9), middleware/index.ts (0.7)
  REFINE：需要路由器模式

周期 3：
  DISPATCH：搜索 "router", "express" 模式
  EVALUATE：找到 router-setup.ts (0.8)
  REFINE：上下文足够

结果：throttle.ts, middleware/index.ts, router-setup.ts
```

## 与代理集成

在代理提示中使用：

```markdown
为此任务检索上下文时：
1. 从广泛的关键词搜索开始
2. 评估每个文件的相关性（0-1 比例）
3. 识别仍缺失的上下文
4. 优化搜索标准并重复（最多 3 个周期）
5. 返回相关性 >= 0.7 的文件
```

## 最佳实践

1. **从广泛开始，逐步缩小** - 不要过度指定初始查询
2. **学习代码库术语** - 第一个周期通常会揭示命名约定
3. **跟踪缺失内容** - 明确的差距识别驱动优化
4. **在“足够好”时停止** - 3 个高相关性文件胜过 10 个普通文件
5. **自信地排除** - 低相关性文件不会变得相关

## 相关资源

- [长篇指南](https://x.com/affaanmustafa/status/2014040193557471352) - 子代理编排部分
- `continuous-learning` 技能 - 用于随时间改进的模式
- `~/.claude/agents/` 中的代理定义