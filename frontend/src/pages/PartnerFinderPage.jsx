import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { DashboardLayout } from '../layouts/DashboardLayout';
import {
  Building2,
  MapPin,
  Phone,
  Truck,
  ArrowLeft,
  Search,
  Filter,
  CheckCircle2,
  ExternalLink,
  ShieldCheck,
  Award
} from 'lucide-react';

import { DeliveryQRScannerModal } from '../components/DeliveryQRScannerModal';

export const PartnerFinderPage = () => {
  const navigate = useNavigate();
  const [scannerOpen, setScannerOpen] = useState(false);

  const STATES_AREAS = {
    "Andhra Pradesh": [
      "Nellore - VRC Centre Area",
      "Nellore - Trunk Road Hub",
      "Kakinada - Main Road Hub",
      "Kakinada - Port Area Industrial Zone",
      "Visakhapatnam - Gajuwaka Industrial Zone",
      "Visakhapatnam - Dwaraka Nagar",
      "Vijayawada - Auto Nagar Hub",
      "Vijayawada - Benz Circle",
      "Tirupati - Renigunta Road",
      "Guntur - Market Yard Area"
    ],
    "Karnataka": [
      "Bangalore - Peenya Industrial Area",
      "Bangalore - Koramangala",
      "Bangalore - Indiranagar",
      "Bangalore - Whitefield",
      "Bangalore - Electronic City",
      "Bangalore - Jayanagar",
      "Mysore - Industrial Suburb",
      "Hubli - Gokul Road Area"
    ],
    "Maharashtra": [
      "Mumbai - Andheri East",
      "Mumbai - Bandra West",
      "Mumbai - Thane West",
      "Mumbai - Navi Mumbai Vashi",
      "Pune - Chinchwad Industrial Zone",
      "Pune - Kothrud",
      "Nagpur - MIDC Area"
    ],
    "Delhi NCR": [
      "New Delhi - Okhla Industrial Estate",
      "New Delhi - Connaught Place",
      "New Delhi - Dwarka Sector 12",
      "Noida - Sector 63",
      "Gurgaon - Udyog Vihar"
    ],
    "Tamil Nadu": [
      "Chennai - Guindy Industrial Estate",
      "Chennai - T. Nagar",
      "Chennai - Velachery",
      "Chennai - Ambattur",
      "Coimbatore - Peelamedu",
      "Madurai - K.K. Nagar"
    ],
    "Telangana": [
      "Hyderabad - Hitech City Phase 2",
      "Hyderabad - Gachibowli",
      "Hyderabad - Secunderabad",
      "Hyderabad - Kukatpally Housing Board"
    ],
    "Gujarat": [
      "Ahmedabad - GIDC Naroda",
      "Ahmedabad - Satellite Area",
      "Surat - Ichhapore GIDC",
      "Vadodara - Makarpura"
    ],
    "West Bengal": [
      "Kolkata - Salt Lake Sector V",
      "Kolkata - Howrah Industrial Hub",
      "Kolkata - Park Street"
    ]
  };

  const categories = ["Battery", "Biological", "Cardboard", "Clothes", "Glass", "Metal", "Paper", "Plastic", "Shoes", "Trash"];

  const [selectedState, setSelectedState] = useState("Karnataka");
  const [selectedArea, setSelectedArea] = useState(STATES_AREAS["Karnataka"][0]);
  const [selectedCategory, setSelectedCategory] = useState("Clothes");

  const handleStateChange = (state) => {
    setSelectedState(state);
    setSelectedArea(STATES_AREAS[state][0]);
  };

  // Generate dynamic location-sensitive partners based on selectedState, selectedArea & selectedCategory
  const getDynamicPartners = () => {
    const stateShort = selectedState.substring(0, 3).toUpperCase();
    const areaName = selectedArea.split(" - ")[1] || selectedArea;

    return [
      {
        name: `${areaName} Certified ${selectedCategory} Recycling Hub`,
        type: "Govt Certified Facility",
        phone: "+91 80 4400 1122",
        rating: 4.9,
        pickup: true,
        address: `${selectedArea}, ${selectedState}`,
        rate: selectedCategory === 'Clothes' || selectedCategory === 'Shoes' 
          ? "Free Pickup & Donation" 
          : `Scrap Rate: ₹${selectedCategory === 'Metal' ? '50' : selectedCategory === 'Battery' ? '42' : '12'} / kg`
      },
      {
        name: `GreenLoop ${selectedCategory} Pickup Partner (${stateShort})`,
        type: "Authorized Collection Center",
        phone: "+91 98 7654 3210",
        rating: 4.8,
        pickup: true,
        address: `${selectedArea}, ${selectedState}`,
        rate: "Free Doorstep Pickup Available"
      },
      {
        name: `${selectedState} Environmental NGO Shelter`,
        type: "Community NGO",
        phone: "+91 80 9988 7766",
        rating: 4.7,
        pickup: true,
        address: `${selectedArea}, ${selectedState}`,
        rate: "Community Upcycling Stream"
      }
    ];
  };

  const partners = getDynamicPartners();

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-purple-700 via-indigo-700 to-teal-800 text-white shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-3">
              <Building2 className="h-8 w-8 text-emerald-300 shrink-0" />
              <h1 className="text-2xl md:text-3xl font-extrabold font-heading">Smart Local NGO & Pickup Partner Finder</h1>
            </div>
            <p className="text-xs md:text-sm text-purple-100/90">
              Select your state, city area, and material to connect directly with verified recycling centers & NGO pickup services.
            </p>
          </div>

          <div className="flex items-center space-x-2 shrink-0">
            <button
              onClick={() => setScannerOpen(true)}
              className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 backdrop-blur-md rounded-2xl text-xs font-extrabold flex items-center space-x-2 transition-all text-white shadow-md"
            >
              <ShieldCheck className="h-4 w-4" />
              <span>Delivery Agent QR Scanner</span>
            </button>

            <button
              onClick={() => navigate('/dashboard')}
              className="px-4 py-2 bg-white/10 hover:bg-white/20 backdrop-blur-md rounded-2xl border border-white/20 text-xs font-bold flex items-center space-x-2 transition-all text-white shadow-sm"
            >
              <ArrowLeft className="h-4 w-4 text-emerald-300" />
              <span>Back to Dashboard</span>
            </button>
          </div>
        </div>

        {/* Location & Category Selection Controls */}
        <div className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
          <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-3">
            <Filter className="h-5 w-5 text-purple-600" />
            <span>Select Location & Material Filters</span>
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* State Select */}
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">State</label>
              <select
                value={selectedState}
                onChange={(e) => handleStateChange(e.target.value)}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:ring-2 focus:ring-purple-500"
              >
                {Object.keys(STATES_AREAS).map((state) => (
                  <option key={state} value={state}>{state}</option>
                ))}
              </select>
            </div>

            {/* City / Area Select */}
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">City / Main Area</label>
              <select
                value={selectedArea}
                onChange={(e) => setSelectedArea(e.target.value)}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:ring-2 focus:ring-purple-500"
              >
                {STATES_AREAS[selectedState].map((area) => (
                  <option key={area} value={area}>{area}</option>
                ))}
              </select>
            </div>

            {/* Category Select */}
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Material Category</label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:ring-2 focus:ring-purple-500"
              >
                {categories.map((cat) => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Partners Grid */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-extrabold uppercase tracking-wider text-slate-400">
              Verified Partners in {selectedArea}, {selectedState} ({selectedCategory})
            </h3>
            <span className="px-3 py-1 bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-200 rounded-full text-xs font-bold">
              {partners.length} Collection Hubs Active
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {partners.map((partner, idx) => (
              <div
                key={idx}
                className="p-5 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 hover:border-purple-500 transition-all space-y-4 shadow-sm flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="flex items-start justify-between">
                    <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-200">
                      {partner.type}
                    </span>
                    <span className="text-xs font-bold text-amber-500">★ {partner.rating}</span>
                  </div>

                  <h4 className="text-base font-bold text-slate-900 dark:text-slate-100">{partner.name}</h4>

                  <p className="text-xs text-slate-500 flex items-start space-x-1">
                    <MapPin className="h-4 w-4 text-purple-600 shrink-0 mt-0.5" />
                    <span>{partner.address}</span>
                  </p>

                  <p className="text-xs font-extrabold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 p-2 rounded-xl border border-emerald-200 dark:border-emerald-800">
                    {partner.rate}
                  </p>
                </div>

                <div className="pt-3 border-t border-slate-200 dark:border-slate-800 space-y-2">
                  <span className="flex items-center space-x-1.5 text-xs text-slate-600 dark:text-slate-300 font-medium">
                    <Truck className="h-4 w-4 text-purple-600" />
                    <span>Free Doorstep Pickup Available</span>
                  </span>

                  <a
                    href={`tel:${partner.phone}`}
                    className="w-full py-2.5 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-bold text-xs flex items-center justify-center space-x-2 shadow-sm transition-all"
                  >
                    <Phone className="h-4 w-4" />
                    <span>Call {partner.phone}</span>
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <DeliveryQRScannerModal
        open={scannerOpen}
        onClose={() => setScannerOpen(false)}
      />
    </DashboardLayout>
  );
};
