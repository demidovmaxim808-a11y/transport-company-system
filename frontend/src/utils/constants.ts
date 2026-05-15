export const ROLES = {
  ADMIN: 'admin',
  MANAGER: 'manager',
  DRIVER: 'driver',
}

export const STATUS = {
  DRIVER: {
    AVAILABLE: 'available',
    BUSY: 'busy',
    OFF_DUTY: 'off_duty',
    ON_LEAVE: 'on_leave',
  },
  TRAILER: {
    AVAILABLE: 'available',
    IN_USE: 'in_use',
    MAINTENANCE: 'maintenance',
  },
  TRIP: {
    PLANNED: 'planned',
    IN_PROGRESS: 'in_progress',
    COMPLETED: 'completed',
    CANCELLED: 'cancelled',
  },
  ORDER: {
    PENDING: 'pending',
    IN_TRANSIT: 'in_transit',
    DELIVERED: 'delivered',
    CANCELLED: 'cancelled',
  },
}

export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_SIZE: 20,
  MAX_SIZE: 100,
}

export const API_ROUTES = {
  AUTH: {
    LOGIN: '/api/auth/login',
    REGISTER: '/api/auth/register',
  },
  DRIVERS: '/api/drivers',
  TRAILERS: '/api/trailers',
  ROUTES: '/api/routes',
  TRIPS: '/api/trips',
  ORDERS: '/api/orders',
  ANALYTICS: '/api/analytics',
  AUDIT_LOGS: '/api/audit-logs',
  USERS: '/api/users',
}