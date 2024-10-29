import os
from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import Account
from notification.models import Notification
from transaction_history.models import TransactionHistory

from .models import Analysis

User = get_user_model()


class AnalysisAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass123", nickname="TestUser"
        )
        self.client.force_authenticate(user=self.user)

        # 테스트용 분석 데이터 생성
        self.analysis = Analysis.objects.create(
            user=self.user,
            about="Test Analysis",
            type="monthly",
            period_start=date.today() - timedelta(days=30),
            period_end=date.today(),
            description="Test description",
        )

    def test_create_analysis(self):
        # 테스트용 계좌 생성
        account = Account.objects.create(
            user=self.user, account_number="1234567890", balance=1000
        )

        # 테스트용 거래 내역 생성
        TransactionHistory.objects.create(
            account=account,
            amount=100,
            transaction_type="deposit",
            transaction_method="online",
            created_at=timezone.now() - timedelta(days=15),
        )
        TransactionHistory.objects.create(
            account=account,
            amount=50,
            transaction_type="withdrawal",
            transaction_method="ATM",
            created_at=timezone.now() - timedelta(days=5),
        )

        url = reverse("analysis-list-create")

        period_start = (timezone.now() - timedelta(days=20)).date()
        period_end = timezone.now().date()

        data = {
            "about": "New Analysis",
            "type": "weekly",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "description": "New test description",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        # 테스트 후 이미지 파일 삭제
        analysis_results_dir = os.path.join(settings.MEDIA_ROOT, "analysis_results")

        # 디렉토리가 존재하면 그 안의 모든 파일 삭제
        if os.path.exists(analysis_results_dir):
            # 마지막 생성된 파일 이름을 가져옵니다.
            files = os.listdir(analysis_results_dir)
            if files:
                # 마지막 생성된 파일 이름 (정렬 후 마지막)
                last_file = sorted(
                    files,
                    key=lambda x: os.path.getmtime(
                        os.path.join(analysis_results_dir, x)
                    ),
                )[-1]
                last_file_path = os.path.join(analysis_results_dir, last_file)

                # 나머지 파일 삭제
                for filename in files:
                    file_path = os.path.join(analysis_results_dir, filename)
                    if file_path != last_file_path and os.path.isfile(file_path):
                        os.remove(file_path)

    def test_list_analysis(self):
        url = reverse("analysis-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_analysis(self):
        url = reverse("analysis-detail", kwargs={"pk": self.analysis.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["about"], "Test Analysis")

    def test_update_analysis(self):
        url = reverse("analysis-detail", kwargs={"pk": self.analysis.pk})
        data = {"about": "Updated Analysis"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Analysis.objects.get(pk=self.analysis.pk).about, "Updated Analysis"
        )

    def test_delete_analysis(self):
        url = reverse("analysis-detail", kwargs={"pk": self.analysis.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Analysis.objects.count(), 0)

    def test_analysis_summary(self):
        url = reverse("analysis-summary")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_analyses"], 1)

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)
        url = reverse("analysis-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AnalysisNotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )

    def test_create_analysis_notification(self):
        analysis = Analysis.objects.create(
            user=self.user,
            about="Test Analysis",
            type="Weekly",
            period_start=date(2023, 1, 1),
            period_end=date(2023, 1, 7),
            description="This is a test analysis.",
        )
        notification = Notification.objects.filter(user=self.user).first()
        self.assertIsNotNone(notification)
        self.assertEqual(
            notification.message,
            f"새로운 분석 '{analysis.about}'이(가) 생성되었습니다. (유형: {analysis.type})",
        )

    def test_update_analysis_notification(self):
        analysis = Analysis.objects.create(
            user=self.user,
            about="Test Analysis",
            type="Weekly",
            period_start=date(2023, 1, 1),
            period_end=date(2023, 1, 7),
            description="This is a test analysis.",
        )
        Notification.objects.all().delete()  # 기존 알림 삭제

        analysis.description = "Updated description"
        analysis.save()

        notification = Notification.objects.filter(user=self.user).first()
        self.assertIsNotNone(notification)
        self.assertEqual(
            notification.message,
            f"분석 '{analysis.about}'이(가) 수정되었습니다. (유형: {analysis.type})",
        )
