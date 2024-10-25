from django.test import TestCase
from users.models import User
from accounts.models import Account

class AccountModelTestCase(TestCase):
    def setUp(self):
        # Given: 테스트용 사용자 생성
        self.user = User.objects.create_user(
            email='testuser@example.com',
            nickname='testuser',
            password='testpassword1234'
        )
        self.account_data = {
            'user': self.user,
            'account_number': '1234567890',
            'bank_code': '001',
            'account_type': 'checking',
            'balance': 1000.00
        }

    def test_create_account(self):
        # When: 입력 받은 데이터를 바탕으로 계좌 모델을 생성하면
        account = Account.objects.create(**self.account_data)

        # Then: 성공적으로 생성된 계좌 모델은 입력받은 데이터와 일치해야 한다.
        self.assertEqual(account.account_number, self.account_data['account_number'])
        self.assertEqual(account.bank_code, self.account_data['bank_code'])
        self.assertEqual(account.account_type, self.account_data['account_type'])
        self.assertEqual(account.balance, self.account_data['balance'])
        self.assertEqual(account.user, self.user)