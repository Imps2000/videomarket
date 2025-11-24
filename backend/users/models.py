from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    사용자 모델
    - 요청자(requester)이자 생성자(creator) 역할
    """
    
    # 재화 시스템
    coins = models.IntegerField(default=1000, help_text="보유 재화")
    
    # 통계
    completed_requests = models.IntegerField(default=0, help_text="완료한 의뢰 수")
    total_earnings = models.IntegerField(default=0, help_text="총 수익")
    
    # 프로필
    profile_image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True,
        help_text="프로필 이미지"
    )
    bio = models.TextField(blank=True, help_text="자기소개")
    
    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'
    
    def __str__(self):
        return self.username