from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Request(models.Model):
    """의뢰"""
    
    REQUEST_TYPE_CHOICES = [
        ('global', '글로벌 공개'),
        ('specific', '특정 사용자'),
    ]
    
    STATUS_CHOICES = [
        ('open', '대기중'),
        ('in_progress', '진행중'),
        ('completed', '완료'),
        ('cancelled', '취소'),
    ]
    
    # 의뢰자
    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_requests',
        help_text="의뢰자"
    )
    
    # 의뢰 내용
    title = models.CharField(max_length=200, help_text="제목")
    concept = models.TextField(help_text="컨셉 설명")
    style = models.CharField(max_length=100, help_text="원하는 스타일")
    duration = models.IntegerField(help_text="희망 영상 길이 (초)")
    purpose = models.TextField(help_text="영상 용도")
    
    # 타입 및 금액
    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE_CHOICES,
        default='global',
        help_text="의뢰 타입"
    )
    target_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='targeted_requests',
        help_text="특정 사용자 지정 (선택)"
    )
    reward = models.IntegerField(help_text="보상 재화")
    
    # 상태
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )
    
    # 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'requests'
        verbose_name = '의뢰'
        verbose_name_plural = '의뢰들'
        ordering = ['-created_at']  # 최신순
    
    def __str__(self):
        return f"{self.title} by {self.requester.username}"