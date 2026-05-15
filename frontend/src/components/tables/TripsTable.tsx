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
import { Trip } from '../../types/trip.types'
import { Loader } from '../ui/Loader'
import { format } from 'date-fns'

interface TripsTableProps {
  trips: Trip[]
  total: number
  page: number
  onPageChange: (page: number) => void
  onEdit?: (trip: Trip) => void
  onDelete?: (id: number) => void
  loading?: boolean
}

const getStatusColor = (status: string): "success" | "error" | "warning" | "info" => {
  switch (status) {
    case 'completed':
      return 'success'
    case 'in_progress':
      return 'info'
    case 'planned':
      return 'warning'
    case 'cancelled':
      return 'error'
    default:
      return 'default'
  }
}

export const TripsTable: React.FC<TripsTableProps> = ({
  trips,
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
              <TableCell>Driver ID</TableCell>
              <TableCell>Trailer ID</TableCell>
              <TableCell>Route ID</TableCell>
              <TableCell>Start Date</TableCell>
              <TableCell>End Date</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {trips.map((trip) => (
              <TableRow key={trip.id}>
                <TableCell>{trip.id}</TableCell>
                <TableCell>{trip.driver_id}</TableCell>
                <TableCell>{trip.trailer_id}</TableCell>
                <TableCell>{trip.route_id}</TableCell>
                <TableCell>
                  {format(new Date(trip.start_date), 'yyyy-MM-dd HH:mm')}
                </TableCell>
                <TableCell>
                  {trip.end_date
                    ? format(new Date(trip.end_date), 'yyyy-MM-dd HH:mm')
                    : 'N/A'}
                </TableCell>
                <TableCell>
                  <Chip
                    label={trip.status.replace('_', ' ')}
                    color={getStatusColor(trip.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {onEdit && (
                    <IconButton onClick={() => onEdit(trip)} size="small">
                      <EditIcon />
                    </IconButton>
                  )}
                  {onDelete && (
                    <IconButton onClick={() => onDelete(trip.id)} size="small">
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