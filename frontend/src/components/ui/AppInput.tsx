import React from 'react'
import TextField, { TextFieldProps } from '@mui/material/TextField'

interface AppInputProps extends Omit<TextFieldProps, 'error'> {
  error?: string | boolean
}

export const AppInput: React.FC<AppInputProps> = ({
  error,
  helperText,
  ...props
}) => {
  return (
    <TextField
      fullWidth
      variant="outlined"
      margin="normal"
      error={!!error}
      helperText={error || helperText}
      {...props}
    />
  )
}