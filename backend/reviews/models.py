from django.db import models
from django.contrib.auth import get_user_model
from submissions.models import Submission

User = get_user_model()

class Review(models.Model):
    """평가 (한 줄 평)"""
    
    # 연결
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name='review',
        help_text="제출물"
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_reviews',
        help_text="평가자 (의뢰자)"
    )
    
    # 평가 내용
    comment = models.TextField(max_length=500, help_text="한 줄 평")
    
    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        verbose_name = '평가'
        verbose_name_plural = '평가들'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review by {self.reviewer.username}"