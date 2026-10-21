import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { StatusBadge } from '../components/StatusBadge';
import { InventoryModal } from '../components/InventoryModal';
import { TransactionModal } from '../components/TransactionModal';
import { formatCurrency, formatDate } from '../utils/formatters';
import {
  Boxes,
  Plus,
  Search,
  Filter,
  Edit2,
  Trash2,
  ArrowLeftRight,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  LayoutGrid,
  List as ListIcon
} from 'lucide-react';

export const InventoryPage = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [condition, setCondition] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'table'

  const [isItemModalOpen, setIsItemModalOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);

  const [isTxModalOpen, setIsTxModalOpen] = useState(false);
  const [txSelectedItem, setTxSelectedItem] = useState(null);

  useEffect(() => {
    fetchInventory();
  }, [page, search, category, statusFilter, condition]);

  const fetchInventory = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.append('page', page);
      params.append('page_size', 9);
      if (search) params.append('search', search);
      if (category) params.append('category', category);
      if (statusFilter) params.append('status', statusFilter);
      if (condition) params.append('condition', condition);

      const res = await api.get(`/inventory/?${params.toString()}`);
      setItems(res.data.items || []);
      setTotalPages(res.data.total_pages || 1);
      setTotalItems(res.data.total_items || 0);
    } catch (err) {
      // Ignore
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (item) => {
    setSelectedItem(item);
    setIsItemModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this inventory item?')) return;
    try {
      await api.delete(`/inventory/${id}`);
      fetchInventory();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to delete item');
    }
  };

  const handleTransact = (item) => {
    setTxSelectedItem(item);
    setIsTxModalOpen(true);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
          <div>
            <h1 className="text-2xl font-bold font-heading text-slate-900 dark:text-slate-100 flex items-center space-x-2">
              <Boxes className="h-7 w-7 text-emerald-600 dark:text-emerald-400" />
              <span>Inventory Catalog</span>
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Browse, add, filter, and manage circular inventory items ({totalItems} items)
            </p>
          </div>

          <div className="flex space-x-3">
            <div className="flex bg-slate-200 dark:bg-slate-800 p-1 rounded-xl">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-1.5 rounded-lg text-xs font-semibold ${viewMode === 'grid' ? 'bg-white dark:bg-slate-900 text-emerald-600 shadow-sm' : 'text-slate-500'}`}
              >
                <LayoutGrid className="h-4 w-4" />
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`p-1.5 rounded-lg text-xs font-semibold ${viewMode === 'table' ? 'bg-white dark:bg-slate-900 text-emerald-600 shadow-sm' : 'text-slate-500'}`}
              >
                <ListIcon className="h-4 w-4" />
              </button>
            </div>

            <button
              onClick={() => {
                setSelectedItem(null);
                setIsItemModalOpen(true);
              }}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs flex items-center space-x-2 shadow-md shadow-emerald-600/20 transition-all"
            >
              <Plus className="h-4 w-4" />
              <span>Add Item</span>
            </button>
          </div>
        </div>

        {/* Search & Filter Bar */}
        <div className="p-4 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          <div className="relative">
            <Search className="h-4 w-4 absolute left-3 top-3 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by item name or details..."
              className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="">All Categories</option>
            <option value="Battery">Battery</option>
            <option value="Biological">Biological</option>
            <option value="Cardboard">Cardboard</option>
            <option value="Clothes">Clothes</option>
            <option value="Glass">Glass</option>
            <option value="Metal">Metal</option>
            <option value="Paper">Paper</option>
            <option value="Plastic">Plastic</option>
            <option value="Shoes">Shoes</option>
            <option value="Trash">Trash</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="">All Statuses</option>
            <option value="Available">Available</option>
            <option value="Reserved">Reserved</option>
            <option value="Sold">Sold</option>
            <option value="Recycled">Recycled</option>
          </select>

          <select
            value={condition}
            onChange={(e) => setCondition(e.target.value)}
            className="px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            <option value="">All Conditions</option>
            <option value="New">New</option>
            <option value="Excellent">Excellent</option>
            <option value="Good">Good</option>
            <option value="Fair">Fair</option>
            <option value="Poor">Poor</option>
          </select>
        </div>

        {/* Content */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 animate-pulse">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="h-44 bg-slate-200 dark:bg-slate-800 rounded-2xl"></div>
            ))}
          </div>
        ) : items.length === 0 ? (
          <div className="p-12 text-center glass-card border border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
            <Boxes className="h-12 w-12 text-slate-400 mx-auto" />
            <h3 className="text-base font-bold text-slate-800 dark:text-slate-200">No Inventory Items Found</h3>
            <p className="text-xs text-slate-500">Try clearing filters or adding a new inventory item.</p>
          </div>
        ) : viewMode === 'grid' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {items.map((item) => (
              <div
                key={item.id}
                className="p-5 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 flex flex-col justify-between hover:shadow-xl transition-all space-y-4"
              >
                <div className="space-y-2">
                  <div className="flex justify-between items-start">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/40">
                      {item.category}
                    </span>
                    <StatusBadge status={item.status} />
                  </div>

                  <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 line-clamp-1">
                    {item.item_name || item.title}
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-2">
                    {item.description || 'No description provided.'}
                  </p>
                </div>

                <div className="space-y-3 pt-3 border-t border-slate-100 dark:border-slate-800">
                  <div className="flex justify-between items-center text-xs">
                    <div>
                      <p className="text-slate-400 text-[10px]">Condition</p>
                      <p className="font-semibold text-slate-700 dark:text-slate-300">{item.condition}</p>
                    </div>
                    <div>
                      <p className="text-slate-400 text-[10px]">Stock</p>
                      <p className="font-semibold text-slate-700 dark:text-slate-300">{item.quantity} {item.unit}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-slate-400 text-[10px]">Price</p>
                      <p className="font-bold text-emerald-600 dark:text-emerald-400 text-sm">{formatCurrency(item.price)}</p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <button
                      onClick={() => handleTransact(item)}
                      className="px-3 py-1.5 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-100 rounded-lg text-xs font-semibold flex items-center space-x-1 transition-colors"
                    >
                      <ArrowLeftRight className="h-3.5 w-3.5" />
                      <span>Transact</span>
                    </button>

                    <div className="flex space-x-1">
                      <button
                        onClick={() => handleEdit(item)}
                        className="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
                        title="Edit Item"
                      >
                        <Edit2 className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="p-1.5 rounded-lg text-rose-500 hover:text-rose-700 hover:bg-rose-50 dark:hover:bg-rose-950/40"
                        title="Delete Item"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="glass-card border border-slate-200 dark:border-slate-800 rounded-2xl overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 dark:bg-slate-900/60 text-slate-700 dark:text-slate-300 font-bold border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th className="p-3.5">Item Name</th>
                  <th className="p-3.5">Category</th>
                  <th className="p-3.5">Quantity</th>
                  <th className="p-3.5">Price</th>
                  <th className="p-3.5">Condition</th>
                  <th className="p-3.5">Status</th>
                  <th className="p-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/40">
                    <td className="p-3.5 font-bold text-slate-900 dark:text-slate-100">{item.item_name || item.title}</td>
                    <td className="p-3.5 text-slate-600 dark:text-slate-400">{item.category}</td>
                    <td className="p-3.5 font-semibold">{item.quantity} {item.unit}</td>
                    <td className="p-3.5 font-bold text-emerald-600 dark:text-emerald-400">{formatCurrency(item.price)}</td>
                    <td className="p-3.5 text-slate-600 dark:text-slate-400">{item.condition}</td>
                    <td className="p-3.5"><StatusBadge status={item.status} /></td>
                    <td className="p-3.5 text-right space-x-2">
                      <button onClick={() => handleTransact(item)} className="text-emerald-600 font-semibold hover:underline">Transact</button>
                      <button onClick={() => handleEdit(item)} className="text-slate-500 hover:text-slate-900 font-semibold">Edit</button>
                      <button onClick={() => handleDelete(item.id)} className="text-rose-500 hover:text-rose-700 font-semibold">Delete</button>
                    </td>
                  </tr>
                ))}
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

      {/* Modals */}
      <InventoryModal
        isOpen={isItemModalOpen}
        onClose={() => setIsItemModalOpen(false)}
        onRefresh={fetchInventory}
        initialData={selectedItem}
      />

      <TransactionModal
        isOpen={isTxModalOpen}
        onClose={() => setIsTxModalOpen(false)}
        onRefresh={fetchInventory}
        preselectedItem={txSelectedItem}
      />
    </DashboardLayout>
  );
};
