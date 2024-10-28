from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("signup/", views.UserSignupView.as_view(), name="user-signup"),
    path("logout/", views.UserLogoutView.as_view(), name="user-logout"),
    path("login/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/protected/", views.ProtectedView.as_view(), name="protected"),
]
