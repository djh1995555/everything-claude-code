---
name: deployment-patterns
description: 部署工作流、CI/CD管道模式、Docker容器化、健康检查、回滚策略和Web应用程序的生产就绪检查表。
origin: ECC
---

# 部署模式

生产部署工作流和CI/CD最佳实践。

## 激活时机

- 设置CI/CD管道
- 容器化应用程序
- 规划部署策略（蓝绿、金丝雀、滚动）
- 实现健康检查和就绪探针
- 准备生产发布
- 配置特定环境的设置

## 部署策略

### 滚动部署（默认）

逐步替换实例 — 在推出期间旧版本和新版本同时运行。

```
实例1: v1 → v2  (先更新)
实例2: v1        (仍运行v1)
实例3: v1        (仍运行v1)

实例1: v2
实例2: v1 → v2  (第二个更新)
实例3: v1

实例1: v2
实例2: v2
实例3: v1 → v2  (最后更新)
```

**优点：** 零停机，逐步推出
**缺点：** 两个版本同时运行 — 需要向后兼容的更改
**使用场景：** 标准部署，向后兼容的更改

### 蓝绿部署

运行两个相同的环境。原子切换流量。

```
蓝  (v1) ← 流量
绿 (v2)   空闲，运行新版本

# 验证后：
蓝  (v1)   空闲（成为备用）
绿 (v2) ← 流量
```

**优点：** 即时回滚（切换回蓝），干净的切换
**缺点：** 部署期间需要2倍基础设施
**使用场景：** 关键服务，零容忍问题

### 金丝雀部署

先将小部分流量路由到新版本。

```
v1: 95% 流量
v2:  5% 流量  (金丝雀)

# 如果指标看起来不错：
v1: 50% 流量
v2: 50% 流量

# 最终：
v2: 100% 流量
```

**优点：** 在全面推出前用真实流量发现问题
**缺点：** 需要流量拆分基础设施、监控
**使用场景：** 高流量服务，风险更改，功能标志

## Docker

### 多阶段Dockerfile（Node.js）

```dockerfile
# 阶段1：安装依赖
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --production=false

# 阶段2：构建
FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build
RUN npm prune --production

# 阶段3：生产镜像
FROM node:22-alpine AS runner
WORKDIR /app

RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001
USER appuser

COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/package.json ./

ENV NODE_ENV=production
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/server.js"]
```

### 多阶段Dockerfile（Go）

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /server ./cmd/server

FROM alpine:3.19 AS runner
RUN apk --no-cache add ca-certificates
RUN adduser -D -u 1001 appuser
USER appuser

COPY --from=builder /server /server

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:8080/health || exit 1
CMD ["/server"]
```

### 多阶段Dockerfile（Python/Django）

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

FROM python:3.12-slim AS runner
WORKDIR /app

RUN useradd -r -u 1001 appuser
USER appuser

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### Docker最佳实践

```
# 推荐实践
- 使用特定版本标签（node:22-alpine，而非node:latest）
- 多阶段构建以最小化镜像大小
- 以非root用户运行
- 先复制依赖文件（层缓存）
- 使用.dockerignore排除node_modules、.git、tests
- 添加HEALTHCHECK指令
- 在docker-compose或k8s中设置资源限制

# 不推荐实践
- 以root运行
- 使用:latest标签
- 在一个COPY层中复制整个仓库
- 在生产镜像中安装开发依赖
- 在镜像中存储密钥（使用环境变量或密钥管理器）
```

## CI/CD管道

### GitHub Actions（标准管道）

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```