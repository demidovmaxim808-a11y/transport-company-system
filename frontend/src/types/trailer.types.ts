export interface Trailer {
  id: number
  model: string
  plate_number: string
  capacity: number
  status: string
  created_at: string
}

export interface TrailerCreate {
  model: string
  plate_number: string
  capacity: number
  status: string
}

export interface TrailerUpdate {
  model?: string
  plate_number?: string
  capacity?: number
  status?: string
}

export interface TrailersListResponse {
  items: Trailer[]
  total: number
  page: number
  size: number
  pages: number
}