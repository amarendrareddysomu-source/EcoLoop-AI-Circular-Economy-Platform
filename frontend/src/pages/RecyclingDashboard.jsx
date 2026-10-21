import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { StatusBadge } from '../components/StatusBadge';
import { formatDate } from '../utils/formatters';
import { Recycle, Layers, CheckCircle2, TrendingUp } from 'lucide-react';

export const RecyclingDashboard = () => {
  const [recyclingTxs, setRecyclingTxs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRecyclingData();
  }, []);

  const fetchRecyclingData = async () => {
    setLoading(true);
    try {
      const res = await api.get('/transactions/?transaction_type=recycling');
      setRecyclingTxs(res.data.items || []);
    } catch (err) {
      // Ignore
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-teal-700 via-emerald-800 to-slate-900 text-white shadow-xl flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold font-heading flex items-center space-x-2">
              <Recycle className="h-7 w-7" />
              <span>Recycling Center Portal</span>
            </h1>
            <p className="text-xs text-emerald-100 mt-1">
              Process e-waste and material recycling streams, track waste diversion kg, and log recycling batches.
            </p>
          </div>
        </div>

        {/* Recycling Queue Table */}
        <div className="p-5 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4">
          <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2">
            <Layers className="h-5 w-5 text-emerald-600" />
            <span>Recycling Batch Queue</span>
          </h3>

          {loading ? (
            <div className="h-48 bg-slate-200 dark:bg-slate-800 rounded-2xl animate-pulse"></div>
          ) : recyclingTxs.length === 0 ? (
            <p className="py-8 text-xs text-slate-400 text-center">No active recycling batches queued.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-100 dark:bg-slate-900/60 text-slate-700 dark:text-slate-300 font-bold border-b border-slate-200 dark:border-slate-800">
                  <tr>
                    <th className="p-3.5">ID</th>
                    <th className="p-3.5">Item ID</th>
                    <th className="p-3.5">Quantity</th>
                    <th className="p-3.5">Status</th>
                    <th className="p-3.5">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  {recyclingTxs.map((r) => (
                    <tr key={r.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/40">
                      <td className="p-3.5 font-bold">#{r.id}</td>
                      <td className="p-3.5 text-slate-600 dark:text-slate-400">Item #{r.item_id}</td>
                      <td className="p-3.5 font-semibold">{r.quantity} units</td>
                      <td className="p-3.5"><StatusBadge status={r.transaction_status || r.status} /></td>
                      <td className="p-3.5 text-slate-400">{formatDate(r.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};
