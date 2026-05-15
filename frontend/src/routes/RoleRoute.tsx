import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAppSelector } from '../app/hooks'

interface RoleRouteProps {
  children: React.ReactNode
  roles: string[]
}

export const RoleRoute: React.FC<RoleRouteProps> = ({ children, roles }) => {
  const { user } = useAppSelector((state) => state.auth)

  if (!user || !roles.includes(user.role)) {
    const defaultRoute = user?.role === 'admin' ? '/admin/dashboard' :
                        user?.role === 'manager' ? '/manager/dashboard' :
                        '/driver/my-trips'
    return <Navigate to={defaultRoute} replace />
  }

  return <>{children}</>
}