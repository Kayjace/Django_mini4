from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User  # User 모델을 임포트합니다.

from .models import Account  # Account 모델을 임포트합니다.


class AccountTests(APITestCase):
    def setUp(self):
        # 사용자 생성
        self.user = User.objects.create_user(
            email="test_user@example.com",
            password="password123",
            nickname="test_nickname",
            name="Test User",
            phone_number="1234567890",
        )

        # 고유한 계좌 번호 생성
        self.account_data = {
            "user": self.user,  # User 인스턴스를 직접 사용
            "account_number": "1234567890",  # 고유한 계좌 번호 사용
            "bank_code": "001",  # 예시 은행 코드
            "account_type": "checking",  # 예시 계좌 유형
            "balance": 1000.00,
        }
        self.account = Account.objects.create(**self.account_data)

    def test_create_account(self):
        # 새로운 고유한 계좌 번호로 요청 보내기
        new_account_data = {
            "user": self.user.id,  # User 인스턴스의 ID 사용
            "account_number": "9876543210",  # 다른 고유한 계좌 번호 사용
            "bank_code": "001",
            "account_type": "checking",
            "balance": 1000.00,
        }
        response = self.client.post(reverse("account-list"), new_account_data)
        print(response.data)  # 응답 내용을 출력하여 오류 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_account(self):
        response = self.client.get(reverse("account-detail", args=[self.account.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 원래 계좌번호와 비교
        self.assertEqual(response.data["account_number"], self.account.account_number)

        # 마스킹된 계좌번호가 올바르게 생성되었는지 확인
        expected_masked_account_number = self.account.account_number[:-4] + "****"
        self.assertEqual(
            response.data["masked_account_number"], expected_masked_account_number
        )

    def test_update_account(self):
        updated_data = {"balance": 1500.00}
        response = self.client.patch(
            reverse("account-detail", args=[self.account.id]), updated_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 1500.00)

    def test_delete_account(self):
        response = self.client.delete(reverse("account-detail", args=[self.account.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(id=self.account.id).exists())
