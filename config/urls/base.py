from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("accounts/", include("accounts.urls")),
    path("transaction_history/", include("transaction_history.urls")),
]
