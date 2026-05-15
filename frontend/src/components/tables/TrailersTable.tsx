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
import { Trailer } from '../../types/trailer.types'
import { Loader } from '../ui/Loader'

interface TrailersTableProps {
  trailers: Trailer[]
  total: number
  page: number
  onPageChange: (page: number) => void
  onEdit?: (trailer: Trailer) => void
  onDelete?: (id: number) => void
  loading?: boolean
}

const getStatusColor = (status: string): "success" | "error" | "warning" | "default" => {
  switch (status) {
    case 'available':
      return 'success'
    case 'in_use':
      return 'warning'
    case 'maintenance':
      return 'error'
    default:
      return 'default'
  }
}

export const TrailersTable: React.FC<TrailersTableProps> = ({
  trailers,
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
              <TableCell>Model</TableCell>
              <TableCell>Plate Number</TableCell>
              <TableCell>Capacity (kg)</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {trailers.map((trailer) => (
              <TableRow key={trailer.id}>
                <TableCell>{trailer.id}</TableCell>
                <TableCell>{trailer.model}</TableCell>
                <TableCell>{trailer.plate_number}</TableCell>
                <TableCell>{trailer.capacity.toLocaleString()}</TableCell>
                <TableCell>
                  <Chip
                    label={trailer.status.replace('_', ' ')}
                    color={getStatusColor(trailer.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {onEdit && (
                    <IconButton onClick={() => onEdit(trailer)} size="small">
                      <EditIcon />
                    </IconButton>
                  )}
                  {onDelete && (
                    <IconButton onClick={() => onDelete(trailer.id)} size="small">
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