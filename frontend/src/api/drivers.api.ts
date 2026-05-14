import api from './axios'
import { DriversListResponse, Driver, DriverCreate, DriverUpdate } from '../types/driver.types'

export const driversAPI = {
  getDrivers: async (params?: {
    page?: number
    size?: number
    sort_by?: string
    sort_order?: string
    status?: string
  }): Promise<DriversListResponse> => {
    const response = await api.get<DriversListResponse>('/api/drivers/', { params })
    return response.data
  },

  getDriver: async (driverId: number): Promise<Driver> => {
    const response = await api.get<Driver>(`/api/drivers/${driverId}`)
    return response.data
  },

  createDriver: async (data: DriverCreate): Promise<Driver> => {
    const response = await api.post<Driver>('/api/drivers/', data)
    return response.data
  },

  updateDriver: async (driverId: number, data: DriverUpdate): Promise<Driver> => {
    const response = await api.put<Driver>(`/api/drivers/${driverId}`, data)
    return response.data
  },

  deleteDriver: async (driverId: number): Promise<void> => {
    await api.delete(`/api/drivers/${driverId}`)
  },
}