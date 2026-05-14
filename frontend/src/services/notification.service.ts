import { toast } from 'react-toastify'

export const notificationService = {
  success: (message: string): void => {
    toast.success(message)
  },

  error: (message: string): void => {
    toast.error(message)
  },

  warning: (message: string): void => {
    toast.warning(message)
  },

  info: (message: string): void => {
    toast.info(message)
  },
}