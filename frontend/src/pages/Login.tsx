import { useState } from 'react'
import { Form, Input, Button, Card, Typography, message } from 'antd'
import { UserOutlined, LockOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { authApi } from '../services/api'
import { useAuth } from '../hooks/useAuth'
import type { LoginRequest } from '../types'

const { Title, Text } = Typography

function Login() {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login } = useAuth()

  const onFinish = async (values: LoginRequest) => {
    setLoading(true)
    try {
      const tokenResponse = await authApi.login(values)
      const userData = await authApi.getCurrentUser()
      
      login(tokenResponse.access_token, userData)
      message.success('登录成功')
      navigate('/chat')
    } catch (error: any) {
      message.error(error.response?.data?.message || '登录失败，请检查用户名和密码')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <Card
        style={{
          width: 400,
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: 24 }}>
          <Title level={2} style={{ color: '#667eea' }}>
            AI Chat
          </Title>
          <Text type="secondary">智能对话助手</Text>
        </div>

        <Form
          name="login"
          onFinish={onFinish}
          autoComplete="off"
          size="large"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="用户名"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: '请输入密码' }]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="密码"
            />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
              style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none'
              }}
            >
              登录
            </Button>
          </Form.Item>

          <div style={{ textAlign: 'center' }}>
            <Text type="secondary">
              还没有账号？{' '}
              <a href="/register" style={{ color: '#667eea' }}>
                立即注册
              </a>
            </Text>
          </div>
        </Form>
      </Card>
    </div>
  )
}

export default Login
