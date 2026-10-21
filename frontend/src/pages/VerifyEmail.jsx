import React from 'react';
import { Link } from 'react-router-dom';
import { CheckCircle, Leaf } from 'lucide-react';

export const VerifyEmail = () => {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950 text-slate-100">
      <div className="max-w-md w-full glass-card p-8 rounded-3xl shadow-2xl space-y-6 text-center border border-slate-800">
        <div className="h-12 w-12 rounded-2xl bg-emerald-600 flex items-center justify-center mx-auto shadow-lg shadow-emerald-600/30">
          <Leaf className="h-7 w-7 text-white" />
        </div>
        <CheckCircle className="h-12 w-12 text-emerald-400 mx-auto" />
        <h2 className="text-2xl font-bold font-heading gradient-text">Email Verified!</h2>
        <p className="text-xs text-slate-400">Your account email has been successfully verified. You can now access all features.</p>
        <Link
          to="/login"
          className="inline-block w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm rounded-xl shadow-lg shadow-emerald-600/30 transition-all"
        >
          Continue to Sign In
        </Link>
      </div>
    </div>
  );
};
