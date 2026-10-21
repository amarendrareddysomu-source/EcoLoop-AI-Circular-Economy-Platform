import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { DashboardLayout } from '../layouts/DashboardLayout';
import api from '../api/axios';
import {
  Gift,
  Award,
  ArrowLeft,
  Sparkles,
  CheckCircle2,
  Leaf,
  ShoppingBag,
  TrendingUp,
  Zap,
  Tag,
  ShieldCheck,
  Copy,
  Check
} from 'lucide-react';

const REWARDS_CATALOG = [
  {
    id: 1,
    title: "₹100 Off Green Metro & EV Ride Voucher",
    category: "Eco Transport",
    pointsCost: 150,
    co2Equivalent: "1.5 kg CO2 Saved",
    provider: "Metro Express & Rapido EV",
    code: "GREEN-METRO-100"
  },
  {
    id: 2,
    title: "Free Upcycled Cotton Tote Bag",
    category: "Sustainable Goods",
    pointsCost: 250,
    co2Equivalent: "2.5 kg CO2 Saved",
    provider: "Goonj Eco Store",
    code: "FREE-TOTE-BAG-2026"
  },
  {
    id: 3,
    title: "20% Discount on Solar Power Bank",
    category: "Clean Tech",
    pointsCost: 350,
    co2Equivalent: "3.5 kg CO2 Saved",
    provider: "GreenEnergy Accessories",
    code: "SOLAR-POWER-20"
  },
  {
    id: 4,
    title: "Free Organic Compost Pack (5kg)",
    category: "Urban Farming",
    pointsCost: 200,
    co2Equivalent: "2.0 kg CO2 Saved",
    provider: "Andhra Urban Farmers Guild",
    code: "ORGANIC-COMPOST-5KG"
  }
];

const LEADERBOARD = [
  { rank: 1, name: "Visakhapatnam Eco Club", city: "Visakhapatnam", recycledKg: 420, points: 4200 },
  { rank: 2, name: "Bangalore Circular Youth", city: "Bangalore", recycledKg: 380, points: 3800 },
  { rank: 3, name: "Nellore Recycling Army", city: "Nellore", recycledKg: 310, points: 3100 },
  { rank: 4, name: "Kakinada Green Earth NGO", city: "Kakinada", recycledKg: 290, points: 2900 },
  { rank: 5, name: "Vijayawada Clean Action", city: "Vijayawada", recycledKg: 240, points: 2400 }
];

export const RewardsStorePage = () => {
  const navigate = useNavigate();

  const [walletPoints, setWalletPoints] = useState(1000);
  const [claimedVouchers, setClaimedVouchers] = useState([]);
  const [lastRedeemed, setLastRedeemed] = useState(null);
  const [copiedCode, setCopiedCode] = useState('');
  const [recycledCount, setRecycledCount] = useState(10);

  useEffect(() => {
    const fetchLiveCount = async () => {
      try {
        const res = await api.get('/items/');
        if (res.data && Array.isArray(res.data)) {
          setRecycledCount(res.data.length || 10);
        }
      } catch (err) {
        // use live default count
      }
    };
    fetchLiveCount();
  }, []);

  const handleRedeem = (item) => {
    if (walletPoints < item.pointsCost) {
      alert("Insufficient Eco-Points in your Green Wallet!");
      return;
    }
    setWalletPoints(prev => prev - item.pointsCost);
    setClaimedVouchers(prev => [item, ...prev]);
    setLastRedeemed(item);
  };

  const handleCopyCode = (code) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(code);
    setTimeout(() => setCopiedCode(''), 3000);
  };

  const co2DivertedKg = (walletPoints * 0.025).toFixed(1);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-emerald-600 via-teal-600 to-indigo-800 text-white shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-3">
              <Gift className="h-8 w-8 text-amber-300 shrink-0" />
              <h1 className="text-2xl md:text-3xl font-extrabold font-heading">Carbon Credits & Green Rewards Store</h1>
            </div>
            <p className="text-xs md:text-sm text-emerald-100/90">
              Earn Eco-Points for every item repaired, reused, or recycled, and redeem vouchers for green rewards!
            </p>
          </div>

          <button
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 bg-white/10 hover:bg-white/20 backdrop-blur-md rounded-2xl border border-white/20 text-xs font-bold flex items-center space-x-2 transition-all text-white shadow-sm shrink-0"
          >
            <ArrowLeft className="h-4 w-4 text-emerald-300" />
            <span>Back to Dashboard</span>
          </button>
        </div>

        {/* Success Alert Banner with ONE-CLICK COPY BUTTON */}
        {lastRedeemed && (
          <div className="p-5 bg-gradient-to-r from-emerald-600 to-teal-700 text-white rounded-3xl shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 animate-fadeIn border border-emerald-400/40">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-white text-emerald-600 rounded-2xl shrink-0 shadow-md">
                <CheckCircle2 className="h-6 w-6" />
              </div>
              <div className="space-y-0.5">
                <span className="text-[10px] font-extrabold uppercase text-amber-300 tracking-wider">
                  Voucher Claimed Successfully!
                </span>
                <h4 className="text-base font-extrabold">{lastRedeemed.title}</h4>
                <p className="text-xs text-emerald-100">Provider: {lastRedeemed.provider}</p>
              </div>
            </div>

            <div className="flex items-center space-x-3 bg-black/20 p-2.5 rounded-2xl border border-white/20 shrink-0 w-full sm:w-auto justify-between sm:justify-start">
              <div className="space-y-0.5">
                <span className="text-[9px] uppercase text-emerald-200 block font-bold">Voucher Code</span>
                <span className="text-sm font-mono font-extrabold text-amber-300">{lastRedeemed.code}</span>
              </div>
              <button
                onClick={() => handleCopyCode(lastRedeemed.code)}
                className="px-3.5 py-2 bg-white text-emerald-800 hover:bg-emerald-50 rounded-xl text-xs font-extrabold flex items-center space-x-1.5 shadow-md transition-all shrink-0"
              >
                {copiedCode === lastRedeemed.code ? (
                  <>
                    <Check className="h-4 w-4 text-emerald-600" />
                    <span>Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy className="h-4 w-4 text-emerald-600" />
                    <span>Copy Code</span>
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Green Wallet Balance Banner */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Green Wallet Balance Card */}
          <div className="p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-indigo-950 text-white shadow-md border border-slate-800 space-y-3 flex flex-col justify-between">
            <div className="space-y-1">
              <span className="text-[10px] font-extrabold text-emerald-400 uppercase tracking-wider block">Your Green Wallet Balance</span>
              <div className="flex items-center space-x-2 pt-1">
                <Sparkles className="h-8 w-8 text-amber-400" />
                <span className="text-3xl font-extrabold text-emerald-300">{walletPoints} Eco-Points</span>
              </div>
            </div>
            <p className="text-[10px] text-slate-400">Equivalent to {co2DivertedKg} kg CO2 Diverted from Landfills</p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 space-y-2">
            <span className="text-[10px] font-extrabold text-slate-400 uppercase block">Total Items Processed</span>
            <span className="text-3xl font-extrabold text-slate-900 dark:text-slate-100">{recycledCount} Items</span>
            <p className="text-[10px] text-emerald-600 font-bold">Live Inventory Stream in AP & India</p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 space-y-2">
            <span className="text-[10px] font-extrabold text-slate-400 uppercase block">Active Vouchers Claimed</span>
            <span className="text-3xl font-extrabold text-teal-600 dark:text-teal-400">{claimedVouchers.length} Claimed</span>
            <p className="text-[10px] text-slate-500">Ready to copy & redeem at partner hubs</p>
          </div>
        </div>

        {/* My Claimed Vouchers List (if any) */}
        {claimedVouchers.length > 0 && (
          <div className="p-6 rounded-3xl glass-card border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
            <h3 className="text-base font-extrabold text-slate-900 dark:text-slate-100 flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <ShieldCheck className="h-5 w-5 text-emerald-600" />
              <span>Your Claimed Vouchers & Discount Codes ({claimedVouchers.length})</span>
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {claimedVouchers.map((v, i) => (
                <div key={i} className="p-4 bg-emerald-50/80 dark:bg-emerald-950/40 rounded-2xl border border-emerald-200 dark:border-emerald-800 flex items-center justify-between">
                  <div className="space-y-1">
                    <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100">{v.title}</h4>
                    <p className="text-[10px] text-slate-500">Code: <strong className="font-mono text-emerald-700 dark:text-emerald-300">{v.code}</strong></p>
                  </div>
                  <button
                    onClick={() => handleCopyCode(v.code)}
                    className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-extrabold flex items-center space-x-1 shadow-sm transition-all shrink-0"
                  >
                    {copiedCode === v.code ? (
                      <>
                        <Check className="h-3.5 w-3.5" />
                        <span>Copied</span>
                      </>
                    ) : (
                      <>
                        <Copy className="h-3.5 w-3.5" />
                        <span>Copy Code</span>
                      </>
                    )}
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Rewards Catalog & Leaderboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Vouchers Catalog (Left Side) */}
          <div className="lg:col-span-8 space-y-4">
            <h3 className="text-lg font-extrabold text-slate-900 dark:text-slate-100 flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <ShoppingBag className="h-5 w-5 text-emerald-600" />
              <span>Available Rewards & Vouchers</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {REWARDS_CATALOG.map((item) => (
                <div key={item.id} className="p-5 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-3 shadow-sm hover:shadow-md transition-all flex flex-col justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="px-2.5 py-1 bg-emerald-100 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200 rounded-full text-[10px] font-bold">
                        {item.category}
                      </span>
                      <span className="text-xs font-mono font-extrabold text-amber-500">
                        {item.pointsCost} Points
                      </span>
                    </div>

                    <h4 className="text-sm font-extrabold text-slate-900 dark:text-slate-100 leading-snug">{item.title}</h4>
                    <p className="text-xs text-slate-500">Partner: <strong>{item.provider}</strong></p>
                    <p className="text-[10px] text-emerald-600 font-bold">{item.co2Equivalent}</p>
                  </div>

                  <button
                    onClick={() => handleRedeem(item)}
                    disabled={walletPoints < item.pointsCost}
                    className={`w-full py-2.5 rounded-xl font-bold text-xs shadow-sm transition-all flex items-center justify-center space-x-2 ${
                      walletPoints >= item.pointsCost
                        ? 'bg-emerald-600 hover:bg-emerald-700 text-white'
                        : 'bg-slate-200 dark:bg-slate-800 text-slate-400 cursor-not-allowed'
                    }`}
                  >
                    <Tag className="h-4 w-4" />
                    <span>{walletPoints >= item.pointsCost ? `Redeem for ${item.pointsCost} Points` : 'Insufficient Points'}</span>
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Leaderboard (Right Side) */}
          <div className="lg:col-span-4 space-y-4">
            <h3 className="text-lg font-extrabold text-slate-900 dark:text-slate-100 flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <TrendingUp className="h-5 w-5 text-amber-500" />
              <span>AP & National Eco Leaderboard</span>
            </h3>

            <div className="p-5 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-3 shadow-sm">
              {LEADERBOARD.map((user) => (
                <div key={user.rank} className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700">
                  <div className="flex items-center space-x-3">
                    <span className={`w-6 h-6 rounded-full flex items-center justify-center font-extrabold text-xs text-white ${
                      user.rank === 1 ? 'bg-amber-500' : user.rank === 2 ? 'bg-slate-400' : user.rank === 3 ? 'bg-amber-700' : 'bg-slate-700'
                    }`}>
                      {user.rank}
                    </span>
                    <div>
                      <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100">{user.name}</h4>
                      <p className="text-[10px] text-slate-500">{user.city} • {user.recycledKg} kg Recycled</p>
                    </div>
                  </div>

                  <span className="text-xs font-extrabold text-emerald-600 dark:text-emerald-400">
                    {user.points} pts
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};
