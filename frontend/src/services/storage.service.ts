const TOKEN_KEY = 'access_token'
const USER_KEY = 'user_data'

export const storageService = {
  getToken: (): string | null => {
    return localStorage.getItem(TOKEN_KEY)
  },

  setToken: (token: string): void => {
    localStorage.setItem(TOKEN_KEY, token)
  },

  clearToken: (): void => {
    localStorage.removeItem(TOKEN_KEY)
  },

  getUser: (): any | null => {
    const userStr = localStorage.getItem(USER_KEY)
    if (userStr) {
      return JSON.parse(userStr)
    }
    return null
  },

  setUser: (user: any): void => {
    localStorage.setItem(USER_KEY, JSON.stringify(user))
  },

  clearUser: (): void => {
    localStorage.removeItem(USER_KEY)
  },

  clearAll: (): void => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
  },
}