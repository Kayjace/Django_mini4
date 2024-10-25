from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mini4',
        'USER': 'admin',
        'PASSWORD': '0000',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}