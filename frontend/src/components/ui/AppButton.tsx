import React from 'react'
import Button, { ButtonProps } from '@mui/material/Button'
import CircularProgress from '@mui/material/CircularProgress'

interface AppButtonProps extends ButtonProps {
  loading?: boolean
}

export const AppButton: React.FC<AppButtonProps> = ({ 
  loading, 
  disabled, 
  children, 
  ...props 
}) => {
  return (
    <Button
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <CircularProgress
          size={20}
          color="inherit"
          sx={{ mr: 1 }}
        />
      )}
      {children}
    </Button>
  )
}