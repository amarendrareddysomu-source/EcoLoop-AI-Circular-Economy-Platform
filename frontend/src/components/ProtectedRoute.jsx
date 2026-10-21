import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const ProtectedRoute = ({ children, allowedRoles }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-emerald-600"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && allowedRoles.length > 0) {
    const userRole = user.role ? user.role.toLowerCase() : '';
    const hasRole = allowedRoles.some((r) => r.toLowerCase() === userRole) || userRole === 'admin' || userRole === 'super_admin';

    if (!hasRole) {
      return <Navigate to="/dashboard" replace />;
    }
  }

  return children;
};
