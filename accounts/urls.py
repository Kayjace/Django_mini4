from django.urls import path

from .views import AccountDetailView, AccountListCreateView

urlpatterns = [
    path(
        "accounts/", AccountListCreateView.as_view(), name="account-list-create"
    ),  # 계좌 목록 생성 및 조회
    path(
        "accounts/<int:pk>/", AccountDetailView.as_view(), name="account-detail"
    ),  # 특정 계좌 조회, 수정, 삭제
]
