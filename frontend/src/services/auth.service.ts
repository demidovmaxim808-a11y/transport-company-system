import { storageService } from './storage.service'
import { AuthResponse } from '../types/auth.types'

export const authService = {
  isAuthenticated: (): boolean => {
    const token = storageService.getToken()
    return !!token
  },

  getUserRole: (): string | null => {
    const user = storageService.getUser()
    return user?.role || null
  },

  hasRole: (roles: string[]): boolean => {
    const user = storageService.getUser()
    if (!user) return false
    return roles.includes(user.role)
  },

  saveAuthData: (authData: AuthResponse): void => {
    storageService.setToken(authData.access_token)
    storageService.setUser({
      user_id: authData.user_id,
      email: authData.email,
      role: authData.role,
      full_name: authData.full_name,
    })
  },

  logout: (): void => {
    storageService.clearAll()
  },
}