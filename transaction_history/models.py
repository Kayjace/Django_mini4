from django.db import models
from accounts.models import Account  # Account 모델을 임포트

class TransactionHistory(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', '입금'),
        ('withdrawal', '출금'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)  # Accounts 테이블과의 외래 키 관계
    amount = models.DecimalField(max_digits=20, decimal_places=2)  # 거래 금액
    balance_after_transaction = models.DecimalField(max_digits=20, decimal_places=2)  # 거래 후 잔액
    description = models.CharField(max_length=255)  # 계좌인자내역(ex. 오픈뱅킹출금, ATM현금입금, 올리브영, 홍콩반점, 나이키 등)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)  # 거래 타입 : 입금 / 출금 중 선택
    transaction_method = models.CharField(max_length=20)  # 거래 방법 (현금, 계좌이체, 자동이체, 카드결제 등)
    transaction_datetime = models.DateTimeField(auto_now_add=True)  # 거래 발생 시간

    class Meta:
        db_table = 'transaction_history'  # 테이블 이름 설정
        verbose_name = 'Transaction History'
        verbose_name_plural = 'Transaction Histories'
        ordering = ['-transaction_datetime']  # 최신 거래가 위로 오도록 정렬

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.transaction_datetime} (Account: {self.account.account_number})"