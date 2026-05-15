import React, { useEffect, useState } from 'react'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import AddIcon from '@mui/icons-material/Add'
import { MainLayout } from '../../components/layout/MainLayout'
import { DriversTable } from '../../components/tables/DriversTable'
import { Modal } from '../../components/ui/Modal'
import { DriverForm } from '../../components/forms/DriverForm'
import { driversAPI } from '../../api/drivers.api'
import { Driver, DriverCreate, DriverUpdate } from '../../types/driver.types'
import { notificationService } from '../../services/notification.service'

export const DriversPage: React.FC = () => {
  const [drivers, setDrivers] = useState<Driver[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editDriver, setEditDriver] = useState<Driver | null>(null)

  useEffect(() => {
    loadDrivers()
  }, [page])

  const loadDrivers = async () => {
    setLoading(true)
    try {
      const result = await driversAPI.getDrivers({ page, size: 20 })
      setDrivers(result.items)
      setTotal(result.total)
    } catch (error) {
      notificationService.error('Failed to load drivers')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (data: DriverCreate) => {
    try {
      await driversAPI.createDriver(data)
      notificationService.success('Driver created successfully')
      setModalOpen(false)
      loadDrivers()
    } catch (error: any) {
      notificationService.error(error.response?.data?.detail || 'Failed to create driver')
    }
  }

  const handleUpdate = async (data: DriverCreate) => {
    if (!editDriver) return
    try {
      await driversAPI.updateDriver(editDriver.id, data as DriverUpdate)
      notificationService.success('Driver updated successfully')
      setModalOpen(false)
      setEditDriver(null)
      loadDrivers()
    } catch (error: any) {
      notificationService.error(error.response?.data?.detail || 'Failed to update driver')
    }
  }

  const handleDelete = async (driverId: number) => {
    try {
      await driversAPI.deleteDriver(driverId)
      notificationService.success('Driver deleted successfully')
      loadDrivers()
    } catch (error) {
      notificationService.error('Failed to delete driver')
    }
  }

  const handleEdit = (driver: Driver) => {
    setEditDriver(driver)
    setModalOpen(true)
  }

  return (
    <MainLayout>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Drivers</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setEditDriver(null)
            setModalOpen(true)
          }}
        >
          Add Driver
        </Button>
      </Box>

      <DriversTable
        drivers={drivers}
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
          setEditDriver(null)
        }}
        title={editDriver ? 'Edit Driver' : 'Add Driver'}
      >
        <DriverForm
          onSubmit={editDriver ? handleUpdate : handleCreate}
          onCancel={() => {
            setModalOpen(false)
            setEditDriver(null)
          }}
          initialData={editDriver || undefined}
        />
      </Modal>
    </MainLayout>
  )
}