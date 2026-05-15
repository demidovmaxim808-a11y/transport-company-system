import React from 'react'
import { useForm } from 'react-hook-form'
import Box from '@mui/material/Box'
import Grid from '@mui/material/Grid'
import MenuItem from '@mui/material/MenuItem'
import { AppInput } from '../ui/AppInput'
import { AppButton } from '../ui/AppButton'
import { TripCreate } from '../../types/trip.types'

interface TripFormProps {
  onSubmit: (data: TripCreate) => void
  onCancel: () => void
  initialData?: TripCreate
  isLoading?: boolean
}

export const TripForm: React.FC<TripFormProps> = ({
  onSubmit,
  onCancel,
  initialData,
  isLoading,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<TripCreate>({
    defaultValues: initialData || {
      driver_id: 0,
      trailer_id: 0,
      route_id: 0,
      start_date: new Date().toISOString().slice(0, 16),
      end_date: null,
      status: 'planned',
    },
  })

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Driver ID"
            type="number"
            {...register('driver_id', {
              required: 'Driver ID is required',
              valueAsNumber: true,
            })}
            error={errors.driver_id?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Trailer ID"
            type="number"
            {...register('trailer_id', {
              required: 'Trailer ID is required',
              valueAsNumber: true,
            })}
            error={errors.trailer_id?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Route ID"
            type="number"
            {...register('route_id', {
              required: 'Route ID is required',
              valueAsNumber: true,
            })}
            error={errors.route_id?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Status"
            select
            {...register('status')}
          >
            <MenuItem value="planned">Planned</MenuItem>
            <MenuItem value="in_progress">In Progress</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
            <MenuItem value="cancelled">Cancelled</MenuItem>
          </AppInput>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Start Date"
            type="datetime-local"
            InputLabelProps={{ shrink: true }}
            {...register('start_date', {
              required: 'Start date is required',
            })}
            error={errors.start_date?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="End Date"
            type="datetime-local"
            InputLabelProps={{ shrink: true }}
            {...register('end_date')}
          />
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