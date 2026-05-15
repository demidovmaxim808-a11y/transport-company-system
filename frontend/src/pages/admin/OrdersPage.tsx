import React, { useEffect, useState } from 'react'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import AddIcon from '@mui/icons-material/Add'
import { MainLayout } from '../../components/layout/MainLayout'
import { OrdersTable } from '../../components/tables/OrdersTable'
import { Modal } from '../../components/ui/Modal'
import { OrderForm } from '../../components/forms/OrderForm'
import { ordersAPI } from '../../api/orders.api'
import { Order, OrderCreate, OrderUpdate } from '../../types/order.types'
import { notificationService } from '../../services/notification.service'

export const OrdersPage: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [editOrder, setEditOrder] = useState<Order | null>(null)

  useEffect(() => {
    loadOrders()
  }, [page])

  const loadOrders = async () => {
    setLoading(true)
    try {
      const result = await ordersAPI.getOrders({ page, size: 20 })
      setOrders(result.items)
      setTotal(result.total)
    } catch (error) {
      notificationService.error('Failed to load orders')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async (data: OrderCreate) => {
    try {
      await ordersAPI.createOrder(data)
      notificationService.success('Order created successfully')
      setModalOpen(false)
      loadOrders()
    } catch (error: any) {
      notificationService.error(error.response?.data?.detail || 'Failed to create order')
    }
  }

  const handleUpdate = async (data: OrderCreate) => {
    if (!editOrder) return
    try {
      await ordersAPI.updateOrder(editOrder.id, data as OrderUpdate)
      notificationService.success('Order updated successfully')
      setModalOpen(false)
      setEditOrder(null)
      loadOrders()
    } catch (error: any) {
      notificationService.error(error.response?.data?.detail || 'Failed to update order')
    }
  }

  const handleDelete = async (orderId: number) => {
    try {
      await ordersAPI.deleteOrder(orderId)
      notificationService.success('Order deleted successfully')
      loadOrders()
    } catch (error) {
      notificationService.error('Failed to delete order')
    }
  }

  const handleEdit = (order: Order) => {
    setEditOrder(order)
    setModalOpen(true)
  }

  return (
    <MainLayout>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Orders</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            setEditOrder(null)
            setModalOpen(true)
          }}
        >
          Add Order
        </Button>
      </Box>

      <OrdersTable
        orders={orders}
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
          setEditOrder(null)
        }}
        title={editOrder ? 'Edit Order' : 'Add Order'}
      >
        <OrderForm
          onSubmit={editOrder ? handleUpdate : handleCreate}
          onCancel={() => {
            setModalOpen(false)
            setEditOrder(null)
          }}
          initialData={editOrder || undefined}
        />
      </Modal>
    </MainLayout>
  )
}