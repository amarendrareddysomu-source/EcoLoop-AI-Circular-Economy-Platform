import React from 'react';
import { Card, CardMedia, CardContent, CardActions, Typography, Box, Button, Chip } from '@mui/material';
import { AutoAwesome, LocationOn, AttachMoney } from '@mui/icons-material';
import { StatusChip } from './StatusChip';
import { useNavigate } from 'react-router-dom';

export const ItemCard = ({ item, onActionClick }) => {
  const navigate = useNavigate();

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', transition: 'transform 0.2s', '&:hover': { transform: 'translateY(-4px)' } }}>
      <Box sx={{ position: 'relative' }}>
        <CardMedia
          component="img"
          height="180"
          image={item.image_url || 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=600&q=80'}
          alt={item.title}
        />
        <Box sx={{ position: 'absolute', top: 12, right: 12 }}>
          <StatusChip label={item.recommended_action} />
        </Box>
        <Box sx={{ position: 'absolute', bottom: 12, left: 12 }}>
          <Chip label={item.category} size="small" sx={{ bgcolor: 'rgba(0,0,0,0.7)', color: '#fff', fontWeight: 600 }} />
        </Box>
      </Box>

      <CardContent sx={{ flexGrow: 1, pb: 1 }}>
        <Typography variant="h6" fontWeight={700} noWrap gutterBottom>
          {item.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden', height: 40, mb: 1.5 }}>
          {item.description || 'No description provided.'}
        </Typography>

        <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ bgcolor: 'action.hover', p: 1.5, borderRadius: 2, mb: 1 }}>
          <Box>
            <Typography variant="caption" color="text.secondary">Est. Value</Typography>
            <Typography variant="subtitle1" fontWeight={800} color="primary.main">
              ${item.estimated_price?.toFixed(2) || '0.00'}
            </Typography>
          </Box>
          <Box textAlign="right">
            <Typography variant="caption" color="text.secondary">Condition</Typography>
            <Typography variant="body2" fontWeight={700}>
              {item.condition}
            </Typography>
          </Box>
        </Box>

        <Box display="flex" alignItems="center" gap={1} color="text.secondary">
          <LocationOn fontSize="small" />
          <Typography variant="caption">{item.location}</Typography>
        </Box>
      </CardContent>

      <CardActions sx={{ p: 2, pt: 0 }}>
        <Button fullWidth variant="outlined" color="primary" onClick={() => navigate(`/items/${item.id}`)}>
          View AI Report
        </Button>
      </CardActions>
    </Card>
  );
};
