import api from './axios'
import { UsersListResponse, UserResponse, UserUpdate } from '../types/user.types'

export const usersAPI = {
  getUsers: async (params?: {
    page?: number
    size?: number
    sort_by?: string
    sort_order?: string
    role?: string
  }): Promise<UsersListResponse> => {
    const response = await api.get<UsersListResponse>('/api/users/', { params })
    return response.data
  },

  getUser: async (userId: number): Promise<UserResponse> => {
    const response = await api.get<UserResponse>(`/api/users/${userId}`)
    return response.data
  },

  updateUser: async (userId: number, data: UserUpdate): Promise<UserResponse> => {
    const response = await api.put<UserResponse>(`/api/users/${userId}`, data)
    return response.data
  },

  deleteUser: async (userId: number): Promise<void> => {
    await api.delete(`/api/users/${userId}`)
  },
}