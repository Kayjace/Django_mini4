from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/transaction_history/", include("transaction_history.urls")),
    path("analysis/", include("analysis.urls")),
    path("api/notifications/", include("notification.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
