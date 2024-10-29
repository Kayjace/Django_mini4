import logging
import os
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from django.conf import settings  # 추가된 부분
from django.core.files.base import ContentFile

from transaction_history.models import TransactionHistory

from .models import Analysis

logger = logging.getLogger(__name__)


def analyze_transactions(user, period_start, period_end, analysis_type):
    logger.info(
        f"Analyzing transactions for user {user.id} from {period_start} to {period_end}"
    )

    transactions = TransactionHistory.objects.filter(
        account__user=user, created_at__range=[period_start, period_end]
    )

    logger.info(f"Number of transactions found: {transactions.count()}")

    if not transactions.exists():
        logger.warning("No transactions found for the given period.")
        raise ValueError("No transactions found for the given period.")

    transaction_data = list(
        transactions.values(
            "amount", "transaction_type", "created_at", "account__account_number"
        )
    )
    logger.info(f"Raw transaction data: {transaction_data}")

    df = pd.DataFrame(transaction_data)

    logger.info(f"DataFrame shape: {df.shape}")
    logger.info(f"DataFrame columns: {df.columns}")
    logger.info(f"DataFrame head:\n{df.head().to_string()}")
    logger.info(f"DataFrame info:\n{df.info()}")

    # 데이터 타입 확인 및 변환
    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        logger.info(f"Amount column data types: {df['amount'].dtype}")
        logger.info(f"Amount column unique values: {df['amount'].unique()}")

    # 데이터 분석 (예: 계좌별 총 지출 및 수입 계산)
    if (
        "account__account_number" in df.columns
        and "transaction_type" in df.columns
        and "amount" in df.columns
    ):
        summary = (
            df.groupby(["account__account_number", "transaction_type"])["amount"]
            .sum()
            .unstack()
        )
        logger.info(f"Summary shape: {summary.shape}")
        logger.info(f"Summary:\n{summary.to_string()}")
    else:
        logger.error(f"Required columns are missing. Available columns: {df.columns}")
        raise ValueError("Required columns are missing in the transaction data")

    if summary.empty:
        logger.warning("No numeric data to plot after grouping.")
        raise ValueError("No numeric data to plot after grouping.")

    # 시각화
    plt.figure(figsize=(12, 6))
    summary.plot(kind="bar", stacked=True)
    plt.title("Transaction Summary by Account")
    plt.xlabel("Account Number")
    plt.ylabel("Amount")

    # 이미지를 메모리에 저장
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Analysis 모델 생성
    analysis = Analysis(
        user=user,
        about="Account Transactions",
        type=analysis_type,
        period_start=period_start,
        period_end=period_end,
        description="Analysis of transactions across all accounts within the specified period.",
    )

    # 이미지 파일 저장
    image_file = ContentFile(buffer.getvalue())
    file_name = f"{user.id}_{period_start}_{period_end}.png"

    analysis.result_image.save(file_name, image_file)

    # Analysis 객체 저장
    analysis.save()

    # 이미지 필드 확인
    assert analysis.result_image is not None, "Image field is None after saving."

    # 파일 경로 확인
    original_image_path = os.path.join(settings.MEDIA_ROOT, analysis.result_image.name)
    assert os.path.exists(
        original_image_path
    ), "Image file does not exist at expected path."

    logger.info(f"Analysis created successfully: {analysis.id}")

    return {
        "id": analysis.id,
        "user": user.id,
        "about": analysis.about,
        "type": analysis.type,
        "period_start": analysis.period_start,
        "period_end": analysis.period_end,
        "description": analysis.description,
        "result_image": analysis.result_image.url if analysis.result_image else None,
        "created_at": analysis.created_at,
        "updated_at": analysis.updated_at,
    }
