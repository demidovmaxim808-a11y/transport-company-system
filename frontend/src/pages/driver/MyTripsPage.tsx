import React, { useEffect, useState } from 'react'
import Typography from '@mui/material/Typography'
import { MainLayout } from '../../components/layout/MainLayout'
import { tripsAPI } from '../../api/trips.api'
import { Trip } from '../../types/trip.types'
import { TripsTable } from '../../components/tables/TripsTable'
import { notificationService } from '../../services/notification.service'

export const MyTripsPage: React.FC = () => {
  const [trips, setTrips] = useState<Trip[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadMyTrips()
  }, [page])

  const loadMyTrips = async () => {
    setLoading(true)
    try {
      const result = await tripsAPI.getMyTrips({ page, size: 20 })
      setTrips(result.items)
      setTotal(result.total)
    } catch (error) {
      notificationService.error('Failed to load trips')
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <Typography variant="h4" gutterBottom>
        My Trips
      </Typography>

      <TripsTable
        trips={trips}
        total={total}
        page={page}
        onPageChange={setPage}
        loading={loading}
      />
    </MainLayout>
  )
}