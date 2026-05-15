import React, { useEffect, useState } from 'react'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Grid'
import { MainLayout } from '../../components/layout/MainLayout'
import { analyticsAPI } from '../../api/analytics.api'
import { AnalyticsDashboard } from '../../types/order.types'
import { RevenueChart } from '../../components/analytics/RevenueChart'
import { ProfitCard } from '../../components/analytics/ProfitCard'
import { TopDriverCard } from '../../components/analytics/TopDriverCard'
import { TopTrailerCard } from '../../components/analytics/TopTrailerCard'
import { Loader } from '../../components/ui/Loader'

export const AnalyticsPage: React.FC = () => {
  const [data, setData] = useState<AnalyticsDashboard | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAnalytics()
  }, [])

  const loadAnalytics = async () => {
    try {
      const result = await analyticsAPI.getDashboard('month')
      setData(result)
    } catch (error) {
      console.error('Failed to load analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <MainLayout><Loader /></MainLayout>
  if (!data) return <MainLayout><Typography>No data available</Typography></MainLayout>

  return (
    <MainLayout>
      <Typography variant="h4" gutterBottom>
        Analytics
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <ProfitCard
            totalRevenue={data.total_revenue}
            totalOrders={data.total_orders}
          />
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