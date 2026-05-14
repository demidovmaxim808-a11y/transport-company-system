import api from './axios'
import { RoutesListResponse, Route, RouteCreate, RouteUpdate } from '../types/route.types'

export const routesAPI = {
  getRoutes: async (params?: {
    page?: number
    size?: number
    sort_by?: string
    sort_order?: string
  }): Promise<RoutesListResponse> => {
    const response = await api.get<RoutesListResponse>('/api/routes/', { params })
    return response.data
  },

  getRoute: async (routeId: number): Promise<Route> => {
    const response = await api.get<Route>(`/api/routes/${routeId}`)
    return response.data
  },

  createRoute: async (data: RouteCreate): Promise<Route> => {
    const response = await api.post<Route>('/api/routes/', data)
    return response.data
  },

  updateRoute: async (routeId: number, data: RouteUpdate): Promise<Route> => {
    const response = await api.put<Route>(`/api/routes/${routeId}`, data)
    return response.data
  },

  deleteRoute: async (routeId: number): Promise<void> => {
    await api.delete(`/api/routes/${routeId}`)
  },
}