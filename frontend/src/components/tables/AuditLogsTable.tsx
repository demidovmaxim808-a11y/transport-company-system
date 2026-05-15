import React from 'react'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import TablePagination from '@mui/material/TablePagination'
import Paper from '@mui/material/Paper'
import Chip from '@mui/material/Chip'
import { Loader } from '../ui/Loader'
import { format } from 'date-fns'

interface AuditLog {
  id: number
  user_id: number
  action: string
  entity_name: string
  entity_id: number | null
  details: string | null
  created_at: string
}

interface AuditLogsTableProps {
  logs: AuditLog[]
  total: number
  page: number
  onPageChange: (page: number) => void
  loading?: boolean
}

export const AuditLogsTable: React.FC<AuditLogsTableProps> = ({
  logs,
  total,
  page,
  onPageChange,
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
              <TableCell>User ID</TableCell>
              <TableCell>Action</TableCell>
              <TableCell>Entity</TableCell>
              <TableCell>Entity ID</TableCell>
              <TableCell>Details</TableCell>
              <TableCell>Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {logs.map((log) => (
              <TableRow key={log.id}>
                <TableCell>{log.id}</TableCell>
                <TableCell>{log.user_id}</TableCell>
                <TableCell>
                  <Chip label={log.action} size="small" color="primary" />
                </TableCell>
                <TableCell>{log.entity_name}</TableCell>
                <TableCell>{log.entity_id || 'N/A'}</TableCell>
                <TableCell>{log.details || 'N/A'}</TableCell>
                <TableCell>
                  {format(new Date(log.created_at), 'yyyy-MM-dd HH:mm:ss')}
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