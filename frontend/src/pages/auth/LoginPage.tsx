import React, { useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import Container from '@mui/material/Container'
import Paper from '@mui/material/Paper'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import { LoginForm } from '../../components/forms/LoginForm'
import { useAppDispatch, useAppSelector } from '../../app/hooks'
import { login } from '../../features/auth/authSlice'
import { LoginCredentials } from '../../types/auth.types'
import { notificationService } from '../../services/notification.service'

export const LoginPage: React.FC = () => {
  const dispatch = useAppDispatch()
  const navigate = useNavigate()
  const { isAuthenticated, isLoading, error } = useAppSelector((state) => state.auth)

  useEffect(() => {
    if (isAuthenticated) {
      const user = JSON.parse(localStorage.getItem('user_data') || '{}')
      if (user.role === 'admin') {
        navigate('/admin/dashboard')
      } else if (user.role === 'manager') {
        navigate('/manager/dashboard')
      } else {
        navigate('/driver/my-trips')
      }
    }
  }, [isAuthenticated, navigate])

  const handleSubmit = async (data: LoginCredentials) => {
    const result = await dispatch(login(data))
    if (login.fulfilled.match(result)) {
      notificationService.success('Welcome back!')
    }
  }

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          <LoginForm onSubmit={handleSubmit} isLoading={isLoading} error={error} />
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Typography variant="body2">
              Don't have an account?{' '}
              <Link to="/register">Register here</Link>
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  )
}