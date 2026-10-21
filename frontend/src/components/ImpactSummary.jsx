import React from 'react';
import { Card, CardContent, Typography, Grid, Box, Avatar } from '@mui/material';
import { Forest, DeleteSweep, EnergySavingsLeaf, WorkspacePremium } from '@mui/icons-material';

export const ImpactSummary = ({ co2Saved = 0, wasteDiverted = 0, points = 0 }) => {
  const stats = [
    { title: 'CO₂ Saved', value: `${co2Saved.toFixed(1)} kg`, icon: <EnergySavingsLeaf />, color: '#10b981' },
    { title: 'Landfill Waste Diverted', value: `${wasteDiverted.toFixed(1)} kg`, icon: <DeleteSweep />, color: '#0ea5e9' },
    { title: 'Environmental Points', value: `${points.toFixed(0)} pts`, icon: <WorkspacePremium />, color: '#f59e0b' },
    { title: 'Equivalent Tree-Days', value: `${(co2Saved * 0.15).toFixed(1)} days`, icon: <Forest />, color: '#8b5cf6' },
  ];

  return (
    <Grid container spacing={3} sx={{ mb: 4 }}>
      {stats.map((stat, idx) => (
        <Grid item xs={12} sm={6} md={3} key={idx}>
          <Card sx={{ borderLeft: `5px solid ${stat.color}`, background: 'rgba(255,255,255,0.02)' }}>
            <CardContent display="flex" alignItems="center">
              <Box display="flex" alignItems="center" gap={2}>
                <Avatar sx={{ bgcolor: `${stat.color}20`, color: stat.color, width: 48, height: 48 }}>
                  {stat.icon}
                </Avatar>
                <Box>
                  <Typography variant="caption" color="text.secondary" fontWeight={600}>
                    {stat.title}
                  </Typography>
                  <Typography variant="h5" fontWeight={800}>
                    {stat.value}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};
