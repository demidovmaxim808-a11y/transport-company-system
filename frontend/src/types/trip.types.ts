export interface Trip {
  id: number
  driver_id: number
  trailer_id: number
  route_id: number
  start_date: string
  end_date: string | null
  status: string
  created_at: string
}

export interface TripCreate {
  driver_id: number
  trailer_id: number
  route_id: number
  start_date: string
  end_date?: string | null
  status: string
}

export interface TripUpdate {
  driver_id?: number
  trailer_id?: number
  route_id?: number
  start_date?: string
  end_date?: string | null
  status?: string
}

export interface TripsListResponse {
  items: Trip[]
  total: number
  page: number
  size: number
  pages: number
}