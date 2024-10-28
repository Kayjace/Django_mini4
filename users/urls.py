from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("signup/", views.UserSignupView.as_view(), name="user-signup"),
    path("logout/", views.UserLogoutView.as_view(), name="user-logout"),
    path("login/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/protected/", views.ProtectedView.as_view(), name="protected"),
    path("auth/google/", views.google_login, name="google_login"),  # 구글 로그인 요청
    path(
        "auth/google/callback/", views.google_callback, name="google_callback"
    ),  # 구글 로그인 후 콜백
    path(
        "register_user/<str:email>/<str:name>/",
        views.register_user,
        name="register_user",
    ),  # 추가된 URL 패턴
    path("info/<int:pk>/", views.UserInfoView.as_view(), name="user-info"),
]
