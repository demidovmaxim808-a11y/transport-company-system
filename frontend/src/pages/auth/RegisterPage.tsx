import React, { useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import Container from '@mui/material/Container'
import Paper from '@mui/material/Paper'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import { useForm } from 'react-hook-form'
import { AppInput } from '../../components/ui/AppInput'
import { AppButton } from '../../components/ui/AppButton'
import { useAppDispatch, useAppSelector } from '../../app/hooks'
import { register as registerAction } from '../../features/auth/authSlice'
import { RegisterCredentials } from '../../types/auth.types'
import { notificationService } from '../../services/notification.service'

export const RegisterPage: React.FC = () => {
  const dispatch = useAppDispatch()
  const navigate = useNavigate()
  const { isAuthenticated, isLoading, error } = useAppSelector((state) => state.auth)
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterCredentials>()

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/driver/my-trips')
    }
  }, [isAuthenticated, navigate])

  const onSubmit = async (data: RegisterCredentials) => {
    const result = await dispatch(registerAction(data))
    if (registerAction.fulfilled.match(result)) {
      notificationService.success('Registration successful!')
      navigate('/driver/my-trips')
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
          <Typography variant="h5" gutterBottom align="center">
            Register
          </Typography>
          
          <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
            <AppInput
              label="Full Name"
              {...register('full_name', {
                required: 'Full name is required',
              })}
              error={errors.full_name?.message}
            />
            
            <AppInput
              label="Email"
              type="email"
              {...register('email', {
                required: 'Email is required',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: 'Invalid email address',
                },
              })}
              error={errors.email?.message}
            />
            
            <AppInput
              label="Password"
              type="password"
              {...register('password', {
                required: 'Password is required',
                minLength: {
                  value: 6,
                  message: 'Password must be at least 6 characters',
                },
              })}
              error={errors.password?.message}
            />
            
            {error && (
              <Typography color="error" variant="body2" sx={{ mt: 1 }}>
                {error}
              </Typography>
            )}
            
            <AppButton
              type="submit"
              fullWidth
              variant="contained"
              loading={isLoading}
              sx={{ mt: 2 }}
            >
              Register
            </AppButton>
          </Box>
          
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Typography variant="body2">
              Already have an account?{' '}
              <Link to="/login">Sign In</Link>
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  )
}