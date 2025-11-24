from django.db import models
from django.contrib.auth import get_user_model
from requests.models import Request

User = get_user_model()

class Submission(models.Model):
    """제출된 영상"""
    
    # 연결
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name='submissions',
        help_text="의뢰"
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_submissions',
        help_text="제작자"
    )
    
    # 영상 파일
    original_video = models.FileField(
        upload_to='videos/original/%Y/%m/%d/',
        help_text="원본 영상 (고화질)"
    )
    preview_video = models.FileField(
        upload_to='videos/preview/%Y/%m/%d/',
        null=True,
        blank=True,
        help_text="프리뷰 영상 (저화질 + 워터마크)"
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/%Y/%m/%d/',
        null=True,
        blank=True,
        help_text="썸네일"
    )
    
    # 설명
    description = models.TextField(blank=True, help_text="제작자 코멘트")
    
    # 결제 상태
    is_paid = models.BooleanField(default=False, help_text="결제 완료 여부")
    
    # 타임스탬프
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'submissions'
        verbose_name = '제출물'
        verbose_name_plural = '제출물들'
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.request.title} - {self.creator.username}"