---
name: django-tdd
description: 使用pytest-django、TDD方法、factory_boy、模拟、覆盖率和测试Django REST Framework API的Django测试策略。
origin: ECC
---

# 使用TDD进行Django测试

使用pytest、factory_boy和Django REST Framework进行Django应用程序的测试驱动开发。

## 激活时机

- 编写新的Django应用程序
- 实现Django REST Framework API
- 测试Django模型、视图和序列化器
- 为Django项目设置测试基础设施

## Django的TDD工作流

### 红-绿-重构循环

```python
# 步骤1：红 - 编写失败的测试
def test_user_creation():
    user = User.objects.create_user(email='test@example.com', password='testpass123')
    assert user.email == 'test@example.com'
    assert user.check_password('testpass123')
    assert not user.is_staff

# 步骤2：绿 - 使测试通过
# 创建User模型或工厂

# 步骤3：重构 - 在保持测试通过的同时改进
```

## 设置

### pytest配置

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --reuse-db
    --nomigrations
    --cov=apps
    --cov-report=html
    --cov-report=term-missing
    --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

### 测试设置

```python
# config/settings/test.py
from .base import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# 禁用迁移以提高速度
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# 更快的密码哈希
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# 电子邮件后端
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Celery总是立即执行
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
```

### conftest.py

```python
# tests/conftest.py
import pytest
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture(autouse=True)
def timezone_settings(settings):
    """确保一致的时区。"""
    settings.TIME_ZONE = 'UTC'

@pytest.fixture
def user(db):
    """创建测试用户。"""
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        username='testuser'
    )

@pytest.fixture
def admin_user(db):
    """创建管理员用户。"""
    return User.objects.create_superuser(
        email='admin@example.com',
        password='adminpass123',
        username='admin'
    )

@pytest.fixture
def authenticated_client(client, user):
    """返回已认证的客户端。"""
    client.force_login(user)
    return client

@pytest.fixture
def api_client():
    """返回DRF API客户端。"""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def authenticated_api_client(api_client, user):
    """返回已认证的API客户端。"""
    api_client.force_authenticate(user=user)
    return api_client
```

## Factory Boy

### 工厂设置

```python
# tests/factories.py
import factory
from factory import fuzzy
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from apps.products.models import Product, Category

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    """User模型的工厂。"""

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True

class CategoryFactory(factory.django.DjangoModelFactory):
    """Category模型的工厂。"""

    class Meta:
        model = Category

    name = factory.Faker('word')
    slug = factory.LazyAttribute(lambda obj: obj.name.lower())
    description = factory.Faker('text')

class ProductFactory(factory.django.DjangoModelFactory):
    """Product模型的工厂。"""

    class Meta:
        model = Product

    name = factory.Faker('sentence', nb_words=3)
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(' ', '-'))
    description = factory.Faker('text')
    price = fuzzy.FuzzyDecimal(10.00, 1000.00, 2)
    stock = fuzzy.FuzzyInteger(0, 100)
    is_active = True
    category = factory.SubFactory(CategoryFactory)
    created_by = factory.SubFactory(UserFactory)
```