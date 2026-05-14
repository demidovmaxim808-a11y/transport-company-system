import api from './axios'
import { LoginCredentials, RegisterCredentials, AuthResponse } from '../types/auth.types'

export const authAPI = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/auth/login', credentials)
    return response.data
  },

  register: async (credentials: RegisterCredentials): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/auth/register', credentials)
    return response.data
  },
}