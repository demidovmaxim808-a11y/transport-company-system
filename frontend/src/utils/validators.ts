export const validators = {
  email: (email: string): boolean => {
    const re = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i
    return re.test(email)
  },

  phone: (phone: string): boolean => {
    const re = /^\+?[\d\s\-\(\)]{7,20}$/
    return re.test(phone)
  },

  plateNumber: (plate: string): boolean => {
    const re = /^[A-Z0-9]{5,20}$/i
    return re.test(plate)
  },

  password: (password: string): { valid: boolean; message?: string } => {
    if (password.length < 6) {
      return { valid: false, message: 'Password must be at least 6 characters' }
    }
    return { valid: true }
  },

  required: (value: any): boolean => {
    if (value === null || value === undefined || value === '') {
      return false
    }
    return true
  },
}