import api from './axios'
import { AnalyticsDashboard } from '../types/order.types'

export const analyticsAPI = {
  getDashboard: async (period: string = 'month'): Promise<AnalyticsDashboard> => {
    const response = await api.get<AnalyticsDashboard>('/api/analytics/dashboard', {
      params: { period }
    })
    return response.data
  },
}