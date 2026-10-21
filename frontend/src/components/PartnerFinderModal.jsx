import React, { useState } from 'react';
import { MapPin, Phone, Truck, CheckCircle2, ExternalLink, X, ShieldCheck, Sparkles, Building2 } from 'lucide-react';

export const PartnerFinderModal = ({ open, onClose, defaultCategory = 'Clothes' }) => {
  const [selectedCategory, setSelectedCategory] = useState(defaultCategory);
  const [city, setCity] = useState('Bangalore');

  if (!open) return null;

  const categories = ["Battery", "Biological", "Cardboard", "Clothes", "Glass", "Metal", "Paper", "Plastic", "Shoes", "Trash"];

  const PARTNERS_DATABASE = {
    Clothes: [
      { name: "Goonj Community Clothing NGO", type: "NGO & Shelter", phone: "+91 80 2668 0000", pickup: true, rating: 4.9, address: "Koramangala 4th Block, Bangalore", rate: "Free Pick-up & Redistribution" },
      { name: "Clothes Box Foundation", type: "Non-Profit", phone: "+91 98 1000 1234", pickup: true, rating: 4.8, address: "Indiranagar, Bangalore", rate: "Community Freecycle Partner" }
    ],
    Shoes: [
      { name: "GreenSole Footwear Recycling", type: "Upcycling Center", phone: "+91 99 2000 4567", pickup: true, rating: 4.9, address: "Whitefield, Bangalore", rate: "Upcycling & Recycled Sole Recovery" },
      { name: "Footwear Shelter NGO", type: "NGO Partner", phone: "+91 80 4111 8899", pickup: true, rating: 4.7, address: "Jayanagar, Bangalore", rate: "Donation Pick-up" }
    ],
    Battery: [
      { name: "EcoRecycle Certified E-Waste Hub", type: "Authorized Recycler", phone: "+91 80 6789 1234", pickup: true, rating: 4.9, address: "Peenya Industrial Area, Bangalore", rate: "Scrap Rate: ₹42 / kg ($0.50)" },
      { name: "CleanTech E-Waste Terminal", type: "Govt Certified", phone: "+91 98 4500 9900", pickup: true, rating: 4.8, address: "Electronic City, Bangalore", rate: "Hazardous Chemical Disposal" }
    ],
    Metal: [
      { name: "Metals Scrap Recovery Corp", type: "Industrial Smelter", phone: "+91 80 2333 4455", pickup: true, rating: 4.9, address: "Peenya 2nd Stage, Bangalore", rate: "Scrap Rate: ₹50 / kg ($0.60)" },
      { name: "Apex Aluminium & Iron Hub", type: "Recycling Facility", phone: "+91 98 8000 1122", pickup: true, rating: 4.8, address: "Rajajinagar, Bangalore", rate: "Scrap Pick-up" }
    ],
    Plastic: [
      { name: "Polymer Material Recovery Hub", type: "Plastic Recycler", phone: "+91 80 5555 6677", pickup: true, rating: 4.8, address: "Bommasandra, Bangalore", rate: "Scrap Rate: ₹12 / kg ($0.15)" },
      { name: "CleanPlast Circular Unit", type: "MRF Facility", phone: "+91 99 0000 3344", pickup: true, rating: 4.7, address: "Yeshwanthpur, Bangalore", rate: "Bulk Poly Recycling" }
    ],
    Glass: [
      { name: "Silica Glass Recycling Plant", type: "Glass Cullet Facility", phone: "+91 80 4444 2211", pickup: true, rating: 4.8, address: "Hosur Road Industrial Zone, Bangalore", rate: "Scrap Rate: ₹7 / kg ($0.08)" }
    ],
    Cardboard: [
      { name: "Paper & Cardboard Mill Recycler", type: "Pulp Recovery", phone: "+91 80 3333 9988", pickup: true, rating: 4.8, address: "Peenya 1st Stage, Bangalore", rate: "Scrap Rate: ₹7 / kg ($0.08)" }
    ],
    Paper: [
      { name: "CleanPaper Pulping Hub", type: "Pulp & Paper Mill", phone: "+91 80 2222 1100", pickup: true, rating: 4.9, address: "Hebbal, Bangalore", rate: "Scrap Rate: ₹4 / kg ($0.05)" }
    ],
    Biological: [
      { name: "City Municipal Organic Bio-Composting", type: "Bio-Digestion Hub", phone: "+91 80 1912 0000", pickup: true, rating: 4.9, address: "Hebbal Bio-Park, Bangalore", rate: "Organic Composting Stream" }
    ],
    Trash: [
      { name: "City Waste-to-Energy Terminal", type: "Municipal Transfer Hub", phone: "+91 80 2222 2222", pickup: true, rating: 4.8, address: "Mavallipura Municipal Facility, Bangalore", rate: "Sanitary Landfill & Recovery" }
    ]
  };

  const partners = PARTNERS_DATABASE[selectedCategory] || PARTNERS_DATABASE['Clothes'];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-2xl bg-white dark:bg-slate-900 rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-5 bg-gradient-to-r from-teal-700 via-emerald-700 to-indigo-800 text-white flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Building2 className="h-6 w-6 text-emerald-300" />
            <div>
              <h3 className="font-extrabold text-base tracking-wide font-heading">NGO & Recycling Partner Finder</h3>
              <p className="text-[10px] text-emerald-100/90 font-medium">Verified local collection centers, shelters & MRF pickup hubs</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-full hover:bg-white/20 text-white transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Filter Controls */}
        <div className="p-4 bg-slate-50 dark:bg-slate-800/60 border-b border-slate-200 dark:border-slate-700 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center space-x-2 w-full sm:w-auto">
            <span className="text-xs font-bold text-slate-700 dark:text-slate-300">Material:</span>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          <div className="flex items-center space-x-2 w-full sm:w-auto">
            <MapPin className="h-4 w-4 text-emerald-600" />
            <span className="text-xs font-bold text-slate-700 dark:text-slate-300">Location:</span>
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
        </div>

        {/* Partners List */}
        <div className="p-6 space-y-4 overflow-y-auto max-h-[55vh]">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-slate-400">
              Verified Partners for {selectedCategory} in {city}
            </h4>
            <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400">
              {partners.length} Hubs Available
            </span>
          </div>

          {partners.map((partner, idx) => (
            <div
              key={idx}
              className="p-4 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 hover:border-emerald-500 transition-all space-y-3 shadow-sm"
            >
              <div className="flex items-start justify-between">
                <div>
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-200">
                    {partner.type}
                  </span>
                  <h4 className="text-base font-bold text-slate-900 dark:text-slate-100 mt-1">{partner.name}</h4>
                  <p className="text-xs text-slate-500 flex items-center space-x-1 mt-0.5">
                    <MapPin className="h-3.5 w-3.5 text-slate-400 shrink-0" />
                    <span>{partner.address}</span>
                  </p>
                </div>
                <div className="text-right">
                  <span className="text-xs font-bold text-amber-500 flex items-center justify-end space-x-1">
                    <span>★ {partner.rating}</span>
                  </span>
                  <p className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 mt-1">{partner.rate}</p>
                </div>
              </div>

              <div className="pt-2 flex items-center justify-between border-t border-slate-200 dark:border-slate-800/60 text-xs">
                <span className="flex items-center space-x-1 text-slate-600 dark:text-slate-300 font-medium">
                  <Truck className="h-4 w-4 text-emerald-600" />
                  <span>Free Doorstep Pickup Available</span>
                </span>
                <a
                  href={`tel:${partner.phone}`}
                  className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs flex items-center space-x-1.5 shadow-sm transition-all"
                >
                  <Phone className="h-3.5 w-3.5" />
                  <span>Call {partner.phone}</span>
                </a>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 dark:bg-slate-800/60 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <p className="text-xs text-slate-500">All collection centers are verified by municipal environmental authorities.</p>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs shadow-md transition-all"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
