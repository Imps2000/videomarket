import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { submissionsAPI } from '../services/submissions';

function SubmitWork() {
  const { requestId } = useParams();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    description: '',
    show_in_portfolio: true,
  });
  const [videoFile, setVideoFile] = useState(null);
  const [error, setError] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value,
    });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // 비디오 파일 확인
      if (!file.type.startsWith('video/')) {
        setError('비디오 파일만 업로드 가능합니다.');
        return;
      }
      // 파일 크기 확인 (100MB 제한)
      if (file.size > 100 * 1024 * 1024) {
        setError('파일 크기는 100MB 이하여야 합니다.');
        return;
      }
      setVideoFile(file);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!videoFile) {
      setError('영상 파일을 선택해주세요.');
      return;
    }

    try {
      setUploading(true);
      setError('');

      // FormData 생성
      const submitData = new FormData();
      submitData.append('request', requestId);
      submitData.append('original_video', videoFile);
      submitData.append('description', formData.description);
      submitData.append('show_in_portfolio', formData.show_in_portfolio);

      await submissionsAPI.createSubmission(submitData);
      
      // 성공 시 의뢰 상세 페이지로 이동
      navigate(`/request/${requestId}`);
      
    } catch (err) {
      setError('제출 실패: ' + (err.response?.data?.message || '다시 시도해주세요.'));
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="submit-work-page">
      <div className="submit-work-container">
        <button onClick={() => navigate(`/request/${requestId}`)} className="btn-back">
          ← 뒤로가기
        </button>

        <h1>영상 제출하기</h1>
        {error && <div className="error">{error}</div>}

        <form onSubmit={handleSubmit} className="submit-form">
          {/* 파일 업로드 */}
          <div className="form-group">
            <label>영상 파일 *</label>
            <div className="file-upload-area">
              <input
                type="file"
                accept="video/*"
                onChange={handleFileChange}
                className="file-input"
                id="video-file"
              />
              <label htmlFor="video-file" className="file-label">
                {videoFile ? (
                  <div className="file-selected">
                    <span className="file-icon">🎬</span>
                    <span className="file-name">{videoFile.name}</span>
                    <span className="file-size">
                      ({(videoFile.size / (1024 * 1024)).toFixed(2)} MB)
                    </span>
                  </div>
                ) : (
                  <div className="file-placeholder">
                    <span className="upload-icon">📤</span>
                    <span>클릭하여 영상 파일 선택</span>
                    <span className="file-hint">MP4, MOV, AVI 등 (최대 100MB)</span>
                  </div>
                )}
              </label>
            </div>
          </div>

          {/* 설명 */}
          <div className="form-group">
            <label>설명 (선택)</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              placeholder="제작 의도, 특징 등을 설명해주세요."
            />
          </div>

          {/* 포트폴리오 공개 */}
          <div className="form-group checkbox-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="show_in_portfolio"
                checked={formData.show_in_portfolio}
                onChange={handleChange}
              />
              <span>포트폴리오에 공개</span>
            </label>
            <p className="help-text">
              의뢰가 완료되면 프리뷰 영상이 내 포트폴리오에 표시됩니다.
            </p>
          </div>

          {/* 제출 버튼 */}
          <div className="form-actions">
            <button 
              type="button" 
              onClick={() => navigate(`/request/${requestId}`)}
              className="btn-cancel"
              disabled={uploading}
            >
              취소
            </button>
            <button 
              type="submit" 
              className="btn-submit"
              disabled={uploading}
            >
              {uploading ? '업로드 중...' : '제출하기'}
            </button>
          </div>

          {uploading && (
            <div className="upload-notice">
              <p>⏳ 영상을 업로드하고 프리뷰를 생성 중입니다...</p>
              <p>파일 크기에 따라 시간이 걸릴 수 있습니다.</p>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

export default SubmitWork;