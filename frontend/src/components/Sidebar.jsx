import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  Boxes,
  ArrowLeftRight,
  BrainCircuit,
  BarChart3,
  ShieldCheck,
  Building2,
  Recycle,
  Wrench,
  Gift,
  Leaf,
  Award
} from 'lucide-react';

export const Sidebar = () => {
  const { user } = useAuth();
  const role = user?.role?.toLowerCase() || 'user';

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Inventory Catalog', path: '/inventory', icon: Boxes },
    { name: 'Transactions', path: '/transactions', icon: ArrowLeftRight },
    { name: 'AI Decision Engine', path: '/ai-predictions', icon: BrainCircuit },
    { name: 'Impact Passports', path: '/impact-passports', icon: Award },
    { name: 'NGO Pickup Partners', path: '/pickup-partners', icon: Building2 },
    { name: 'AI Repair & Upcycling', path: '/repair-guide', icon: Wrench },
    { name: 'Green Rewards Store', path: '/rewards-store', icon: Gift },
    { name: 'Reports & Analytics', path: '/reports', icon: BarChart3 },
  ];

  if (role === 'admin' || role === 'super_admin') {
    navItems.push({ name: 'Admin Portal', path: '/admin-dashboard', icon: ShieldCheck });
  }
  if (role === 'ngo' || role === 'admin' || role === 'super_admin') {
    navItems.push({ name: 'NGO Portal', path: '/ngo-dashboard', icon: Building2 });
  }
  if (role === 'recycling_center' || role === 'admin' || role === 'super_admin') {
    navItems.push({ name: 'Recycling Portal', path: '/recycling-dashboard', icon: Recycle });
  }

  return (
    <aside className="w-64 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col justify-between hidden md:flex min-h-[calc(100vh-4rem)]">
      <div className="p-4 space-y-6">
        <div className="flex items-center space-x-3 px-3 py-2 bg-emerald-50 dark:bg-emerald-950/40 rounded-xl border border-emerald-200 dark:border-emerald-800/50">
          <Leaf className="h-6 w-6 text-emerald-600 dark:text-emerald-400" />
          <div>
            <h2 className="text-sm font-bold text-emerald-950 dark:text-emerald-200 font-heading">EcoLoop Platform</h2>
            <p className="text-xs text-emerald-700 dark:text-emerald-400 capitalize">{role} Workspace</p>
          </div>
        </div>

        <nav className="space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/20'
                    : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-100'
                }`
              }
            >
              <item.icon className="h-5 w-5" />
              <span>{item.name}</span>
            </NavLink>
          ))}
        </nav>
      </div>

      <div className="p-4 border-t border-slate-200 dark:border-slate-800 text-xs text-slate-400 dark:text-slate-500 text-center">
        EcoLoop AI Circular Platform v2.0
      </div>
    </aside>
  );
};
