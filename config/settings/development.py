from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_dev_db_name',
        'USER': 'your_dev_user',
        'PASSWORD': 'your_dev_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}