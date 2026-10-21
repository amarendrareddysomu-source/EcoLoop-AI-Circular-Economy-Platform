import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { StatusBadge } from '../components/StatusBadge';
import { formatDate } from '../utils/formatters';
import {
  ShieldCheck,
  Users,
  Boxes,
  ArrowLeftRight,
  UserCheck,
  UserX,
  Search,
  CheckCircle,
  AlertCircle
} from 'lucide-react';

export const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('');

  useEffect(() => {
    fetchUsers();
  }, [search, roleFilter]);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      if (roleFilter) params.append('role', roleFilter);

      const res = await api.get(`/users/?${params.toString()}`);
      setUsers(res.data || []);
    } catch (err) {
      // Fallback: search/filter local or empty
    } finally {
      setLoading(false);
    }
  };

  const handleToggleActive = async (userId, currentStatus) => {
    try {
      await api.put(`/users/${userId}`, { is_active: !currentStatus });
      fetchUsers();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to update user status');
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white shadow-xl flex items-center justify-between border border-slate-800">
          <div>
            <h1 className="text-2xl font-bold font-heading flex items-center space-x-2">
              <ShieldCheck className="h-7 w-7 text-indigo-400" />
              <span>Admin Control Panel</span>
            </h1>
            <p className="text-xs text-slate-300 mt-1">
              User management, role assignment, platform-wide audit, and security controls.
            </p>
          </div>
        </div>

        {/* User Search & Filters */}
        <div className="p-4 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-lg">
          <div className="relative">
            <Search className="h-4 w-4 absolute left-3 top-3 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search user name or email..."
              className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
            />
          </div>

          <select
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
            className="px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs capitalize"
          >
            <option value="">All Roles</option>
            <option value="user">User</option>
            <option value="ngo">NGO</option>
            <option value="recycling_center">Recycling Manager</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        {/* User Management Table */}
        {loading ? (
          <div className="h-64 bg-slate-200 dark:bg-slate-800 rounded-2xl animate-pulse"></div>
        ) : (
          <div className="glass-card border border-slate-200 dark:border-slate-800 rounded-2xl overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-100 dark:bg-slate-900/60 text-slate-700 dark:text-slate-300 font-bold border-b border-slate-200 dark:border-slate-800">
                <tr>
                  <th className="p-3.5">ID</th>
                  <th className="p-3.5">Full Name</th>
                  <th className="p-3.5">Email</th>
                  <th className="p-3.5">Role</th>
                  <th className="p-3.5">Status</th>
                  <th className="p-3.5">Joined</th>
                  <th className="p-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/40">
                    <td className="p-3.5 font-bold">#{u.id}</td>
                    <td className="p-3.5 font-bold text-slate-900 dark:text-slate-100">{u.full_name}</td>
                    <td className="p-3.5 text-slate-500">{u.email}</td>
                    <td className="p-3.5 font-semibold text-emerald-600 dark:text-emerald-400 capitalize">{u.role}</td>
                    <td className="p-3.5">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold ${u.is_active ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300'}`}>
                        {u.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="p-3.5 text-slate-400">{formatDate(u.created_at)}</td>
                    <td className="p-3.5 text-right">
                      <button
                        onClick={() => handleToggleActive(u.id, u.is_active)}
                        className={`px-2.5 py-1 rounded-lg font-semibold text-xs transition-colors ${u.is_active ? 'bg-rose-50 text-rose-600 hover:bg-rose-100' : 'bg-emerald-50 text-emerald-600 hover:bg-emerald-100'}`}
                      >
                        {u.is_active ? 'Deactivate' : 'Activate'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};
