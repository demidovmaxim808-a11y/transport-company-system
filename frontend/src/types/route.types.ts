export interface Route {
  id: number
  departure_point: string
  destination_point: string
  distance_km: number
  created_at: string
}

export interface RouteCreate {
  departure_point: string
  destination_point: string
  distance_km: number
}

export interface RouteUpdate {
  departure_point?: string
  destination_point?: string
  distance_km?: number
}

export interface RoutesListResponse {
  items: Route[]
  total: number
  page: number
  size: number
  pages: number
}