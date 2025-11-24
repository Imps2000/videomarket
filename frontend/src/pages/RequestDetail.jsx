import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { requestsAPI } from '../services/requests';
import { submissionsAPI } from '../services/submissions';
import VideoModal from '../components/VideoModal';

function RequestDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [request, setRequest] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [currentVideo, setCurrentVideo] = useState(null);

  useEffect(() => {
    fetchRequestDetail();
  }, [id]);

  const fetchRequestDetail = async () => {
    try {
      setLoading(true);
      
      // 의뢰 상세 정보
      const requestRes = await requestsAPI.getRequest(id);
      setRequest(requestRes.data);
      console.log('Request:', requestRes.data); 
      console.log('Is mine?', requestRes.data.is_mine);
      
      // 제출물 목록 (의뢰인만 볼 수 있음)
      try {
        const submissionsRes = await submissionsAPI.getRequestSubmissions(id);
        setSubmissions(submissionsRes.data);
        console.log('Submissions:', submissionsRes.data);  
        console.log('Submissions length:', submissionsRes.data.length);
      } catch (err) {
        console.log('Submissions error:', err);
        setSubmissions([]);
      }
      
    } catch (err) {
      setError('의뢰를 불러오는데 실패했습니다.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  const handlePreview = (submission) => {
    setCurrentVideo({
      url: `http://localhost:8000${submission.preview_video}`,
      title: `${submission.creator.username}의 제출물`
    });
    setModalOpen(true);
  };

  if (loading) return <div className="loading">로딩 중...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!request) return <div className="error">의뢰를 찾을 수 없습니다.</div>;

  return (
    <div className="request-detail-page">
      <div className="request-detail-container">
        <button onClick={() => navigate('/')} className="btn-back">
          ← 목록으로
        </button>

        <div className="request-detail-header">
          <h1>
            {request.title}
            {request.is_mine && <span className="badge-mine">내 의뢰</span>}
          </h1>
          <div className="request-detail-meta">
            <span className={`status ${request.status}`}>
              {request.status === 'open' ? '대기중' : 
               request.status === 'in_progress' ? '진행중' : '완료'}
            </span>
            <span className="reward">💰 {request.reward} 코인</span>
          </div>
        </div>

        <div className="request-detail-body">
          <div className="detail-section">
            <h3>컨셉</h3>
            <p>{request.concept}</p>
          </div>

          <div className="detail-row">
            <div className="detail-section">
              <h3>스타일</h3>
              <p>{request.style}</p>
            </div>
            <div className="detail-section">
              <h3>길이</h3>
              <p>{request.duration}초</p>
            </div>
          </div>

          <div className="detail-section">
            <h3>용도</h3>
            <p>{request.purpose}</p>
          </div>

          <div className="detail-section">
            <h3>의뢰 타입</h3>
            <p>{request.request_type === 'global' ? '글로벌 공개' : '특정 사용자'}</p>
          </div>

          <div className="detail-section">
            <h3>의뢰자</h3>
            <p>{request.requester.username}</p>
          </div>
        </div>

        {request.is_mine && submissions.length > 0 && (
          <div className="submissions-section">
            <h2>제출된 영상 ({submissions.length})</h2>
            <div className="submissions-grid">
              {submissions.map((submission) => (
                <div key={submission.id} className="submission-card">
                  {submission.thumbnail && (
                    <img 
                      src={`http://localhost:8000${submission.thumbnail}`} 
                      alt="썸네일"
                      className="submission-thumbnail"
                    />
                  )}
                  <div className="submission-info">
                    <p className="submission-creator">제작자: {submission.creator.username}</p>
                    <p className="submission-desc">{submission.description}</p>
                    <div className="submission-actions">
                      <button 
                        className="btn-preview"
                        onClick={() => handlePreview(submission)}  // 수정
                      >
                        프리뷰 보기
                      </button>
                      {!submission.is_paid && (
                        <button className="btn-purchase">구매하기</button>
                      )}
                      {submission.is_paid && (
                        <span className="badge-paid">구매 완료</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {!request.is_mine && (request.status === 'open' || request.status === 'in_progress') && (
        <div className="submit-section">
            <button 
            onClick={() => navigate(`/submit/${request.id}`)}
            className="btn-submit-work"
            >
            영상 제출하기
            </button>
        </div>
        )}
      </div>

      {/* 비디오 모달 추가 */}
      <VideoModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        videoUrl={currentVideo?.url}
        title={currentVideo?.title}
      />
    </div>
  );
}

export default RequestDetail;
