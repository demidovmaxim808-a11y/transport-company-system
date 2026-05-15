import React, { useEffect, useState } from 'react'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import AddIcon from '@mui/icons-material/Add'
import { MainLayout } from '../../components/layout/MainLayout'
import { TrailersTable } from '../../components/tables/TrailersTable'
import { Modal } from '../../components/ui/Modal'
import { TrailerForm } from '../../components/forms/TrailerForm'
import { trailersAPI } from '../../api/trailers.api'
import { Trailer, TrailerCreate, TrailerUpdate } from '../../types/trailer.types'
import { notificationService } from '../../services/notification.service'

export const TrailersPage: React.FC = () => {
  const [trailers, setTrailers] = useState<Trailer[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editTrailer, setEditTrailer] = useState<Trailer | null>(null)

  useEffect(() => {
    loadTrailers()
  }, [page])

  const loadTrailers = async () => {
    setLoading(true)
    try {
      const result = await trailersAPI.getTrailers({ page, size: 20 })
      setTrailers(result.items)
      setTotal(result.total)
    } catch (error) {
      notificationService.error('Failed to load trailers')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (data: TrailerCreate) => {
    try {
      await trailersAPI.createTrailer(data)
      notificationService.success('Trailer created successfully')
      setModalOpen(false)
      loadTrailers()
    } catch (error: any) {
      notificationService.error(error.response?.data?.detail || 'Failed to create trailer')
    }
  }

  const handleUpdate = async (data: TrailerCreate) => {
    if (!editTrailer) return
    try {
      await trailersAPI.updateTrailer(editTrailer.id, data as TrailerUpdate)
      notificationService.success('Trailer updated successfully')
      setModalOpen(false)
      setEditTrailer(null)
      loadTrailers()
    } catch (error: any) {
      notificationService.error(error.response?.data?.detail || 'Failed to update trailer')
    }
  }

  const handleDelete = async (trailerId: number) => {
    try {
      await trailersAPI.deleteTrailer(trailerId)
      notificationService.success('Trailer deleted successfully')
      loadTrailers()
    } catch (error) {
      notificationService.error('Failed to delete trailer')
    }
  }

  const handleEdit = (trailer: Trailer) => {
    setEditTrailer(trailer)
    setModalOpen(true)
  }

  return (
    <MainLayout>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Trailers</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setEditTrailer(null)
            setModalOpen(true)
          }}
        >
          Add Trailer
        </Button>
      </Box>

      <TrailersTable
        trailers={trailers}
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
          setEditTrailer(null)
        }}
        title={editTrailer ? 'Edit Trailer' : 'Add Trailer'}
      >
        <TrailerForm
          onSubmit={editTrailer ? handleUpdate : handleCreate}
          onCancel={() => {
            setModalOpen(false)
            setEditTrailer(null)
          }}
          initialData={editTrailer || undefined}
        />
      </Modal>
    </MainLayout>
  )
}