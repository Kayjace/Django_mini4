import re

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a user with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")

        # 이메일 형식 검증
        self.validate_email(email)

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 비밀번호 해싱
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", True)

        return self.create_user(email, password, **extra_fields)

    @staticmethod
    def validate_email(email):
        """이메일 형식 검증"""
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            raise ValidationError("Invalid email format.")


class User(AbstractBaseUser, PermissionsMixin):  # PermissionsMixin 추가
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()  # 사용자 매니저 설정

    USERNAME_FIELD = "email"  # 로그인 시 사용할 필드
    REQUIRED_FIELDS = []  # 필수 필드 (email 외에 추가 필드가 필요하면 여기에 추가)

    class Meta:
        db_table = "users"  # 테이블 이름 설정
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """스태프 및 어드민 사용자만 권한을 가집니다."""
        return self.is_staff or self.is_admin

    def has_module_perms(self, app_label):
        """스태프 및 어드민 사용자만 모듈 권한을 가집니다."""
        return self.is_staff or self.is_admin
