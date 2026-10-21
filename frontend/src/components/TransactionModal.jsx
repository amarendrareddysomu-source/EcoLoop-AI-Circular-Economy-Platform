import React, { useState, useEffect } from 'react';
import api from '../api/axios';
import { X, AlertCircle, RefreshCw } from 'lucide-react';

export const TransactionModal = ({ isOpen, onClose, onRefresh, preselectedItem = null }) => {
  const [formData, setFormData] = useState({
    item_id: '',
    transaction_type: 'sale',
    transaction_status: 'Pending',
    quantity: 1,
    unit_price: 0,
    notes: ''
  });

  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      fetchAvailableItems();
      if (preselectedItem) {
        setFormData({
          item_id: preselectedItem.id,
          transaction_type: 'sale',
          transaction_status: 'Pending',
          quantity: 1,
          unit_price: preselectedItem.price || 0,
          notes: ''
        });
      }
    }
    setError('');
  }, [isOpen, preselectedItem]);

  const fetchAvailableItems = async () => {
    try {
      const res = await api.get('/inventory/?page_size=50');
      setItems(res.data.items || []);
    } catch (err) {
      // Ignore
    }
  };

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => {
      let nextStatus = prev.transaction_status;
      if (name === 'transaction_type') {
        nextStatus = (value === 'donation' || value === 'recycling' || value === 'transfer' || value === 'repair') ? 'Pending' : 'Completed';
      }
      return {
        ...prev,
        [name]: name === 'item_id' || name === 'quantity' || name === 'unit_price' ? parseFloat(value) || 0 : value,
        transaction_status: name === 'transaction_type' ? nextStatus : (name === 'transaction_status' ? value : prev.transaction_status)
      };
    });
  };

  const handleItemSelect = (e) => {
    const id = parseInt(e.target.value);
    const selected = items.find((i) => i.id === id);
    setFormData((prev) => ({
      ...prev,
      item_id: id,
      unit_price: selected ? selected.price : prev.unit_price
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await api.post('/transactions/', formData);
      onRefresh();
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Transaction failed. Check inventory stock availability.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
          <h3 className="text-lg font-bold font-heading text-slate-900 dark:text-slate-100">Create New Transaction</h3>
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
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Select Item *</label>
            <select
              name="item_id"
              required
              value={formData.item_id}
              onChange={handleItemSelect}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">-- Choose Inventory Item --</option>
              {items.map((i) => (
                <option key={i.id} value={i.id}>
                  {i.item_name || i.title} (Available: {i.quantity} {i.unit})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Transaction Type *</label>
            <select
              name="transaction_type"
              value={formData.transaction_type}
              onChange={handleChange}
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 capitalize"
            >
              <option value="sale">Sale (Outbound)</option>
              <option value="purchase">Purchase (Inbound Restock)</option>
              <option value="donation">Donation (NGO Route)</option>
              <option value="recycling">Recycling (Center Processing)</option>
              <option value="transfer">Transfer (Internal Relocation)</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Quantity *</label>
              <input
                type="number"
                name="quantity"
                min="1"
                required
                value={formData.quantity}
                onChange={handleChange}
                className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Unit Price ($)</label>
              <input
                type="number"
                name="unit_price"
                step="0.01"
                min="0"
                value={formData.unit_price}
                onChange={handleChange}
                className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>

          <div className="p-3 bg-slate-100 dark:bg-slate-800/60 rounded-xl text-xs flex justify-between font-semibold">
            <span className="text-slate-600 dark:text-slate-400">Total Amount:</span>
            <span className="text-emerald-600 dark:text-emerald-400">${(formData.quantity * formData.unit_price).toFixed(2)}</span>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Notes</label>
            <input
              type="text"
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              placeholder="Order ID, recipient NGO, or remarks..."
              className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
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
              {loading ? 'Processing...' : 'Submit Transaction'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
