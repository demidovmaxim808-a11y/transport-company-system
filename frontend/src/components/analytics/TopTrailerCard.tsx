import React from 'react'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemText from '@mui/material/ListItemText'
import { TrailerUtilization } from '../../types/order.types'

interface TopTrailerCardProps {
  trailers: TrailerUtilization[]
}

export const TopTrailerCard: React.FC<TopTrailerCardProps> = ({ trailers }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Trailer Utilization
        </Typography>
        <List>
          {trailers.map((trailer) => (
            <ListItem key={trailer.trailer_id}>
              <ListItemText
                primary={trailer.plate_number}
                secondary={`${trailer.trips_count} trips · ${trailer.utilization_percent}% utilization`}
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  )
}