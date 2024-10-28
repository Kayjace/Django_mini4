from django.contrib import admin
from django.urls import include, path

from .base import *

urlpatterns = [
    path("users/", include("users.urls")),
]
