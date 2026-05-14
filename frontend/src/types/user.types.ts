export interface UserResponse {
  id: number
  email: string
  full_name: string | null
  role: string
  created_at: string
}

export interface UserUpdate {
  email?: string
  full_name?: string | null
  role?: string
  password?: string
}

export interface UsersListResponse {
  items: UserResponse[]
  total: number
  page: number
  size: number
  pages: number
}