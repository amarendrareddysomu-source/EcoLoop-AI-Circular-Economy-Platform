import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { StatusBadge } from '../components/StatusBadge';
import { TransactionModal } from '../components/TransactionModal';
import { formatCurrency, formatDateTime } from '../utils/formatters';
import {
  ArrowLeftRight,
  Plus,
  Filter,
  Ban,
  ChevronLeft,
  ChevronRight,
  TrendingDown,
  TrendingUp,
  RefreshCw
} from 'lucide-react';

export const TransactionsPage = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [typeFilter, setTypeFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);

  const [isTxModalOpen, setIsTxModalOpen] = useState(false);

  useEffect(() => {
    fetchTransactions();
  }, [page, typeFilter, statusFilter]);

  const fetchTransactions = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.append('page', page);
      params.append('page_size', 10);
      if (typeFilter) params.append('transaction_type', typeFilter);
      if (statusFilter) params.append('status', statusFilter);

      const res = await api.get(`/transactions/?${params.toString()}`);
      setTransactions(res.data.items || []);
      setTotalPages(res.data.total_pages || 1);
      setTotalItems(res.data.total_items || 0);
    } catch (err) {
      // Ignore
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (id) => {
    if (!window.confirm('Cancel transaction? Inventory stock will be automatically restored.')) return;
    try {
      await api.delete(`/transactions/${id}`);
      fetchTransactions();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to cancel transaction');
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
          <div>
            <h1 className="text-2xl font-bold font-heading text-slate-900 dark:text-slate-100 flex items-center space-x-2">
              <ArrowLeftRight className="h-7 w-7 text-emerald-600 dark:text-emerald-400" />
              <span>Transaction Monitoring</span>
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Track purchase, sale, donation, recycling, and transfer operations ({totalItems} transactions)
            </p>
          </div>

          <button
            onClick={() => setIsTxModalOpen(true)}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs flex items-center space-x-2 shadow-md shadow-emerald-600/20 transition-all"
          >
            <Plus className="h-4 w-4" />
            <span>New Transaction</span>
          </button>
        </div>

        {/* Filters */}
        <div className="p-4 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-lg">
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500 capitalize"
          >
            <option value="">All Transaction Types</option>
            <option value="sale">Sale</option>
            <option value="purchase">Purchase</option>
            <option value="donation">Donation</option>
            <option value="recycling">Recycling</option>
            <option value="transfer">Transfer</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="">All Statuses</option>
            <option value="Completed">Completed</option>
            <option value="Pending">Pending</option>
            <option value="Cancelled">Cancelled</option>
          </select>
        </div>

        {/* Table */}
        {loading ? (
          <div className="h-64 bg-slate-200 dark:bg-slate-800 rounded-2xl animate-pulse"></div>
        ) : transactions.length === 0 ? (
          <div className="p-12 text-center glass-card border border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
            <ArrowLeftRight className="h-12 w-12 text-slate-400 mx-auto" />
            <h3 className="text-base font-bold text-slate-800 dark:text-slate-200">No Transactions Found</h3>
            <p className="text-xs text-slate-500">Initiate a transaction to see records here.</p>
          </div>
        ) : (
          <div className="glass-card border border-slate-200 dark:border-slate-800 rounded-2xl overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 dark:bg-slate-900/60 text-slate-700 dark:text-slate-300 font-bold border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th className="p-3.5">ID</th>
                  <th className="p-3.5">Type</th>
                  <th className="p-3.5">Item ID</th>
                  <th className="p-3.5">Quantity</th>
                  <th className="p-3.5">Total Amount</th>
                  <th className="p-3.5">Status</th>
                  <th className="p-3.5">Payment</th>
                  <th className="p-3.5">Date</th>
                  <th className="p-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {transactions.map((tx) => {
                  const isCancelled = (tx.transaction_status || tx.status) === 'Cancelled';
                  return (
                    <tr key={tx.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/40">
                      <td className="p-3.5 font-bold">#{tx.id}</td>
                      <td className="p-3.5 font-semibold text-emerald-600 dark:text-emerald-400 capitalize">
                        {tx.transaction_type || tx.action_type}
                      </td>
                      <td className="p-3.5 text-slate-500">Item #{tx.item_id}</td>
                      <td className="p-3.5 font-semibold">{tx.quantity}</td>
                      <td className="p-3.5 font-bold text-slate-900 dark:text-slate-100">{formatCurrency(tx.total_amount)}</td>
                      <td className="p-3.5"><StatusBadge status={tx.transaction_status || tx.status} /></td>
                      <td className="p-3.5"><StatusBadge status={tx.payment_status} /></td>
                      <td className="p-3.5 text-slate-400">{formatDateTime(tx.created_at)}</td>
                      <td className="p-3.5 text-right">
                        {!isCancelled && (
                          <button
                            onClick={() => handleCancel(tx.id)}
                            className="p-1.5 rounded-lg text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/40 font-semibold text-xs flex items-center space-x-1 ml-auto"
                            title="Cancel Transaction & Restore Inventory Stock"
                          >
                            <Ban className="h-3.5 w-3.5" />
                            <span>Cancel</span>
                          </button>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between pt-4">
            <span className="text-xs text-slate-500">Page {page} of {totalPages}</span>
            <div className="flex space-x-2">
              <button
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                className="p-2 rounded-xl border border-slate-200 dark:border-slate-800 text-xs disabled:opacity-50"
              >
                <ChevronLeft className="h-4 w-4" />
              </button>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                className="p-2 rounded-xl border border-slate-200 dark:border-slate-800 text-xs disabled:opacity-50"
              >
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}
      </div>

      <TransactionModal
        isOpen={isTxModalOpen}
        onClose={() => setIsTxModalOpen(false)}
        onRefresh={fetchTransactions}
      />
    </DashboardLayout>
  );
};
