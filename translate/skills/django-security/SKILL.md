---
name: django-security
description: Django安全最佳实践、身份验证、授权、CSRF保护、SQL注入预防、XSS预防和安全部署配置。
origin: ECC
---

# Django安全最佳实践

Django应用程序的综合安全指南，以防范常见漏洞。

## 激活时机

- 设置Django身份验证和授权
- 实现用户权限和角色
- 配置生产安全设置
- 审查Django应用程序的安全问题
- 将Django应用程序部署到生产环境

## 核心安全设置

### 生产设置配置

```python
# settings/production.py
import os

DEBUG = False  # 关键：生产中永远不要使用True

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# 安全头
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1年
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS和Cookie
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# 密钥（必须通过环境变量设置）
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured('DJANGO_SECRET_KEY环境变量是必需的')

# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

## 身份验证

### 自定义用户模型

```python
# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """用于更好安全性的自定义用户模型。"""

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = 'email'  # 使用电子邮件作为用户名
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

# settings/base.py
AUTH_USER_MODEL = 'users.User'
```

### 密码哈希

```python
# Django默认使用PBKDF2。为了更强的安全性：
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
```

### 会话管理

```python
# 会话配置
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # 或 'db'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 3600 * 24 * 7  # 1周
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 更好的用户体验，但安全性较低
```

## 授权

### 权限

```python
# models.py
from django.db import models
from django.contrib.auth.models import Permission

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ('can_publish', '可以发布帖子'),
            ('can_edit_others', '可以编辑他人的帖子'),
        ]

    def user_can_edit(self, user):
        """检查用户是否可以编辑此帖子。"""
        return self.author == user or user.has_perm('app.can_edit_others')

# views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    permission_required = 'app.can_edit_others'
    raise_exception = True  # 返回403而不是重定向

    def get_queryset(self):
        """只允许用户编辑自己的帖子。"""
        return Post.objects.filter(author=self.request.user)
```

### 自定义权限

```python
# permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """只允许所有者编辑对象。"""

    def has_object_permission(self, request, view, obj):
        # 任何请求都允许读取权限
        if request.method in permissions.SAFE_METHODS:
            return True

        # 只允许所有者写入权限
        return obj.author == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """允许管理员执行任何操作，其他人只读。"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsVerifiedUser(permissions.BasePermission):
    """只允许已验证的用户。"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_verified
```

### 基于角色的访问控制（RBAC）

```python
# models.py
from django.contrib.auth.models import AbstractUser, Group
```