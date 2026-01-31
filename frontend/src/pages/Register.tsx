import { useState } from 'react'
import { Form, Input, Button, Card, Typography, message } from 'antd'
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { authApi } from '../services/api'
import type { RegisterRequest } from '../types'

const { Title, Text } = Typography

function Register() {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const onFinish = async (values: RegisterRequest) => {
    setLoading(true)
    try {
      await authApi.register(values)
      message.success('注册成功，请登录')
      navigate('/login')
    } catch (error: any) {
      message.error(error.response?.data?.message || '注册失败，请稍后重试')
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
          <Text type="secondary">注册新账号</Text>
        </div>

        <Form
          name="register"
          onFinish={onFinish}
          autoComplete="off"
          size="large"
        >
          <Form.Item
            name="username"
            rules={[
              { required: true, message: '请输入用户名' },
              { min: 3, message: '用户名至少3个字符' }
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="用户名"
            />
          </Form.Item>

          <Form.Item
            name="nickname"
            rules={[
              { required: true, message: '请输入昵称' }
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="昵称"
            />
          </Form.Item>

          <Form.Item
            name="email"
            rules={[
              { required: true, message: '请输入邮箱' },
              { type: 'email', message: '请输入有效的邮箱地址' }
            ]}
          >
            <Input
              prefix={<MailOutlined />}
              placeholder="邮箱"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[
              { required: true, message: '请输入密码' },
              { min: 6, message: '密码至少6个字符' }
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="密码"
            />
          </Form.Item>

          <Form.Item
            name="confirmPassword"
            dependencies={['password']}
            rules={[
              { required: true, message: '请确认密码' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve()
                  }
                  return Promise.reject(new Error('两次输入的密码不一致'))
                }
              })
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="确认密码"
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
              注册
            </Button>
          </Form.Item>

          <div style={{ textAlign: 'center' }}>
            <Text type="secondary">
              已有账号？{' '}
              <a href="/login" style={{ color: '#667eea' }}>
                立即登录
              </a>
            </Text>
          </div>
        </Form>
      </Card>
    </div>
  )
}

export default Register
