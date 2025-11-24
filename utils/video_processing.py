from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import os

def create_preview_video(original_path, preview_path):
    """
    프리뷰 영상 생성 (워터마크 + 저화질)
    
    Args:
        original_path: 원본 영상 경로
        preview_path: 프리뷰 영상 저장 경로
    
    Returns:
        bool: 성공 여부
    """
    try:
        print(f"프리뷰 생성 시작: {original_path}")
        
        # 원본 로드
        video = VideoFileClip(original_path)
        
        # 해상도 낮추기 (50%)
        video_resized = video.resized(0.5)
        
        # 워터마크 생성
        try:
            txt = TextClip(
                text="PREVIEW",
                font_size=50,
                color='white',
                stroke_color='black',
                stroke_width=2
            )
            txt = txt.with_position('center').with_duration(video_resized.duration)
            
            # 합성
            result = CompositeVideoClip([video_resized, txt])
        except Exception as e:
            print(f"워터마크 생성 실패: {e}, 워터마크 없이 진행")
            result = video_resized
        
        # 저장
        result.write_videofile(
            preview_path,
            codec='libx264',
            bitrate='500k',
            audio_codec='aac',
            logger=None  # 진행바 숨기기
        )
        
        print(f"프리뷰 생성 완료: {preview_path}")
        
        # 메모리 정리
        video.close()
        result.close()
        
        return True
        
    except Exception as e:
        print(f"프리뷰 생성 실패: {e}")
        return False


def create_thumbnail(video_path, thumbnail_path, time=1.0):
    """
    썸네일 생성 (영상의 특정 시점 캡처)
    
    Args:
        video_path: 영상 경로
        thumbnail_path: 썸네일 저장 경로
        time: 캡처 시점 (초)
    
    Returns:
        bool: 성공 여부
    """
    try:
        print(f"썸네일 생성 시작: {video_path}")
        
        video = VideoFileClip(video_path)
        
        # 영상 길이보다 긴 시간이면 중간으로
        if time > video.duration:
            time = video.duration / 2
        
        # 프레임 저장
        frame = video.get_frame(time)
        from PIL import Image
        img = Image.fromarray(frame)
        img.save(thumbnail_path)
        
        video.close()
        
        print(f"썸네일 생성 완료: {thumbnail_path}")
        return True
        
    except Exception as e:
        print(f"썸네일 생성 실패: {e}")
        return False