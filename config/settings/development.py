from celery.schedules import crontab
from django.contrib.auth import get_user_model
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

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# 기본 스케줄 설정
CELERY_BEAT_SCHEDULE = {}
