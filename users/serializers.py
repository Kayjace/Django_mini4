from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "nickname", "name", "phone_number")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        print(f"Attempting to validate with attrs: {attrs}")
        credentials = {
            self.username_field: attrs.get(self.username_field),
            "password": attrs.get("password"),
        }
        print(f"Credentials: {credentials}")
        user = authenticate(**credentials)
        print(f"Authenticated user: {user}")

        if user is None or not user.is_active:
            # AuthenticationFailed 예외를 발생시켜 401 상태 코드 반환
            raise AuthenticationFailed(
                "No active account found with the given credentials"
            )

        data = super().validate(attrs)
        return data
