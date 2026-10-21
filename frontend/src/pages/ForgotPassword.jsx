import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Leaf, Mail, CheckCircle2 } from 'lucide-react';

export const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-slate-950 text-slate-100">
      <div className="max-w-md w-full glass-card p-8 rounded-3xl shadow-2xl space-y-6 border border-slate-800">
        <div className="text-center space-y-2">
          <div className="h-12 w-12 rounded-2xl bg-emerald-600 flex items-center justify-center mx-auto shadow-lg shadow-emerald-600/30">
            <Leaf className="h-7 w-7 text-white" />
          </div>
          <h2 className="text-2xl font-bold font-heading gradient-text">Reset Password</h2>
          <p className="text-xs text-slate-400">Enter your email to receive recovery instructions</p>
        </div>

        {submitted ? (
          <div className="p-4 bg-emerald-950/60 border border-emerald-800 rounded-xl text-center space-y-2">
            <CheckCircle2 className="h-8 w-8 text-emerald-400 mx-auto" />
            <p className="text-sm font-semibold text-emerald-200">Password Reset Email Sent!</p>
            <p className="text-xs text-slate-400">Check your inbox for further instructions.</p>
            <Link to="/login" className="inline-block pt-2 text-xs font-bold text-emerald-400 hover:underline">
              Return to Login
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Email Address</label>
              <div className="relative">
                <Mail className="h-4 w-4 absolute left-3 top-3 text-slate-500" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="user@circulareconomy.org"
                  className="w-full pl-9 pr-3 py-2.5 rounded-xl border border-slate-700 bg-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 text-slate-100"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm rounded-xl shadow-lg shadow-emerald-600/30 transition-all"
            >
              Send Reset Link
            </button>
          </form>
        )}

        <div className="text-center text-xs text-slate-400">
          <Link to="/login" className="text-emerald-400 font-semibold hover:underline">Back to Login</Link>
        </div>
      </div>
    </div>
  );
};
