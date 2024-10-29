from datetime import datetime

from django.db.models import Count, Max, Min
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .analyzer import analyze_transactions
from .models import Analysis
from .serializer import AnalysisSerializer


class AnalysisListCreateView(generics.ListCreateAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Analysis.objects.filter(user=user)

        # 분석 유형 필터링
        analysis_type = self.request.query_params.get("type")
        if analysis_type:
            queryset = queryset.filter(type=analysis_type)

        # 날짜 범위 필터링
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if start_date and end_date:
            queryset = queryset.filter(
                period_start__gte=start_date, period_end__lte=end_date
            )

        return queryset

    def create(self, request, *args, **kwargs):
        # 분석 생성 로직
        period_start = request.data.get("period_start")
        period_end = request.data.get("period_end")
        analysis_type = request.data.get("type")

        if not all([period_start, period_end, analysis_type]):
            return Response(
                {"error": "Missing required parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            period_start = datetime.strptime(period_start, "%Y-%m-%d").date()
            period_end = datetime.strptime(period_end, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            analysis_data = analyze_transactions(
                request.user, period_start, period_end, analysis_type
            )
            serializer = self.get_serializer(data=analysis_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnalysisDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Analysis.objects.filter(user=self.request.user)


class AnalysisSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        summary = Analysis.objects.filter(user=user).aggregate(
            total_count=Count("id"),
            types_count=Count("type", distinct=True),
            earliest_date=Min("period_start"),
            latest_date=Max("period_end"),
        )

        return Response(
            {
                "total_analyses": summary["total_count"],
                "unique_types": summary["types_count"],
                "earliest_analysis_date": summary["earliest_date"],
                "latest_analysis_date": summary["latest_date"],
            }
        )
