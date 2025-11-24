import { useEffect } from 'react';

function VideoModal({ isOpen, onClose, videoUrl, title }) {
  // ESC 키로 닫기
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === 'Escape') onClose();
    };
    
    if (isOpen) {
      document.addEventListener('keydown', handleEsc);
      document.body.style.overflow = 'hidden'; // 스크롤 방지
    }
    
    return () => {
      document.removeEventListener('keydown', handleEsc);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>{title}</h3>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>
        
        <div className="modal-body">
          <video 
            controls 
            autoPlay
            className="video-player"
            src={videoUrl}
          >
            브라우저가 비디오를 지원하지 않습니다.
          </video>
        </div>
        
        <div className="modal-footer">
          <p className="watermark-notice">
            ⚠️ 프리뷰 영상입니다 (워터마크 + 저화질)
          </p>
        </div>
      </div>
    </div>
  );
}

export default VideoModal;