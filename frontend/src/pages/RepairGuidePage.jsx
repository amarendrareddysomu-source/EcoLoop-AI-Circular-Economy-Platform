import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { DashboardLayout } from '../layouts/DashboardLayout';
import {
  Wrench,
  Sparkles,
  ArrowLeft,
  CheckCircle2,
  Clock,
  DollarSign,
  Layers,
  Flame,
  ShieldAlert,
  ChevronRight,
  BookOpen,
  Award
} from 'lucide-react';

const REPAIR_DATA = {
  Clothes: {
    "Minor Tear / Split Seam": {
      difficulty: "Easy",
      time: "15 mins",
      cost_inr: 20,
      value_added_inr: 350,
      tools: ["Needle & Matching Thread", "Fabric Scissors", "Safety Pins"],
      steps: [
        "Turn garment inside out to expose the broken seam.",
        "Pin the edges together smoothly to maintain alignment.",
        "Thread needle with double-stranded thread and execute a backstitch along the original seam line.",
        "Tie a secure double knot at the end and press with an iron to smooth out stitches."
      ]
    },
    "Stain or Fading": {
      difficulty: "Medium",
      time: "45 mins",
      cost_inr: 80,
      value_added_inr: 500,
      tools: ["Baking Soda", "White Vinegar", "Soft Fabric Brush", "Natural Dye Batch"],
      steps: [
        "Apply baking soda paste to stain and let sit for 20 minutes.",
        "Rinse thoroughly under lukewarm water.",
        "If color is faded, submerge garment in eco-friendly fabric dye bath for 30 minutes.",
        "Rinse in cold water until water runs clear and air dry in shade."
      ]
    },
    "Broken Zipper Slider": {
      difficulty: "Easy",
      time: "20 mins",
      cost_inr: 40,
      value_added_inr: 400,
      tools: ["Needle-Nose Pliers", "Replacement Zipper Slider", "Seam Ripper"],
      steps: [
        "Remove the metal top stop at the top of the zipper track using pliers.",
        "Slide off the damaged zipper slider and replace it with a new matching slider.",
        "Test zipper track alignment by zipping up and down gently.",
        "Crimp a new top stop onto the zipper teeth to lock slider in track."
      ]
    }
  },

  Shoes: {
    "Sole Separation": {
      difficulty: "Medium",
      time: "30 mins",
      cost_inr: 120,
      value_added_inr: 600,
      tools: ["Barge Super Adhesive / Shoe Goo", "Sandpaper (120-grit)", "Clamps / Heavy Rubber Bands", "Isopropyl Alcohol"],
      steps: [
        "Clean both separated rubber surfaces with isopropyl alcohol to remove dirt and old glue.",
        "Gently roughen the contact area with 120-grit sandpaper for maximum adhesion.",
        "Apply an even layer of shoe adhesive to both surfaces and let dry for 5 minutes until tacky.",
        "Press sole firmly against upper and secure tightly with clamps or rubber bands for 24 hours."
      ]
    },
    "Scuffed Leather": {
      difficulty: "Easy",
      time: "20 mins",
      cost_inr: 50,
      value_added_inr: 400,
      tools: ["Microfiber Cloth", "Matching Leather Polish / Conditioner", "Horsehair Brush"],
      steps: [
        "Wipe surface clean with a damp microfiber cloth to remove dust.",
        "Apply a pea-sized amount of leather cream conditioner in circular motions.",
        "Buff vigorously with horsehair brush to restore natural shine and seal scuffs."
      ]
    },
    "Torn Eyelets & Laces": {
      difficulty: "Easy",
      time: "15 mins",
      cost_inr: 30,
      value_added_inr: 250,
      tools: ["Metal Eyelet Punch Tool", "Brass Eyelet Rings", "New Heavy Duty Laces"],
      steps: [
        "Punch a clean hole through the torn lace channel.",
        "Insert brass eyelet ring and crimp firmly using the eyelet punch tool.",
        "Thread new reinforced laces through the repaired eyelets."
      ]
    }
  },

  Battery: {
    "Corroded Battery Contacts": {
      difficulty: "Easy",
      time: "15 mins",
      cost_inr: 15,
      value_added_inr: 250,
      tools: ["Vinegar or Lemon Juice", "Cotton Swabs", "Brass Wire Brush / Fine Sandpaper", "Dielectric Grease"],
      steps: [
        "Dip cotton swab in mild white vinegar or lemon juice to neutralize alkaline corrosion.",
        "Scrub metal terminal contacts gently until shiny brass/copper layer is restored.",
        "Wipe clean with dry cloth and apply a thin dab of dielectric grease to prevent future oxidation."
      ]
    },
    "Terminal Cleaning & De-Oxidation": {
      difficulty: "Easy",
      time: "10 mins",
      cost_inr: 10,
      value_added_inr: 200,
      tools: ["Contact Cleaner Spray", "Lint-Free Cloth", "Brass Terminal Brush"],
      steps: [
        "Spray electronic contact cleaner onto battery terminals.",
        "Scrub lead/copper oxides away with soft brass brush.",
        "Wipe dry and verify voltage conductivity using a multimeter."
      ]
    }
  },

  Metal: {
    "Rust & Oxidation": {
      difficulty: "Medium",
      time: "40 mins",
      cost_inr: 60,
      value_added_inr: 450,
      tools: ["Steel Wool (0000 grade)", "Rust Converter Spray / Vinegar Bath", "Anti-Rust Clear Coat"],
      steps: [
        "Submerge metal part in vinegar bath for 2 hours to dissolve surface rust.",
        "Scrub remaining rust flakes away using fine steel wool.",
        "Apply rust converter spray and seal with clear anti-corrosion lacquer."
      ]
    },
    "Dented Sheet Metal": {
      difficulty: "Medium",
      time: "30 mins",
      cost_inr: 50,
      value_added_inr: 350,
      tools: ["Rubber Mallet", "Wood Dolly Block", "Heat Gun"],
      steps: [
        "Warm dented metal area with heat gun to make metal pliable.",
        "Place wood dolly block behind dent and tap gently from inside out using rubber mallet.",
        "Smooth out minor high spots with light tapping until contour is restored."
      ]
    }
  },

  Glass: {
    "Surface Scratching": {
      difficulty: "Easy",
      time: "25 mins",
      cost_inr: 30,
      value_added_inr: 300,
      tools: ["Cerium Oxide Polish / Whitening Toothpaste", "Buffing Pad / Felt Wheel"],
      steps: [
        "Clean glass surface with microfiber cloth and glass cleaner.",
        "Apply cerium oxide polishing paste directly over scratch.",
        "Buff in firm circular motions with felt wheel for 10 minutes until scratch vanishes."
      ]
    },
    "Upcycle Bottle into Self-Watering Planter": {
      difficulty: "Medium",
      time: "35 mins",
      cost_inr: 40,
      value_added_inr: 380,
      tools: ["Glass Bottle Cutter Tool", "Boiling Water & Ice Bath", "Cotton Wick", "Potting Soil"],
      steps: [
        "Score bottle circumference evenly using bottle cutter tool.",
        "Alternate pouring boiling water and ice water over score line until glass snaps cleanly.",
        "Sand sharp cut edges smooth with 220-grit wet sandpaper.",
        "Insert top half upside down into bottom half, thread cotton wick, and fill with soil and plant."
      ]
    }
  },

  Plastic: {
    "Cracked Plastic Container": {
      difficulty: "Medium",
      time: "20 mins",
      cost_inr: 40,
      value_added_inr: 280,
      tools: ["Plastic Weld Epoxy / Heat Gun", "Reinforcement Mesh Wire"],
      steps: [
        "Clean crack area thoroughly with alcohol.",
        "Apply 2-part plastic epoxy along the seam inside and outside.",
        "Press stainless steel mesh wire across crack for structural strength and allow 4 hours to cure."
      ]
    },
    "Upcycle Plastic Bucket into Storage Bin": {
      difficulty: "Easy",
      time: "30 mins",
      cost_inr: 35,
      value_added_inr: 320,
      tools: ["Jute Rope", "Hot Glue Gun", "Fabric Lining"],
      steps: [
        "Clean plastic bucket exterior and dry completely.",
        "Wrap jute rope tightly around bucket exterior starting from base, securing with hot glue.",
        "Insert fabric lining inside bucket for a chic upcycled storage container."
      ]
    }
  },

  Cardboard: {
    "Torn Box Flaps & Structural Sag": {
      difficulty: "Easy",
      time: "15 mins",
      cost_inr: 25,
      value_added_inr: 200,
      tools: ["Heavy Duty Kraft Tape", "PVA Wood Glue", "Reinforcement Cardboard Strips"],
      steps: [
        "Glue reinforcement cardboard strips across inner crease joints.",
        "Apply water-activated kraft tape along external box edges to restore compression strength.",
        "Weight box down with flat heavy book for 1 hour to set glue."
      ]
    },
    "Upcycle Cardboard into Desk Organizer": {
      difficulty: "Easy",
      time: "30 mins",
      cost_inr: 30,
      value_added_inr: 350,
      tools: ["Craft Utility Knife", "Ruler", "Decorative Wrapping Paper", "Glue Stick"],
      steps: [
        "Cut cardboard box into tiered slanted compartment sections.",
        "Cover exterior and dividers with decorative wrapping paper.",
        "Assemble dividers inside main box shell to create a multi-slot desk organizer."
      ]
    }
  },

  Paper: {
    "Torn Document Pages": {
      difficulty: "Easy",
      time: "10 mins",
      cost_inr: 15,
      value_added_inr: 180,
      tools: ["Archival Document Repair Tape", "Bone Folder Tool"],
      steps: [
        "Align torn paper edges under bright light.",
        "Apply acid-free archival mending tape over tear line.",
        "Smooth tape flat with bone folder tool to eliminate air bubbles."
      ]
    },
    "Upcycle Waste Paper into Seed Paper": {
      difficulty: "Medium",
      time: "40 mins",
      cost_inr: 25,
      value_added_inr: 300,
      tools: ["Blender", "Deckle & Mould Frame", "Planting Seeds", "Water"],
      steps: [
        "Shred waste paper and soak in warm water for 2 hours.",
        "Blend soaked paper into fine pulp and stir in flower or herb seeds.",
        "Scoop pulp onto deckle screen frame, press out excess water, and let dry into plantable seed paper."
      ]
    }
  },

  Biological: {
    "Home Composting Organic Waste": {
      difficulty: "Easy",
      time: "20 mins",
      cost_inr: 50,
      value_added_inr: 400,
      tools: ["Aerated Compost Bin", "Dry Leaves (Browns)", "Kitchen Scraps (Greens)"],
      steps: [
        "Layer 2 inches of dry leaves/cardboard at bin bottom for aeration.",
        "Add kitchen fruit & veggie peels in 1:2 ratio with dry brown matter.",
        "Mix compost pile weekly to oxygenate and harvest nutrient-rich black humus in 4-6 weeks."
      ]
    },
    "Fermenting Citrus Peels into Bio-Cleaner": {
      difficulty: "Easy",
      time: "15 mins",
      cost_inr: 30,
      value_added_inr: 320,
      tools: ["Glass Jar", "Citrus Peels (Lemon/Orange)", "White Vinegar"],
      steps: [
        "Pack citrus peels into glass jar until 3/4 full.",
        "Pour white vinegar to completely submerge peels.",
        "Seal jar and steep for 2 weeks, then strain liquid into spray bottle for natural grease-cutting cleaner."
      ]
    }
  },

  Trash: {
    "Upcycling Trash Containers into Herb Pots": {
      difficulty: "Easy",
      time: "20 mins",
      cost_inr: 20,
      value_added_inr: 250,
      tools: ["Hand Drill / Nail", "Acrylic Paint", "Gravel & Soil"],
      steps: [
        "Drill 3 drainage holes in base of discarded plastic or tin container.",
        "Paint exterior with waterproof acrylic paint.",
        "Add 1 inch of drainage gravel at bottom, fill with potting soil, and plant herbs."
      ]
    }
  }
};

export const RepairGuidePage = () => {
  const navigate = useNavigate();

  const [selectedCategory, setSelectedCategory] = useState("Clothes");
  const categories = Object.keys(REPAIR_DATA);
  const issues = Object.keys(REPAIR_DATA[selectedCategory] || {});
  const [selectedIssue, setSelectedIssue] = useState(issues[0] || "");

  const activeGuide = REPAIR_DATA[selectedCategory]?.[selectedIssue] || REPAIR_DATA["Clothes"]["Minor Tear / Split Seam"];

  const handleCategoryChange = (cat) => {
    setSelectedCategory(cat);
    const catIssues = Object.keys(REPAIR_DATA[cat] || {});
    setSelectedIssue(catIssues[0] || "");
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-amber-600 via-orange-600 to-indigo-800 text-white shadow-xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-3">
              <Wrench className="h-8 w-8 text-amber-300 shrink-0" />
              <h1 className="text-2xl md:text-3xl font-extrabold font-heading">AI Circular Repair & Upcycling Guide</h1>
            </div>
            <p className="text-xs md:text-sm text-amber-100/90">
              Extend item lifespans across all 10 material categories with step-by-step DIY repair guides, tool checklists, and ROI value estimation.
            </p>
          </div>

          <button
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 bg-white/10 hover:bg-white/20 backdrop-blur-md rounded-2xl border border-white/20 text-xs font-bold flex items-center space-x-2 transition-all text-white shadow-sm shrink-0"
          >
            <ArrowLeft className="h-4 w-4 text-amber-300" />
            <span>Back to Dashboard</span>
          </button>
        </div>

        {/* Category & Damage Selector */}
        <div className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
          <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-3">
            <BookOpen className="h-5 w-5 text-amber-600" />
            <span>Select Item Category & Issue (All 10 Material Classes)</span>
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Item Category (10 Classes)</label>
              <select
                value={selectedCategory}
                onChange={(e) => handleCategoryChange(e.target.value)}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:ring-2 focus:ring-amber-500"
              >
                {categories.map((cat) => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Specific Issue / Upcycling Project</label>
              <select
                value={selectedIssue}
                onChange={(e) => setSelectedIssue(e.target.value)}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs font-semibold focus:ring-2 focus:ring-amber-500"
              >
                {issues.map((iss) => (
                  <option key={iss} value={iss}>{iss}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Repair Walkthrough Display */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* ROI & Overview Metrics Card (Left Side) */}
          <div className="lg:col-span-4 space-y-4">
            <div className="p-6 rounded-3xl bg-slate-900 text-white shadow-xl space-y-5 border border-slate-800">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="px-3 py-1 bg-amber-500/20 text-amber-300 border border-amber-500/40 rounded-full text-[10px] font-extrabold uppercase">
                  Repair Feasibility AI Assessment
                </span>
              </div>

              <div className="space-y-1">
                <h3 className="text-xl font-extrabold text-white">{selectedIssue}</h3>
                <p className="text-xs text-slate-400 font-medium">Category: <strong>{selectedCategory}</strong></p>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 bg-slate-800/80 rounded-2xl border border-slate-700 space-y-1">
                  <span className="text-[10px] text-slate-400 font-bold uppercase block">Difficulty</span>
                  <span className="text-sm font-extrabold text-emerald-400">{activeGuide.difficulty}</span>
                </div>

                <div className="p-3 bg-slate-800/80 rounded-2xl border border-slate-700 space-y-1">
                  <span className="text-[10px] text-slate-400 font-bold uppercase block">Est. Time</span>
                  <span className="text-sm font-extrabold text-amber-400">{activeGuide.time}</span>
                </div>
              </div>

              <div className="p-4 bg-gradient-to-r from-emerald-950 to-teal-950 rounded-2xl border border-emerald-800 space-y-2">
                <span className="text-[10px] font-extrabold text-emerald-400 uppercase tracking-wider block">Financial ROI Math</span>
                <div className="flex items-center justify-between text-xs font-bold">
                  <span className="text-slate-300">DIY Material Cost:</span>
                  <span className="text-red-400">₹{activeGuide.cost_inr}</span>
                </div>
                <div className="flex items-center justify-between text-xs font-bold">
                  <span className="text-slate-300">Resale Value Increase:</span>
                  <span className="text-emerald-400">+₹{activeGuide.value_added_inr}</span>
                </div>
                <div className="pt-2 border-t border-emerald-800/80 flex items-center justify-between text-sm font-extrabold">
                  <span className="text-white">Net Value Added:</span>
                  <span className="text-emerald-300">₹{activeGuide.value_added_inr - activeGuide.cost_inr}</span>
                </div>
              </div>

              {/* Required Tools Checklist */}
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Required Tools Checklist</h4>
                <div className="space-y-1.5">
                  {activeGuide.tools.map((tool, idx) => (
                    <div key={idx} className="flex items-center space-x-2 text-xs font-medium text-slate-300">
                      <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" />
                      <span>{tool}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Step-by-Step Instructions (Right Side) */}
          <div className="lg:col-span-8 p-6 rounded-3xl glass-card border border-slate-200 dark:border-slate-800 space-y-6 shadow-sm">
            <h3 className="text-lg font-extrabold text-slate-900 dark:text-slate-100 flex items-center space-x-2 border-b border-slate-200 dark:border-slate-800 pb-3">
              <Sparkles className="h-5 w-5 text-amber-500" />
              <span>Step-by-Step Repair Instructions</span>
            </h3>

            <div className="space-y-4">
              {activeGuide.steps.map((stepText, idx) => (
                <div key={idx} className="p-4 bg-slate-50 dark:bg-slate-800/60 rounded-2xl border border-slate-200 dark:border-slate-700 flex items-start space-x-4">
                  <div className="w-8 h-8 rounded-full bg-amber-500 text-white font-extrabold text-sm flex items-center justify-center shrink-0 shadow-md">
                    {idx + 1}
                  </div>
                  <div className="space-y-1 pt-1">
                    <h4 className="text-xs font-extrabold uppercase text-amber-600 dark:text-amber-400 tracking-wider">
                      Phase {idx + 1}
                    </h4>
                    <p className="text-xs md:text-sm font-medium text-slate-700 dark:text-slate-200 leading-relaxed">
                      {stepText}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
              <span className="text-xs text-slate-500">Guide verified by GreenLoop Repair Engineers</span>
              <button
                onClick={() => navigate('/impact-passports')}
                className="px-4 py-2.5 bg-amber-600 hover:bg-amber-700 text-white rounded-xl font-bold text-xs shadow-md transition-all flex items-center space-x-2"
              >
                <span>Generate Passport After Repair</span>
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};
