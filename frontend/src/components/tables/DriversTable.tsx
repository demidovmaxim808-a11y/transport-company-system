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
import { Driver } from '../../types/driver.types'
import { Loader } from '../ui/Loader'

interface DriversTableProps {
  drivers: Driver[]
  total: number
  page: number
  onPageChange: (page: number) => void
  onEdit?: (driver: Driver) => void
  onDelete?: (id: number) => void
  loading?: boolean
}

const getStatusColor = (status: string): "success" | "error" | "warning" | "default" => {
  switch (status) {
    case 'available':
      return 'success'
    case 'busy':
      return 'warning'
    case 'off_duty':
      return 'default'
    case 'on_leave':
      return 'error'
    default:
      return 'default'
  }
}

export const DriversTable: React.FC<DriversTableProps> = ({
  drivers,
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
              <TableCell>Full Name</TableCell>
              <TableCell>License Number</TableCell>
              <TableCell>Phone</TableCell>
              <TableCell>Experience (years)</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {drivers.map((driver) => (
              <TableRow key={driver.id}>
                <TableCell>{driver.id}</TableCell>
                <TableCell>{driver.full_name}</TableCell>
                <TableCell>{driver.license_number}</TableCell>
                <TableCell>{driver.phone}</TableCell>
                <TableCell>{driver.experience_years}</TableCell>
                <TableCell>
                  <Chip
                    label={driver.status.replace('_', ' ')}
                    color={getStatusColor(driver.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {onEdit && (
                    <IconButton onClick={() => onEdit(driver)} size="small">
                      <EditIcon />
                    </IconButton>
                  )}
                  {onDelete && (
                    <IconButton onClick={() => onDelete(driver.id)} size="small">
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