import os

# 기본적으로 개발 환경으로 설정
ENVIRONMENT = os.environ.get("DJANGO_ENV", "development")

if ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "development":
    from .development import *
else:
    from .base import *
