from rest_framework import serializers

from .models import TransactionHistory


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = "__all__"  # 모든 필드를 포함해야 합니다.
