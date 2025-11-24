"""
동영상 처리 테스트 스크립트
워터마크 추가 & 저화질 변환 테스트
"""
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import os

def add_watermark(input_path, output_path):
    """워터마크 추가 (간단 버전)"""
    print(f"처리 시작: {input_path}")
    
    # 원본 영상 로드
    video = VideoFileClip(input_path)
    
    try:
        # 텍스트 워터마크 생성 (최소 파라미터)
        txt = TextClip(
            text="PREVIEW",
            font_size=70,
            color='white'
        )
        
        # 워터마크 위치 설정 (중앙)
        txt = txt.with_position('center').with_duration(video.duration)
        
        # 영상과 워터마크 합성
        result = CompositeVideoClip([video, txt])
        
    except Exception as e:
        print(f"⚠️ TextClip 에러: {e}")
        print("워터마크 없이 저장합니다.")
        result = video
    
    # 저장
    result.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac'
    )
    
    print(f"완료: {output_path}")
    
    # 메모리 정리
    video.close()
    result.close()

def reduce_quality(input_path, output_path):
    """저화질 변환"""
    print(f"저화질 변환 시작: {input_path}")
    
    video = VideoFileClip(input_path)
    
    # 해상도 낮추기 (원본의 50%)
    video_resized = video.resized(0.5)
    
    # 저장 (낮은 비트레이트)
    video_resized.write_videofile(
        output_path,
        codec='libx264',
        bitrate='500k',  # 낮은 비트레이트
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )
    
    print(f"완료: {output_path}")
    
    video.close()
    video_resized.close()

if __name__ == "__main__":
    # 테스트용 영상 파일 경로 (본인 파일로 변경)
    input_video = "test_input.mp4"  # 테스트할 영상 파일
    
    if not os.path.exists(input_video):
        print(f"❌ 테스트 영상 파일이 없습니다: {input_video}")
        print("test_input.mp4 파일을 프로젝트 루트에 넣어주세요.")
    else:
        # 워터마크 추가
        add_watermark(input_video, "output_watermark.mp4")
        
        # 저화질 변환
        reduce_quality(input_video, "output_lowquality.mp4")
        
        print("\n✅ 테스트 완료!")
        print("- output_watermark.mp4 (워터마크)")
        print("- output_lowquality.mp4 (저화질)")