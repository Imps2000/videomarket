from django.db import models
from django.contrib.auth import get_user_model
from submissions.models import Submission

User = get_user_model()

class Transaction(models.Model):
    """재화 거래 내역"""
    
    TRANSACTION_TYPE_CHOICES = [
        ('payment', '결제 (원본 구매)'),
        ('earning', '수익 (제작 완료)'),
        ('refund', '환불'),
        ('bonus', '보너스'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
        help_text="사용자"
    )
    amount = models.IntegerField(help_text="금액 (+면 수입, -면 지출)")
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
        help_text="거래 타입"
    )
    submission = models.ForeignKey(
        Submission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        help_text="관련 제출물"
    )
    description = models.TextField(blank=True, help_text="거래 설명")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'transactions'
        verbose_name = '거래'
        verbose_name_plural = '거래들'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type}: {self.amount}"