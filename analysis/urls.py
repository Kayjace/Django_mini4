from django.urls import path

from .views import AnalysisDetailView, AnalysisListCreateView, AnalysisSummaryView

urlpatterns = [
    path("analysis/", AnalysisListCreateView.as_view(), name="analysis-list-create"),
    path("analysis/<int:pk>/", AnalysisDetailView.as_view(), name="analysis-detail"),
    path("analysis/summary/", AnalysisSummaryView.as_view(), name="analysis-summary"),
]
