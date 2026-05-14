export interface User {
  id: number
  email: string
  full_name: string
  role: string
  created_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  email: string
  password: string
  full_name: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user_id: number
  email: string
  role: string
  full_name: string
}

export interface AuthState {
  user: AuthResponse | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}