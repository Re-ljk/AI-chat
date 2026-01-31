export interface User {
  id: string
  username: string
  nickname: string
  email: string
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  password: string
  nickname: string
  email: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export interface Conversation {
  id: string
  user_id: string
  title: string
  model: string
  content: Message[]
  total_tokens: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface CreateConversationRequest {
  title: string
  model: string
}

export interface CreateMessageRequest {
  role: 'user' | 'assistant'
  content: string
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}
