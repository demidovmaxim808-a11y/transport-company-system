import React from 'react'
import { useForm } from 'react-hook-form'
import Box from '@mui/material/Box'
import Grid from '@mui/material/Grid'
import MenuItem from '@mui/material/MenuItem'
import { AppInput } from '../ui/AppInput'
import { AppButton } from '../ui/AppButton'
import { OrderCreate } from '../../types/order.types'

interface OrderFormProps {
  onSubmit: (data: OrderCreate) => void
  onCancel: () => void
  initialData?: OrderCreate
  isLoading?: boolean
}

export const OrderForm: React.FC<OrderFormProps> = ({
  onSubmit,
  onCancel,
  initialData,
  isLoading,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<OrderCreate>({
    defaultValues: initialData || {
      customer_name: '',
      cargo_type: '',
      cargo_weight: 0,
      trip_id: null,
      status: 'pending',
      price: 0,
    },
  })

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <AppInput
            label="Customer Name"
            {...register('customer_name', {
              required: 'Customer name is required',
            })}
            error={errors.customer_name?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Cargo Type"
            {...register('cargo_type', {
              required: 'Cargo type is required',
            })}
            error={errors.cargo_type?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Cargo Weight (kg)"
            type="number"
            {...register('cargo_weight', {
              required: 'Weight is required',
              min: { value: 0, message: 'Must be > 0' },
              valueAsNumber: true,
            })}
            error={errors.cargo_weight?.message}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Price"
            type="number"
            {...register('price', {
              valueAsNumber: true,
            })}
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <AppInput
            label="Status"
            select
            {...register('status')}
          >
            <MenuItem value="pending">Pending</MenuItem>
            <MenuItem value="in_transit">In Transit</MenuItem>
            <MenuItem value="delivered">Delivered</MenuItem>
            <MenuItem value="cancelled">Cancelled</MenuItem>
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