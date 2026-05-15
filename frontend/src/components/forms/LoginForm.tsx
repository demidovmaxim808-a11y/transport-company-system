import React from 'react'
import { useForm } from 'react-hook-form'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import { AppInput } from '../ui/AppInput'
import { AppButton } from '../ui/AppButton'
import { LoginCredentials } from '../../types/auth.types'

interface LoginFormProps {
  onSubmit: (data: LoginCredentials) => void
  isLoading: boolean
  error?: string | null
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSubmit, isLoading, error }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginCredentials>()

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      <Typography variant="h5" gutterBottom align="center">
        Sign In
      </Typography>
      
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
        Sign In
      </AppButton>
    </Box>
  )
}