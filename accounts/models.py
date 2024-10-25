from django.db import models

from users.models import User  # User 모델을 임포트


class Account(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Users 테이블과의 외래 키 관계
    account_number = models.CharField(max_length=20, unique=True)  # 고유 계좌 번호
    bank_code = models.CharField(max_length=8)  # 은행 코드, 최대 8자리로 임시 설정
    account_type = models.CharField(
        max_length=20
    )  # 계좌 유형 (예: 입출금, 마이너스통장 등)
    """
    추후 
    ACCOUNT_TYPE_CHOICES = [
        ('checking', '입출금 계좌'),
        ('savings', '예금 계좌'),
        ('credit', '신용 계좌'),
    ] 및 
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES) 이용해서 선택지중에 선택하도록 수정 가능.
    """
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 잔액

    class Meta:
        db_table = "accounts"  # 테이블 이름 설정
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return f"{self.user.email} : {self.account_number}"  # 사용자 메일이 먼저 오게 설정. 추후 표기 순서 고려나 메일대신 닉네임 표기 고려
