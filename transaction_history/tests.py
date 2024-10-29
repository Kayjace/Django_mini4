from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Account
from transaction_history.models import TransactionHistory
from users.models import User


class TransactionHistoryTests(APITestCase):
    def setUp(self):
        # 사용자 생성
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass"
        )

        # JWT 토큰 생성
        self.token = RefreshToken.for_user(self.user)

        # 계좌 생성
        self.account = Account.objects.create(
            user=self.user,
            account_number="123456789",
            bank_code="001",
            account_type="savings",
            balance=1000.00,
        )

    def authenticate(self):
        """JWT 토큰을 사용하여 인증"""
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(self.token.access_token)
        )

    def test_create_transaction(self):
        self.authenticate()  # 인증 수행

        url = reverse("transaction-list-create")
        data = {
            "account": self.account.id,
            "amount": 200.00,
            "description": "Deposit",
            "transaction_type": "deposit",
            "transaction_method": "online",
        }

        response = self.client.post(url, data, format="json")

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 거래 내역이 생성되었는지 확인
        self.assertEqual(TransactionHistory.objects.count(), 1)

        # 계좌 잔액이 업데이트 되었는지 확인
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 1200.00)  # 초기 잔액 1000 + 200

    def test_list_transactions(self):
        # 거래 내역 생성
        TransactionHistory.objects.create(
            account=self.account,
            amount=100.00,
            description="Withdrawal",
            transaction_type="withdrawal",
            transaction_method="ATM",
        )

        url = reverse("transaction-list-create")

        self.authenticate()  # 인증 수행

        response = self.client.get(url)

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 거래 내역이 반환되었는지 확인
        self.assertEqual(len(response.data), 1)

    def test_retrieve_transaction(self):
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=100.00,
            description="Withdrawal",
            transaction_type="withdrawal",
            transaction_method="ATM",
        )

        url = reverse("transaction-detail", args=[transaction.id])

        self.authenticate()  # 인증 수행

        response = self.client.get(url)

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 거래 내역 데이터가 올바른지 확인
        self.assertEqual(response.data["description"], transaction.description)

    def test_update_transaction(self):
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=100.00,
            description="Withdrawal",
            transaction_type="withdrawal",
            transaction_method="ATM",
        )

        url = reverse("transaction-detail", args=[transaction.id])

        data = {
            "account": self.account.id,
            "amount": 50.00,
            "description": "Updated Withdrawal",
            "transaction_type": "withdrawal",
            "transaction_method": "ATM",
        }

        self.authenticate()  # 인증 수행

        response = self.client.put(url, data, format="json")

        # 응답 상태 코드 확인
        if response.status_code != status.HTTP_200_OK:
            print(f"Failed to update transaction: {response.data}")  # 오류 메시지 출력

        if self.assertEqual(response.status_code, status.HTTP_200_OK):
            # 계좌 잔액이 자동으로 업데이트 되었는지 확인 (잔액 계산 방식에 따라 다름)
            expected_balance_after_update = 950  # 초기 잔액 - (기존 금액 - 새 금액)
            self.account.refresh_from_db()
            self.assertEqual(self.account.balance, expected_balance_after_update)

    def test_delete_transaction(self):
        transaction = TransactionHistory.objects.create(
            account=self.account,
            amount=100.00,
            description="Withdrawal",
            transaction_type="withdrawal",
            transaction_method="ATM",
        )

        url = reverse("transaction-detail", args=[transaction.id])

        self.authenticate()  # 인증 수행

        response = self.client.delete(url)

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 거래 내역이 삭제되었는지 확인
        self.assertEqual(TransactionHistory.objects.count(), 0)
