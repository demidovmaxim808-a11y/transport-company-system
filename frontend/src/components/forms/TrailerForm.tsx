import React from 'react'
import { useForm } from 'react-hook-form'
import Box from '@mui/material/Box'
import Grid from '@mui/material/Grid'
import MenuItem from '@mui/material/MenuItem'
import { AppInput } from '../ui/AppInput'
import { AppButton } from '../ui/AppButton'
import { TrailerCreate } from '../../types/trailer.types'

interface TrailerFormProps {
  onSubmit: (data: TrailerCreate) => void
  onCancel: () => void
  initialData?: TrailerCreate
  isLoading?: boolean
}

export const TrailerForm: React.FC<TrailerFormProps> = ({
  onSubmit,
  onCancel,
  initialData,
  isLoading,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<TrailerCreate>({
    defaultValues: initialData || {
      model: '',
      plate_number: '',
      capacity: 0,
      status: 'available',
    },
  })

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <AppInput
            label="Model"
            {...register('model', {
              required: 'Model is required',
            })}
            error={errors.model?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Plate Number"
            {...register('plate_number', {
              required: 'Plate number is required',
              pattern: {
                value: /^[A-Z0-9]{5,20}$/i,
                message: 'Invalid plate number',
              },
            })}
            error={errors.plate_number?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Capacity (kg)"
            type="number"
            {...register('capacity', {
              required: 'Capacity is required',
              min: { value: 0, message: 'Must be > 0' },
              valueAsNumber: true,
            })}
            error={errors.capacity?.message}
          />
        </Grid>
        
        <Grid item xs={12}>
          <AppInput
            label="Status"
            select
            {...register('status')}
          >
            <MenuItem value="available">Available</MenuItem>
            <MenuItem value="in_use">In Use</MenuItem>
            <MenuItem value="maintenance">Maintenance</MenuItem>
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