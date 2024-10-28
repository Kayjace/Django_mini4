from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # 계좌번호의 끝자리 마스킹
        if "account_number" in representation:
            representation["account_number"] = (
                representation["account_number"][:-6] + "****"
            )
        return representation
