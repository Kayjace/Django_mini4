from django.db.models.signals import post_save
from django.dispatch import receiver

from notification.models import Notification

from .models import Analysis


@receiver(post_save, sender=Analysis)
def create_analysis_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"새로운 분석 '{instance.about}'이(가) 생성되었습니다. (유형: {instance.type})",
        )
    else:
        Notification.objects.create(
            user=instance.user,
            message=f"분석 '{instance.about}'이(가) 수정되었습니다. (유형: {instance.type})",
        )
