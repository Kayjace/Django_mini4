from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User  # User 모델을 임포트합니다.
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account  # Account 모델을 임포트합니다


class AccountTests(APITestCase):
    def setUp(self):
        try:
            # 사용자 생성
            self.user = User.objects.create_user(
                email="test_user@example.com",
                password="password123",
                nickname="test_nickname",
                name="Test User",
                phone_number="1234567890",
            )

            # JWT 토큰 생성
            self.token = RefreshToken.for_user(self.user)

            # 고유한 계좌 번호 생성
            self.account_data = {
                "user": self.user,  # User 인스턴스를 사용해야 합니다.
                "account_number": "1234567890",  # 고유한 계좌 번호 사용
                "bank_code": "001",  # 예시 은행 코드
                "account_type": "checking",  # 예시 계좌 유형
                "balance": 1000.00,
            }
            self.account = Account.objects.create(**self.account_data)
        except Exception as e:
            print(f"Error in setUp: {e}")

    def authenticate(self):
        """JWT 토큰을 사용하여 인증"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))

    def test_create_account(self):
        self.authenticate()  # 인증 수행

        new_account_data = {
            "user": self.user.id,  # User ID를 사용하여 인스턴스를 참조합니다.
            "account_number": "9876543210",  # 다른 고유한 계좌 번호 사용
            "bank_code": "001",
            "account_type": "checking",
            "balance": 1000.00,
        }

        response = self.client.post(reverse("account-list-create"), new_account_data)

        if response.status_code != status.HTTP_201_CREATED:
            print(f"Failed to create account: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_account(self):
        self.authenticate()  # 인증 수행

        response = self.client.get(reverse("account-detail", args=[self.account.id]))

        if response.status_code != status.HTTP_200_OK:
            print(f"Failed to retrieve account: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_account(self):
        self.authenticate()  # 인증 수행

        updated_data = {"balance": 1500.00}
        response = self.client.patch(
            reverse("account-detail", args=[self.account.id]), updated_data
        )

        if response.status_code != status.HTTP_200_OK:
            print(f"Failed to update account: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.account.refresh_from_db()

        # 잔액이 업데이트되었는지 확인
        self.assertEqual(self.account.balance, 1500.00)

    def test_delete_account(self):
        self.authenticate()  # 인증 수행

        response = self.client.delete(reverse("account-detail", args=[self.account.id]))

        if response.status_code != status.HTTP_204_NO_CONTENT:
            print(f"Failed to delete account: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 계좌가 삭제되었는지 확인
        self.assertFalse(Account.objects.filter(id=self.account.id).exists())


class AccountAPITests(APITestCase):

    def setUp(self):
         try:
             self.user = User.objects.create_user(
                 email='test@example.com',
                 password='testpass'
             )

             # JWT 토큰 생성
             self.token = RefreshToken.for_user(self.user)

             # 고유한 계좌 번호 생성 (여기서도 필요할 경우)
             self.account_data = {
                 "user": self.user,  # User 인스턴스를 사용해야 합니다.
                 "account_number": "1234567890",  
                 "bank_code": "001",  
                 "account_type": "checking",  
                 "balance": 1000.00,
             }
             self.account = Account.objects.create(**self.account_data)
         except Exception as e:
             print(f"Error in setUp: {e}")

    def authenticate(self):
         """JWT 토큰을 사용하여 인증"""
         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))

    def test_create_account(self):
         self.authenticate()  

         response = self.client.post(reverse('account-list-create'), {
             'user': self.user.id,  # User ID를 사용하여 인스턴스를 참조합니다.
             'account_number': '1234567891',  # 다른 고유한 계좌 번호 사용
             'bank_code': '001',
             'account_type': 'checking',
             'balance': 1000,
         })

         if response.status_code != status.HTTP_201_CREATED:
             print(f"Failed to create account: {response.data}")

         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_accounts(self):
         self.authenticate()  
         
         response = self.client.get(reverse('account-list-create'))
         
         if response.status_code != status.HTTP_200_OK:
             print(f"Failed to retrieve accounts: {response.data}")

         self.assertEqual(response.status_code, status.HTTP_200_OK)