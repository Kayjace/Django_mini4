from django.conf import settings
from django.db import models


class Analysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about = models.CharField(max_length=255)  # 어떤 것에 대한 분석인지
    type = models.CharField(max_length=50)  # 기간별 분석 유형 (주간, 월간 등)
    period_start = models.DateField()  # 기간의 시작일
    period_end = models.DateField()  # 기간의 마지막 날
    description = models.TextField()  # 데이터 분석 설명
    result_image = models.ImageField(
        upload_to="analysis_results/", null=True, blank=True
    )  # 시각화한 그래프 이미지
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시점
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시점

    def __str__(self):
        return f"{self.about} - {self.user.username}"
