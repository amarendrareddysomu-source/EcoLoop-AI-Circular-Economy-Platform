import React from 'react';
import { Chip } from '@mui/material';

const actionColors = {
  Repair: 'warning',
  Reuse: 'info',
  Donate: 'primary',
  Sell: 'success',
  Recycle: 'secondary',
  Available: 'default',
};

export const StatusChip = ({ label, type = 'action' }) => {
  const color = actionColors[label] || 'default';
  return (
    <Chip
      label={label}
      color={color}
      size="small"
      sx={{
        fontWeight: 700,
        fontSize: '0.75rem',
        borderRadius: '6px',
        px: 0.5,
      }}
    />
  );
};
