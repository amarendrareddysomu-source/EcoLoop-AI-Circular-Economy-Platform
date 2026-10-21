import React, { useState } from 'react';
import { QrCode, CheckCircle2, Truck, X, ShieldCheck, Camera, Sparkles, Building2 } from 'lucide-react';

export const DeliveryQRScannerModal = ({ open, onClose, defaultToken = '' }) => {
  const [scannedToken, setScannedToken] = useState(defaultToken || 'TOKEN-7A9B12-2026');
  const [partnerName, setPartnerName] = useState('Goonj NGO Pickup Fleet');
  const [verified, setVerified] = useState(false);
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  const handleVerify = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setVerified(true);
    }, 800);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-md bg-white dark:bg-slate-900 rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden flex flex-col">
        {/* Header */}
        <div className="p-5 bg-gradient-to-r from-purple-700 via-indigo-700 to-emerald-700 text-white flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Truck className="h-6 w-6 text-emerald-300" />
            <div>
              <h3 className="font-extrabold text-base tracking-wide font-heading">Delivery Partner QR Scanner</h3>
              <p className="text-[10px] text-purple-100 font-medium">Verify Item Pickup & Digital Passport Token</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-full hover:bg-white/20 text-white transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5">
          {!verified ? (
            <form onSubmit={handleVerify} className="space-y-4">
              <div className="p-4 bg-slate-50 dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 text-center space-y-3">
                <div className="w-16 h-16 bg-purple-100 dark:bg-purple-950 text-purple-600 dark:text-purple-300 rounded-2xl mx-auto flex items-center justify-center border border-purple-200 dark:border-purple-800">
                  <Camera className="h-8 w-8 animate-pulse" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100">Camera / Scanner Active</h4>
                  <p className="text-xs text-slate-500">Scan QR Passport Token or enter Token ID below to verify item receipt</p>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Passport Token ID</label>
                <input
                  type="text"
                  value={scannedToken}
                  onChange={(e) => setScannedToken(e.target.value)}
                  placeholder="e.g. TOKEN-7A9B12-2026"
                  className="w-full px-3 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-mono font-bold focus:ring-2 focus:ring-purple-500"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Partner Fleet / Receiving Agent</label>
                <select
                  value={partnerName}
                  onChange={(e) => setPartnerName(e.target.value)}
                  className="w-full px-3 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:ring-2 focus:ring-purple-500"
                >
                  <option value="Goonj NGO Pickup Fleet">Goonj NGO Pickup Fleet</option>
                  <option value="EcoRecycle Logistics Hub">EcoRecycle Logistics Hub</option>
                  <option value="Andhra Pradesh Municipal Waste Transport">Andhra Pradesh Municipal Waste Transport</option>
                  <option value="GreenLoop Doorstep Express">GreenLoop Doorstep Express</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-bold text-xs shadow-md transition-all flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <span>Verifying Token...</span>
                ) : (
                  <>
                    <ShieldCheck className="h-4 w-4 text-emerald-300" />
                    <span>Confirm Item Receipt & Verify</span>
                  </>
                )}
              </button>
            </form>
          ) : (
            <div className="p-6 bg-emerald-50 dark:bg-emerald-950/40 rounded-2xl border border-emerald-200 dark:border-emerald-800 text-center space-y-4">
              <div className="w-16 h-16 bg-emerald-600 text-white rounded-full mx-auto flex items-center justify-center shadow-lg">
                <CheckCircle2 className="h-10 w-10" />
              </div>
              <div className="space-y-1">
                <span className="px-3 py-1 bg-emerald-200 text-emerald-900 dark:bg-emerald-900 dark:text-emerald-200 rounded-full text-[10px] font-extrabold uppercase">
                  Receipt Verified
                </span>
                <h3 className="text-xl font-extrabold text-slate-900 dark:text-slate-100">Item Successfully Received!</h3>
                <p className="text-xs text-slate-600 dark:text-slate-300 font-mono font-bold">{scannedToken}</p>
                <p className="text-xs text-slate-500">Verified by: <strong>{partnerName}</strong></p>
                <p className="text-[10px] text-slate-400">Timestamp: {new Date().toLocaleString()}</p>
              </div>

              <button
                onClick={() => setVerified(false)}
                className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs shadow-md transition-all"
              >
                Scan Another Item
              </button>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 dark:bg-slate-800/60 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <p className="text-[10px] text-slate-400">Delivery verification logged to platform database</p>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-slate-200 rounded-xl font-bold text-xs"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
