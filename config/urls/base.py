from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/transaction_history/", include("transaction_history.urls")),
]
