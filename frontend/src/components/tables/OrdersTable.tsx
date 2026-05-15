import React from 'react'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import TablePagination from '@mui/material/TablePagination'
import Paper from '@mui/material/Paper'
import IconButton from '@mui/material/IconButton'
import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/Delete'
import Chip from '@mui/material/Chip'
import { Order } from '../../types/order.types'
import { Loader } from '../ui/Loader'

interface OrdersTableProps {
  orders: Order[]
  total: number
  page: number
  onPageChange: (page: number) => void
  onEdit?: (order: Order) => void
  onDelete?: (id: number) => void
  loading?: boolean
}

const getStatusColor = (status: string): "success" | "error" | "warning" | "info" => {
  switch (status) {
    case 'delivered':
      return 'success'
    case 'in_transit':
      return 'info'
    case 'pending':
      return 'warning'
    case 'cancelled':
      return 'error'
    default:
      return 'default'
  }
}

export const OrdersTable: React.FC<OrdersTableProps> = ({
  orders,
  total,
  page,
  onPageChange,
  onEdit,
  onDelete,
  loading,
}) => {
  if (loading) return <Loader />

  return (
    <Paper>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Customer</TableCell>
              <TableCell>Cargo Type</TableCell>
              <TableCell>Weight (kg)</TableCell>
              <TableCell>Price</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {orders.map((order) => (
              <TableRow key={order.id}>
                <TableCell>{order.id}</TableCell>
                <TableCell>{order.customer_name}</TableCell>
                <TableCell>{order.cargo_type}</TableCell>
                <TableCell>{order.cargo_weight}</TableCell>
                <TableCell>${order.price?.toLocaleString() || 'N/A'}</TableCell>
                <TableCell>
                  <Chip
                    label={order.status.replace('_', ' ')}
                    color={getStatusColor(order.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {onEdit && (
                    <IconButton onClick={() => onEdit(order)} size="small">
                      <EditIcon />
                    </IconButton>
                  )}
                  {onDelete && (
                    <IconButton onClick={() => onDelete(order.id)} size="small">
                      <DeleteIcon />
                    </IconButton>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        count={total}
        page={page - 1}
        onPageChange={(_, newPage) => onPageChange(newPage + 1)}
        rowsPerPage={20}
        rowsPerPageOptions={[20]}
      />
    </Paper>
  )
}