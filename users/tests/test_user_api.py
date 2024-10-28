from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from ..models import User


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse("user-signup")
        self.login_url = reverse("token_obtain_pair")
        self.logout_url = reverse("user-logout")
        self.protected_url = reverse("protected")  # 보호된 엔드포인트
        self.user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "nickname": "testuser",
            "name": "Test User",
            "phone_number": "1234567890",
        }

    def test_user_signup(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_user_login(self):
        # 먼저 사용자 생성
        user = User.objects.create_user(**self.user_data)
        print(f"Created user: {user}, is_active: {user.is_active}")
        # 데이터베이스에서 사용자를 다시 조회하여 상태 확인
        saved_user = User.objects.get(email=self.user_data["email"])
        print(f"Saved user: {saved_user}, is_active: {saved_user.is_active}")

        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data)
        print(f"Login response: {response.content}")  # 디버깅을 위해 응답 내용 출력
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_invalid_credentials(self):
        login_data = {"email": "wrong@example.com", "password": "wrongpass"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout(self):
        # 먼저 사용자 생성 및 로그인
        user = User.objects.create_user(**self.user_data)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        # 로그인 상태 확인
        response = self.client.get(self.protected_url)  # 실제 보호된 엔드포인트
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.logout_url, {"refresh": str(refresh)})
        print(f"Logout response: {response.content}")  # 디버깅을 위해 응답 내용 출력
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)

    def test_user_str_method(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data["email"])

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="testpass123")

class UserInfoTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass',
            name='TestName',
            phone_number = '0100001234'
            # 필요한 다른 필드 추가
        )
        self.token = RefreshToken.for_user(self.user)
    
    def test_get_user_info(self):
        # 헤더에 토큰 추가
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))
        response = self.client.get(reverse('user-info', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_user_info(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))
        response = self.client.put(reverse('user-info', args=[self.user.id]), {
            'email': 'new_email@example.com',
            'password': 'newPass',
            'nickname': 'testnew',
            'name': 'New Name',
            'phone_number': '0001231231'  # 필요한 다른 필드 추가
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_user_info(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token.access_token))
        response = self.client.delete(reverse('user-info', args=[self.user.id]))
        self.assertEqual(response.status_code, 204)