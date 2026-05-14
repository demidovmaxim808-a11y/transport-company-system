import api from './axios'
import { TripsListResponse, Trip, TripCreate, TripUpdate } from '../types/trip.types'

export const tripsAPI = {
  getTrips: async (params?: {
    page?: number
    size?: number
    sort_by?: string
    sort_order?: string
    status?: string
    driver_id?: number
  }): Promise<TripsListResponse> => {
    const response = await api.get<TripsListResponse>('/api/trips/', { params })
    return response.data
  },

  getMyTrips: async (params?: {
    page?: number
    size?: number
  }): Promise<TripsListResponse> => {
    const response = await api.get<TripsListResponse>('/api/trips/my-trips', { params })
    return response.data
  },

  getTrip: async (tripId: number): Promise<Trip> => {
    const response = await api.get<Trip>(`/api/trips/${tripId}`)
    return response.data
  },

  createTrip: async (data: TripCreate): Promise<Trip> => {
    const response = await api.post<Trip>('/api/trips/', data)
    return response.data
  },

  updateTrip: async (tripId: number, data: TripUpdate): Promise<Trip> => {
    const response = await api.put<Trip>(`/api/trips/${tripId}`, data)
    return response.data
  },

  deleteTrip: async (tripId: number): Promise<void> => {
    await api.delete(`/api/trips/${tripId}`)
  },
}