export interface Order {
  id: number
  customer_name: string
  cargo_type: string
  cargo_weight: number
  trip_id: number | null
  status: string
  price: number | null
  created_at: string
}

export interface OrderCreate {
  customer_name: string
  cargo_type: string
  cargo_weight: number
  trip_id?: number | null
  status: string
  price?: number | null
}

export interface OrderUpdate {
  customer_name?: string
  cargo_type?: string
  cargo_weight?: number
  trip_id?: number | null
  status?: string
  price?: number | null
}

export interface OrdersListResponse {
  items: Order[]
  total: number
  page: number
  size: number
  pages: number
}

export interface AnalyticsDashboard {
  total_revenue: number
  total_orders: number
  active_trips: number
  available_drivers: number
  available_trailers: number
  revenue_by_month: RevenueByPeriod[]
  top_drivers: DriverPerformance[]
  trailer_utilization: TrailerUtilization[]
  order_status_summary: OrderStatusSummary[]
}

export interface RevenueByPeriod {
  period: string
  revenue: number
  orders_count: number
}

export interface DriverPerformance {
  driver_id: number
  driver_name: string
  trips_count: number
  total_km: number
  revenue_generated: number
}

export interface TrailerUtilization {
  trailer_id: number
  plate_number: string
  trips_count: number
  utilization_percent: number
}

export interface OrderStatusSummary {
  status: string
  count: number
  percentage: number
}