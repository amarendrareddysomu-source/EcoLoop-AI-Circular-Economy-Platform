import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axios';
import { useAuth } from '../context/AuthContext';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { StatusBadge } from '../components/StatusBadge';
import { formatCurrency, formatDate } from '../utils/formatters';
import {
  Boxes,
  ArrowLeftRight,
  Leaf,
  Recycle,
  Sparkles,
  TrendingUp,
  PlusCircle
} from 'lucide-react';

export const Dashboard = () => {
  const { user } = useAuth();
  const [analytics, setAnalytics] = useState(null);
  const [recentItems, setRecentItems] = useState([]);
  const [recentTransactions, setRecentTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [analyticsRes, itemsRes, txRes] = await Promise.all([
        api.get('/analytics/dashboard'),
        api.get('/inventory/?page_size=5'),
        api.get('/transactions/?page_size=5')
      ]);

      setAnalytics(analyticsRes.data);
      setRecentItems(itemsRes.data.items || []);
      setRecentTransactions(txRes.data.items || []);
    } catch (err) {
      // Ignore
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Banner */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-emerald-600 via-teal-600 to-indigo-700 text-white shadow-xl flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
          <div>
            <h1 className="text-2xl font-bold font-heading">Welcome, {user?.full_name || 'Sustainability Pioneer'}!</h1>
            <p className="text-xs text-emerald-100 mt-1 max-w-xl">
              Track inventory lifecycle, analyze carbon footprint reduction, and drive circular transactions across the ecosystem.
            </p>
          </div>
          <div className="flex space-x-3">
            <Link
              to="/inventory"
              className="px-4 py-2 bg-white text-emerald-950 rounded-xl font-bold text-xs hover:bg-emerald-50 transition-colors shadow-md"
            >
              Manage Inventory
            </Link>
            <Link
              to="/ai-predictions"
              className="px-4 py-2 bg-emerald-500/30 backdrop-blur-md border border-white/20 text-white rounded-xl font-bold text-xs hover:bg-emerald-500/50 transition-colors"
            >
              AI Evaluation
            </Link>
          </div>
        </div>

        {/* Analytics Cards */}
        {loading ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 animate-pulse">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-28 bg-slate-200 dark:bg-slate-800 rounded-2xl"></div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-2">
              <div className="flex justify-between items-center text-emerald-600 dark:text-emerald-400">
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">Total Items</span>
                <Boxes className="h-5 w-5" />
              </div>
              <p className="text-2xl font-bold font-heading text-slate-900 dark:text-slate-100">
                {analytics?.total_items || 0}
              </p>
              <p className="text-xs text-slate-400">Catalog inventory units</p>
            </div>

            <div className="p-4 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-2">
              <div className="flex justify-between items-center text-teal-600 dark:text-teal-400">
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 font-heading">Transactions</span>
                <ArrowLeftRight className="h-5 w-5" />
              </div>
              <p className="text-2xl font-bold font-heading text-slate-900 dark:text-slate-100">
                {analytics?.total_transactions || 0}
              </p>
              <p className="text-xs text-slate-400">Completed operations</p>
            </div>

            <div className="p-4 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-2">
              <div className="flex justify-between items-center text-indigo-600 dark:text-indigo-400">
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">CO2 Saved</span>
                <Leaf className="h-5 w-5" />
              </div>
              <p className="text-2xl font-bold font-heading text-slate-900 dark:text-slate-100">
                {analytics?.co2_saved_kg || 0} <span className="text-xs text-slate-400 font-normal">kg</span>
              </p>
              <p className="text-xs text-slate-400">Emissions prevented</p>
            </div>

            <div className="p-4 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-2">
              <div className="flex justify-between items-center text-amber-600 dark:text-amber-400">
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">Waste Reduced</span>
                <Recycle className="h-5 w-5" />
              </div>
              <p className="text-2xl font-bold font-heading text-slate-900 dark:text-slate-100">
                {analytics?.waste_reduced_kg || 0} <span className="text-xs text-slate-400 font-normal">kg</span>
              </p>
              <p className="text-xs text-slate-400">Diverted from landfills</p>
            </div>
          </div>
        )}

        {/* Recent Activity Sections */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Inventory */}
          <div className="p-5 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-base font-bold font-heading text-slate-900 dark:text-slate-100">Recent Inventory Items</h3>
              <Link to="/inventory" className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline">
                View All
              </Link>
            </div>

            <div className="divide-y divide-slate-100 dark:divide-slate-800">
              {recentItems.length === 0 ? (
                <p className="py-4 text-xs text-slate-400 text-center">No inventory items registered yet.</p>
              ) : (
                recentItems.map((item) => (
                  <div key={item.id} className="py-3 flex items-center justify-between">
                    <div>
                      <h4 className="text-xs font-bold text-slate-800 dark:text-slate-200">{item.item_name || item.title}</h4>
                      <p className="text-[11px] text-slate-400">{item.category} • {item.quantity} {item.unit}</p>
                    </div>
                    <div className="text-right space-y-1">
                      <p className="text-xs font-bold text-emerald-600 dark:text-emerald-400">{formatCurrency(item.price)}</p>
                      <StatusBadge status={item.status} />
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Recent Transactions */}
          <div className="p-5 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-base font-bold font-heading text-slate-900 dark:text-slate-100">Recent Transactions</h3>
              <Link to="/transactions" className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 hover:underline">
                View All
              </Link>
            </div>

            <div className="divide-y divide-slate-100 dark:divide-slate-800">
              {recentTransactions.length === 0 ? (
                <p className="py-4 text-xs text-slate-400 text-center">No transactions recorded yet.</p>
              ) : (
                recentTransactions.map((tx) => (
                  <div key={tx.id} className="py-3 flex items-center justify-between">
                    <div>
                      <h4 className="text-xs font-bold text-slate-800 dark:text-slate-200 capitalize">
                        {tx.transaction_type || tx.action_type} Transaction #{tx.id}
                      </h4>
                      <p className="text-[11px] text-slate-400">Qty: {tx.quantity} • {formatDate(tx.created_at)}</p>
                    </div>
                    <div className="text-right space-y-1">
                      <p className="text-xs font-bold text-slate-900 dark:text-slate-100">{formatCurrency(tx.total_amount)}</p>
                      <StatusBadge status={tx.transaction_status || tx.status} />
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};
