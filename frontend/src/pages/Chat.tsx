import { useState, useEffect, useRef } from 'react'
import { Layout, List, Input, Button, Card, Typography, Space, message, Modal, Drawer, Tag, Tooltip, Spin } from 'antd'
import { 
  PlusOutlined, 
  DeleteOutlined, 
  SendOutlined, 
  MessageOutlined,
  RobotOutlined,
  UserOutlined,
  CopyOutlined,
  ThunderboltOutlined
} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { conversationApi } from '../services/api'
import { useAuth } from '../hooks/useAuth'
import type { Conversation, Message } from '../types'

const { Sider, Content } = Layout
const { TextArea } = Input
const { Title, Text, Paragraph } = Typography

function Chat() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const [streaming, setStreaming] = useState(false)
  const [streamResponse, setStreamResponse] = useState('')
  const [summaryVisible, setSummaryVisible] = useState(false)
  const [summary, setSummary] = useState<{ summary: string, message_count: number } | null>(null)
  const [contextVisible, setContextVisible] = useState(false)
  const [context, setContext] = useState<{ context: string, message_count: number, max_context_length: number } | null>(null)
  const [langChainStatus, setLangChainStatus] = useState<{ initialized: boolean, message: string } | null>(null)
  
  const navigate = useNavigate()
  const { logout, user } = useAuth()
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadConversations()
    checkLangChainStatus()
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages, streamResponse])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadConversations = async () => {
    try {
      const data = await conversationApi.getConversations()
      setConversations(data)
      if (data.length > 0 && !currentConversation) {
        selectConversation(data[0])
      }
    } catch (error: any) {
      message.error('加载对话列表失败')
    }
  }

  const checkLangChainStatus = async () => {
    try {
      const status = await conversationApi.getLangChainStatus()
      setLangChainStatus(status)
    } catch (error) {
      console.error('Failed to check LangChain status:', error)
    }
  }

  const selectConversation = async (conversation: Conversation) => {
    setCurrentConversation(conversation)
    try {
      const msgs = await conversationApi.getMessages(conversation.id)
      setMessages(msgs)
    } catch (error: any) {
      message.error('加载消息失败')
    }
  }

  const createNewConversation = async () => {
    try {
      const newConv = await conversationApi.createConversation({
        title: '新对话',
        model: 'gpt-3.5-turbo'
      })
      setConversations([newConv, ...conversations])
      selectConversation(newConv)
      message.success('创建新对话成功')
    } catch (error: any) {
      message.error('创建对话失败')
    }
  }

  const deleteConversation = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation()
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个对话吗？',
      onOk: async () => {
        try {
          await conversationApi.deleteConversation(id)
          setConversations(conversations.filter(c => c.id !== id))
          if (currentConversation?.id === id) {
            setCurrentConversation(null)
            setMessages([])
          }
          message.success('删除成功')
        } catch (error: any) {
          message.error('删除失败')
        }
      }
    })
  }

  const showSummary = async () => {
    if (!currentConversation) return
    try {
      setLoading(true)
      const data = await conversationApi.getSummary(currentConversation.id)
      setSummary(data)
      setSummaryVisible(true)
    } catch (error: any) {
      message.error('获取对话总结失败')
    } finally {
      setLoading(false)
    }
  }

  const showContext = async () => {
    if (!currentConversation) return
    try {
      setLoading(true)
      const data = await conversationApi.getContext(currentConversation.id)
      setContext(data)
      setContextVisible(true)
    } catch (error: any) {
      message.error('获取对话上下文失败')
    } finally {
      setLoading(false)
    }
  }

  const sendMessage = async () => {
    if (!inputValue.trim() || !currentConversation) return

    const userMessage: Message = {
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    }

    setMessages([...messages, userMessage])
    setInputValue('')
    setStreaming(true)
    setStreamResponse('')

    try {
      let fullResponse = ''
      
      const eventSource = conversationApi.streamMessage(
        currentConversation.id,
        userMessage.content,
        (data) => {
          if (data.type === 'message') {
            fullResponse += data.data.content
            setStreamResponse(fullResponse)
          } else if (data.type === 'done') {
            setStreaming(false)
            
            const assistantMessage: Message = {
              role: 'assistant',
              content: fullResponse,
              timestamp: new Date().toISOString()
            }
            
            conversationApi.saveStreamMessage(currentConversation.id, assistantMessage)
            setMessages([...messages, userMessage, assistantMessage])
            setStreamResponse('')
          } else if (data.type === 'error') {
            setStreaming(false)
            message.error(data.data.message || '发送消息失败')
          }
        },
        (error) => {
          setStreaming(false)
          message.error('连接失败')
        }
      )

      return () => {
        eventSource.close()
      }
    } catch (error: any) {
      setStreaming(false)
      message.error('发送消息失败')
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    message.success('已复制到剪贴板')
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        width={300}
        style={{
          background: '#fff',
          borderRight: '1px solid #f0f0f0',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        <div style={{ padding: '16px', borderBottom: '1px solid #f0f0f0' }}>
          <Space direction="vertical" style={{ width: '100%' }} size="middle">
            <Title level={4} style={{ margin: 0 }}>
              AI Chat
            </Title>
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={createNewConversation}
              block
              style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none'
              }}
            >
              新建对话
            </Button>
          </Space>
        </div>

        <div style={{ flex: 1, overflow: 'auto', padding: '8px' }}>
          <List
            dataSource={conversations}
            renderItem={(item) => (
              <List.Item
                style={{
                  padding: '12px',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  background: currentConversation?.id === item.id ? '#f0f7ff' : 'transparent',
                  marginBottom: '8px'
                }}
                onClick={() => selectConversation(item)}
                actions={[
                  <Button
                    type="text"
                    danger
                    icon={<DeleteOutlined />}
                    onClick={(e) => deleteConversation(item.id, e)}
                  />
                ]}
              >
                <List.Item.Meta
                  title={item.title}
                  description={`${item.content?.length || 0} 条消息`}
                />
              </List.Item>
            )}
          />
        </div>

        <div style={{ padding: '16px', borderTop: '1px solid #f0f0f0' }}>
          <Space direction="vertical" style={{ width: '100%' }} size="small">
            <div>
              <Text strong>{user?.username}</Text>
            </div>
            <Button type="link" onClick={handleLogout} style={{ padding: 0 }}>
              退出登录
            </Button>
          </Space>
        </div>
      </Sider>

      <Content style={{ display: 'flex', flexDirection: 'column', background: '#fafafa' }}>
        {currentConversation ? (
          <>
            <div
              style={{
                padding: '16px 24px',
                background: '#fff',
                borderBottom: '1px solid #f0f0f0',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >
              <Space>
                <Title level={4} style={{ margin: 0 }}>
                  {currentConversation.title}
                </Title>
                {langChainStatus?.initialized && (
                  <Tag color="green" icon={<ThunderboltOutlined />}>
                    LangChain已启用
                  </Tag>
                )}
              </Space>
              <Space>
                <Tooltip title="对话总结">
                  <Button
                    icon={<MessageOutlined />}
                    onClick={showSummary}
                    loading={loading}
                  >
                    总结
                  </Button>
                </Tooltip>
                <Tooltip title="对话上下文">
                  <Button
                    icon={<RobotOutlined />}
                    onClick={showContext}
                    loading={loading}
                  >
                    上下文
                  </Button>
                </Tooltip>
              </Space>
            </div>

            <div
              style={{
                flex: 1,
                overflow: 'auto',
                padding: '24px'
              }}
            >
              {messages.length === 0 && (
                <div
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: '100%',
                    color: '#999'
                  }}
                >
                  <RobotOutlined style={{ fontSize: '64px', marginBottom: '16px' }} />
                  <Text>开始新的对话吧</Text>
                </div>
              )}

              {messages.map((msg, index) => (
                <div
                  key={index}
                  style={{
                    display: 'flex',
                    marginBottom: '24px',
                    justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
                  }}
                >
                  <Card
                    style={{
                      maxWidth: '70%',
                      background: msg.role === 'user' ? '#667eea' : '#fff',
                      color: msg.role === 'user' ? '#fff' : '#333',
                      border: msg.role === 'user' ? 'none' : '1px solid #f0f0f0'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                      {msg.role === 'assistant' && (
                        <RobotOutlined style={{ fontSize: '20px', marginTop: '4px' }} />
                      )}
                      <div style={{ flex: 1 }}>
                        <Paragraph style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
                          {msg.content}
                        </Paragraph>
                        <Text type="secondary" style={{ fontSize: '12px' }}>
                          {new Date(msg.timestamp).toLocaleString()}
                        </Text>
                      </div>
                      {msg.role === 'assistant' && (
                        <Button
                          type="text"
                          icon={<CopyOutlined />}
                          onClick={() => copyToClipboard(msg.content)}
                          size="small"
                        />
                      )}
                    </div>
                  </Card>
                </div>
              ))}

              {streaming && (
                <div
                  style={{
                    display: 'flex',
                    marginBottom: '24px',
                    justifyContent: 'flex-start'
                  }}
                >
                  <Card
                    style={{
                      maxWidth: '70%',
                      background: '#fff',
                      border: '1px solid #f0f0f0'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                      <RobotOutlined style={{ fontSize: '20px', marginTop: '4px' }} />
                      <div style={{ flex: 1 }}>
                        <Paragraph style={{ margin: 0, whiteSpace: 'pre-wrap' }}>
                          {streamResponse}
                        </Paragraph>
                        <Spin size="small" style={{ marginLeft: '8px' }} />
                      </div>
                    </div>
                  </Card>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            <div
              style={{
                padding: '16px 24px',
                background: '#fff',
                borderTop: '1px solid #f0f0f0'
              }}
            >
              <Space.Compact style={{ width: '100%' }}>
                <TextArea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onPressEnter={(e) => {
                    if (!e.shiftKey) {
                      e.preventDefault()
                      sendMessage()
                    }
                  }}
                  placeholder="输入消息，按 Enter 发送，Shift + Enter 换行"
                  autoSize={{ minRows: 1, maxRows: 4 }}
                  disabled={streaming}
                />
                <Button
                  type="primary"
                  icon={<SendOutlined />}
                  onClick={sendMessage}
                  loading={streaming}
                  style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    border: 'none'
                  }}
                >
                  发送
                </Button>
              </Space.Compact>
            </div>
          </>
        ) : (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: '#999'
            }}
          >
            <MessageOutlined style={{ fontSize: '64px', marginBottom: '16px' }} />
            <Text>选择或创建一个对话开始聊天</Text>
          </div>
        )}
      </Content>

      <Drawer
        title="对话总结"
        placement="right"
        onClose={() => setSummaryVisible(false)}
        open={summaryVisible}
        width={400}
      >
        {summary && (
          <div>
            <Paragraph>
              <Text strong>消息数量：</Text> {summary.message_count}
            </Paragraph>
            <Paragraph>
              <Text strong>对话总结：</Text>
            </Paragraph>
            <Paragraph style={{ whiteSpace: 'pre-wrap' }}>
              {summary.summary}
            </Paragraph>
          </div>
        )}
      </Drawer>

      <Drawer
        title="对话上下文"
        placement="right"
        onClose={() => setContextVisible(false)}
        open={contextVisible}
        width={400}
      >
        {context && (
          <div>
            <Paragraph>
              <Text strong>消息数量：</Text> {context.message_count}
            </Paragraph>
            <Paragraph>
              <Text strong>上下文长度：</Text> {context.max_context_length}
            </Paragraph>
            <Paragraph>
              <Text strong>对话上下文：</Text>
            </Paragraph>
            <Paragraph style={{ whiteSpace: 'pre-wrap', background: '#f5f5f5', padding: '12px', borderRadius: '4px' }}>
              {context.context}
            </Paragraph>
          </div>
        )}
      </Drawer>
    </Layout>
  )
}

export default Chat
