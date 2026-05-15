import { useCallback } from 'react'
import { useAppDispatch, useAppSelector } from '../app/hooks'
import { login, register, logout } from '../features/auth/authSlice'
import { LoginCredentials, RegisterCredentials } from '../types/auth.types'

export const useAuth = () => {
  const dispatch = useAppDispatch()
  const { user, isAuthenticated, isLoading, error } = useAppSelector(
    (state) => state.auth
  )

  const handleLogin = useCallback(
    async (credentials: LoginCredentials) => {
      return dispatch(login(credentials))
    },
    [dispatch]
  )

  const handleRegister = useCallback(
    async (credentials: RegisterCredentials) => {
      return dispatch(register(credentials))
    },
    [dispatch]
  )

  const handleLogout = useCallback(() => {
    dispatch(logout())
  }, [dispatch])

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login: handleLogin,
    register: handleRegister,
    logout: handleLogout,
  }
}