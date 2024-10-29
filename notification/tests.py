# notification/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User  # 사용자 모델 임포트

from .models import Notification


class NotificationTests(APITestCase):

    def setUp(self):
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

        # 알림 데이터 생성
        self.notification_data = {
            "user": self.user,  # User 인스턴스를 사용해야 합니다.
            "message": "Test notification message",
            "is_read": False,
        }
        self.notification = Notification.objects.create(**self.notification_data)

    def authenticate(self):
        """JWT 토큰을 사용하여 인증"""
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(self.token.access_token)
        )

    def test_create_notification(self):
        self.authenticate()  # 인증 수행

        new_notification_data = {
            "user": self.user.id,  # User ID를 사용하여 인스턴스를 참조합니다.
            "message": "New test notification",
            "is_read": False,
        }

        response = self.client.post(
            reverse("notification-list-create"), new_notification_data
        )

        if response.status_code != status.HTTP_201_CREATED:
            print(f"Failed to create notification: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_unread_notifications(self):
        self.authenticate()  # 인증 수행

        response = self.client.get(reverse("unread_notifications"))

        if response.status_code != status.HTTP_200_OK:
            print(f"Failed to retrieve notifications: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # unread notifications count should be 1

    def test_mark_notification_as_read(self):
        self.authenticate()  # 인증 수행

        response = self.client.patch(
            reverse("mark_notification_as_read", args=[self.notification.id])
        )

        if response.status_code != status.HTTP_200_OK:
            print(f"Failed to mark notification as read: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.notification.refresh_from_db()

        # 알림이 읽음으로 표시되었는지 확인
        self.assertTrue(self.notification.is_read)

    def test_delete_notification(self):
        self.authenticate()  # 인증 수행

        response = self.client.delete(
            reverse("delete_notification", args=[self.notification.id])
        )

        if response.status_code != status.HTTP_204_NO_CONTENT:
            print(f"Failed to delete notification: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 알림이 삭제되었는지 확인
        self.assertFalse(Notification.objects.filter(id=self.notification.id).exists())
