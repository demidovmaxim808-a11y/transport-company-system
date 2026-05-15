import React from 'react'
import Typography from '@mui/material/Typography'
import { MainLayout } from '../../components/layout/MainLayout'

export const ReportsPage: React.FC = () => {
  return (
    <MainLayout>
      <Typography variant="h4">Reports</Typography>
      <Typography variant="body1" sx={{ mt: 2 }}>
        Reports page coming soon...
      </Typography>
    </MainLayout>
  )
}