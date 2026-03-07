---
name: django-verification
description: "Django项目的验证循环：迁移、linting、带覆盖率的测试、安全扫描以及发布或PR前的部署就绪检查。"
origin: ECC
---

# Django验证循环

在PR前、重大变更后和部署前运行，以确保Django应用程序的质量和安全性。

## 激活时机

- 为Django项目打开拉取请求之前
- 重大模型变更、迁移更新或依赖升级之后
- 用于 staging 或生产环境的部署前验证
- 运行完整的环境 → lint → 测试 → 安全 → 部署就绪管道
- 验证迁移安全性和测试覆盖率

## 阶段1：环境检查

```bash
# 验证Python版本
python --version  # 应匹配项目要求

# 检查虚拟环境
which python
pip list --outdated

# 验证环境变量
python -c "import os; import environ; print('DJANGO_SECRET_KEY已设置' if os.environ.get('DJANGO_SECRET_KEY') else '缺失：DJANGO_SECRET_KEY')"
```

如果环境配置错误，请停止并修复。

## 阶段2：代码质量与格式化

```bash
# 类型检查
mypy . --config-file pyproject.toml

# 使用ruff进行linting
ruff check . --fix

# 使用black进行格式化
black . --check
black .  # 自动修复

# 导入排序
isort . --check-only
isort .  # 自动修复

# Django特定检查
python manage.py check --deploy
```

常见问题：
- 公共函数上缺少类型提示
- PEP 8格式违规
- 未排序的导入
- 生产配置中保留了调试设置

## 阶段3：迁移

```bash
# 检查未应用的迁移
python manage.py showmigrations

# 创建缺失的迁移
python manage.py makemigrations --check

# 试运行迁移应用
python manage.py migrate --plan

# 应用迁移（测试环境）
python manage.py migrate

# 检查迁移冲突
python manage.py makemigrations --merge  # 仅当存在冲突时
```

报告：
- 待处理迁移的数量
- 任何迁移冲突
- 没有迁移的模型变更

## 阶段4：测试 + 覆盖率

```bash
# 使用pytest运行所有测试
pytest --cov=apps --cov-report=html --cov-report=term-missing --reuse-db

# 运行特定应用的测试
pytest apps/users/tests/

# 使用标记运行
pytest -m "not slow"  # 跳过慢速测试
pytest -m integration  # 仅运行集成测试

# 覆盖率报告
open htmlcov/index.html
```

报告：
- 总测试数：X通过，Y失败，Z跳过
- 总体覆盖率：XX%
- 每个应用的覆盖率细分

覆盖率目标：

| 组件 | 目标 |
|-----------|--------|
| 模型 | 90%+ |
| 序列化器 | 85%+ |
| 视图 | 80%+ |
| 服务 | 90%+ |
| 总体 | 80%+ |

## 阶段5：安全扫描

```bash
# 依赖漏洞
pip-audit
safety check --full-report

# Django安全检查
python manage.py check --deploy

# Bandit安全linter
bandit -r . -f json -o bandit-report.json

# 密钥扫描（如果安装了gitleaks）
gitleaks detect --source . --verbose

# 环境变量检查
python -c "from django.core.exceptions import ImproperlyConfigured; from django.conf import settings; settings.DEBUG"
```

报告：
- 发现的易受攻击的依赖项
- 安全配置问题
- 检测到硬编码的密钥
- DEBUG模式状态（生产中应为False）

## 阶段6：Django管理命令

```bash
# 检查模型问题
python manage.py check

# 收集静态文件
python manage.py collectstatic --noinput --clear

# 创建超级用户（如果测试需要）
echo "from apps.users.models import User; User.objects.create_superuser('admin@example.com', 'admin')" | python manage.py shell

# 数据库完整性
python manage.py check --database default

# 缓存验证（如果使用Redis）
python -c "from django.core.cache import cache; cache.set('test', 'value', 10); print(cache.get('test'))"
```

## 阶段7：性能检查

```bash
# Django Debug Toolbar输出（检查N+1查询）
# 在开发模式下运行DEBUG=True并访问页面
# 在SQL面板中查找重复查询

# 查询计数分析
django-admin debugsqlshell  # 如果安装了django-debug-sqlshell

# 检查缺失的索引
python manage.py shell << EOF
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT table_name, index_name FROM information_schema.statistics WHERE table_schema = 'public'")
    print(cursor.fetchall())
EOF
```

报告：
- 每页的查询数（典型页面应<50）
- 缺失的数据库索引
- 检测到的重复查询

## 阶段8：静态资源

```bash
# 检查npm依赖项（如果使用npm）
npm audit
npm audit fix

# 构建静态文件（如果使用webpack/vite）
npm run build

# 验证静态文件
ls -la staticfiles/
python manage.py findstatic css/style.css
```