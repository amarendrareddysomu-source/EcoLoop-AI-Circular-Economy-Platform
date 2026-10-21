import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { ImpactPassportModal, CategoryItemPhoto, CATEGORY_SVG_IMAGES } from '../components/ImpactPassportModal';
import {
  Award,
  ArrowLeft,
  Sparkles,
  QrCode,
  Printer,
  ShieldCheck,
  CheckCircle2,
  Leaf,
  DollarSign,
  Layers,
  FileText,
  Upload
} from 'lucide-react';

const SCRAP_RATES_PER_KG_INR = {
  Battery: 42.0,
  Metal: 50.0,
  Plastic: 12.5,
  Shoes: 10.0,
  Clothes: 8.3,
  Glass: 6.6,
  Cardboard: 6.6,
  Paper: 4.15,
  Biological: 0.0,
  Trash: 0.0
};

export const ImpactPassportPage = () => {
  const navigate = useNavigate();
  const [modalOpen, setModalOpen] = useState(false);

  const categories = ["Battery", "Biological", "Cardboard", "Clothes", "Glass", "Metal", "Paper", "Plastic", "Shoes", "Trash"];

  const [form, setForm] = useState({
    title: 'Cotton Denim Jacket',
    category: 'Clothes',
    condition: 'Good',
    weight_kg: 0.8,
    original_price: 1200,
    customImage: null
  });

  const [generatedPassport, setGeneratedPassport] = useState({
    item_name: 'Cotton Denim Jacket',
    predicted_category: 'Clothes',
    condition: 'Good',
    weight_kg: 0.8,
    co2_saved_kg: 3.4,
    waste_diverted_kg: 0.8,
    resale_value_display: '₹744 ($8.96)',
    recycling_value_inr: '₹7 ($0.08) [₹8.3/kg]',
    image_url: CATEGORY_SVG_IMAGES['Clothes'],
    confidence: 0.94
  });

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setForm(prev => ({ ...prev, customImage: reader.result }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleGenerate = (e) => {
    e.preventDefault();
    const co2 = (form.weight_kg * 4.2).toFixed(1);
    const waste = form.weight_kg;
    const orig = form.original_price || 500;
    const condMult = form.condition === 'Excellent' ? 0.75 : form.condition === 'Good' ? 0.62 : 0.45;
    const resaleInr = Math.round(orig * condMult);
    const resaleUsd = (resaleInr / 83.0).toFixed(2);

    const perKgScrapRate = SCRAP_RATES_PER_KG_INR[form.category] !== undefined ? SCRAP_RATES_PER_KG_INR[form.category] : 8.3;
    const totalScrapInr = Math.round(form.weight_kg * perKgScrapRate);
    const totalScrapUsd = (totalScrapInr / 83.0).toFixed(2);
    const scrapDisplay = totalScrapInr > 0 ? `₹${totalScrapInr} ($${totalScrapUsd}) [₹${perKgScrapRate}/kg]` : 'Not Applicable';

    const photoUrl = form.customImage || CATEGORY_SVG_IMAGES[form.category] || CATEGORY_SVG_IMAGES['Clothes'];

    setGeneratedPassport({
      item_name: form.title,
      predicted_category: form.category,
      condition: form.condition,
      weight_kg: form.weight_kg,
      co2_saved_kg: parseFloat(co2),
      waste_diverted_kg: parseFloat(waste),
      resale_value_display: `₹${resaleInr.toLocaleString()} ($${resaleUsd})`,
      recycling_value_inr: scrapDisplay,
      image_url: photoUrl,
      confidence: 0.95
    });
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-teal-700 via-emerald-700 to-indigo-800 text-white shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-3">
              <Award className="h-8 w-8 text-amber-300 shrink-0" />
              <h1 className="text-2xl md:text-3xl font-extrabold font-heading">Digital AI Circular Impact Passport</h1>
            </div>
            <p className="text-xs md:text-sm text-emerald-100/90">
              Generate, verify, and print official material passports with real item photos & environmental metrics.
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

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Passport Form (Left Side) */}
          <div className="lg:col-span-5 p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
            <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <FileText className="h-5 w-5 text-emerald-600" />
              <span>Create Item Passport</span>
            </h3>

            <form onSubmit={handleGenerate} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Item Title / Name</label>
                <input
                  type="text"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:ring-2 focus:ring-emerald-500"
                  required
                />
              </div>

              {/* Upload Item Image File Input */}
              <div>
                <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Upload Item Photo (Optional)</label>
                <div className="flex items-center space-x-3">
                  <label className="px-3 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-bold cursor-pointer text-slate-700 dark:text-slate-200 flex items-center space-x-2 transition-all">
                    <Upload className="h-4 w-4 text-emerald-600" />
                    <span>Choose Custom Image</span>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                    />
                  </label>
                  {form.customImage && (
                    <span className="text-[10px] text-emerald-600 font-bold">Custom Photo Attached</span>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Category</label>
                  <select
                    value={form.category}
                    onChange={(e) => setForm({ ...form, category: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:ring-2 focus:ring-emerald-500"
                  >
                    {categories.map((cat) => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Condition</label>
                  <select
                    value={form.condition}
                    onChange={(e) => setForm({ ...form, condition: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="Excellent">Excellent</option>
                    <option value="Good">Good</option>
                    <option value="Fair">Fair</option>
                    <option value="Poor">Poor</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Weight (kg)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0.1"
                    value={form.weight_kg}
                    onChange={(e) => setForm({ ...form, weight_kg: parseFloat(e.target.value) || 0.1 })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:ring-2 focus:ring-emerald-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Original Price (₹)</label>
                  <input
                    type="number"
                    step="10"
                    min="0"
                    value={form.original_price}
                    onChange={(e) => setForm({ ...form, original_price: parseFloat(e.target.value) || 0 })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs shadow-md transition-all flex items-center justify-center space-x-2"
              >
                <Sparkles className="h-4 w-4 text-amber-300" />
                <span>Generate Digital Impact Passport</span>
              </button>
            </form>
          </div>

          {/* Passport Live Card Display (Right Side) */}
          <div className="lg:col-span-7 space-y-4">
            <div className="p-6 rounded-3xl bg-gradient-to-br from-slate-900 via-indigo-950 to-emerald-950 text-white shadow-xl space-y-5 border border-slate-700">
              <div className="flex items-center justify-between border-b border-slate-700 pb-3">
                <span className="px-3 py-1 bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 rounded-full text-[10px] font-extrabold uppercase tracking-wider">
                  Verified Digital Passport Card
                </span>
                <span className="text-[10px] font-mono text-slate-400">
                  TOKEN-{Math.random().toString(36).substring(2, 8).toUpperCase()}-2026
                </span>
              </div>

              <div className="flex items-center space-x-4">
                <CategoryItemPhoto
                  category={generatedPassport.predicted_category}
                  imageUrl={generatedPassport.image_url}
                  className="w-20 h-20"
                />
                <div className="space-y-1">
                  <h2 className="text-2xl font-extrabold font-heading text-white">{generatedPassport.item_name}</h2>
                  <p className="text-xs text-emerald-300 font-semibold">
                    Category: <strong>{generatedPassport.predicted_category}</strong> • Condition: <strong>{generatedPassport.condition}</strong> • Weight: {generatedPassport.weight_kg} kg
                  </p>
                </div>
              </div>

              {/* Environmental Metrics Grid */}
              <div className="grid grid-cols-3 gap-3 text-center">
                <div className="p-3 bg-white/10 rounded-2xl border border-white/10">
                  <Leaf className="h-5 w-5 text-emerald-400 mx-auto mb-1" />
                  <span className="text-[10px] text-emerald-200 font-bold uppercase block">CO2 Saved</span>
                  <span className="text-base font-extrabold text-emerald-300">{generatedPassport.co2_saved_kg} kg</span>
                </div>
                <div className="p-3 bg-white/10 rounded-2xl border border-white/10">
                  <Award className="h-5 w-5 text-teal-400 mx-auto mb-1" />
                  <span className="text-[10px] text-teal-200 font-bold uppercase block">Waste Diverted</span>
                  <span className="text-base font-extrabold text-teal-300">{generatedPassport.waste_diverted_kg} kg</span>
                </div>
                <div className="p-3 bg-white/10 rounded-2xl border border-white/10">
                  <Sparkles className="h-5 w-5 text-amber-400 mx-auto mb-1" />
                  <span className="text-[10px] text-amber-200 font-bold uppercase block">Tree Equivalent</span>
                  <span className="text-base font-extrabold text-amber-300">{(generatedPassport.co2_saved_kg / 20.0).toFixed(2)} Trees</span>
                </div>
              </div>

              {/* Valuations & QR Trigger */}
              <div className="pt-2 flex items-center justify-between border-t border-slate-700">
                <div>
                  <span className="text-[10px] text-slate-300 block uppercase font-bold">Estimated Market Resale</span>
                  <span className="text-xl font-extrabold text-emerald-400">{generatedPassport.resale_value_display}</span>
                </div>

                <button
                  onClick={() => setModalOpen(true)}
                  className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl text-xs font-extrabold shadow-md transition-all flex items-center space-x-2"
                >
                  <QrCode className="h-4 w-4" />
                  <span>Open Full Passport Modal</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <ImpactPassportModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        itemData={generatedPassport}
      />
    </DashboardLayout>
  );
};
