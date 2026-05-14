import api from './axios'
import { OrdersListResponse, Order, OrderCreate, OrderUpdate } from '../types/order.types'

export const ordersAPI = {
  getOrders: async (params?: {
    page?: number
    size?: number
    sort_by?: string
    sort_order?: string
    status?: string
  }): Promise<OrdersListResponse> => {
    const response = await api.get<OrdersListResponse>('/api/orders/', { params })
    return response.data
  },

  getOrder: async (orderId: number): Promise<Order> => {
    const response = await api.get<Order>(`/api/orders/${orderId}`)
    return response.data
  },

  createOrder: async (data: OrderCreate): Promise<Order> => {
    const response = await api.post<Order>('/api/orders/', data)
    return response.data
  },

  updateOrder: async (orderId: number, data: OrderUpdate): Promise<Order> => {
    const response = await api.put<Order>(`/api/orders/${orderId}`, data)
    return response.data
  },

  deleteOrder: async (orderId: number): Promise<void> => {
    await api.delete(`/api/orders/${orderId}`)
  },
}