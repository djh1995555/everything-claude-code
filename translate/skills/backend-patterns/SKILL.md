---
name: backend-patterns
description: 后端架构模式、API设计、数据库优化以及Node.js、Express和Next.js API路由的服务器端最佳实践。
origin: ECC
---

# 后端开发模式

用于可扩展服务器端应用的后端架构模式和最佳实践。

## 激活时机

- 设计REST或GraphQL API端点
- 实现仓库、服务或控制器层
- 优化数据库查询（N+1、索引、连接池）
- 添加缓存（Redis、内存、HTTP缓存头）
- 设置后台作业或异步处理
- 为API结构化错误处理和验证
- 构建中间件（认证、日志记录、速率限制）

## API设计模式

### RESTful API结构

```typescript
// ✅ 基于资源的URL
GET    /api/markets                 # 列出资源
GET    /api/markets/:id             # 获取单个资源
POST   /api/markets                 # 创建资源
PUT    /api/markets/:id             # 替换资源
PATCH  /api/markets/:id             # 更新资源
DELETE /api/markets/:id             # 删除资源

// ✅ 查询参数用于过滤、排序、分页
GET /api/markets?status=active&sort=volume&limit=20&offset=0
```

### 仓库模式

```typescript
// 抽象数据访问逻辑
interface MarketRepository {
  findAll(filters?: MarketFilters): Promise<Market[]>
  findById(id: string): Promise<Market | null>
  create(data: CreateMarketDto): Promise<Market>
  update(id: string, data: UpdateMarketDto): Promise<Market>
  delete(id: string): Promise<void>
}

class SupabaseMarketRepository implements MarketRepository {
  async findAll(filters?: MarketFilters): Promise<Market[]> {
    let query = supabase.from('markets').select('*')

    if (filters?.status) {
      query = query.eq('status', filters.status)
    }

    if (filters?.limit) {
      query = query.limit(filters.limit)
    }

    const { data, error } = await query

    if (error) throw new Error(error.message)
    return data
  }

  // 其他方法...
}
```

### 服务层模式

```typescript
// 业务逻辑与数据访问分离
class MarketService {
  constructor(private marketRepo: MarketRepository) {}

  async searchMarkets(query: string, limit: number = 10): Promise<Market[]> {
    // 业务逻辑
    const embedding = await generateEmbedding(query)
    const results = await this.vectorSearch(embedding, limit)

    // 获取完整数据
    const markets = await this.marketRepo.findByIds(results.map(r => r.id))

    // 按相似度排序
    return markets.sort((a, b) => {
      const scoreA = results.find(r => r.id === a.id)?.score || 0
      const scoreB = results.find(r => r.id === b.id)?.score || 0
      return scoreA - scoreB
    })
  }

  private async vectorSearch(embedding: number[], limit: number) {
    // 向量搜索实现
  }
}
```

### 中间件模式

```typescript
// 请求/响应处理管道
export function withAuth(handler: NextApiHandler): NextApiHandler {
  return async (req, res) => {
    const token = req.headers.authorization?.replace('Bearer ', '')

    if (!token) {
      return res.status(401).json({ error: 'Unauthorized' })
    }

    try {
      const user = await verifyToken(token)
      req.user = user
      return handler(req, res)
    } catch (error) {
      return res.status(401).json({ error: 'Invalid token' })
    }
  }
}

// 使用
export default withAuth(async (req, res) => {
  // 处理程序可以访问req.user
})
```

## 数据库模式

### 查询优化

```typescript
// ✅ 良好：只选择需要的列
const { data } = await supabase
  .from('markets')
  .select('id, name, status, volume')
  .eq('status', 'active')
  .order('volume', { ascending: false })
  .limit(10)

// ❌ 不良：选择所有列
const { data } = await supabase
  .from('markets')
  .select('*')
```

### N+1查询预防

```typescript
// ❌ 不良：N+1查询问题
const markets = await getMarkets()
for (const market of markets) {
  market.creator = await getUser(market.creator_id)  // N个查询
}

// ✅ 良好：批量获取
const markets = await getMarkets()
const creatorIds = markets.map(m => m.creator_id)
const creators = await getUsers(creatorIds)  // 1个查询
const creatorMap = new Map(creators.map(c => [c.id, c]))

markets.forEach(market => {
  market.creator = creatorMap.get(market.creator_id)
})
```

### 事务模式

```typescript
async function createMarketWithPosition(
  marketData: CreateMarketDto,
  positionData: CreatePositionDto
) {
  // 使用Supabase事务
  const { data, error } = await supabase.rpc('create_market_with_position', {
    market_data: marketData,
    position_data: positionData
  })

  if (error) throw new Error('Transaction failed')
  return data
}

// Supabase中的SQL函数
CREATE OR REPLACE FUNCTION create_market_with_position(
  market_data jsonb,
  position_data jsonb
)
RETURNS jsonb
LANGUAGE plpgsql
AS $$
BEGIN
  -- 自动启动事务
  INSERT INTO markets VALUES (market_data);
  INSERT INTO positions VALUES (position_data);
  RETURN jsonb_build_object('success', true);
EXCEPTION
  WHEN OTHERS THEN
    -- 自动回滚