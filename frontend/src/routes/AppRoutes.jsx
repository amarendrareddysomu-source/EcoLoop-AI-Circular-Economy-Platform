import React, { lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ProtectedRoute } from '../components/ProtectedRoute';
import { useAuth } from '../context/AuthContext';

import { Login } from '../pages/Login';
import { Register } from '../pages/Register';
import { ForgotPassword } from '../pages/ForgotPassword';
import { VerifyEmail } from '../pages/VerifyEmail';
import { Dashboard } from '../pages/Dashboard';
import { InventoryPage } from '../pages/InventoryPage';
import { TransactionsPage } from '../pages/TransactionsPage';
import { AIPredictionsPage } from '../pages/AIPredictionsPage';
import { ImpactPassportPage } from '../pages/ImpactPassportPage';
import { PartnerFinderPage } from '../pages/PartnerFinderPage';
import { RepairGuidePage } from '../pages/RepairGuidePage';
import { RewardsStorePage } from '../pages/RewardsStorePage';
import { ReportsPage } from '../pages/ReportsPage';
import { AdminDashboard } from '../pages/AdminDashboard';
import { NGODashboard } from '../pages/NGODashboard';
import { RecyclingDashboard } from '../pages/RecyclingDashboard';

const PageLoader = () => (
  <div className="flex items-center justify-center min-h-[60vh]">
    <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-emerald-600"></div>
  </div>
);

export const AppRoutes = () => {
  const { user } = useAuth();

  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/verify-email" element={<VerifyEmail />} />

        {/* Protected App Routes */}
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/inventory" element={<ProtectedRoute><InventoryPage /></ProtectedRoute>} />
        <Route path="/transactions" element={<ProtectedRoute><TransactionsPage /></ProtectedRoute>} />
        <Route path="/ai-predictions" element={<ProtectedRoute><AIPredictionsPage /></ProtectedRoute>} />
        <Route path="/impact-passports" element={<ProtectedRoute><ImpactPassportPage /></ProtectedRoute>} />
        <Route path="/pickup-partners" element={<ProtectedRoute><PartnerFinderPage /></ProtectedRoute>} />
        <Route path="/repair-guide" element={<ProtectedRoute><RepairGuidePage /></ProtectedRoute>} />
        <Route path="/rewards-store" element={<ProtectedRoute><RewardsStorePage /></ProtectedRoute>} />
        <Route path="/reports" element={<ProtectedRoute><ReportsPage /></ProtectedRoute>} />

        {/* Role-Specific Portals */}
        <Route path="/admin-dashboard" element={<ProtectedRoute allowedRoles={['admin']}><AdminDashboard /></ProtectedRoute>} />
        <Route path="/ngo-dashboard" element={<ProtectedRoute allowedRoles={['ngo', 'admin']}><NGODashboard /></ProtectedRoute>} />
        <Route path="/recycling-dashboard" element={<ProtectedRoute allowedRoles={['recycling_center', 'admin']}><RecyclingDashboard /></ProtectedRoute>} />

        {/* Default Catch-all */}
        <Route path="*" element={<Navigate to={user ? "/dashboard" : "/login"} replace />} />
      </Routes>
    </Suspense>
  );
};

