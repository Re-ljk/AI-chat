import { useState, useEffect } from 'react'

const AUTH_CHANGED_EVENT = 'auth-changed'

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false)
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('token')
      const userData = localStorage.getItem('user')
      
      console.log('useAuth checkAuth - token:', token)
      console.log('useAuth checkAuth - userData:', userData)
      
      if (token && userData) {
        setIsAuthenticated(true)
        setUser(JSON.parse(userData))
      } else {
        setIsAuthenticated(false)
        setUser(null)
      }
    }

    checkAuth()

    const handleAuthChange = () => {
      console.log('useAuth handleAuthChange - auth state changed')
      checkAuth()
    }

    window.addEventListener(AUTH_CHANGED_EVENT, handleAuthChange)
    
    return () => {
      window.removeEventListener(AUTH_CHANGED_EVENT, handleAuthChange)
    }
  }, [])

  const login = (token: string, userData: any) => {
    console.log('useAuth login - setting token and user data')
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(userData))
    setIsAuthenticated(true)
    setUser(userData)
    
    window.dispatchEvent(new CustomEvent(AUTH_CHANGED_EVENT, { detail: { isAuthenticated: true } }))
  }

  const logout = () => {
    console.log('useAuth logout - clearing token and user data')
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    setUser(null)
    
    window.dispatchEvent(new CustomEvent(AUTH_CHANGED_EVENT, { detail: { isAuthenticated: false } }))
  }

  return {
    isAuthenticated,
    user,
    login,
    logout
  }
}
