import api from './api';

// 의뢰 관련 API
export const requestsAPI = {
  // 의뢰 목록 조회
  getRequests: () => api.get('/requests/'),
  
  // 의뢰 상세 조회
  getRequest: (id) => api.get(`/requests/${id}/`),
  
  // 의뢰 생성
  createRequest: (data) => api.post('/requests/', data),
  
  // 내 의뢰 목록
  getMyRequests: () => api.get('/requests/my/'),
};