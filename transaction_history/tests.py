from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account  # Account 모델을 임포트합니다.
from users.models import User  # User 모델을 임포트합니다.

from .models import TransactionHistory  # TransactionHistory 모델을 임포트합니다.


class TransactionHistoryTests(APITestCase):
    def setUp(self):
        # 사용자 생성
        self.user = User.objects.create_user(
            email="test_user@example.com",
            password="password123",
            nickname="test_nickname",
            name="Test User",
            phone_number="1234567890",
        )

        # 계좌 생성
        self.account = Account.objects.create(
            user=self.user,
            account_number="1234567890",
            bank_code="001",
            account_type="checking",
            balance=1000.00,
        )

        # 거래 내역 데이터 설정
        self.transaction_data = {
            "account": self.account,  # Account 인스턴스를 직접 사용
            "amount": 100.00,
            "balance_after_transaction": 1100.00,
            "description": "ATM 현금 인출",
            "transaction_type": "withdrawal",
            "transaction_method": "ATM",
        }

    def test_create_transaction(self):
        # Account 인스턴스를 직접 사용
        self.transaction_data["account"] = (
            self.account.id
        )  # Account 인스턴스를 직접 사용
        response = self.client.post(reverse("transaction-list"), self.transaction_data)
        print(response.data)  # 응답 내용을 출력하여 오류 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_transaction(self):
        transaction = TransactionHistory.objects.create(**self.transaction_data)
        response = self.client.get(reverse("transaction-detail", args=[transaction.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], transaction.description)

    def test_update_transaction(self):
        transaction = TransactionHistory.objects.create(**self.transaction_data)
        updated_data = {"amount": 200.00}
        response = self.client.patch(
            reverse("transaction-detail", args=[transaction.id]), updated_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.amount, 200.00)

    def test_delete_transaction(self):
        transaction = TransactionHistory.objects.create(**self.transaction_data)
        response = self.client.delete(
            reverse("transaction-detail", args=[transaction.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TransactionHistory.objects.filter(id=transaction.id).exists())
