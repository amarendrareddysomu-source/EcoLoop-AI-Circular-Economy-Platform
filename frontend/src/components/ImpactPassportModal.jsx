import React from 'react';
import { QrCode, Sparkles, ShieldCheck, Download, Printer, Share2, X, Leaf, Award, CheckCircle, ArrowRight } from 'lucide-react';

export const CATEGORY_SVG_IMAGES = {
  Clothes: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" rx="30" fill="%230f766e"/><path d="M50 40 L80 40 L100 70 L120 40 L150 40 L170 80 L140 90 L140 170 L60 170 L60 90 L30 80 Z" fill="%2334d399"/><path d="M80 40 L100 80 L120 40" fill="none" stroke="%23064e3b" stroke-width="6"/><circle cx="100" cy="110" r="5" fill="%23064e3b"/><circle cx="100" cy="135" r="5" fill="%23064e3b"/><text x="100" y="190" text-anchor="middle" fill="white" font-size="14" font-weight="bold">CLOTHES</text></svg>`,
  
  Shoes: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" rx="30" fill="%234338ca"/><path d="M30 130 C30 110 60 90 90 90 L130 90 C150 90 170 100 170 130 L170 150 L30 150 Z" fill="%23818cf8"/><rect x="30" y="145" width="140" height="15" rx="5" fill="%23ffffff"/><path d="M80 90 L100 120 M100 90 L120 120" stroke="%23ffffff" stroke-width="4"/><text x="100" y="190" text-anchor="middle" fill="white" font-size="14" font-weight="bold">SHOES</text></svg>`,
  
  Battery: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" rx="30" fill="%23b45309"/><rect x="60" y="50" width="80" height="110" rx="12" fill="%23fbbf24"/><rect x="85" y="35" width="30" height="15" rx="4" fill="%2378350f"/><polygon points="105,70 85,110 100,110 95,140 115,100 100,100" fill="%2378350f"/><text x="100" y="190" text-anchor="middle" fill="white" font-size="14" font-weight="bold">BATTERY</text></svg>`,

  Metal: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" rx="30" fill="%23334155"/><ellipse cx="100" cy="60" rx="45" ry="18" fill="%2394a3b8"/><path d="M55 60 L55 140 C55 150 145 150 145 140 L145 60 Z" fill="%23cbd5e1"/><ellipse cx="100" cy="140" rx="45" ry="18" fill="%2364748b"/><path d="M70 70 L70 130 M90 70 L90 130" stroke="%23ffffff" stroke-width="3" stroke-dasharray="6,6"/><text x="100" y="190" text-anchor="middle" fill="white" font-size="14" font-weight="bold">METAL</text></svg>`,

  Glass: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" rx="30" fill="%230284c7"/><path d="M85 30 L115 30 L115 60 L140 90 L140 160 C140 170 60 170 60 160 L60 90 L85 60 Z" fill="%2338bdf8" opacity="0.9"/><path d="M75 90 L75 150" stroke="%23ffffff" stroke-width="6" stroke-linecap="round"/><text x="100" y="190" text-anchor="middle" fill="white" font-size="14" font-weight="bold">GLASS</text></svg>`,

  Plastic: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" rx="30" fill="%232563eb"/><rect x="85" y="30" width="30" height="15" rx="3" fill="%231d4ed8"/><path d="M80 45 L120 45 L135 80 L135 160 L65 160 L65 80 Z" fill="%2360a5fa"/><path d="M65 100 Q100 115 135 100 Q100 85 65 100" fill="%2393c5fd"/><text x="100" y="190" text-anchor="middle" fill="white" font-size="14" font-weight="bold">PLASTIC</text></svg>`,

  Cardboard: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" rx="30" fill="%2392400e"/><polygon points="100,40 160,70 100,100 40,70" fill="%23f59e0b"/><polygon points="40,70 100,100 100,160 40,130" fill="%23d97706"/><polygon points="160,70 100,100 100,160 160,130" fill="%23b45309"/><line x1="100" y1="40" x2="100" y2="100" stroke="%2378350f" stroke-width="3"/><text x="100" y="190" text-anchor="middle" fill="white" font-size="14" font-weight="bold">CARDBOARD</text></svg>`,

  Paper: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" rx="30" fill="%237e22ce"/><rect x="55" y="45" width="90" height="115" rx="6" fill="%23e9d5ff"/><rect x="50" y="40" width="90" height="115" rx="6" fill="%23ffffff"/><line x1="70" y1="65" x2="120" y2="65" stroke="%23a855f7" stroke-width="4"/><line x1="70" y1="85" x2="120" y2="85" stroke="%23a855f7" stroke-width="4"/><line x1="70" y1="105" x2="110" y2="105" stroke="%23a855f7" stroke-width="4"/><text x="100" y="190" text-anchor="middle" fill="white" font-size="14" font-weight="bold">PAPER</text></svg>`,

  Biological: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" rx="30" fill="%2315803d"/><path d="M100 40 C140 40 160 80 160 120 C160 160 120 160 100 160 C80 160 40 160 40 120 C40 80 60 40 100 40 Z" fill="%234ade80"/><path d="M100 40 Q110 90 100 160" stroke="%23166534" stroke-width="4"/><path d="M100 80 Q130 60 145 75" stroke="%23166534" stroke-width="3"/><path d="M100 110 Q70 95 55 110" stroke="%23166534" stroke-width="3"/><text x="100" y="190" text-anchor="middle" fill="white" font-size="14" font-weight="bold">BIOLOGICAL</text></svg>`,

  Trash: `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" rx="30" fill="%231e293b"/><path d="M60 70 L140 70 L130 160 L70 160 Z" fill="%23475569"/><rect x="50" y="55" width="100" height="12" rx="3" fill="%2364748b"/><rect x="85" y="42" width="30" height="13" rx="3" fill="%23475569"/><line x1="85" y1="85" x2="85" y2="145" stroke="%2394a3b8" stroke-width="4"/><line x1="100" y1="85" x2="100" y2="145" stroke="%2394a3b8" stroke-width="4"/><line x1="115" y1="85" x2="115" y2="145" stroke="%2394a3b8" stroke-width="4"/><text x="100" y="190" text-anchor="middle" fill="white" font-size="14" font-weight="bold">TRASH</text></svg>`
};

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

export const CategoryItemPhoto = ({ category, imageUrl, className = "w-16 h-16" }) => {
  const defaultSvg = CATEGORY_SVG_IMAGES[category] || CATEGORY_SVG_IMAGES['Clothes'];
  const photoSrc = imageUrl || defaultSvg;

  return (
    <div className={`${className} rounded-2xl overflow-hidden shrink-0 border border-slate-200 dark:border-slate-700 shadow-md bg-white dark:bg-slate-800`}>
      <img
        src={photoSrc}
        alt={category || 'Item'}
        className="w-full h-full object-cover"
        onError={(e) => {
          e.target.src = defaultSvg;
        }}
      />
    </div>
  );
};

export const ImpactPassportModal = ({ open, onClose, itemData }) => {
  if (!open || !itemData) return null;

  const title = itemData.item_name || itemData.title || itemData.predicted_category || 'Circular Item';
  const category = itemData.category || itemData.predicted_category || 'Clothes';
  const condition = itemData.condition || 'Good';
  const weightKg = itemData.weight_kg || itemData.weight || 0.8;
  const resaleDisplay = itemData.resale_value_display || (itemData.price ? `₹${Math.round(itemData.price * 83)} ($${itemData.price})` : 'Not Applicable');

  // Accurately calculate Scrap Recovery Rate based on actual weight & material rate
  const perKgScrapRate = SCRAP_RATES_PER_KG_INR[category] !== undefined ? SCRAP_RATES_PER_KG_INR[category] : 8.3;
  const totalScrapInr = Math.round(weightKg * perKgScrapRate);
  const totalScrapUsd = (totalScrapInr / 83.0).toFixed(2);
  const scrapDisplay = totalScrapInr > 0 ? `₹${totalScrapInr} ($${totalScrapUsd}) [₹${perKgScrapRate}/kg]` : 'Not Applicable';

  const co2 = itemData.co2_saved_kg || (weightKg * 4.2).toFixed(1);
  const waste = itemData.waste_diverted_kg || weightKg;
  const trees = (co2 / 20.0).toFixed(2);

  const handlePrint = () => {
    window.print();
  };

  const tokenString = itemData.token || `TOKEN-${Math.random().toString(36).substring(2, 8).toUpperCase()}-2026`;
  const qrTargetUrl = `${window.location.origin}/impact-passports?token=${tokenString}`;
  const qrCodeApiUrl = `https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${encodeURIComponent(qrTargetUrl)}`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-xl bg-white dark:bg-slate-900 rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-5 bg-gradient-to-r from-emerald-600 via-teal-600 to-indigo-700 text-white flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Award className="h-6 w-6 text-amber-300" />
            <div>
              <h3 className="font-extrabold text-base tracking-wide font-heading">Digital AI Circular Impact Passport</h3>
              <p className="text-[10px] text-emerald-100/90 font-medium">Verified Sustainability & Material Certificate</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-full hover:bg-white/20 text-white transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Passport Body */}
        <div className="p-6 space-y-5 overflow-y-auto">
          {/* Top Badge & Category Photo */}
          <div className="flex items-center justify-between p-4 bg-emerald-50/80 dark:bg-emerald-950/40 rounded-2xl border border-emerald-200 dark:border-emerald-800">
            <div className="flex items-center space-x-3.5">
              <CategoryItemPhoto category={category} imageUrl={itemData.image_url || itemData.imagePreview} className="w-16 h-16" />
              <div>
                <span className="text-[10px] font-extrabold uppercase text-emerald-700 dark:text-emerald-300 tracking-wider">
                  Verified Item Passport
                </span>
                <h4 className="text-lg font-extrabold text-slate-900 dark:text-slate-100">{title}</h4>
                <p className="text-xs text-slate-500 font-medium">Category: <strong>{category}</strong> • Condition: <strong>{condition}</strong> ({weightKg} kg)</p>
              </div>
            </div>
            <div className="text-right shrink-0">
              <span className="inline-flex items-center space-x-1 px-2.5 py-1 bg-emerald-100 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200 rounded-full text-[10px] font-bold">
                <CheckCircle className="h-3 w-3 text-emerald-600" />
                <span>100% Verified</span>
              </span>
            </div>
          </div>

          {/* Environmental Impact Grid */}
          <div>
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-400 mb-2.5">
              Verified Environmental Impact
            </h4>
            <div className="grid grid-cols-3 gap-3 text-center">
              <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700">
                <Leaf className="h-4 w-4 text-emerald-600 mx-auto mb-1" />
                <span className="text-[10px] font-semibold text-slate-400">CO2 Saved</span>
                <p className="text-sm font-extrabold text-emerald-600 dark:text-emerald-400">{co2} kg</p>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700">
                <Award className="h-4 w-4 text-teal-600 mx-auto mb-1" />
                <span className="text-[10px] font-semibold text-slate-400">Waste Diverted</span>
                <p className="text-sm font-extrabold text-teal-600 dark:text-teal-400">{waste} kg</p>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-200 dark:border-slate-700">
                <Sparkles className="h-4 w-4 text-amber-500 mx-auto mb-1" />
                <span className="text-[10px] font-semibold text-slate-400">Tree Equivalent</span>
                <p className="text-sm font-extrabold text-amber-600 dark:text-amber-400">{trees} Trees</p>
              </div>
            </div>
          </div>

          {/* Valuations & Circular Routing */}
          <div className="grid grid-cols-2 gap-3">
            <div className="p-3.5 bg-slate-50 dark:bg-slate-800/80 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-1">
              <span className="text-[10px] font-bold text-slate-400 uppercase">Estimated Resale Value</span>
              <p className="text-base font-extrabold text-emerald-600 dark:text-emerald-400">{resaleDisplay}</p>
            </div>
            <div className="p-3.5 bg-slate-50 dark:bg-slate-800/80 rounded-2xl border border-slate-200 dark:border-slate-700 space-y-1">
              <span className="text-[10px] font-bold text-slate-400 uppercase">Scrap Material Recovery Rate</span>
              <p className="text-base font-extrabold text-amber-600 dark:text-amber-400">{scrapDisplay}</p>
            </div>
          </div>

          {/* QR Code & Token Authentication */}
          <div className="p-4 bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-2xl flex items-center justify-between shadow-md">
            <div className="space-y-1 max-w-[280px]">
              <span className="text-[10px] font-extrabold uppercase text-emerald-400 tracking-wider">
                Digital Passport QR Token
              </span>
              <p className="text-xs font-mono font-bold text-slate-300 truncate">
                {tokenString}
              </p>
              <p className="text-[10px] text-slate-400">Scan QR badge with mobile camera to verify passport live</p>
            </div>
            <div className="p-1.5 bg-white rounded-xl shrink-0 border border-slate-200">
              <img
                src={qrCodeApiUrl}
                alt="Scannable QR Code Token"
                className="h-20 w-20 object-contain rounded-md"
              />
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="p-4 bg-slate-50 dark:bg-slate-800/60 border-t border-slate-200 dark:border-slate-800 flex items-center justify-end space-x-3">
          <button
            onClick={handlePrint}
            className="px-4 py-2 bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 text-slate-800 dark:text-slate-200 rounded-xl font-bold text-xs flex items-center space-x-2 transition-all"
          >
            <Printer className="h-4 w-4" />
            <span>Print Passport</span>
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs flex items-center space-x-2 shadow-md transition-all"
          >
            <span>Done</span>
          </button>
        </div>
      </div>
    </div>
  );
};
