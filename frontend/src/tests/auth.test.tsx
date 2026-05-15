import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Provider } from 'react-redux'
import { BrowserRouter } from 'react-router-dom'
import { configureStore } from '@reduxjs/toolkit'
import authReducer from '../features/auth/authSlice'
import { LoginPage } from '../pages/auth/LoginPage'

const createTestStore = () => {
  return configureStore({
    reducer: {
      auth: authReducer,
    },
  })
}

describe('Auth', () => {
  it('renders login page', () => {
    const store = createTestStore()
    render(
      <Provider store={store}>
        <BrowserRouter>
          <LoginPage />
        </BrowserRouter>
      </Provider>
    )

    expect(screen.getByText('Sign In')).toBeDefined()
    expect(screen.getByLabelText('Email')).toBeDefined()
    expect(screen.getByLabelText('Password')).toBeDefined()
  })
})