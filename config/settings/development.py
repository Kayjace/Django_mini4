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


User = get_user_model()

# 기본 스케줄 설정
CELERY_BEAT_SCHEDULE = {}

# 모든 사용자에 대해 작업 실행
users = User.objects.all()
for user in users:
    CELERY_BEAT_SCHEDULE[f"analyze-task-every-day-{user.id}"] = {
        "task": "analysis.tasks.analyze_transactions",
        "schedule": crontab(hour=0, minute=0),  # 매일 자정에 실행
        "args": (user.id, "2024-01-01", "2024-01-31", "monthly"),  # 예시 인자
    }
