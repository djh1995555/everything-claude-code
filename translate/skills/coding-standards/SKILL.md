---
name: coding-standards
description: 适用于TypeScript、JavaScript、React和Node.js开发的通用编码标准、最佳实践和模式。
origin: ECC
---

# 编码标准与最佳实践

适用于所有项目的通用编码标准。

## 激活时机

- 启动新项目或模块
- 审查代码质量和可维护性
- 重构现有代码以遵循约定
- 强制执行命名、格式或结构一致性
- 设置linting、格式化或类型检查规则
- 向新贡献者介绍编码约定

## 代码质量原则

### 1. 可读性优先
- 代码阅读次数多于编写次数
- 清晰的变量和函数名称
- 优先使用自文档化代码而非注释
- 一致的格式

### 2. KISS（保持简单）
- 最简单可行的解决方案
- 避免过度设计
- 不要过早优化
- 易于理解 > 聪明的代码

### 3. DRY（不要重复自己）
- 将通用逻辑提取到函数中
- 创建可重用组件
- 跨模块共享实用工具
- 避免复制粘贴编程

### 4. YAGNI（你不会需要它）
- 不要在需要之前构建功能
- 避免投机性泛化
- 仅在需要时添加复杂性
- 从简单开始，需要时重构

## TypeScript/JavaScript标准

### 变量命名

```typescript
// ✅ 良好：描述性名称
const marketSearchQuery = 'election'
const isUserAuthenticated = true
const totalRevenue = 1000

// ❌ 不良：不清晰的名称
const q = 'election'
const flag = true
const x = 1000
```

### 函数命名

```typescript
// ✅ 良好：动词-名词模式
async function fetchMarketData(marketId: string) { }
function calculateSimilarity(a: number[], b: number[]) { }
function isValidEmail(email: string): boolean { }

// ❌ 不良：不清晰或仅使用名词
async function market(id: string) { }
function similarity(a, b) { }
function email(e) { }
```

### 不可变模式（关键）

```typescript
// ✅ 始终使用扩展运算符
const updatedUser = {
  ...user,
  name: 'New Name'
}

const updatedArray = [...items, newItem]

// ❌ 永远不要直接修改
user.name = 'New Name'  // 不良
items.push(newItem)     // 不良
```

### 错误处理

```typescript
// ✅ 良好：全面的错误处理
async function fetchData(url: string) {
  try {
    const response = await fetch(url)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw new Error('Failed to fetch data')
  }
}

// ❌ 不良：没有错误处理
async function fetchData(url) {
  const response = await fetch(url)
  return response.json()
}
```

### Async/Await最佳实践

```typescript
// ✅ 良好：尽可能并行执行
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats()
])

// ❌ 不良：不必要的顺序执行
const users = await fetchUsers()
const markets = await fetchMarkets()
const stats = await fetchStats()
```

### 类型安全

```typescript
// ✅ 良好：适当的类型
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
  created_at: Date
}

function getMarket(id: string): Promise<Market> {
  // 实现
}

// ❌ 不良：使用'any'
function getMarket(id: any): Promise<any> {
  // 实现
}
```

## React最佳实践

### 组件结构

```typescript
// ✅ 良好：带类型的函数组件
interface ButtonProps {
  children: React.ReactNode
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({
  children,
  onClick,
  disabled = false,
  variant = 'primary'
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  )
}

// ❌ 不良：没有类型，结构不清晰
export function Button(props) {
  return <button onClick={props.onClick}>{props.children}</button>
}
```

### 自定义Hook

```typescript
// ✅ 良好：可重用的自定义Hook
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
```}}]<|FunctionCallEnd|>