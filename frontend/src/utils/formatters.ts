import { format, parseISO } from 'date-fns'

export const formatters = {
  date: (date: string | Date, formatStr: string = 'yyyy-MM-dd'): string => {
    const dateObj = typeof date === 'string' ? parseISO(date) : date
    return format(dateObj, formatStr)
  },

  currency: (amount: number, currency: string = 'USD'): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency,
    }).format(amount)
  },

  phone: (phone: string): string => {
    const cleaned = phone.replace(/\D/g, '')
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/)
    if (match) {
      return '(' + match[1] + ') ' + match[2] + '-' + match[3]
    }
    return phone
  },

  status: (status: string): string => {
    return status.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())
  },

  percentage: (value: number, decimals: number = 1): string => {
    return value.toFixed(decimals) + '%'
  },

  distance: (km: number): string => {
    return km.toLocaleString() + ' km'
  },

  weight: (kg: number): string => {
    return kg.toLocaleString() + ' kg'
  },
}