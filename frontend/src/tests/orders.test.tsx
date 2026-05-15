import { describe, it, expect } from 'vitest'
import { renderHook } from '@testing-library/react'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import { usePagination } from '../hooks/usePagination'

describe('Pagination Hook', () => {
  it('should initialize with default values', () => {
    const { result } = renderHook(() => usePagination())
    
    expect(result.current.page).toBe(1)
    expect(result.current.size).toBe(20)
  })

  it('should update page', () => {
    const { result } = renderHook(() => usePagination())
    
    result.current.handlePageChange(2)
    expect(result.current.page).toBe(2)
  })
})