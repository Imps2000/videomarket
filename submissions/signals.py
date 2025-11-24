from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Submission
from utils.video_processing import create_preview_video, create_thumbnail
import os
from django.conf import settings

@receiver(post_save, sender=Submission)
def create_preview_on_upload(sender, instance, created, **kwargs):
    """
    Submission 생성 시 자동으로 프리뷰 & 썸네일 생성
    """
    # 새로 생성된 경우에만 (수정 시 재생성 방지)
    if not created:
        return
    
    # 이미 프리뷰가 있으면 스킵
    if instance.preview_video:
        return
    
    print(f"[Signal] Submission {instance.id} 프리뷰 생성 시작")
    
    # 원본 영상 경로
    original_path = instance.original_video.path
    
    # 프리뷰 영상 경로 생성
    original_dir = os.path.dirname(original_path)
    original_name = os.path.basename(original_path)
    name, ext = os.path.splitext(original_name)
    
    # 프리뷰는 같은 폴더에 _preview 붙여서 저장
    preview_filename = f"{name}_preview{ext}"
    preview_path = os.path.join(original_dir, preview_filename)
    
    # 썸네일 경로
    thumbnail_filename = f"{name}_thumb.jpg"
    thumbnail_path = os.path.join(
        settings.MEDIA_ROOT,
        'thumbnails',
        thumbnail_filename
    )
    
    # thumbnails 폴더 생성
    os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
    
    # 프리뷰 생성
    success = create_preview_video(original_path, preview_path)
    
    if success:
        # 프리뷰 경로를 상대 경로로 저장
        relative_preview_path = os.path.relpath(preview_path, settings.MEDIA_ROOT)
        instance.preview_video = relative_preview_path
        
        # 썸네일 생성
        create_thumbnail(preview_path, thumbnail_path)
        
        relative_thumbnail_path = os.path.relpath(thumbnail_path, settings.MEDIA_ROOT)
        instance.thumbnail = relative_thumbnail_path
        
        # 저장 (무한루프 방지: update_fields 사용)
        instance.save(update_fields=['preview_video', 'thumbnail'])
        
        print(f"[Signal] Submission {instance.id} 처리 완료")
    else:
        print(f"[Signal] Submission {instance.id} 처리 실패")