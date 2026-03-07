---
name: api-design
description: REST API设计模式，包括资源命名、状态码、分页、过滤、错误响应、版本控制和生产API的速率限制。
origin: ECC
---

# API设计模式

设计一致、开发者友好的REST API的约定和最佳实践。

## 激活时机

- 设计新的API端点
- 审查现有API契约
- 添加分页、过滤或排序
- 为API实现错误处理
- 规划API版本控制策略
- 构建公共或面向合作伙伴的API

## 资源设计

### URL结构

```
# 资源是名词、复数、小写、短横线分隔
GET    /api/v1/users
GET    /api/v1/users/:id
POST   /api/v1/users
PUT    /api/v1/users/:id
PATCH  /api/v1/users/:id
DELETE /api/v1/users/:id

# 关系的子资源
GET    /api/v1/users/:id/orders
POST   /api/v1/users/:id/orders

# 不映射到CRUD的操作（谨慎使用动词）
POST   /api/v1/orders/:id/cancel
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
```

### 命名规则

```
# 良好实践
/api/v1/team-members          # 多词资源使用短横线分隔
/api/v1/orders?status=active  # 查询参数用于过滤
/api/v1/users/123/orders      # 嵌套资源表示所有权

# 不良实践
/api/v1/getUsers              # URL中使用动词
/api/v1/user                  # 单数（使用复数）
/api/v1/team_members          # URL中使用蛇形命名
/api/v1/users/123/getOrders   # 嵌套资源中使用动词
```

## HTTP方法和状态码

### 方法语义

| 方法 | 幂等性 | 安全性 | 用途 |
|--------|-----------|------|---------|
| GET | 是 | 是 | 检索资源 |
| POST | 否 | 否 | 创建资源、触发操作 |
| PUT | 是 | 否 | 完全替换资源 |
| PATCH | 否* | 否 | 部分更新资源 |
| DELETE | 是 | 否 | 删除资源 |

*通过适当实现，PATCH可以实现幂等性

### 状态码参考

```
# 成功
200 OK                    — GET、PUT、PATCH（带响应体）
201 Created               — POST（包含Location头）
204 No Content            — DELETE、PUT（无响应体）

# 客户端错误
400 Bad Request           — 验证失败、JSON格式错误
401 Unauthorized          — 缺少或无效的身份验证
403 Forbidden             — 已认证但未授权
404 Not Found             — 资源不存在
409 Conflict              — 重复条目、状态冲突
422 Unprocessable Entity  — 语义无效（JSON格式正确，但数据错误）
429 Too Many Requests     — 超过速率限制

# 服务器错误
500 Internal Server Error — 意外失败（绝不暴露细节）
502 Bad Gateway           — 上游服务失败
503 Service Unavailable   — 临时过载，包含Retry-After
```

### 常见错误

```
# 不良：所有情况都返回200
{ "status": 200, "success": false, "error": "Not found" }

# 良好：语义化使用HTTP状态码
HTTP/1.1 404 Not Found
{ "error": { "code": "not_found", "message": "User not found" } }

# 不良：验证错误返回500
# 良好：返回400或422并包含字段级详细信息

# 不良：创建资源返回200
# 良好：返回201并包含Location头
HTTP/1.1 201 Created
Location: /api/v1/users/abc-123
```

## 响应格式

### 成功响应

```json
{
  "data": {
    "id": "abc-123",
    "email": "alice@example.com",
    "name": "Alice",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

### 集合响应（带分页）

```json
{
  "data": [
    { "id": "abc-123", "name": "Alice" },
    { "id": "def-456", "name": "Bob" }
  ],
  "meta": {
    "total": 142,
    "page": 1,
    "per_page": 20,
    "total_pages": 8
  },
  "links": {
    "self": "/api/v1/users?page=1&per_page=20",
    "next": "/api/v1/users?page=2&per_page=20",
    "last": "/api/v1/users?page=8&per_page=20"
  }
}
```

### 错误响应

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address",
        "code": "invalid_format"
      },
      {
        "field": "age",
        "message": "Must be between 0 and 150",
        "code": "out_of_range"
      }
    ]
  }
}
```

### 响应信封变体

```typescript
// 选项A：带数据包装器的信封（公共API推荐）
interface ApiResponse<T> {
  data: T;
  meta?: PaginationMeta;
  links?: PaginationLinks;
}

interface ApiError {
  error: {
    code: string;
    message: string;
    details?: FieldError[];
  };
}

// 选项B：扁平响应（更简单，内部API常用）
// 成功：直接返回资源
// 错误：返回错误对象
// 通过HTTP状态码区分
```

## 分页

### 基于偏移量（简单）