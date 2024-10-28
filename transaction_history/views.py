from rest_framework import generics

from .models import TransactionHistory
from .serializers import TransactionHistorySerializer


class TransactionHistoryListCreateView(generics.ListCreateAPIView):
    queryset = TransactionHistory.objects.all()
    serializer_class = TransactionHistorySerializer


class TransactionHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransactionHistory.objects.all()
    serializer_class = TransactionHistorySerializer
