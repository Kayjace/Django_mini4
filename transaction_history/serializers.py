from rest_framework import serializers
from .models import TransactionHistory

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ['id', 'account', 'amount', 'balance_after_transaction', 'description', 'transaction_type', 'transaction_method']
        read_only_fields = ['balance_after_transaction']  # 읽기 전용 필드로 설정

    def create(self, validated_data):
        # 거래 내역 생성 (잔액 업데이트는 모델에서 처리됨)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # 기존 금액과 새로운 금액 비교 후 잔액 조정 (업데이트 로직도 모델에서 처리됨)
        return super().update(instance, validated_data)