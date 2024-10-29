from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Analysis

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "nickname"]


class AnalysisSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    result_image = serializers.SerializerMethodField()
    period_start = serializers.DateField(format="%Y-%m-%d")
    period_end = serializers.DateField(format="%Y-%m-%d")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Analysis
        fields = [
            "id",
            "user",
            "about",
            "type",
            "period_start",
            "period_end",
            "description",
            "result_image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def get_result_image(self, obj):
        if obj.result_image:
            return self.context["request"].build_absolute_uri(obj.result_image.url)
        return None

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
