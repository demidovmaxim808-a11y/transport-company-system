export interface Driver {
  id: number
  full_name: string
  license_number: string
  phone: string
  experience_years: number
  status: string
  created_at: string
}

export interface DriverCreate {
  full_name: string
  license_number: string
  phone: string
  experience_years: number
  status: string
}

export interface DriverUpdate {
  full_name?: string
  license_number?: string
  phone?: string
  experience_years?: number
  status?: string
}

export interface DriversListResponse {
  items: Driver[]
  total: number
  page: number
  size: number
  pages: number
}