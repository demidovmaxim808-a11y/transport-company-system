import React, { useEffect, useState } from 'react'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import { MainLayout } from '../../components/layout/MainLayout'
import { AuditLogsTable } from '../../components/tables/AuditLogsTable'
import api from '../../api/axios'
import { notificationService } from '../../services/notification.service'

interface AuditLog {
  id: number
  user_id: number
  action: string
  entity_name: string
  entity_id: number | null
  details: string | null
  created_at: string
}

export const AuditLogsPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadLogs()
  }, [page])

  const loadLogs = async () => {
    setLoading(true)
    try {
      const response = await api.get('/api/audit-logs/', {
        params: { page, size: 20 }
      })
      setLogs(response.data.items)
      setTotal(response.data.total)
    } catch (error) {
      notificationService.error('Failed to load audit logs')
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4">Audit Logs</Typography>
      </Box>

      <AuditLogsTable
        logs={logs}
        total={total}
        page={page}
        onPageChange={setPage}
        loading={loading}
      />
    </MainLayout>
  )
}