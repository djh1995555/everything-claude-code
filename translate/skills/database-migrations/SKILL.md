---
name: database-migrations
description: 数据库迁移最佳实践，用于模式更改、数据迁移、回滚和零停机部署，适用于PostgreSQL、MySQL和常见ORM（Prisma、Drizzle、Django、TypeORM、golang-migrate）。
origin: ECC
---

# 数据库迁移模式

生产系统的安全、可逆数据库模式更改。

## 激活时机

- 创建或修改数据库表
- 添加/删除列或索引
- 运行数据迁移（回填、转换）
- 规划零停机模式更改
- 为新项目设置迁移工具

## 核心原则

1. **每个更改都是一个迁移** — 永远不要手动修改生产数据库
2. **迁移在生产中只能向前** — 回滚使用新的向前迁移
3. **模式和数据迁移是分开的** — 永远不要在一个迁移中混合DDL和DML
4. **针对生产规模的数据测试迁移** — 在100行上工作的迁移可能会在10M行上锁定
5. **迁移在部署后是不可变的** — 永远不要编辑已在生产中运行的迁移

## 迁移安全检查表

在应用任何迁移之前：

- [ ] 迁移同时有UP和DOWN（或明确标记为不可逆）
- [ ] 对大表没有全表锁定（使用并发操作）
- [ ] 新列有默认值或可为空（永远不要在没有默认值的情况下添加NOT NULL）
- [ ] 索引是并发创建的（不要在现有表的CREATE TABLE中内联）
- [ ] 数据回填是与模式更改分开的迁移
- [ ] 针对生产数据的副本进行了测试
- [ ] 回滚计划已记录

## PostgreSQL模式

### 安全添加列

```sql
-- 推荐：可为空列，无锁定
ALTER TABLE users ADD COLUMN avatar_url TEXT;

-- 推荐：带默认值的列（Postgres 11+是即时的，无需重写）
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT true;

-- 不推荐：在现有表上添加NOT NULL而没有默认值（需要完全重写）
ALTER TABLE users ADD COLUMN role TEXT NOT NULL;
-- 这会锁定表并重写每一行
```

### 无停机添加索引

```sql
-- 不推荐：在大表上阻止写入
CREATE INDEX idx_users_email ON users (email);

-- 推荐：非阻塞，允许并发写入
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);

-- 注意：CONCURRENTLY不能在事务块内运行
-- 大多数迁移工具需要特殊处理
```

### 重命名列（零停机）

永远不要在生产中直接重命名。使用展开-收缩模式：

```sql
-- 步骤1：添加新列（迁移001）
ALTER TABLE users ADD COLUMN display_name TEXT;

-- 步骤2：回填数据（迁移002，数据迁移）
UPDATE users SET display_name = username WHERE display_name IS NULL;

-- 步骤3：更新应用程序代码以读写两列
-- 部署应用程序更改

-- 步骤4：停止写入旧列，删除它（迁移003）
ALTER TABLE users DROP COLUMN username;
```

### 安全删除列

```sql
-- 步骤1：移除所有对该列的应用程序引用
-- 步骤2：部署不包含该列引用的应用程序
-- 步骤3：在下一次迁移中删除列
ALTER TABLE orders DROP COLUMN legacy_status;

-- 对于Django：使用SeparateDatabaseAndState从模型中移除
-- 而不生成DROP COLUMN（然后在下一次迁移中删除）
```

### 大数据迁移

```sql
-- 不推荐：在一个事务中更新所有行（锁定表）
UPDATE users SET normalized_email = LOWER(email);

-- 推荐：批量更新并显示进度
DO $$
DECLARE
  batch_size INT := 10000;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE users
    SET normalized_email = LOWER(email)
    WHERE id IN (
      SELECT id FROM users
      WHERE normalized_email IS NULL
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED
    );
    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    RAISE NOTICE 'Updated % rows', rows_updated;
    EXIT WHEN rows_updated = 0;
    COMMIT;
  END LOOP;
END $$;
```

## Prisma（TypeScript/Node.js）

### 工作流

```bash
# 从模式更改创建迁移
npx prisma migrate dev --name add_user_avatar

# 在生产中应用待处理的迁移
npx prisma migrate deploy

# 重置数据库（仅开发）
npx prisma migrate reset

# 模式更改后生成客户端
npx prisma generate
```

### 模式示例

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  avatarUrl String?  @map("avatar_url")
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  orders    Order[]

  @@map("users")
  @@index([email])
}
```

### 自定义SQL迁移

对于Prisma无法表达的操作（并发索引、数据回填）：

```bash
# 创建空迁移，然后手动编辑SQL
npx prisma migrate dev --create-only --name add_email_index
```

```sql
-- migrations/20240115_add_email_index/migration.sql
-- Prisma无法生成CONCURRENTLY，所以我们手动编写
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users (email);
```

## Drizzle（TypeScript/Node.js）

### 工作流

```bash
# 从模式更改生成迁移
npx drizzle-kit generate

# 应用迁移
npx drizzle-kit migrate

# 直接推送模式（仅开发，无迁移文件）
npx drizzle-kit push
```

### 模式示例

```typescript
import { pgTable, text, timestamp, uuid, boolean } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  email: text("email").notNull().unique(),
  name: text("name"),
```