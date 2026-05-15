import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import Drawer from '@mui/material/Drawer'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import Divider from '@mui/material/Divider'
import DashboardIcon from '@mui/icons-material/Dashboard'
import PeopleIcon from '@mui/icons-material/People'
import LocalShippingIcon from '@mui/icons-material/LocalShipping'
import ReceiptIcon from '@mui/icons-material/Receipt'
import RouteIcon from '@mui/icons-material/Route'
import AssessmentIcon from '@mui/icons-material/Assessment'
import HistoryIcon from '@mui/icons-material/History'

interface SidebarProps {
  open: boolean
  onClose: () => void
  role: string
}

const DRAWER_WIDTH = 280

const menuItems = {
  admin: [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/admin/dashboard' },
    { text: 'Drivers', icon: <PeopleIcon />, path: '/admin/drivers' },
    { text: 'Trailers', icon: <LocalShippingIcon />, path: '/admin/trailers' },
    { text: 'Routes', icon: <RouteIcon />, path: '/admin/routes' },
    { text: 'Orders', icon: <ReceiptIcon />, path: '/admin/orders' },
    { text: 'Trips', icon: <LocalShippingIcon />, path: '/admin/trips' },
    { text: 'Analytics', icon: <AssessmentIcon />, path: '/admin/analytics' },
    { text: 'Audit Logs', icon: <HistoryIcon />, path: '/admin/audit-logs' },
  ],
  manager: [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/manager/dashboard' },
    { text: 'Drivers', icon: <PeopleIcon />, path: '/manager/drivers' },
    { text: 'Trailers', icon: <LocalShippingIcon />, path: '/manager/trailers' },
    { text: 'Orders', icon: <ReceiptIcon />, path: '/manager/orders' },
    { text: 'Trips', icon: <LocalShippingIcon />, path: '/manager/trips' },
    { text: 'Analytics', icon: <AssessmentIcon />, path: '/manager/analytics' },
  ],
  driver: [
    { text: 'My Trips', icon: <LocalShippingIcon />, path: '/driver/my-trips' },
  ],
}

export const Sidebar: React.FC<SidebarProps> = ({ open, onClose, role }) => {
  const navigate = useNavigate()
  const location = useLocation()

  const items = menuItems[role as keyof typeof menuItems] || []

  const handleNavigation = (path: string) => {
    navigate(path)
    onClose()
  }

  return (
    <Drawer
      open={open}
      onClose={onClose}
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
        },
      }}
      variant="temporary"
    >
      <Divider />
      <List>
        {items.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => handleNavigation(item.path)}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  )
}