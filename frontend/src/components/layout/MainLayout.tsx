import React, { useState } from 'react'
import Box from '@mui/material/Box'
import { Header } from './Header'
import { Sidebar } from './Sidebar'
import { useAppSelector } from '../../app/hooks'

interface MainLayoutProps {
  children: React.ReactNode
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { user } = useAppSelector((state) => state.auth)

  const handleMenuClick = () => {
    setSidebarOpen(!sidebarOpen)
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Header onMenuClick={handleMenuClick} />
      <Sidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        role={user?.role || 'driver'}
      />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        {children}
      </Box>
    </Box>
  )
}