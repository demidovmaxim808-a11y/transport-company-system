import React, { useEffect, useState } from 'react'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import AddIcon from '@mui/icons-material/Add'
import { MainLayout } from '../../components/layout/MainLayout'
import { TripsTable } from '../../components/tables/TripsTable'
import { Modal } from '../../components/ui/Modal'
import { TripForm } from '../../components/forms/TripForm'
import { tripsAPI } from '../../api/trips.api'
import { Trip, TripCreate, TripUpdate } from '../../types/trip.types'
import { notificationService } from '../../services/notification.service'

export const TripsPage: React.FC = () => {
  const [trips, setTrips] = useState<Trip[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editTrip, setEditTrip] = useState<Trip | null>(null)

  useEffect(() => {
    loadTrips()
  }, [page])

  const loadTrips = async () => {
    setLoading(true)
    try {
      const result = await tripsAPI.getTrips({ page, size: 20 })
      setTrips(result.items)
      setTotal(result.total)
    } catch (error) {
      notificationService.error('Failed to load trips')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (data: TripCreate) => {
    try {
      await tripsAPI.createTrip(data)
      notificationService.success('Trip created successfully')
      setModalOpen(false)
      loadTrips()
    } catch (error: any) {
      notificationService.error(error.response?.data?.detail || 'Failed to create trip')
    }
  }

  const handleUpdate = async (data: TripCreate) => {
    if (!editTrip) return
    try {
      await tripsAPI.updateTrip(editTrip.id, data as TripUpdate)
      notificationService.success('Trip updated successfully')
      setModalOpen(false)
      setEditTrip(null)
      loadTrips()
    } catch (error: any) {
      notificationService.error(error.response?.data?.detail || 'Failed to update trip')
    }
  }

  const handleDelete = async (tripId: number) => {
    try {
      await tripsAPI.deleteTrip(tripId)
      notificationService.success('Trip deleted successfully')
      loadTrips()
    } catch (error) {
      notificationService.error('Failed to delete trip')
    }
  }

  const handleEdit = (trip: Trip) => {
    setEditTrip(trip)
    setModalOpen(true)
  }

  return (
    <MainLayout>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Trips</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setEditTrip(null)
            setModalOpen(true)
          }}
        >
          Add Trip
        </Button>
      </Box>

      <TripsTable
        trips={trips}
        total={total}
        page={page}
        onPageChange={setPage}
        onEdit={handleEdit}
        onDelete={handleDelete}
        loading={loading}
      />

      <Modal
        open={modalOpen}
        onClose={() => {
          setModalOpen(false)
          setEditTrip(null)
        }}
        title={editTrip ? 'Edit Trip' : 'Add Trip'}
      >
        <TripForm
          onSubmit={editTrip ? handleUpdate : handleCreate}
          onCancel={() => {
            setModalOpen(false)
            setEditTrip(null)
          }}
          initialData={editTrip || undefined}
        />
      </Modal>
    </MainLayout>
  )
}