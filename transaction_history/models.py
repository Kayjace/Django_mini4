from django.db import models, transaction
from accounts.models import Account

class TransactionHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2, blank=True)  # blank=True 추가
    description = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=20)  # 예: withdrawal, deposit
    transaction_method = models.CharField(max_length=50)  # 예: ATM, online

    def save(self, *args, **kwargs):
        with transaction.atomic():  # 트랜잭션 시작
            if self.transaction_type == "withdrawal":
                if self.account.balance < self.amount:
                    raise ValueError("Insufficient funds for withdrawal.")
                self.balance_after_transaction = self.account.balance - self.amount
                self.account.balance -= self.amount
            
            elif self.transaction_type == "deposit":
                self.balance_after_transaction = self.account.balance + self.amount
                self.account.balance += self.amount
            
            else:
                raise ValueError("Invalid transaction type")

            # 계좌 저장 호출
            self.account.save()
            super().save(*args, **kwargs)  # 거래 내역 저장 호출