import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Grid, Card, CardMedia, CardContent, Chip, Button, Divider, Alert, CircularProgress } from '@mui/material';
import { AutoAwesome, LocationOn, AttachMoney, ShieldCheck, EnergySavingsLeaf, ArrowBack, LocalShipping, Favorite, Recycling } from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { StatusChip } from '../components/StatusChip';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

export const ItemDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionSuccess, setActionSuccess] = useState('');

  useEffect(() => {
    fetchItemDetails();
  }, [id]);

  const fetchItemDetails = async () => {
    try {
      const res = await api.get(`/items/${id}`);
      setItem(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (actionType) => {
    try {
      await api.post('/transactions/', {
        item_id: item.id,
        action_type: actionType,
        notes: `User initiated ${actionType} action on platform.`
      });
      setActionSuccess(`Successfully initiated ${actionType} action! View updates on your dashboard.`);
      fetchItemDetails();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <Box display="flex" justifyContent="center" py={10}><CircularProgress /></Box>;
  if (!item) return <Container sx={{ py: 6 }}><Typography>Item not found.</Typography></Container>;

  return (
    <Container maxWidth="lg" sx={{ py: 6 }}>
      <Button startIcon={<ArrowBack />} onClick={() => navigate(-1)} sx={{ mb: 3 }}>
        Back
      </Button>

      {actionSuccess && <Alert severity="success" sx={{ mb: 3 }}>{actionSuccess}</Alert>}

      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Card variant="outlined" sx={{ overflow: 'hidden' }}>
            <CardMedia
              component="img"
              height="380"
              image={item.image_url || 'https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=800&q=80'}
              alt={item.title}
            />
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Box display="flex" alignItems="center" gap={1.5} mb={1}>
            <StatusChip label={item.recommended_action} />
            <Chip label={item.category} size="small" variant="outlined" />
            <Chip label={`Status: ${item.status}`} size="small" color="primary" />
          </Box>

          <Typography variant="h3" fontWeight={800} gutterBottom>{item.title}</Typography>
          
          <Box display="flex" alignItems="center" gap={1} color="text.secondary" mb={3}>
            <LocationOn fontSize="small" />
            <Typography variant="body2">{item.location} • Age: {item.age_years} yrs • Usage: {item.usage_level}</Typography>
          </Box>

          <Typography variant="body1" color="text.secondary" paragraph>
            {item.description || 'No detailed description provided.'}
          </Typography>

          <Divider sx={{ my: 3 }} />

          {/* AI Decision Breakdown */}
          <Box sx={{ bgcolor: 'action.hover', p: 3, borderRadius: 3, mb: 3 }}>
            <Typography variant="h6" fontWeight={700} color="primary" display="flex" alignItems="center" gap={1} mb={2}>
              <AutoAwesome /> AI Multi-Model Evaluation Report
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography variant="caption" color="text.secondary">Primary Classifier:</Typography>
                <Typography variant="body2" fontWeight={700}>{item.predicted_category || item.category} (EfficientNet-B0)</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="caption" color="text.secondary">Predicted Wear Condition:</Typography>
                <Typography variant="body2" fontWeight={700}>{item.predicted_condition || item.condition} (CNN Transfer)</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="caption" color="text.secondary">Est. Resale Price:</Typography>
                <Typography variant="h6" fontWeight={800} color="primary.main">${item.estimated_price?.toFixed(2)}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="caption" color="text.secondary">Original Value:</Typography>
                <Typography variant="body1" sx={{ textDecoration: 'line-through' }}>${item.original_price?.toFixed(2)}</Typography>
              </Grid>
            </Grid>
          </Box>

          {/* Environmental Impact Badges */}
          <Grid container spacing={2} mb={3}>
            <Grid item xs={4}>
              <Card variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                <Typography variant="caption" color="text.secondary">CO₂ Saved</Typography>
                <Typography variant="h6" fontWeight={800} color="success.main">{item.co2_saved_kg} kg</Typography>
              </Card>
            </Grid>
            <Grid item xs={4}>
              <Card variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                <Typography variant="caption" color="text.secondary">Waste Diverted</Typography>
                <Typography variant="h6" fontWeight={800} color="info.main">{item.waste_diverted_kg} kg</Typography>
              </Card>
            </Grid>
            <Grid item xs={4}>
              <Card variant="outlined" sx={{ p: 1.5, textAlign: 'center' }}>
                <Typography variant="caption" color="text.secondary">Impact Score</Typography>
                <Typography variant="h6" fontWeight={800} color="warning.main">{item.environmental_impact_points} pts</Typography>
              </Card>
            </Grid>
          </Grid>

          {/* Action Buttons */}
          {user && item.status === 'Available' && (
            <Box display="flex" gap={2}>
              {item.recommended_action === 'Donate' && (
                <Button fullWidth variant="contained" color="primary" startIcon={<Favorite />} onClick={() => handleAction('donate')}>
                  Donate to Partner NGO
                </Button>
              )}
              {item.recommended_action === 'Recycle' && (
                <Button fullWidth variant="contained" color="secondary" startIcon={<Recycling />} onClick={() => handleAction('recycle')}>
                  Send to Recycling Center
                </Button>
              )}
              {item.recommended_action === 'Sell' && (
                <Button fullWidth variant="contained" color="success" startIcon={<AttachMoney />} onClick={() => handleAction('sell')}>
                  List for Resale (${item.estimated_price?.toFixed(2)})
                </Button>
              )}
              {(item.recommended_action === 'Repair' || item.recommended_action === 'Reuse') && (
                <Button fullWidth variant="contained" color="warning" startIcon={<ShieldCheck />} onClick={() => handleAction('repair')}>
                  Mark Repaired / Reused
                </Button>
              )}
            </Box>
          )}
        </Grid>
      </Grid>
    </Container>
  );
};
