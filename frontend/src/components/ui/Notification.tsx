import React from 'react'
import Snackbar from '@mui/material/Snackbar'
import Alert from '@mui/material/Alert'

interface NotificationProps {
  open: boolean
  onClose: () => void
  message: string
  severity?: 'success' | 'error' | 'warning' | 'info'
}

export const Notification: React.FC<NotificationProps> = ({
  open,
  onClose,
  message,
  severity = 'info',
}) => {
  return (
    <Snackbar
      open={open}
      autoHideDuration={6000}
      onClose={onClose}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
    >
      <Alert onClose={onClose} severity={severity} sx={{ width: '100%' }}>
        {message}
      </Alert>
    </Snackbar>
  )
}