import api from './api';

// 인증 관련 API
export const authAPI = {
  // 회원가입
  register: (data) => api.post('/users/register/', data),
  
  // 로그인
  login: async (data) => {
    const response = await api.post('/users/login/', data);
    if (response.data.tokens) {
      localStorage.setItem('access_token', response.data.tokens.access);
      localStorage.setItem('refresh_token', response.data.tokens.refresh);
    }
    return response;
  },
  
  // 로그아웃
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
  
  // 내 정보
  getMe: () => api.get('/users/me/'),
};
