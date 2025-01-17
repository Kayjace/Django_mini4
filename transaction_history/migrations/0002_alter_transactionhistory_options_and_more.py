# Generated by Django 5.1.2 on 2024-10-28 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transaction_history", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="transactionhistory",
            options={},
        ),
        migrations.RemoveField(
            model_name="transactionhistory",
            name="transaction_datetime",
        ),
        migrations.AlterField(
            model_name="transactionhistory",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="transactionhistory",
            name="balance_after_transaction",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="transactionhistory",
            name="transaction_method",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="transactionhistory",
            name="transaction_type",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterModelTable(
            name="transactionhistory",
            table=None,
        ),
    ]
