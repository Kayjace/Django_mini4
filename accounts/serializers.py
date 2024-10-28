from rest_framework import serializers
from .models import Account
from transaction_history.serializers import TransactionHistorySerializer
from users.models import User  # User 모델을 임포트합니다.

class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionHistorySerializer(many=True, read_only=True)  # 거래 내역 포함
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)  # 사용자 필드 추가

    class Meta:
        model = Account
        fields = ['id', 'user', 'account_number', 'bank_code', 'account_type', 'balance', 'transactions']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # 계좌번호의 끝자리 마스킹 처리
        if 'account_number' in representation:
            representation['account_number'] = representation['account_number'][:-6] + '******'
        return representation

    def create(self, validated_data):
        user = validated_data.pop('user')  # user 정보를 가져옵니다.
        account = Account.objects.create(user=user, **validated_data)  # 계좌 생성
        return account