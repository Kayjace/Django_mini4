from django.urls import path

from .views import TransactionHistoryDetailView, TransactionHistoryListCreateView

urlpatterns = [
    path(
        "transactions/",
        TransactionHistoryListCreateView.as_view(),
        name="transaction-list",
    ),
    path(
        "transactions/<int:pk>/",
        TransactionHistoryDetailView.as_view(),
        name="transaction-detail",
    ),
]
