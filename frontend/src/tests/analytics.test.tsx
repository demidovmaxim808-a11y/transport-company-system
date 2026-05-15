import { describe, it, expect } from 'vitest'
import { formatters } from '../utils/formatters'

describe('Formatters', () => {
  it('should format currency correctly', () => {
    const result = formatters.currency(1234.56)
    expect(result).toContain('1,234.56')
  })

  it('should format date correctly', () => {
    const result = formatters.date('2024-01-15', 'yyyy-MM-dd')
    expect(result).toBe('2024-01-15')
  })

  it('should format status correctly', () => {
    const result = formatters.status('in_progress')
    expect(result).toBe('In Progress')
  })
})