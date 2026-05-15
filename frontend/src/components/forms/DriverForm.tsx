import React from 'react'
import { useForm } from 'react-hook-form'
import Box from '@mui/material/Box'
import Grid from '@mui/material/Grid'
import MenuItem from '@mui/material/MenuItem'
import { AppInput } from '../ui/AppInput'
import { AppButton } from '../ui/AppButton'
import { DriverCreate } from '../../types/driver.types'

interface DriverFormProps {
  onSubmit: (data: DriverCreate) => void
  onCancel: () => void
  initialData?: DriverCreate
  isLoading?: boolean
}

export const DriverForm: React.FC<DriverFormProps> = ({
  onSubmit,
  onCancel,
  initialData,
  isLoading,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<DriverCreate>({
    defaultValues: initialData || {
      full_name: '',
      license_number: '',
      phone: '',
      experience_years: 0,
      status: 'available',
    },
  })

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <AppInput
            label="Full Name"
            {...register('full_name', {
              required: 'Full name is required',
              minLength: {
                value: 2,
                message: 'Must be at least 2 characters',
              },
            })}
            error={errors.full_name?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="License Number"
            {...register('license_number', {
              required: 'License number is required',
            })}
            error={errors.license_number?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Phone"
            {...register('phone', {
              required: 'Phone is required',
              pattern: {
                value: /^\+?[\d\s\-\(\)]{7,20}$/,
                message: 'Invalid phone number',
              },
            })}
            error={errors.phone?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Experience (years)"
            type="number"
            {...register('experience_years', {
              required: 'Experience is required',
              min: { value: 0, message: 'Must be >= 0' },
            })}
            error={errors.experience_years?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Status"
            select
            {...register('status')}
          >
            <MenuItem value="available">Available</MenuItem>
            <MenuItem value="busy">Busy</MenuItem>
            <MenuItem value="off_duty">Off Duty</MenuItem>
            <MenuItem value="on_leave">On Leave</MenuItem>
          </AppInput>
        </Grid>
      </Grid>
      
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
        <AppButton onClick={onCancel} color="inherit">
          Cancel
        </AppButton>
        <AppButton type="submit" variant="contained" loading={isLoading}>
          Save
        </AppButton>
      </Box>
    </Box>
  )
}