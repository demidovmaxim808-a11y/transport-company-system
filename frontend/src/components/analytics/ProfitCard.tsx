import React from 'react'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Grid'
import TrendingUpIcon from '@mui/icons-material/TrendingUp'
import ReceiptIcon from '@mui/icons-material/Receipt'

interface ProfitCardProps {
  totalRevenue: number
  totalOrders: number
}

export const ProfitCard: React.FC<ProfitCardProps> = ({
  totalRevenue,
  totalOrders,
}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Financial Overview
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={6}>
            <TrendingUpIcon color="success" sx={{ fontSize: 40 }} />
            <Typography variant="h4" color="success.main">
              ${totalRevenue.toLocaleString()}
            </Typography>
            <Typography color="textSecondary">Total Revenue</Typography>
          </Grid>
          <Grid item xs={6}>
            <ReceiptIcon color="primary" sx={{ fontSize: 40 }} />
            <Typography variant="h4" color="primary">
              {totalOrders}
            </Typography>
            <Typography color="textSecondary">Total Orders</Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  )
}