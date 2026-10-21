import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import { X, Sparkles, AlertCircle } from 'lucide-react';

export const InventoryModal = ({ isOpen, onClose, onRefresh, initialData = null }) => {
  const [formData, setFormData] = useState({
    item_name: '',
    description: '',
    category: 'Electronics',
    quantity: 1,
    unit: 'pcs',
    price: 0,
    condition: 'Good',
    status: 'Available',
    brand: 'Generic',
    location: 'Local City'
  });

  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState('');
  const [aiSuggestion, setAiSuggestion] = useState(null);

  const normalizeCategory = (cat) => {
    if (!cat) return 'Clothes';
    if (cat === 'Clothing') return 'Clothes';
    if (cat === 'Organic Waste') return 'Biological';
    if (cat === 'Cardboard Box') return 'Cardboard';
    if (cat === 'Paper Sheet') return 'Paper';
    if (cat === 'Glass Bottle') return 'Glass';
    if (cat === 'Aluminium Can' || cat === 'Steel Can') return 'Metal';
    if (cat === 'Plastic Bottle' || cat === 'Plastic Cover' || cat === 'Plastic Bag') return 'Plastic';
    if (cat === 'Battery AA' || cat === 'Battery AAA') return 'Battery';
    if (cat === 'Footwear' || cat === 'Sneakers') return 'Shoes';
    const valid = ['Battery', 'Biological', 'Cardboard', 'Clothes', 'Glass', 'Metal', 'Paper', 'Plastic', 'Shoes', 'Trash'];
    return valid.includes(cat) ? cat : 'Clothes';
  };

  useEffect(() => {
    if (initialData) {
      setFormData({
        item_name: initialData.item_name || initialData.title || '',
        description: initialData.description || '',
        category: normalizeCategory(initialData.category),
        quantity: initialData.quantity || 1,
        unit: initialData.unit || 'pcs',
        price: initialData.price || 0,
        condition: initialData.condition || 'Good',
        status: initialData.status || 'Available',
        brand: initialData.brand || 'Generic',
        location: initialData.location || 'Local City'
      });
    } else {
      setFormData({
        item_name: '',
        description: '',
        category: 'Clothes',
        quantity: 1,
        unit: 'pcs',
        price: 0,
        condition: 'Good',
        status: 'Available',
        brand: 'Generic',
        location: 'Local City'
      });
    }
    setError('');
    setAiSuggestion(null);
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'quantity' || name === 'price' ? parseFloat(value) || 0 : value
    }));
  };

  const handleAiEvaluate = async () => {
    if (!formData.category) return;
    setAiLoading(true);
    try {
      const res = await api.post('/ai/predict-price', {
        category: formData.category,
        brand: formData.brand,
        age_years: 1.0,
        condition: formData.condition,
        original_price: formData.price || 100.0
      });
      setAiSuggestion(res.data);
      if (res.data.predicted_resale_price) {
        setFormData((prev) => ({ ...prev, price: res.data.predicted_resale_price }));
      }
    } catch (err) {
      // Ignore AI error
    } finally {
      setAiLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (initialData?.id) {
        await api.put(`/inventory/${initialData.id}`, formData);
      } else {
        await api.post('/inventory/', formData);
      }
      onRefresh();
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save inventory item');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <h3 className="text-lg font-bold font-heading text-slate-900 dark:text-slate-100">
            {initialData ? 'Edit Inventory Item' : 'Add New Inventory Item'}
          </h3>
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
            <X className="h-5 w-5" />
          </button>
        </div>

        {error && (
          <div className="p-3 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 rounded-xl text-rose-600 dark:text-rose-400 text-xs flex items-center space-x-2">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Item Name *</label>
            <input
              type="text"
              name="item_name"
              required
              value={formData.item_name}
              onChange={handleChange}
              placeholder="e.g. Solar Generator 2000W"
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Category *</label>
              <select
                name="category"
                value={formData.category}
                onChange={handleChange}
                className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                {['Battery', 'Biological', 'Cardboard', 'Clothes', 'Glass', 'Metal', 'Paper', 'Plastic', 'Shoes', 'Trash'].map((cat) => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Condition *</label>
              <select
                name="condition"
                value={formData.condition}
                onChange={handleChange}
                className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="New">New</option>
                <option value="Used">Used</option>
                <option value="Excellent">Excellent</option>
                <option value="Good">Good</option>
                <option value="Fair">Fair</option>
                <option value="Poor">Poor</option>
                <option value="Damaged">Damaged</option>
                <option value="Recycled">Recycled</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Quantity</label>
              <input
                type="number"
                name="quantity"
                min="0"
                value={formData.quantity}
                onChange={handleChange}
                className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Unit</label>
              <input
                type="text"
                name="unit"
                value={formData.unit}
                onChange={handleChange}
                placeholder="pcs"
                className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Price (USD $)</label>
              <input
                type="number"
                name="price"
                step="0.01"
                min="0"
                value={formData.price}
                onChange={handleChange}
                className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>

          <div className="flex items-center justify-between p-3 bg-emerald-50 dark:bg-emerald-950/40 rounded-xl border border-emerald-200 dark:border-emerald-800/50 text-xs">
            <div className="flex items-center space-x-2">
              <Sparkles className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
              <span className="font-medium text-emerald-950 dark:text-emerald-200">AI Price Estimator</span>
            </div>
            <button
              type="button"
              onClick={handleAiEvaluate}
              disabled={aiLoading}
              className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold text-xs transition-colors"
            >
              {aiLoading ? 'Estimating...' : 'Suggest Price'}
            </button>
          </div>

          {aiSuggestion && (
            <p className="text-xs text-emerald-600 dark:text-emerald-400 font-semibold">
              Suggested Value: {aiSuggestion.resale_value_display !== 'Not Applicable' ? aiSuggestion.resale_value_display : (aiSuggestion.recycling_value_display || `₹${Math.round((aiSuggestion.recycling_value || 0) * 83)} ($${aiSuggestion.recycling_value || 0})`)}
            </p>
          )}

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Description</label>
            <textarea
              name="description"
              rows="3"
              value={formData.description}
              onChange={handleChange}
              placeholder="Item condition details, specifications, or notes..."
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            ></textarea>
          </div>

          <div className="flex justify-end space-x-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2 text-sm font-semibold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-md shadow-emerald-600/20"
            >
              {loading ? 'Saving...' : initialData ? 'Update Item' : 'Create Item'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
