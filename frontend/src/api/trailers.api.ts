import api from './axios'
import { TrailersListResponse, Trailer, TrailerCreate, TrailerUpdate } from '../types/trailer.types'

export const trailersAPI = {
  getTrailers: async (params?: {
    page?: number
    size?: number
    sort_by?: string
    sort_order?: string
    status?: string
  }): Promise<TrailersListResponse> => {
    const response = await api.get<TrailersListResponse>('/api/trailers/', { params })
    return response.data
  },

  getTrailer: async (trailerId: number): Promise<Trailer> => {
    const response = await api.get<Trailer>(`/api/trailers/${trailerId}`)
    return response.data
  },

  createTrailer: async (data: TrailerCreate): Promise<Trailer> => {
    const response = await api.post<Trailer>('/api/trailers/', data)
    return response.data
  },

  updateTrailer: async (trailerId: number, data: TrailerUpdate): Promise<Trailer> => {
    const response = await api.put<Trailer>(`/api/trailers/${trailerId}`, data)
    return response.data
  },

  deleteTrailer: async (trailerId: number): Promise<void> => {
    await api.delete(`/api/trailers/${trailerId}`)
  },
}