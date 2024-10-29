from dotenv import load_dotenv

from .base import *

DEBUG = False

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


ALLOWED_HOSTS = ['ec2-13-125-216-236.ap-northeast-2.compute.amazonaws.com', '13.125.216.236']

# S3 Storage
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.environ.get("ACCESS"),
            "secret_key": os.environ.get("SECRET"),
            "bucket_name": os.environ.get("NAME"),
            "region_name": os.environ.get("REGION"),
            "location": "media",
            "default_acl": "public-read",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.environ.get("ACCESS"),
            "secret_key": os.environ.get("SECRET"),
            "bucket_name": os.environ.get("NAME"),
            "region_name": os.environ.get("REGION"),
            "custom_domain": f'{os.environ.get("NAME")}.s3.amazonaws.com',
            "location": "static",
            "default_acl": "public-read",
        },
    },
}

# Static, Media URL
STATIC_URL = f'https://{os.environ.get("NAME")}.s3.amazonaws.com/static/'
MEDIA_URL = f'https://{os.environ.get("NAME")}.s3.amazonaws.com/media/'