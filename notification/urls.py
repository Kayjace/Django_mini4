from django.urls import path

from .views import (
    CreateNotificationView,
    DeleteNotification,
    MarkNotificationAsRead,
    UnreadNotificationList,
)

urlpatterns = [
    path("unread/", UnreadNotificationList.as_view(), name="unread_notifications"),
    path("create/", CreateNotificationView.as_view(), name="notification-list-create"),
    path(
        "<int:pk>/read/",
        MarkNotificationAsRead.as_view(),
        name="mark_notification_as_read",
    ),
    path("<int:pk>/", DeleteNotification.as_view(), name="delete_notification"),
]
