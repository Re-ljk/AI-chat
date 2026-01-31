import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { Layout } from 'antd'
import { useEffect } from 'react'
import Login from './pages/Login'
import Register from './pages/Register'
import Chat from './pages/Chat'
import { useAuth } from './hooks/useAuth'

const { Content } = Layout

function App() {
  const { isAuthenticated } = useAuth()
  const location = useLocation()

  useEffect(() => {
    console.log('App rendered, isAuthenticated:', isAuthenticated, 'location:', location.pathname)
  }, [isAuthenticated, location])

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Content>
        <Routes>
          <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/chat" replace />} />
          <Route path="/register" element={!isAuthenticated ? <Register /> : <Navigate to="/chat" replace />} />
          <Route path="/chat" element={isAuthenticated ? <Chat /> : <Navigate to="/login" replace />} />
          <Route path="/" element={<Navigate to={isAuthenticated ? "/chat" : "/login"} replace />} />
        </Routes>
      </Content>
    </Layout>
  )
}

export default App
