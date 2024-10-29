# notification/views.py

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializer import NotificationSerializer


class UnreadNotificationList(generics.ListAPIView):
    """사용자의 미확인 알림 목록을 반환하는 뷰"""

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 요청한 사용자의 미확인 알림만 필터링하여 반환
        return Notification.objects.filter(user=self.request.user, is_read=False)


class CreateNotificationView(generics.CreateAPIView):
    """새로운 알림을 생성하는 뷰"""

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 현재 로그인한 사용자와 함께 알림 생성
        serializer.save(user=self.request.user)


class MarkNotificationAsRead(generics.UpdateAPIView):
    """알림을 읽음으로 표시하는 뷰"""

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True  # 읽음으로 표시
        notification.save()
        return Response(
            NotificationSerializer(notification).data, status=status.HTTP_200_OK
        )


class DeleteNotification(generics.DestroyAPIView):
    """알림을 삭제하는 뷰"""

    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.delete()  # 알림 삭제
        return Response(status=status.HTTP_204_NO_CONTENT)
