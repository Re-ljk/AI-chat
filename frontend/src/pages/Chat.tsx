import { useState, useEffect, useRef } from 'react'
import { Layout, List, Input, Button, Card, Typography, Space, message, Modal, Drawer, Tag, Tooltip, Spin, Popover } from 'antd'
import { 
  PlusOutlined, 
  DeleteOutlined, 
  SendOutlined, 
  MessageOutlined,
  RobotOutlined,
  UserOutlined,
  CopyOutlined,
  ThunderboltOutlined,
  StopOutlined,
  RedoOutlined,
  SettingOutlined,
  SearchOutlined,
  EditOutlined,
  DownloadOutlined,
  StarOutlined,
  StarFilled,
  BellOutlined,
  SmileOutlined,
  UploadOutlined
} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { conversationApi } from '../services/api'
import { useAuth } from '../hooks/useAuth'
import type { Conversation, Message } from '../types'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import EmojiPicker from 'emoji-picker-react'

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
  const [settingsVisible, setSettingsVisible] = useState(false)
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  const [fontSize, setFontSize] = useState(14)
  const [searchText, setSearchText] = useState('')
  const [editModalVisible, setEditModalVisible] = useState(false)
  const [editingConversation, setEditingConversation] = useState<Conversation | null>(null)
  const [newTitle, setNewTitle] = useState('')
  const [eventSource, setEventSource] = useState<any>(null)
  const [emojiPickerVisible, setEmojiPickerVisible] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [messageSearchText, setMessageSearchText] = useState('')
  const [searchResults, setSearchResults] = useState<number[]>([])
  const [notificationsEnabled, setNotificationsEnabled] = useState(false)
  
  const navigate = useNavigate()
  const { logout, user } = useAuth()
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadConversations()
    if (user) {
      checkLangChainStatus()
    }
  }, [user])

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
      setConversations([newConv, ...(conversations || [])])
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
          setConversations((conversations || []).filter(c => c.id !== id))
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

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setStreaming(true)
    setStreamResponse('')

    try {
      let fullResponse = ''
      
      const source = conversationApi.streamMessage(
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
            setMessages(prev => [...prev, assistantMessage])
            setStreamResponse('')
            showNotification('AI回复', 'AI已生成回复')
          } else if (data.type === 'error') {
            setStreaming(false)
            message.error(data.data.message || '发送消息失败')
            showNotification('错误', data.data.message || '发送消息失败')
          }
        },
        (error) => {
          setStreaming(false)
          message.error('连接失败')
        }
      )
      
      setEventSource(source)
    } catch (error: any) {
      setStreaming(false)
      message.error('发送消息失败')
    }
  }

  const handleEmojiClick = (emojiData: any) => {
    setInputValue(prev => prev + emojiData.emoji)
    setEmojiPickerVisible(false)
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    setUploadedFiles(prev => [...prev, ...files])
  }

  const removeFile = (index: number) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index))
  }

  const handleFileUploadClick = () => {
    fileInputRef.current?.click()
  }

  const searchMessages = (text: string) => {
    setMessageSearchText(text)
    if (!text.trim()) {
      setSearchResults([])
      return
    }
    
    const results: number[] = []
    messages.forEach((msg, index) => {
      if (msg.content.toLowerCase().includes(text.toLowerCase())) {
        results.push(index)
      }
    })
    setSearchResults(results)
  }

  const highlightText = (text: string, highlight: string) => {
    if (!highlight.trim()) return text
    
    const regex = new RegExp(`(${highlight})`, 'gi')
    const parts = text.split(regex)
    
    return parts.map((part, index) => 
      regex.test(part) ? (
        <span key={index} style={{ background: '#ffeb3b', padding: '0 2px', borderRadius: '2px' }}>
          {part}
        </span>
      ) : (
        part
      )
    )
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    message.success('已复制到剪贴板')
  }

  const stopGeneration = () => {
    if (eventSource) {
      eventSource.close()
      setStreaming(false)
      message.info('已停止生成')
    }
  }

  const regenerateLastResponse = async () => {
    if (!currentConversation || messages.length === 0) return
    
    const lastUserMessage = [...messages].reverse().find(m => m.role === 'user')
    if (!lastUserMessage) return

    const userMessage: Message = {
      role: 'user',
      content: lastUserMessage.content,
      timestamp: new Date().toISOString()
    }

    setMessages([...messages, userMessage])
    setInputValue('')
    setStreaming(true)
    setStreamResponse('')

    try {
      let fullResponse = ''
      
      const source = conversationApi.streamMessage(
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
      
      setEventSource(source)
    } catch (error: any) {
      setStreaming(false)
      message.error('发送消息失败')
    }
  }

  const exportMessages = () => {
    if (!currentConversation || messages.length === 0) {
      message.warning('没有可导出的消息')
      return
    }

    const exportData = {
      conversation: {
        id: currentConversation.id,
        title: currentConversation.title,
        model: currentConversation.model,
        created_at: currentConversation.created_at
      },
      messages: messages,
      exported_at: new Date().toISOString()
    }

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `conversation_${currentConversation.title}_${new Date().toISOString().slice(0, 10)}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    message.success('导出成功')
  }

  const openEditModal = (conversation: Conversation, e: React.MouseEvent) => {
    e.stopPropagation()
    setEditingConversation(conversation)
    setNewTitle(conversation.title)
    setEditModalVisible(true)
  }

  const handleEditTitle = async () => {
    if (!editingConversation || !newTitle.trim()) return

    try {
      await conversationApi.updateConversation(editingConversation.id, { title: newTitle })
      setConversations(conversations.map(c => 
        c.id === editingConversation.id ? { ...c, title: newTitle } : c
      ))
      if (currentConversation?.id === editingConversation.id) {
        setCurrentConversation({ ...currentConversation, title: newTitle })
      }
      message.success('修改成功')
      setEditModalVisible(false)
    } catch (error) {
      message.error('修改失败')
    }
  }

  const togglePin = async (conversation: Conversation, e: React.MouseEvent) => {
    e.stopPropagation()
    try {
      const updated = await conversationApi.updateConversation(conversation.id, { 
        is_pinned: !conversation.is_pinned 
      })
      setConversations(conversations.map(c => 
        c.id === conversation.id ? { ...c, is_pinned: !c.is_pinned } : c
      ))
      message.success(conversation.is_pinned ? '已取消置顶' : '已置顶')
    } catch (error) {
      message.error('操作失败')
    }
  }

  const filteredConversations = (conversations || []).filter(conv => 
    conv.title.toLowerCase().includes(searchText.toLowerCase())
  ).sort((a, b) => {
    if (a.is_pinned && !b.is_pinned) return -1
    if (!a.is_pinned && b.is_pinned) return 1
    return 0
  })

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        if (e.key === 'k') {
          e.preventDefault()
          document.querySelector('input[placeholder*="搜索"]')?.dispatchEvent(new Event('focus'))
        } else if (e.key === 'n') {
          e.preventDefault()
          createNewConversation()
        } else if (e.key === 'e') {
          e.preventDefault()
          exportMessages()
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [currentConversation, messages])

  useEffect(() => {
    if ('Notification' in window && notificationsEnabled) {
      Notification.requestPermission().then(permission => {
        if (permission !== 'granted') {
          message.warning('未启用通知权限')
          setNotificationsEnabled(false)
        }
      })
    }
  }, [notificationsEnabled])

  const showNotification = (title: string, body: string) => {
    if (notificationsEnabled && 'Notification' in window && Notification.permission === 'granted') {
      new Notification(title, {
        body,
        icon: '/favicon.ico'
      })
    }
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
            <Input
              placeholder="搜索对话 (Ctrl+K)"
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              allowClear
            />
          </Space>
        </div>

        <div style={{ flex: 1, overflow: 'auto', padding: '8px' }}>
          <List
            dataSource={filteredConversations}
            renderItem={(item) => (
              <List.Item
                style={{
                  padding: '12px',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  background: currentConversation?.id === item.id ? '#f0f7ff' : 'transparent',
                  marginBottom: '8px',
                  border: item.is_pinned ? '1px solid #667eea' : 'none'
                }}
                onClick={() => selectConversation(item)}
                actions={[
                  <Tooltip title="编辑">
                    <Button
                      type="text"
                      icon={<EditOutlined />}
                      onClick={(e) => openEditModal(item, e)}
                    />
                  </Tooltip>,
                  <Tooltip title={item.is_pinned ? '取消置顶' : '置顶'}>
                    <Button
                      type="text"
                      icon={item.is_pinned ? <StarFilled style={{ color: '#667eea' }} /> : <StarOutlined />}
                      onClick={(e) => togglePin(item, e)}
                    />
                  </Tooltip>,
                  <Tooltip title="删除">
                    <Button
                      type="text"
                      danger
                      icon={<DeleteOutlined />}
                      onClick={(e) => deleteConversation(item.id, e)}
                    />
                  </Tooltip>
                ]}
              >
                <List.Item.Meta
                  title={
                    <Space>
                      {item.is_pinned && <StarFilled style={{ color: '#667eea', fontSize: '12px' }} />}
                      {item.title}
                    </Space>
                  }
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
                {messages.length > 0 && (
                  <>
                    <Tooltip title="搜索消息">
                      <Input
                        placeholder="搜索消息"
                        prefix={<SearchOutlined />}
                        value={messageSearchText}
                        onChange={(e) => searchMessages(e.target.value)}
                        style={{ width: 200 }}
                        allowClear
                      />
                    </Tooltip>
                    <Tooltip title="重新生成">
                      <Button
                        icon={<RedoOutlined />}
                        onClick={regenerateLastResponse}
                        disabled={streaming}
                      >
                        重新生成
                      </Button>
                    </Tooltip>
                    <Tooltip title="导出对话 (Ctrl+E)">
                      <Button
                        icon={<DownloadOutlined />}
                        onClick={exportMessages}
                      >
                        导出
                      </Button>
                    </Tooltip>
                  </>
                )}
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
                <Tooltip title="设置">
                  <Button
                    icon={<SettingOutlined />}
                    onClick={() => setSettingsVisible(true)}
                  />
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
                    justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                    animation: 'fadeIn 0.3s ease-in'
                  }}
                >
                  <Card
                    style={{
                      maxWidth: '70%',
                      background: msg.role === 'user' 
                        ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' 
                        : '#fff',
                      color: msg.role === 'user' ? '#fff' : '#333',
                      border: msg.role === 'user' ? 'none' : '1px solid #f0f0f0',
                      fontSize: `${fontSize}px`,
                      borderRadius: msg.role === 'user' ? '20px 20px 4px 20px' : '20px 20px 20px 4px',
                      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                      transition: 'all 0.3s ease'
                    }}
                    hoverable
                  >
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                      {msg.role === 'assistant' && (
                        <div style={{
                          width: '32px',
                          height: '32px',
                          borderRadius: '50%',
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          flexShrink: 0
                        }}>
                          <RobotOutlined style={{ color: '#fff', fontSize: '16px' }} />
                        </div>
                      )}
                      <div style={{ flex: 1 }}>
                        {msg.role === 'assistant' ? (
                          <ReactMarkdown
                            components={{
                              code({ node, inline, className, children, ...props }: any) {
                                const match = /language-(\w+)/.exec(className || '')
                                return !inline && match ? (
                                  <SyntaxHighlighter
                                    style={vscDarkPlus}
                                    language={match[1]}
                                    PreTag="div"
                                    {...props}
                                  >
                                    {String(children).replace(/\n$/, '')}
                                  </SyntaxHighlighter>
                                ) : (
                                  <code className={className} {...props}>
                                    {children}
                                  </code>
                                )
                              }
                            }}
                          >
                            {msg.content}
                          </ReactMarkdown>
                        ) : (
                          <Paragraph style={{ margin: 0, whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>
                            {messageSearchText && searchResults.includes(index)
                              ? highlightText(msg.content, messageSearchText)
                              : msg.content}
                          </Paragraph>
                        )}
                        <Text type={msg.role === 'user' ? 'secondary' : 'secondary'} style={{ 
                          fontSize: '12px', 
                          color: msg.role === 'user' ? 'rgba(255,255,255,0.7)' : undefined,
                          display: 'block',
                          marginTop: '8px'
                        }}>
                          {new Date(msg.timestamp).toLocaleString()}
                        </Text>
                      </div>
                      {msg.role === 'assistant' && (
                        <Button
                          type="text"
                          icon={<CopyOutlined />}
                          onClick={() => copyToClipboard(msg.content)}
                          size="small"
                          style={{ color: msg.role === 'user' ? '#fff' : undefined }}
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
                    justifyContent: 'flex-start',
                    animation: 'fadeIn 0.3s ease-in'
                  }}
                >
                  <Card
                    style={{
                      maxWidth: '70%',
                      background: '#fff',
                      border: '1px solid #f0f0f0',
                      fontSize: `${fontSize}px`,
                      borderRadius: '20px 20px 20px 4px',
                      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                      transition: 'all 0.3s ease'
                    }}
                    hoverable
                  >
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                      <div style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '50%',
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        flexShrink: 0
                      }}>
                        <RobotOutlined style={{ color: '#fff', fontSize: '16px' }} />
                      </div>
                      <div style={{ flex: 1 }}>
                        <ReactMarkdown
                          components={{
                            code({ node, inline, className, children, ...props }: any) {
                              const match = /language-(\w+)/.exec(className || '')
                              return !inline && match ? (
                                <SyntaxHighlighter
                                  style={vscDarkPlus}
                                  language={match[1]}
                                  PreTag="div"
                                  {...props}
                                >
                                  {String(children).replace(/\n$/, '')}
                                </SyntaxHighlighter>
                              ) : (
                                <code className={className} {...props}>
                                  {children}
                                </code>
                              )
                            }
                          }}
                        >
                          {streamResponse}
                        </ReactMarkdown>
                        <Space style={{ marginTop: '8px' }}>
                          <Spin size="small" />
                          <Button
                            type="text"
                            size="small"
                            icon={<StopOutlined />}
                            onClick={stopGeneration}
                            danger
                          >
                            停止生成
                          </Button>
                        </Space>
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
              {uploadedFiles.length > 0 && (
                <div style={{ marginBottom: '12px' }}>
                  <Space wrap>
                    {uploadedFiles.map((file, index) => (
                      <Tag
                        key={index}
                        closable
                        onClose={() => removeFile(index)}
                        style={{
                          background: '#f0f7ff',
                          borderColor: '#667eea',
                          color: '#667eea'
                        }}
                      >
                        {file.name}
                      </Tag>
                    ))}
                  </Space>
                </div>
              )}
              <Space.Compact style={{ width: '100%' }}>
                <Popover
                  content={<EmojiPicker onEmojiClick={handleEmojiClick} />}
                  trigger="click"
                  open={emojiPickerVisible}
                  onOpenChange={setEmojiPickerVisible}
                >
                  <Button icon={<SmileOutlined />} />
                </Popover>
                <Button icon={<UploadOutlined />} onClick={handleFileUploadClick} />
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  style={{ display: 'none' }}
                  onChange={handleFileSelect}
                />
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

      <Drawer
        title="设置"
        placement="right"
        onClose={() => setSettingsVisible(false)}
        open={settingsVisible}
        width={400}
      >
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <div>
            <Paragraph>
              <Text strong>主题</Text>
            </Paragraph>
            <Space>
              <Button
                type={theme === 'light' ? 'primary' : 'default'}
                onClick={() => setTheme('light')}
              >
                浅色
              </Button>
              <Button
                type={theme === 'dark' ? 'primary' : 'default'}
                onClick={() => setTheme('dark')}
              >
                深色
              </Button>
            </Space>
          </div>

          <div>
            <Paragraph>
              <Text strong>字体大小</Text>
            </Paragraph>
            <Space>
              <Button
                size="small"
                onClick={() => setFontSize(Math.max(12, fontSize - 2))}
              >
                -
              </Button>
              <Text>{fontSize}px</Text>
              <Button
                size="small"
                onClick={() => setFontSize(Math.min(20, fontSize + 2))}
              >
                +
              </Button>
            </Space>
          </div>

          <div>
            <Paragraph>
              <Text strong>消息通知</Text>
            </Paragraph>
            <Button
              type={notificationsEnabled ? 'primary' : 'default'}
              onClick={() => setNotificationsEnabled(!notificationsEnabled)}
            >
              {notificationsEnabled ? '已启用' : '已禁用'}
            </Button>
          </div>

          <div>
            <Paragraph>
              <Text strong>快捷键</Text>
            </Paragraph>
            <List
              size="small"
              dataSource={[
                { key: 'Ctrl + K', desc: '搜索对话' },
                { key: 'Ctrl + N', desc: '新建对话' },
                { key: 'Ctrl + E', desc: '导出对话' },
                { key: 'Enter', desc: '发送消息' },
                { key: 'Shift + Enter', desc: '换行' }
              ]}
              renderItem={(item) => (
                <List.Item>
                  <Space style={{ width: '100%', justifyContent: 'space-between' }}>
                    <Text>{item.desc}</Text>
                    <Tag>{item.key}</Tag>
                  </Space>
                </List.Item>
              )}
            />
          </div>
        </Space>
      </Drawer>

      <Modal
        title="编辑对话标题"
        open={editModalVisible}
        onOk={handleEditTitle}
        onCancel={() => setEditModalVisible(false)}
        okText="确定"
        cancelText="取消"
      >
        <Input
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="请输入新标题"
          onPressEnter={handleEditTitle}
          autoFocus
        />
      </Modal>

      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </Layout>
  )
}

export default Chat
