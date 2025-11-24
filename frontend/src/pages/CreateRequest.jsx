import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { requestsAPI } from '../services/requests';

function CreateRequest() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    concept: '',
    style: '',
    duration: '',
    purpose: '',
    request_type: 'global',
    reward: '',
    is_anonymous: false,
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await requestsAPI.createRequest(formData);
      navigate('/');
    } catch (err) {
      setError('의뢰 생성 실패: ' + (err.response?.data?.message || '다시 시도해주세요.'));
    }
  };

  return (
    <div className="create-request-page">
      <div className="create-request-container">
        <h1>새 의뢰 만들기</h1>
        {error && <div className="error">{error}</div>}
        
        <form onSubmit={handleSubmit} className="request-form">
          <div className="form-group">
            <label>제목 *</label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              placeholder="예: 제품 홍보 영상 제작"
            />
          </div>

          <div className="form-group">
            <label>컨셉 *</label>
            <textarea
              name="concept"
              value={formData.concept}
              onChange={handleChange}
              required
              rows="4"
              placeholder="원하시는 영상의 전체적인 분위기와 컨셉을 설명해주세요."
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>스타일 *</label>
              <input
                type="text"
                name="style"
                value={formData.style}
                onChange={handleChange}
                required
                placeholder="예: 모션그래픽"
              />
            </div>

            <div className="form-group">
              <label>길이 (초) *</label>
              <input
                type="number"
                name="duration"
                value={formData.duration}
                onChange={handleChange}
                required
                min="1"
                placeholder="30"
              />
            </div>
          </div>

          <div className="form-group">
            <label>용도 *</label>
            <textarea
              name="purpose"
              value={formData.purpose}
              onChange={handleChange}
              required
              rows="3"
              placeholder="영상의 사용 목적을 알려주세요. (예: SNS 광고, 프레젠테이션 등)"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>의뢰 타입 *</label>
              <select
                name="request_type"
                value={formData.request_type}
                onChange={handleChange}
              >
                <option value="global">글로벌 공개</option>
                <option value="specific">특정 사용자</option>
              </select>
            </div>

            <div className="form-group">
              <label>보상 (코인) *</label>
              <input
                type="number"
                name="reward"
                value={formData.reward}
                onChange={handleChange}
                required
                min="100"
                placeholder="500"
              />
            </div>
          </div>
          <div className="form-group checkbox-group">
            <label className="checkbox-label">
             <input
               type="checkbox"
               name="is_anonymous"
               checked={formData.is_anonymous}
               onChange={handleChange}
           />
            <span>익명으로 의뢰하기</span>
           </label>
           <p className="help-text">체크 시 의뢰자 정보가 표시되지 않습니다.</p>
          </div>
          <div className="form-actions">
            <button type="button" onClick={() => navigate('/')} className="btn-cancel">
              취소
            </button>
            <button type="submit" className="btn-submit">
              의뢰 등록
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateRequest;