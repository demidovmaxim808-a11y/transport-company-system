import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { LoginPage } from '../pages/auth/LoginPage'
import { RegisterPage } from '../pages/auth/RegisterPage'
import { DashboardPage } from '../pages/admin/DashboardPage'
import { DriversPage } from '../pages/admin/DriversPage'
import { TrailersPage } from '../pages/admin/TrailersPage'
import { OrdersPage } from '../pages/admin/OrdersPage'
import { TripsPage } from '../pages/admin/TripsPage'
import { AuditLogsPage } from '../pages/admin/AuditLogsPage'
import { AnalyticsPage } from '../pages/manager/AnalyticsPage'
import { ReportsPage } from '../pages/manager/ReportsPage'
import { MyTripsPage } from '../pages/driver/MyTripsPage'
import { ProtectedRoute } from './ProtectedRoute'
import { RoleRoute } from './RoleRoute'

const AppRouter: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      
      <Route
        path="/admin/dashboard"
        element={
          <ProtectedRoute>
            <RoleRoute roles={['admin', 'manager']}>
              <DashboardPage />
            </RoleRoute>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/admin/drivers"
        element={
          <ProtectedRoute>
            <RoleRoute roles={['admin', 'manager']}>
              <DriversPage />
            </RoleRoute>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/admin/trailers"
        element={
          <ProtectedRoute>
            <RoleRoute roles={['admin', 'manager']}>
              <TrailersPage />
            </RoleRoute>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/admin/orders"
        element={
          <ProtectedRoute>
            <RoleRoute roles={['admin', 'manager']}>
              <OrdersPage />
            </RoleRoute>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/admin/trips"
        element={
          <ProtectedRoute>
            <RoleRoute roles={['admin', 'manager']}>
              <TripsPage />
            </RoleRoute>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/admin/audit-logs"
        element={
          <ProtectedRoute>
            <RoleRoute roles={['admin']}>
              <AuditLogsPage />
            </RoleRoute>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/manager/dashboard"
        element={
          <ProtectedRoute>
            <RoleRoute roles={['admin', 'manager']}>
              <DashboardPage />
            </RoleRoute>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/manager/analytics"
        element={
          <ProtectedRoute>
            <RoleRoute roles={['admin', 'manager']}>
              <AnalyticsPage />
            </RoleRoute>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/manager/reports"
        element={
          <ProtectedRoute>
            <RoleRoute roles={['admin', 'manager']}>
              <ReportsPage />
            </RoleRoute>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/driver/my-trips"
        element={
          <ProtectedRoute>
            <RoleRoute roles={['driver']}>
              <MyTripsPage />
            </RoleRoute>
          </ProtectedRoute>
        }
      />
      
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}

export default AppRouter