import api from './api';

// 제출물 관련 API
export const submissionsAPI = {
  // 제출물 생성
  createSubmission: (formData) => api.post('/submissions/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  
  // 의뢰별 제출물 목록
  getRequestSubmissions: (requestId) => api.get(`/submissions/request/${requestId}/`),
  
  // 내 제출물 목록
  getMySubmissions: () => api.get('/submissions/'),
};