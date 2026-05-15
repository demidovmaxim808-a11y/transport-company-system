import { storageService } from '../services/storage.service'

export const permissions = {
  isAdmin: (): boolean => {
    const user = storageService.getUser()
    return user?.role === 'admin'
  },

  isManager: (): boolean => {
    const user = storageService.getUser()
    return user?.role === 'manager'
  },

  isDriver: (): boolean => {
    const user = storageService.getUser()
    return user?.role === 'driver'
  },

  hasAccess: (allowedRoles: string[]): boolean => {
    const user = storageService.getUser()
    if (!user) return false
    return allowedRoles.includes(user.role)
  },
}