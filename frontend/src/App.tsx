import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from 'antd'
import Login from './pages/Login'
import Register from './pages/Register'
import Chat from './pages/Chat'
import { useAuth } from './hooks/useAuth'

const { Content } = Layout

function App() {
  const { isAuthenticated } = useAuth()

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Content>
        <Routes>
          <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/chat" />} />
          <Route path="/register" element={!isAuthenticated ? <Register /> : <Navigate to="/chat" />} />
          <Route path="/chat" element={isAuthenticated ? <Chat /> : <Navigate to="/login" />} />
          <Route path="/" element={<Navigate to={isAuthenticated ? "/chat" : "/login"} />} />
        </Routes>
      </Content>
    </Layout>
  )
}

export default App
