import os

from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "DJANGO_MINI4.config.settings.development"
)

app = Celery("DJANGO_MINI4")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
