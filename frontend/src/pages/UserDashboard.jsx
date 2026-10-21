import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Button, Grid, Tab, Tabs, Card, CardContent, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { Add, AutoAwesome, History, NaturePeople } from '@mui/icons-material';
import { ImpactSummary } from '../components/ImpactSummary';
import { ItemCard } from '../components/ItemCard';
import { ItemUploadModal } from '../components/ItemUploadModal';
import { StatusChip } from '../components/StatusChip';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

export const UserDashboard = () => {
  const { user } = useAuth();
  const [items, setItems] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [uploadOpen, setUploadOpen] = useState(false);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const itemRes = await api.get('/items/my-items');
      setItems(itemRes.data);
      const txRes = await api.get('/transactions/my-transactions');
      setTransactions(txRes.data);
    } catch (err) {
      console.error(err);
    }
  };

  const totalCo2 = items.reduce((acc, curr) => acc + (curr.co2_saved_kg || 0), 0);
  const totalWaste = items.reduce((acc, curr) => acc + (curr.waste_diverted_kg || 0), 0);
  const totalPoints = items.reduce((acc, curr) => acc + (curr.environmental_impact_points || 0), 0);

  return (
    <Container maxWidth="lg" sx={{ py: 6 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Box>
          <Typography variant="h4" fontWeight={800}>User Sustainability Dashboard</Typography>
          <Typography variant="body2" color="text.secondary">Manage uploaded items, view AI evaluations, and track your environmental impact.</Typography>
        </Box>
        <Button variant="contained" color="primary" startIcon={<Add />} onClick={() => setUploadOpen(true)} size="large">
          Analyze & Upload Item
        </Button>
      </Box>

      {/* Impact Overview */}
      <ImpactSummary co2Saved={totalCo2} wasteDiverted={totalWaste} points={totalPoints} />

      <Tabs value={tabValue} onChange={(e, val) => setTabValue(val)} sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tab label={`My Items (${items.length})`} icon={<AutoAwesome />} iconPosition="start" />
        <Tab label={`Transaction History (${transactions.length})`} icon={<History />} iconPosition="start" />
      </Tabs>

      {tabValue === 0 && (
        <Grid container spacing={3}>
          {items.length > 0 ? (
            items.map((item) => (
              <Grid item xs={12} sm={6} md={4} key={item.id}>
                <ItemCard item={item} />
              </Grid>
            ))
          ) : (
            <Grid item xs={12}>
              <Card sx={{ p: 4, textAlign: 'center' }}>
                <Typography variant="h6">No items uploaded yet</Typography>
                <Typography variant="body2" color="text.secondary" mb={2}>Upload an item image or details to receive AI circular recommendations.</Typography>
                <Button variant="contained" color="primary" onClick={() => setUploadOpen(true)}>Upload Your First Item</Button>
              </Card>
            </Grid>
          )}
        </Grid>
      )}

      {tabValue === 1 && (
        <TableContainer component={Paper} variant="outlined">
          <Table>
            <TableHead sx={{ bgcolor: 'action.hover' }}>
              <TableRow>
                <TableCell><b>TX ID</b></TableCell>
                <TableCell><b>Action Type</b></TableCell>
                <TableCell><b>Status</b></TableCell>
                <TableCell><b>CO₂ Saved</b></TableCell>
                <TableCell><b>Waste Diverted</b></TableCell>
                <TableCell><b>Notes</b></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {transactions.length > 0 ? (
                transactions.map((tx) => (
                  <TableRow key={tx.id}>
                    <TableCell>#{tx.id}</TableCell>
                    <TableCell><StatusChip label={tx.action_type.toUpperCase()} /></TableCell>
                    <TableCell>{tx.status}</TableCell>
                    <TableCell>{tx.co2_saved_kg} kg</TableCell>
                    <TableCell>{tx.waste_diverted_kg} kg</TableCell>
                    <TableCell>{tx.notes || '—'}</TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={6} align="center">No transactions recorded yet.</TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <ItemUploadModal open={uploadOpen} onClose={() => setUploadOpen(false)} onItemCreated={fetchUserData} />
    </Container>
  );
};
