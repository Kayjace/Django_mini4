from django.test import TestCase

from accounts.models import Account
from transaction_history.models import TransactionHistory
from users.models import User


class TransactionHistoryModelTestCase(TestCase):
    def setUp(self):
        # Given: 테스트용 사용자 및 계좌 생성
        self.user = User.objects.create_user(
            email="testuser@example.com",
            nickname="testuser",
            password="testpassword1234",
        )
        self.account = Account.objects.create(
            user=self.user,
            account_number="1234567890",
            bank_code="001",
            account_type="checking",
            balance=1000.00,
        )

        self.transaction_data = {
            "account": self.account,
            "amount": 100.00,
            "balance_after_transaction": 900.00,
            "description": "Test deposit",
            "transaction_type": "deposit",
            "transaction_method": "online",
        }

    def test_create_transaction_history(self):
        # When: 입력 받은 데이터를 바탕으로 거래 기록 모델을 생성하면
        transaction = TransactionHistory.objects.create(**self.transaction_data)

        # Then: 성공적으로 생성된 거래 기록 모델은 입력받은 데이터와 일치해야 한다.
        self.assertEqual(transaction.amount, self.transaction_data["amount"])
        self.assertEqual(
            transaction.balance_after_transaction,
            self.transaction_data["balance_after_transaction"],
        )
        self.assertEqual(transaction.description, self.transaction_data["description"])
        self.assertEqual(
            transaction.transaction_type, self.transaction_data["transaction_type"]
        )
        self.assertEqual(
            transaction.transaction_method, self.transaction_data["transaction_method"]
        )
        self.assertEqual(transaction.account, self.account)
