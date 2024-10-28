import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import path
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer, UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # 쿠키에 토큰 저장 (필요한 경우)
        refresh_token = response.data["refresh"]
        access_token = response.data["access"]

        response.set_cookie(
            key="refresh", value=refresh_token, httponly=True, secure=True
        )  # 필요 시 secure=True 설정
        response.set_cookie(
            key="access", value=access_token, httponly=True, secure=True
        )

        return response


User = get_user_model()


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # 블랙리스트에 추가
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except KeyError:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TokenError:
            return Response(
                {"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view!"})


def google_login(request):
    # 구글 인증 URL로 리다이렉트
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_CALLBACK_URI}"
        "&scope=email profile"
    )
    return redirect(google_auth_url)


def google_callback(request):
    code = request.GET.get("code")

    # 액세스 토큰 요청
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_CALLBACK_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    # 액세스 토큰으로 사용자 정보 요청
    access_token = token_json.get("access_token")
    user_info_response = requests.get(
        f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"
    )

    user_info = user_info_response.json()

    email = user_info["email"]
    name = user_info["name"]

    # 기존 사용자 확인
    try:
        user = User.objects.get(email=email)
        login(request, user)  # 기존 사용자 로그인
        return redirect("/")  # 로그인 후 리다이렉트할 URL
    except User.DoesNotExist:
        # 사용자가 존재하지 않으면 추가 정보 입력 페이지로 리다이렉트
        return redirect(
            "register_user", email=email, name=name
        )  # URL 패턴에 맞게 수정 필요


def register_user(request, email, name):
    if request.method == "POST":
        nickname = request.POST.get("nickname")
        phone_number = request.POST.get("phone_number")

        # 새로운 사용자 생성
        user = User.objects.create(
            email=email,
            nickname=nickname,
            name=name,
            phone_number=phone_number,
            is_active=True,
        )

        login(request, user)  # 로그인 처리
        return redirect("/")  # 가입 후 리다이렉트할 URL

    return render(request, "register_user.html", {"email": email, "name": name})
