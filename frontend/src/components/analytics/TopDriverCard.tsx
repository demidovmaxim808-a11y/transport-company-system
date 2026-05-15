import React from 'react'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemText from '@mui/material/ListItemText'
import { DriverPerformance } from '../../types/order.types'

interface TopDriverCardProps {
  drivers: DriverPerformance[]
}

export const TopDriverCard: React.FC<TopDriverCardProps> = ({ drivers }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Top Drivers
        </Typography>
        <List>
          {drivers.map((driver) => (
            <ListItem key={driver.driver_id}>
              <ListItemText
                primary={driver.driver_name}
                secondary={`${driver.trips_count} trips · ${driver.total_km.toLocaleString()} km · $${driver.revenue_generated.toLocaleString()}`}
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  )
}