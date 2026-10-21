import React, { useState } from 'react';
import {
  Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField,
  MenuItem, Grid, Box, Typography, Alert, CircularProgress, Card, CardContent, Divider
} from '@mui/material';
import { AutoAwesome, CloudUpload } from '@mui/icons-material';
import api from '../services/api';

const categories = ["Battery", "Biological", "Cardboard", "Clothes", "Glass", "Metal", "Paper", "Plastic", "Shoes", "Trash"];
const conditions = ["Excellent", "Good", "Fair", "Poor"];
const usageLevels = ["Light", "Moderate", "Heavy"];

export const ItemUploadModal = ({ open, onClose, onItemCreated }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'Clothes',
    brand: 'Generic',
    age_years: 1.0,
    usage_level: 'Moderate',
    condition: 'Good',
    original_price: 100,
    location: 'Local City',
  });
  const [imageFile, setImageFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [loadingAi, setLoadingAi] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      runAiPreview(file);
    }
  };

  const runAiPreview = async (file) => {
    setLoadingAi(true);
    try {
      const data = new FormData();
      if (file) data.append('image', file);
      data.append('category_hint', formData.category);
      data.append('brand', formData.brand);
      data.append('age_years', formData.age_years);
      data.append('usage_level', formData.usage_level);
      data.append('original_price', formData.original_price);
      data.append('condition', formData.condition);

      const res = await api.post('/ai/analyze-image', data, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setAiAnalysis(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingAi(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      const submitData = new FormData();
      Object.keys(formData).forEach((key) => {
        submitData.append(key, formData[key]);
      });
      if (imageFile) {
        submitData.append('image', imageFile);
      }

      await api.post('/items/upload', submitData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      onItemCreated();
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload item');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle display="flex" alignItems="center" gap={1}>
        <AutoAwesome color="primary" /> Upload Item for AI Analysis
      </DialogTitle>
      <DialogContent dividers>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        
        <form id="upload-form" onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Box sx={{ border: '2px dashed', borderColor: 'divider', borderRadius: 3, p: 3, textAlign: 'center', bgcolor: 'action.hover', cursor: 'pointer' }} component="label">
                <input type="file" accept="image/*" hidden onChange={handleImageChange} />
                {previewUrl ? (
                  <Box component="img" src={previewUrl} sx={{ maxWidth: '100%', maxHeight: 200, borderRadius: 2 }} />
                ) : (
                  <>
                    <CloudUpload sx={{ fontSize: 48, color: 'text.secondary', mb: 1 }} />
                    <Typography variant="body1" fontWeight={600}>Upload Item Photo</Typography>
                    <Typography variant="caption" color="text.secondary">EfficientNet-B0 will classify your image automatically</Typography>
                  </>
                )}
              </Box>

              <TextField fullWidth margin="normal" label="Item Title" name="title" value={formData.title} onChange={handleChange} required />
              <TextField fullWidth margin="normal" label="Category" name="category" select value={formData.category} onChange={handleChange}>
                {categories.map((cat) => <MenuItem key={cat} value={cat}>{cat}</MenuItem>)}
              </TextField>
              <TextField fullWidth margin="normal" label="Brand / Manufacturer" name="brand" value={formData.brand} onChange={handleChange} />
              <TextField fullWidth margin="normal" label="Description" name="description" multiline rows={2} value={formData.description} onChange={handleChange} />
            </Grid>

            <Grid item xs={12} md={6}>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField fullWidth label="Age (Years)" name="age_years" type="number" value={formData.age_years} onChange={handleChange} required />
                </Grid>
                <Grid item xs={6}>
                  <TextField fullWidth label="Usage Level" name="usage_level" select value={formData.usage_level} onChange={handleChange}>
                    {usageLevels.map((lvl) => <MenuItem key={lvl} value={lvl}>{lvl}</MenuItem>)}
                  </TextField>
                </Grid>
                <Grid item xs={6}>
                  <TextField fullWidth label="Condition" name="condition" select value={formData.condition} onChange={handleChange}>
                    {conditions.map((cond) => <MenuItem key={cond} value={cond}>{cond}</MenuItem>)}
                  </TextField>
                </Grid>
                <Grid item xs={6}>
                  <TextField fullWidth label="Original Price ($)" name="original_price" type="number" value={formData.original_price} onChange={handleChange} required />
                </Grid>
                <Grid item xs={12}>
                  <TextField fullWidth label="Location / City" name="location" value={formData.location} onChange={handleChange} />
                </Grid>
              </Grid>

              {/* Instant AI Prediction Preview Card */}
              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle2" color="primary" fontWeight={700} display="flex" alignItems="center" gap={0.5} gutterBottom>
                  <AutoAwesome fontSize="small" /> AI Live Evaluation Preview
                </Typography>
                <Card variant="outlined" sx={{ bgcolor: 'action.hover' }}>
                  <CardContent sx={{ py: 1.5, '&:last-child': { pb: 1.5 } }}>
                    {loadingAi ? (
                      <Box display="flex" alignItems="center" gap={2} py={2}>
                        <CircularProgress size={24} />
                        <Typography variant="caption">AI Analyzing EfficientNet-B0 & Random Forest model...</Typography>
                      </Box>
                    ) : aiAnalysis ? (
                      <Grid container spacing={1}>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">Rec. Action:</Typography>
                          <Typography variant="body2" fontWeight={800} color="primary">{aiAnalysis.recommended_action}</Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">Est. Resale:</Typography>
                          <Typography variant="body2" fontWeight={800}>${aiAnalysis.estimated_resale_price}</Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">CO₂ Saved:</Typography>
                          <Typography variant="body2">{aiAnalysis.co2_saved_kg} kg</Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">Waste Diverted:</Typography>
                          <Typography variant="body2">{aiAnalysis.waste_diverted_kg} kg</Typography>
                        </Grid>
                      </Grid>
                    ) : (
                      <Button variant="text" size="small" onClick={() => runAiPreview(imageFile)}>
                        Click to calculate instant AI estimate
                      </Button>
                    )}
                  </CardContent>
                </Card>
              </Box>
            </Grid>
          </Grid>
        </form>
      </DialogContent>
      <DialogActions sx={{ px: 3, py: 2 }}>
        <Button onClick={onClose}>Cancel</Button>
        <Button type="submit" form="upload-form" variant="contained" color="primary" disabled={submitting} startIcon={<AutoAwesome />}>
          {submitting ? 'Analyzing & Uploading...' : 'Upload & Run Full AI Analysis'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
