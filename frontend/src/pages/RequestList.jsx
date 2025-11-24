import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { requestsAPI } from '../services/requests';

function RequestList() {
  const navigate = useNavigate();
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      setLoading(true);
      const response = await requestsAPI.getRequests();
      setRequests(response.data);
    } catch (err) {
      setError('의뢰 목록을 불러오는데 실패했습니다.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">로딩 중...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="request-list">
      <h1>의뢰 목록</h1>
      <div className="requests-grid">
        {requests.map((request) => (
          <div 
            key={request.id} 
            className={`request-card ${request.is_mine ? 'my-request' : ''}`}
            onClick={() => navigate(`/request/${request.id}`)}
          >
            <h3>
              {request.title}
              {request.is_mine && <span className="badge-mine">내 의뢰</span>}
            </h3>
            <p>{request.concept}</p>
            <div className="request-info">
              <span>스타일: {request.style}</span>
              <span>길이: {request.duration}초</span>
              <span className="reward">💰 {request.reward} 코인</span>
            </div>
            <div className="request-meta">
              <span>
                의뢰자: {request.requester.username}
                {request.is_anonymous && <span className="badge-anonymous"> 익명</span>}
              </span>
              <span className={`status ${request.status}`}>
                {request.status === 'open' ? '대기중' : 
                 request.status === 'in_progress' ? '진행중' : '완료'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RequestList;