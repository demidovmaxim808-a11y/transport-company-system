import React, { useEffect, useState } from 'react'
import Grid from '@mui/material/Grid'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import { MainLayout } from '../../components/layout/MainLayout'
import { analyticsAPI } from '../../api/analytics.api'
import { AnalyticsDashboard } from '../../types/order.types'
import { RevenueChart } from '../../components/analytics/RevenueChart'
import { ProfitCard } from '../../components/analytics/ProfitCard'
import { TopDriverCard } from '../../components/analytics/TopDriverCard'
import { TopTrailerCard } from '../../components/analytics/TopTrailerCard'
import { Loader } from '../../components/ui/Loader'

export const DashboardPage: React.FC = () => {
  const [data, setData] = useState<AnalyticsDashboard | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      const result = await analyticsAPI.getDashboard('month')
      setData(result)
    } catch (error) {
      console.error('Failed to load dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <MainLayout><Loader /></MainLayout>

  if (!data) return <MainLayout><Typography>No data available</Typography></MainLayout>

  return (
    <MainLayout>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Revenue
              </Typography>
              <Typography variant="h5">
                ${data.total_revenue.toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Orders
              </Typography>
              <Typography variant="h5">
                {data.total_orders}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active Trips
              </Typography>
              <Typography variant="h5">
                {data.active_trips}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Available Drivers
              </Typography>
              <Typography variant="h5">
                {data.available_drivers}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Available Trailers
              </Typography>
              <Typography variant="h5">
                {data.available_trailers}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12}>
          <RevenueChart data={data.revenue_by_month} />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <TopDriverCard drivers={data.top_drivers} />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <TopTrailerCard trailers={data.trailer_utilization} />
        </Grid>
      </Grid>
    </MainLayout>
  )
}