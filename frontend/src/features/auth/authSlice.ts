import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { authAPI } from '../../api/auth.api'
import { authService } from '../../services/auth.service'
import { AuthState, LoginCredentials, RegisterCredentials, AuthResponse } from '../../types/auth.types'

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
}

export const login = createAsyncThunk(
  'auth/login',
  async (credentials: LoginCredentials, { rejectWithValue }) => {
    try {
      const response = await authAPI.login(credentials)
      authService.saveAuthData(response)
      return response
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Login failed')
    }
  }
)

export const register = createAsyncThunk(
  'auth/register',
  async (credentials: RegisterCredentials, { rejectWithValue }) => {
    try {
      const response = await authAPI.register(credentials)
      authService.saveAuthData(response)
      return response
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Registration failed')
    }
  }
)

export const checkAuthStatus = createAsyncThunk(
  'auth/checkStatus',
  async (_, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('access_token')
      const user = JSON.parse(localStorage.getItem('user_data') || '{}')
      
      if (token && user) {
        return {
          access_token: token,
          token_type: 'bearer',
          user_id: user.user_id,
          email: user.email,
          role: user.role,
          full_name: user.full_name,
        }
      }
      return rejectWithValue('No auth data')
    } catch (error) {
      return rejectWithValue('Auth check failed')
    }
  }
)

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null
      state.token = null
      state.isAuthenticated = false
      authService.logout()
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(login.fulfilled, (state, action: PayloadAction<AuthResponse>) => {
        state.isLoading = false
        state.isAuthenticated = true
        state.user = action.payload
        state.token = action.payload.access_token
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(register.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(register.fulfilled, (state, action: PayloadAction<AuthResponse>) => {
        state.isLoading = false
        state.isAuthenticated = true
        state.user = action.payload
        state.token = action.payload.access_token
      })
      .addCase(register.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(checkAuthStatus.pending, (state) => {
        state.isLoading = true
      })
      .addCase(checkAuthStatus.fulfilled, (state, action: PayloadAction<AuthResponse>) => {
        state.isLoading = false
        state.isAuthenticated = true
        state.user = action.payload
        state.token = action.payload.access_token
      })
      .addCase(checkAuthStatus.rejected, (state) => {
        state.isLoading = false
        state.isAuthenticated = false
      })
  },
})

export const { logout, clearError } = authSlice.actions
export default authSlice.reducer