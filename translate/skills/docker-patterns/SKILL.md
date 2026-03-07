---
name: docker-patterns
description: Docker和Docker Compose模式，用于本地开发、容器安全、网络、卷策略和多服务编排。
origin: ECC
---

# Docker模式

Docker和Docker Compose的最佳实践，用于容器化开发。

## 激活时机

- 为本地开发设置Docker Compose
- 设计多容器架构
- 排查容器网络或卷问题
- 审查Dockerfile的安全性和大小
- 从本地开发迁移到容器化工作流

## Docker Compose用于本地开发

### 标准Web应用栈

```yaml
# docker-compose.yml
services:
  app:
    build:
      context: .
      target: dev                     # 使用多阶段Dockerfile的开发阶段
    ports:
      - "3000:3000"
    volumes:
      - .:/app                        # 绑定挂载用于热重载
      - /app/node_modules             # 匿名卷 -- 保留容器依赖
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/app_dev
      - REDIS_URL=redis://redis:6379/0
      - NODE_ENV=development
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: npm run dev

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app_dev
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data

  mailpit:                            # 本地电子邮件测试
    image: axllent/mailpit
    ports:
      - "8025:8025"                   # Web UI
      - "1025:1025"                   # SMTP

volumes:
  pgdata:
  redisdata:
```

### 开发与生产Dockerfile

```dockerfile
# 阶段：依赖
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# 阶段：开发（热重载、调试工具）
FROM node:22-alpine AS dev
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# 阶段：构建
FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build && npm prune --production

# 阶段：生产（最小镜像）
FROM node:22-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001
USER appuser
COPY --from=build --chown=appuser:appgroup /app/dist ./dist
COPY --from=build --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=build --chown=appuser:appgroup /app/package.json ./
ENV NODE_ENV=production
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

### 覆盖文件

```yaml
# docker-compose.override.yml（自动加载，仅开发设置）
services:
  app:
    environment:
      - DEBUG=app:*
      - LOG_LEVEL=debug
    ports:
      - "9229:9229"                   # Node.js调试器

# docker-compose.prod.yml（生产显式设置）
services:
  app:
    build:
      target: production
    restart: always
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
```

```bash
# 开发（自动加载覆盖）
docker compose up

# 生产
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 网络

### 服务发现

同一Compose网络中的服务通过服务名称解析：
```
# 从"app"容器：
postgres://postgres:postgres@db:5432/app_dev    # "db"解析到db容器
redis://redis:6379/0                             # "redis"解析到redis容器
```

### 自定义网络

```yaml
services:
  frontend:
    networks:
      - frontend-net

  api:
    networks:
      - frontend-net
      - backend-net

  db:
    networks:
      - backend-net              # 只能从api访问，不能从frontend访问

networks:
  frontend-net:
  backend-net:
```

### 只暴露需要的内容

```yaml
services:
  db:
    ports:
      - "127.0.0.1:5432:5432"   # 只能从主机访问，不能从网络访问
    # 在生产中完全省略ports -- 只能在Docker网络内访问
```

## 卷策略

```yaml
volumes:
  # 命名卷：在容器重启之间持久化，由Docker管理
  pgdata:
```