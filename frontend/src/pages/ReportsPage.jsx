import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { DashboardLayout } from '../layouts/DashboardLayout';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend
} from 'recharts';
import {
  BarChart3,
  Download,
  FileText,
  FileSpreadsheet,
  Calendar,
  Sparkles,
  TrendingUp,
  RefreshCw,
  PieChart as PieIcon,
  Layers,
  Filter
} from 'lucide-react';

export const ReportsPage = () => {
  const [txTrends, setTxTrends] = useState(null);
  const [catDist, setCatDist] = useState(null);
  const [recycleDist, setRecycleDist] = useState(null);
  const [susTrends, setSusTrends] = useState(null);
  const [loading, setLoading] = useState(true);

  const [genForm, setGenForm] = useState({
    report_type: 'sustainability',
    period: 'monthly'
  });
  const [genLoading, setGenLoading] = useState(false);
  const [genSuccess, setGenSuccess] = useState('');

  useEffect(() => {
    fetchCharts();
  }, [genForm.period, genForm.report_type]);

  const fetchCharts = async () => {
    setLoading(true);
    try {
      const days = genForm.period === 'daily' ? 7 : (genForm.period === 'weekly' ? 30 : 180);
      const months = genForm.period === 'daily' ? 1 : (genForm.period === 'weekly' ? 3 : 6);

      const [r1, r2, r3, r4] = await Promise.all([
        api.get(`/analytics/charts/transaction-trends?days=${days}`),
        api.get('/analytics/charts/category-distribution'),
        api.get('/analytics/charts/recycling-distribution'),
        api.get(`/analytics/charts/sustainability-trends?months=${months}`)
      ]);

      setTxTrends(r1.data);
      setCatDist(r2.data);
      setRecycleDist(r3.data);
      setSusTrends(r4.data);
    } catch (err) {
      // Ignore
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async (e) => {
    e.preventDefault();
    setGenLoading(true);
    setGenSuccess('');
    try {
      const res = await api.post('/reports/generate', genForm);
      setGenSuccess(`Successfully generated and saved "${res.data.title}" report!`);
    } catch (err) {
      alert('Failed to generate report');
    } finally {
      setGenLoading(false);
    }
  };

  const handleExportCSV = async () => {
    try {
      const res = await api.get(`/reports/export/csv?report_type=${genForm.report_type}&period=${genForm.period}`, {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${genForm.report_type}_${genForm.period}_report.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert('Failed to download CSV report');
    }
  };

  const handleExportPDF = async () => {
    try {
      const res = await api.get(`/reports/export/pdf?report_type=${genForm.report_type}&period=${genForm.period}`, {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${genForm.report_type}_${genForm.period}_report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert('Failed to download PDF report');
    }
  };

  // Modern Color Palette
  const COLORS = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#14b8a6', '#6366f1', '#ec4899'];

  const formatLineData = () => {
    if (!txTrends) return [];
    return txTrends.labels.map((label, idx) => ({
      name: label,
      Volume: txTrends.datasets[0]?.data[idx] || 0,
      'Amount ($)': txTrends.datasets[1]?.data[idx] || 0
    }));
  };

  const formatBarData = () => {
    if (!catDist) return [];
    return catDist.labels.map((label, idx) => ({
      name: label,
      Items: catDist.datasets[0]?.data[idx] || 0
    }));
  };

  const formatPieData = () => {
    if (!recycleDist) return [];
    const raw = recycleDist.labels.map((label, idx) => ({
      name: label,
      value: recycleDist.datasets[0]?.data[idx] || 0
    }));
    // Filter out zero-count values to prevent overlapping labels!
    const nonZero = raw.filter((item) => item.value > 0);
    return nonZero.length > 0 ? nonZero : [{ name: 'No Item Activity', value: 1 }];
  };

  const formatSusData = () => {
    if (!susTrends) return [];
    return susTrends.labels.map((label, idx) => ({
      name: label,
      'CO2 Saved (kg)': susTrends.datasets[0]?.data[idx] || 0,
      'Waste Reduced (kg)': susTrends.datasets[1]?.data[idx] || 0
    }));
  };

  const scope = genForm.report_type;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
          <div>
            <h1 className="text-2xl font-bold font-heading text-slate-900 dark:text-slate-100 flex items-center space-x-2">
              <BarChart3 className="h-7 w-7 text-emerald-600 dark:text-emerald-400" />
              <span>Reports & Analytics Dashboard</span>
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Visual analytics charts, scope-filtered report generator, and CSV / PDF export engine
            </p>
          </div>

          <div className="flex space-x-3">
            <button
              onClick={handleExportCSV}
              className="px-3.5 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 rounded-xl font-bold text-xs flex items-center space-x-2 border border-slate-300 dark:border-slate-700 transition-all"
            >
              <FileSpreadsheet className="h-4 w-4 text-emerald-600" />
              <span>Export CSV</span>
            </button>
            <button
              onClick={handleExportPDF}
              className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs flex items-center space-x-2 shadow-md shadow-emerald-600/20 transition-all"
            >
              <FileText className="h-4 w-4" />
              <span>Export PDF</span>
            </button>
          </div>
        </div>

        {/* Report Generation Controls & Scope Selector */}
        <form onSubmit={handleGenerateReport} className="p-4 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex flex-col sm:flex-row items-center space-y-2 sm:space-y-0 sm:space-x-4 w-full md:w-auto">
            <div className="flex items-center space-x-2 w-full sm:w-auto">
              <span className="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center space-x-1">
                <Filter className="h-3.5 w-3.5 text-emerald-600" />
                <span>Report Scope:</span>
              </span>
              <select
                value={genForm.report_type}
                onChange={(e) => setGenForm({ ...genForm, report_type: e.target.value })}
                className="px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-emerald-500 capitalize"
              >
                <option value="sustainability">Sustainability (CO2 & Waste)</option>
                <option value="transactions">Transactions (Volume & Value)</option>
                <option value="inventory">Inventory (Categories Breakdown)</option>
                <option value="recycling">Recycling (Item Lifecycle)</option>
                <option value="all">All Analytics Scopes</option>
              </select>
            </div>

            <div className="flex items-center space-x-2 w-full sm:w-auto">
              <span className="text-xs font-bold text-slate-700 dark:text-slate-300 flex items-center space-x-1">
                <Calendar className="h-3.5 w-3.5 text-teal-600" />
                <span>Period:</span>
              </span>
              <select
                value={genForm.period}
                onChange={(e) => setGenForm({ ...genForm, period: e.target.value })}
                className="px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-emerald-500 capitalize"
              >
                <option value="daily">Daily (7 Days)</option>
                <option value="weekly">Weekly (30 Days)</option>
                <option value="monthly">Monthly (6 Months)</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={genLoading}
            className="px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white rounded-xl font-bold text-xs flex items-center space-x-2 shadow-md w-full md:w-auto justify-center"
          >
            <Sparkles className="h-4 w-4" />
            <span>{genLoading ? 'Generating...' : 'Generate & Save Report'}</span>
          </button>
        </form>

        {genSuccess && (
          <div className="p-3 bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 rounded-xl text-emerald-700 dark:text-emerald-300 text-xs font-semibold flex items-center space-x-2">
            <Sparkles className="h-4 w-4 shrink-0" />
            <span>{genSuccess}</span>
          </div>
        )}

        {/* Visual Charts Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-pulse">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-64 bg-slate-200 dark:bg-slate-800 rounded-2xl"></div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Chart 1: Transaction Trends Line Chart */}
            {(scope === 'all' || scope === 'transactions') && (
              <div className="p-5 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold font-heading text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                    <TrendingUp className="h-4 w-4 text-emerald-600" />
                    <span>Transaction Trends (Volume & Value)</span>
                  </h3>
                  <span className="text-[10px] font-bold px-2 py-0.5 bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 rounded-full capitalize">
                    {genForm.period}
                  </span>
                </div>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={formatLineData()}>
                      <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                      <XAxis dataKey="name" stroke="#888888" fontSize={11} />
                      <YAxis stroke="#888888" fontSize={11} allowDecimals={false} />
                      <Tooltip />
                      <Legend verticalAlign="bottom" height={36} iconType="circle" />
                      <Line type="monotone" dataKey="Volume" stroke="#10b981" strokeWidth={2.5} dot={{ r: 3 }} />
                      <Line type="monotone" dataKey="Amount ($)" stroke="#3b82f6" strokeWidth={2.5} dot={{ r: 3 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Chart 2: Item Categories Distribution Bar Chart */}
            {(scope === 'all' || scope === 'inventory') && (
              <div className="p-5 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold font-heading text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                    <BarChart3 className="h-4 w-4 text-indigo-600" />
                    <span>Item Categories Distribution (Bar Chart)</span>
                  </h3>
                  <span className="text-[10px] font-bold px-2 py-0.5 bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 rounded-full">
                    10 Material Classes
                  </span>
                </div>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={formatBarData()}>
                      <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                      <XAxis dataKey="name" stroke="#888888" fontSize={11} interval={0} angle={-15} textAnchor="end" height={40} />
                      <YAxis stroke="#888888" fontSize={11} allowDecimals={false} />
                      <Tooltip />
                      <Bar dataKey="Items" radius={[6, 6, 0, 0]}>
                        {formatBarData().map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Chart 3: Recycling Distribution Pie Chart */}
            {(scope === 'all' || scope === 'recycling') && (
              <div className="p-5 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold font-heading text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                    <PieIcon className="h-4 w-4 text-purple-600" />
                    <span>Recycling & Item Lifecycle Distribution (Pie Chart)</span>
                  </h3>
                  <span className="text-[10px] font-bold px-2 py-0.5 bg-purple-100 dark:bg-purple-950 text-purple-700 dark:text-purple-300 rounded-full">
                    Item Statuses
                  </span>
                </div>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={formatPieData()}
                        cx="50%"
                        cy="45%"
                        innerRadius={45}
                        outerRadius={75}
                        paddingAngle={3}
                        dataKey="value"
                      >
                        {formatPieData().map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(val, name) => [val, name]} />
                      <Legend verticalAlign="bottom" height={36} iconType="circle" />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Chart 4: Sustainability Impact Trends */}
            {(scope === 'all' || scope === 'sustainability') && (
              <div className="p-5 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold font-heading text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                    <TrendingUp className="h-4 w-4 text-teal-600" />
                    <span>Sustainability Impact Trends (CO2 & Waste)</span>
                  </h3>
                  <span className="text-[10px] font-bold px-2 py-0.5 bg-teal-100 dark:bg-teal-950 text-teal-700 dark:text-teal-300 rounded-full capitalize">
                    {genForm.period}
                  </span>
                </div>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={formatSusData()}>
                      <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                      <XAxis dataKey="name" stroke="#888888" fontSize={11} />
                      <YAxis stroke="#888888" fontSize={11} />
                      <Tooltip />
                      <Legend verticalAlign="bottom" height={36} iconType="circle" />
                      <Line type="monotone" dataKey="CO2 Saved (kg)" stroke="#10b981" strokeWidth={2.5} dot={{ r: 3 }} />
                      <Line type="monotone" dataKey="Waste Reduced (kg)" stroke="#f59e0b" strokeWidth={2.5} dot={{ r: 3 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};
