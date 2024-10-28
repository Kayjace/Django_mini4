import os
from datetime import timedelta

from dotenv import load_dotenv

from .base import *

DEBUG = True

load_dotenv()  # .env 파일 로드

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

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
