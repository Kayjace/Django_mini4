import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "users",  # Users 테이블을 위한 앱
    "accounts",  # Accounts 테이블을 위한 앱
    "transaction_history",  # Transaction_History 테이블을 위한 앱
    "core",  # wait_for_DB 추가
    "analysis",  # 분석앱
    "django_celery_beat",
    "django_celery_results",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTH_USER_MODEL = "users.User"

SIMPLE_JWT = {
    "USER_ID_FIELD": "email",
    "USER_ID_CLAIM": "email",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),  # 액세스 토큰의 유효 기간
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # 리프레시 토큰의 유효 기간
    "ROTATE_REFRESH_TOKENS": True,  # 리프레시 토큰을 갱신할 때 새로운 리프레시 토큰 발급
    "BLACKLIST_AFTER_ROTATION": True,  # 리프레시 토큰 갱신 후 이전 토큰 블랙리스트 추가
}

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_CALLBACK_URI = os.environ.get("GOOGLE_CALLBACK_URI")

WSGI_APPLICATION = "config.wsgi.application"

# Celery 설정
CELERY_BROKER_URL = "redis://localhost:6379/0"  # Redis를 브로커로 사용할 경우
CELERY_RESULT_BACKEND = "django-db"  # 결과 저장을 위해 Django DB 사용
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Seoul"  # 원하는 시간대 설정

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
