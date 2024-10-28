from .base import *

SECRET_KEY = 'your-hardcoded-secret-key'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
