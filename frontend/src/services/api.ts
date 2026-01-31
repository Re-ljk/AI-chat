import axios from 'axios'
import type { 
  LoginRequest, 
  RegisterRequest, 
  TokenResponse,
  Conversation,
  CreateConversationRequest,
  CreateMessageRequest,
  Message,
  ApiResponse 
} from '../types'

const API_BASE_URL = 'http://localhost:19088/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  console.log('Request interceptor - Token from localStorage:', token)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    console.log('Request interceptor - Authorization header:', config.headers.Authorization)
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authApi = {
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const formData = new URLSearchParams()
    formData.append('username', data.username)
    formData.append('password', data.password)
    
    const response = await api.post<TokenResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    return response.data
  },
  
  register: async (data: RegisterRequest): Promise<void> => {
    await api.post('/users/register', data)
  },
  
  getCurrentUser: async (): Promise<any> => {
    const response = await api.get<ApiResponse<any>>('/users/me')
    return response.data.data
  }
}

export const conversationApi = {
  getConversations: async (skip = 0, limit = 100): Promise<Conversation[]> => {
    const response = await api.get<ApiResponse<Conversation[]>>('/conversations/', {
      params: { skip, limit }
    })
    return response.data.data
  },
  
  getConversation: async (id: string): Promise<Conversation> => {
    const response = await api.get<ApiResponse<Conversation>>(`/conversations/${id}`)
    return response.data.data
  },
  
  createConversation: async (data: CreateConversationRequest): Promise<Conversation> => {
    const response = await api.post<ApiResponse<Conversation>>('/conversations/', data)
    return response.data.data
  },
  
  deleteConversation: async (id: string): Promise<void> => {
    await api.delete(`/conversations/${id}`)
  },

  updateConversation: async (id: string, data: Partial<CreateConversationRequest & { is_pinned: boolean }>): Promise<Conversation> => {
    const response = await api.put<ApiResponse<Conversation>>(`/conversations/${id}`, data)
    return response.data.data
  },
  
  getMessages: async (id: string): Promise<Message[]> => {
    const response = await api.get<ApiResponse<Message[]>>(`/conversations/${id}/messages`)
    return response.data.data
  },
  
  addMessage: async (id: string, data: CreateMessageRequest): Promise<Conversation> => {
    const response = await api.post<ApiResponse<Conversation>>(`/conversations/${id}/messages`, data)
    return response.data.data
  },
  
  streamMessage: async (id: string, content: string, onMessage: (data: any) => void, onError: (error: any) => void) => {
    const token = localStorage.getItem('token')
    
    const controller = new AbortController()
    const signal = controller.signal

    try {
      const response = await fetch(`${API_BASE_URL}/conversations/${id}/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ role: 'user', content }),
        signal
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (reader) {
        let buffer = ''
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          const chunk = decoder.decode(value)
          buffer += chunk

          // 处理完整的JSON对象（以\n\n分隔）
          const messages = buffer.split('\n\n')
          for (let i = 0; i < messages.length - 1; i++) {
            const message = messages[i]
            if (message.trim()) {
              try {
                const data = JSON.parse(message)
                onMessage(data)
              } catch (error) {
                console.error('Error parsing SSE message:', error)
              }
            }
          }
          // 保留未处理的部分
          buffer = messages[messages.length - 1]
        }
      }
    } catch (error) {
      if (error.name !== 'AbortError') {
        onError(error)
      }
    }

    return {
      close: () => controller.abort()
    }
  },

  saveStreamMessage: async (id: string, message: Message): Promise<Conversation> => {
    const response = await api.post<ApiResponse<Conversation>>(`/conversations/${id}/stream/save`, message)
    return response.data.data
  },

  getSummary: async (id: string): Promise<{ summary: string, message_count: number }> => {
    const response = await api.get<ApiResponse<{ summary: string, message_count: number }>>(`/conversations/${id}/summary`)
    return response.data.data
  },

  getContext: async (id: string, maxContextLength = 10): Promise<{ context: string, message_count: number, max_context_length: number }> => {
    const response = await api.get<ApiResponse<{ context: string, message_count: number, max_context_length: number }>>(`/conversations/${id}/context`, {
      params: { max_context_length: maxContextLength }
    })
    return response.data.data
  },

  getLangChainStatus: async (): Promise<{ initialized: boolean, message: string }> => {
    const response = await api.get<ApiResponse<{ initialized: boolean, message: string }>>('/conversations/langchain/status')
    return response.data.data
  }
}

export default api
