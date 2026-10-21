import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Button, Grid, Card, CardContent, Avatar, Chip, Stack } from '@mui/material';
import { Recycling, AutoAwesome, Forest, LocalShipping, ShieldCheck, ArrowForward, Balance } from '@mui/icons-material';
import { Link, useNavigate } from 'react-router-dom';
import { ItemCard } from '../components/ItemCard';
import api from '../services/api';

export const Home = () => {
  const navigate = useNavigate();
  const [recentItems, setRecentItems] = useState([]);

  useEffect(() => {
    fetchPublicItems();
  }, []);

  const fetchPublicItems = async () => {
    try {
      const res = await api.get('/items/');
      setRecentItems(res.data.slice(0, 6));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Box>
      {/* Hero Banner */}
      <Box sx={{ py: 12, background: 'radial-gradient(circle at top right, rgba(16,185,129,0.15), transparent 50%), radial-gradient(circle at bottom left, rgba(14,165,233,0.15), transparent 50%)', borderBottom: 1, borderColor: 'divider' }}>
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={7}>
              <Chip label="AI-POWERED SUSTAINABILITY PLATFORM" color="primary" sx={{ fontWeight: 800, mb: 2, px: 1 }} />
              <Typography variant="h1" sx={{ fontSize: { xs: '2.5rem', md: '3.75rem' }, lineHeight: 1.1, mb: 3 }}>
                Empowering the <span style={{ background: 'linear-gradient(45deg, #10b981, #0ea5e9)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Circular Economy</span> with AI
              </Typography>
              <Typography variant="h6" color="text.secondary" sx={{ fontWeight: 400, mb: 4 }}>
                Upload any item. Our multi-model AI system uses <b>EfficientNet-B0</b> image classification, CNN condition analysis, and Random Forest price prediction to guide your optimal action: <b>Repair, Reuse, Donate, Sell, or Recycle</b>.
              </Typography>
              <Stack direction="row" spacing={2}>
                <Button variant="contained" color="primary" size="large" onClick={() => navigate('/register')} startIcon={<AutoAwesome />}>
                  Analyze Your First Item
                </Button>
                <Button variant="outlined" color="primary" size="large" onClick={() => navigate('/login')}>
                  Browse Market & Impact
                </Button>
              </Stack>
            </Grid>
            <Grid item xs={12} md={5}>
              <Card sx={{ p: 3, border: '1px solid rgba(16,185,129,0.3)', backdropFilter: 'blur(20px)', background: 'rgba(255,255,255,0.03)' }}>
                <Box display="flex" alignItems="center" gap={2} mb={3}>
                  <Avatar sx={{ bgcolor: 'primary.main', width: 56, height: 56 }}>
                    <AutoAwesome fontSize="large" />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" fontWeight={700}>AI Recommendation Engine</Typography>
                    <Typography variant="caption" color="text.secondary">Multimodal Decision Support</Typography>
                  </Box>
                </Box>
                <Grid container spacing={2}>
                  {[
                    { title: "EfficientNet-B0", desc: "9 Category Classification" },
                    { title: "Random Forest", desc: "Resale Price Prediction" },
                    { title: "CNN Transfer Learning", desc: "Wear & Condition Analysis" },
                    { title: "Sustainability Math", desc: "CO₂ & Landfill Diverted" }
                  ].map((m, idx) => (
                    <Grid item xs={6} key={idx}>
                      <Box sx={{ p: 1.5, borderRadius: 2, bgcolor: 'action.hover' }}>
                        <Typography variant="subtitle2" fontWeight={700} color="primary">{m.title}</Typography>
                        <Typography variant="caption" color="text.secondary">{m.desc}</Typography>
                      </Box>
                    </Grid>
                  ))}
                </Grid>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Feature Cards */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h4" fontWeight={700} textAlign="center" mb={1}>
          5 Sustainable Circular Action Paths
        </Typography>
        <Typography variant="body1" color="text.secondary" textAlign="center" mb={6}>
          AI algorithms calculate maximum financial and environmental value for every item.
        </Typography>

        <Grid container spacing={3}>
          {[
            { action: "Repair", desc: "Extend lifespan for electronics and appliances with minor wear.", color: "#f59e0b" },
            { action: "Reuse", desc: "Repurpose and upcycle items to prevent new raw resource extraction.", color: "#0ea5e9" },
            { action: "Donate", desc: "Connect good-condition goods directly to verified partner NGOs.", color: "#10b981" },
            { action: "Sell", desc: "Recover resale market value backed by Random Forest price estimators.", color: "#8b5cf6" },
            { action: "Recycle", desc: "Divert raw materials to specialized recycling center processing queues.", color: "#ec4899" }
          ].map((item, idx) => (
            <Grid item xs={12} sm={6} md={2.4} key={idx}>
              <Card sx={{ height: '100%', textAlign: 'center', p: 2, borderTop: `4px solid ${item.color}` }}>
                <Typography variant="h6" fontWeight={800} sx={{ color: item.color, mb: 1 }}>{item.action}</Typography>
                <Typography variant="body2" color="text.secondary">{item.desc}</Typography>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Recent Platform Uploads */}
        <Box sx={{ mt: 8 }}>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
            <Box>
              <Typography variant="h5" fontWeight={700}>Public Sustainability Stream</Typography>
              <Typography variant="body2" color="text.secondary">Recently uploaded items actively entering the circular economy</Typography>
            </Box>
            <Button endIcon={<ArrowForward />} onClick={() => navigate('/register')}>View All Items</Button>
          </Box>

          {recentItems.length > 0 ? (
            <Grid container spacing={3}>
              {recentItems.map((item) => (
                <Grid item xs={12} sm={6} md={4} key={item.id}>
                  <ItemCard item={item} />
                </Grid>
              ))}
            </Grid>
          ) : (
            <Card sx={{ p: 4, textAlign: 'center' }}>
              <Typography variant="body1" color="text.secondary">No items uploaded yet. Be the first to analyze an item!</Typography>
            </Card>
          )}
        </Box>
      </Container>
    </Box>
  );
};
