import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RequestList from './pages/RequestList';
import Login from './pages/Login';
import CreateRequest from './pages/CreateRequest';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        {/* 네비게이션 */}
        <nav className="navbar">
          <h1>VideoMarket</h1>
          <div className="nav-links">
            <a href="/">의뢰 목록</a>
            <a href="/create">의뢰 등록</a>
            <a href="/login">로그인</a>
          </div>
        </nav>

        {/* 라우팅 - main 태그 없이 */}
        <Routes>
          <Route path="/" element={
            <main className="main-content">
              <RequestList />
            </main>
          } />
          <Route path="/create" element={<CreateRequest />} /> 
          <Route path="/login" element={<Login />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;