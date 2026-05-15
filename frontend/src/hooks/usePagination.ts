import { useState, useCallback } from 'react'

export const usePagination = (initialPage = 1, initialSize = 20) => {
  const [page, setPage] = useState(initialPage)
  const [size, setSize] = useState(initialSize)

  const handlePageChange = useCallback((newPage: number) => {
    setPage(newPage)
  }, [])

  const handleSizeChange = useCallback((newSize: number) => {
    setSize(newSize)
    setPage(1)
  }, [])

  return {
    page,
    size,
    handlePageChange,
    handleSizeChange,
  }
}