import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import api from '../api/axios';
import { DashboardLayout } from '../layouts/DashboardLayout';
import { formatCurrency } from '../utils/formatters';
import {
  BrainCircuit,
  Sparkles,
  ShieldCheck,
  Leaf,
  DollarSign,
  Upload,
  Image as ImageIcon,
  Trash2,
  CheckCircle2,
  ArrowRight,
  ArrowLeft,
  PlusCircle,
  AlertTriangle,
  AlertCircle,
  RefreshCw,
  Eye,
  ChevronDown,
  ChevronUp,
  Cpu,
  Layers,
  Wrench,
  Crosshair,
  Info,
  Zap,
  BarChart3,
  HelpCircle,
  Sliders,
  Award,
  Building2
} from 'lucide-react';
import { ImpactPassportModal } from '../components/ImpactPassportModal';
import { PartnerFinderModal } from '../components/PartnerFinderModal';


export const AIPredictionsPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const fileInputRef = useRef(null);

  // Main Image Pipeline State
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(0);
  const [predictionResult, setPredictionResult] = useState(null);
  const [uploadError, setUploadError] = useState(null);
  const [savingInventory, setSavingInventory] = useState(false);
  const [inventorySaved, setInventorySaved] = useState(false);
  const [showTop5, setShowTop5] = useState(true);
  const [showHeatmap, setShowHeatmap] = useState(false);
  const [showBoundingBoxes, setShowBoundingBoxes] = useState(true);
  const [passportOpen, setPassportOpen] = useState(false);
  const [partnerOpen, setPartnerOpen] = useState(false);

  // Navigation tab
  const [activeTab, setActiveTab] = useState('pipeline'); // 'pipeline' | 'manual' | 'sustainability' | 'price' | 'condition' | 'recommendation' | 'metrics'

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const tab = params.get('tab');
    if (tab === 'passport') {
      navigate('/impact-passports', { replace: true });
    } else if (tab === 'partners') {
      navigate('/pickup-partners', { replace: true });
    } else if (tab) {
      setActiveTab(tab);
    }
  }, [location.search, navigate]);

  // Manual Input Form State
  const [manualForm, setManualForm] = useState({
    item_name: 'Cardboard Box',
    category: 'Cardboard Box',
    condition: 'Good',
    weight_kg: 0.5,
    age_years: 0.5,
    original_price: 25.0
  });
  const [manualResult, setManualResult] = useState(null);
  const [manualLoading, setManualLoading] = useState(false);

  const handleManualSubmit = async (e) => {
    e.preventDefault();
    setManualLoading(true);
    try {
      const res = await api.post('/ai/manual-classify', manualForm);
      setManualResult(res.data);
    } catch (err) {
      alert('Failed to evaluate manual classification');
    } finally {
      setManualLoading(false);
    }
  };


  // Form states for manual exploration sub-tabs
  const [susForm, setSusForm] = useState({
    category: 'Cardboard Box',
    material: 'paper',
    condition: 'Good',
    weight_kg: 0.5,
    reuse_potential: 'High'
  });
  const [susResult, setSusResult] = useState(null);
  const [susLoading, setSusLoading] = useState(false);

  const [priceForm, setPriceForm] = useState({
    category: 'Cardboard Box',
    brand: 'Generic',
    age_years: 0.5,
    condition: 'Good',
    original_price: 25.0
  });
  const [priceResult, setPriceResult] = useState(null);
  const [priceLoading, setPriceLoading] = useState(false);


  const [condForm, setCondForm] = useState({
    age_years: 1.0,
    usage_level: 'Moderate',
    user_stated_condition: 'Good'
  });
  const [condResult, setCondResult] = useState(null);
  const [condLoading, setCondLoading] = useState(false);

  const [recForm, setRecForm] = useState({
    category: 'Electronics',
    condition: 'Fair',
    age_years: 2.5,
    estimated_price: 200.0,
    location: 'Downtown'
  });
  const [recResult, setRecResult] = useState(null);
  const [recLoading, setRecLoading] = useState(false);

  // File Validation Handler
  const validateAndSetFile = (file) => {
    setUploadError(null);
    setPredictionResult(null);
    setInventorySaved(false);
    setShowHeatmap(false);

    if (!file) return;

    const allowedExtensions = ['jpg', 'jpeg', 'png', 'webp'];
    const fileNameParts = file.name.split('.');
    const ext = fileNameParts[fileNameParts.length - 1].toLowerCase();
    const allowedMimes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];

    if (!allowedExtensions.includes(ext) || (file.type && !allowedMimes.includes(file.type.toLowerCase()))) {
      setUploadError('Unsupported file format. Please upload a JPG, JPEG, PNG, or WEBP image.');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setUploadError('File size exceeds maximum 10 MB limit. Please upload a smaller image.');
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleRemoveImage = () => {
    setSelectedFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setPreviewUrl(null);
    setPredictionResult(null);
    setUploadError(null);
    setInventorySaved(false);
    setShowHeatmap(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Run Real AI Pipeline
  const handleAnalyzeImage = async () => {
    if (!selectedFile) return;

    setAnalyzing(true);
    setUploadError(null);
    setPredictionResult(null);
    setShowHeatmap(false);
    setAnalysisStep(1);

    const stepTimer1 = setTimeout(() => setAnalysisStep(2), 600);
    const stepTimer2 = setTimeout(() => setAnalysisStep(3), 1200);

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const res = await api.post('/ai/classify-image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setAnalysisStep(4);
      setTimeout(() => {
        setPredictionResult(res.data);
        setAnalyzing(false);
      }, 400);
    } catch (err) {
      clearTimeout(stepTimer1);
      clearTimeout(stepTimer2);
      setAnalyzing(false);
      const msg = err.response?.data?.detail || 'Failed to analyze image. Please upload a clearer image.';
      setUploadError(msg);
    }
  };

  // Post-prediction Action: Save to Inventory
  const handleSaveToInventory = async () => {
    if (!predictionResult) return;
    setSavingInventory(true);
    try {
      const payload = {
        title: predictionResult.predicted_category,
        item_name: predictionResult.predicted_category,
        category: predictionResult.predicted_category,
        condition: predictionResult.condition,
        price: predictionResult.predicted_price,
        image_url: predictionResult.image_url,
        description: `AI Classified item (${predictionResult.predicted_category}) in ${predictionResult.condition} condition. Repairability: ${predictionResult.repairability_score}/100. Sustainability: ${predictionResult.sustainability_score}/100.`
      };
      await api.post('/inventory/', payload);
      setInventorySaved(true);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to save item to inventory.');
    } finally {
      setSavingInventory(false);
    }
  };

  const handleCreateListing = () => {
    if (!predictionResult) return;
    navigate('/transactions', {
      state: {
        prefillItem: {
          title: predictionResult.predicted_category,
          category: predictionResult.predicted_category,
          condition: predictionResult.condition,
          price: predictionResult.predicted_price,
          image_url: predictionResult.image_url
        }
      }
    });
  };

  // Handlers for secondary manual tabs
  const handleSusSubmit = async (e) => {
    e.preventDefault();
    setSusLoading(true);
    try {
      const res = await api.post('/ai/sustainability-score', susForm);
      setSusResult(res.data);
    } catch (err) {
      alert('Failed to compute sustainability score');
    } finally {
      setSusLoading(false);
    }
  };

  const handlePriceSubmit = async (e) => {
    e.preventDefault();
    setPriceLoading(true);
    try {
      const res = await api.post('/ai/predict-price', priceForm);
      setPriceResult(res.data);
    } catch (err) {
      alert('Failed to predict resale price');
    } finally {
      setPriceLoading(false);
    }
  };

  const handleCondSubmit = async (e) => {
    e.preventDefault();
    setCondLoading(true);
    try {
      const res = await api.post('/ai/predict-condition', condForm);
      setCondResult(res.data);
    } catch (err) {
      alert('Failed to predict condition');
    } finally {
      setCondLoading(false);
    }
  };

  const handleRecSubmit = async (e) => {
    e.preventDefault();
    setRecLoading(true);
    try {
      const res = await api.post('/ai/recommend', recForm);
      setRecResult(res.data);
    } catch (err) {
      alert('Failed to generate recommendations');
    } finally {
      setRecLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Hero Header */}
        <div className="p-6 rounded-3xl bg-gradient-to-r from-teal-700 via-emerald-700 to-indigo-800 text-white shadow-xl flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div className="space-y-1.5 max-w-3xl">
            <h1 className="text-2xl md:text-3xl font-bold font-heading flex items-center space-x-3">
              <BrainCircuit className="h-8 w-8 text-emerald-300 shrink-0" />
              <span>AI Circular Decision Engine</span>
            </h1>
            <p className="text-xs md:text-sm text-emerald-100/90 leading-relaxed">
              Upload any item image to instantly classify materials, detect visual damage, estimate resale market value, and receive AI-guided circular recommendations (Reuse, Repair, Donate, Sell, or Recycle).
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            <button
              onClick={() => {
                if (activeTab !== 'pipeline') {
                  setActiveTab('pipeline');
                } else {
                  navigate('/dashboard');
                }
              }}
              className="px-4 py-2 bg-white/10 hover:bg-white/20 backdrop-blur-md rounded-2xl border border-white/20 text-xs font-bold flex items-center space-x-2 transition-all text-white shadow-sm"
            >
              <ArrowLeft className="h-4 w-4 text-emerald-300" />
              <span>{activeTab !== 'pipeline' ? 'Back to Classifier' : 'Back to Dashboard'}</span>
            </button>

            <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-md px-3.5 py-2 rounded-2xl border border-white/20 text-xs font-semibold">
              <Sparkles className="h-4 w-4 text-amber-300 shrink-0" />
              <span>Instant AI Analysis</span>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-2 border-b border-slate-200 dark:border-slate-800 pb-2 overflow-x-auto">
          {[
            { id: 'pipeline', label: 'Image Classifier', icon: Crosshair },
            { id: 'manual', label: 'Manual Evaluator', icon: Sliders },
            { id: 'sustainability', label: 'Impact Calculator', icon: Leaf },
            { id: 'price', label: 'Price Estimator', icon: DollarSign },
            { id: 'condition', label: 'Condition Assessment', icon: ShieldCheck },
            { id: 'recommendation', label: 'Circular Strategy', icon: Sparkles },
            { id: 'metrics', label: 'System Metrics', icon: BarChart3 }
          ].map((tab) => (

            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-4 py-2.5 rounded-xl font-bold text-xs transition-all ${
                activeTab === tab.id
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/20'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
            >
              <tab.icon className="h-4 w-4" />
              <span>{tab.label}</span>
            </button>
          ))}
        </div>

        {/* TAB 1: MAIN REBUILT 14-PHASE CV PIPELINE */}
        {activeTab === 'pipeline' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Upload & Bounding Box View (Left Side) */}
              <div className="lg:col-span-5 space-y-4">
                <div className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
                  <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                    <Upload className="h-5 w-5 text-emerald-600" />
                    <span>Upload Item Image</span>
                  </h3>

                  {/* Drag & Drop / Preview Zone with Bounding Boxes */}
                  <div
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={() => !selectedFile && fileInputRef.current?.click()}
                    className={`relative border-2 border-dashed rounded-2xl p-4 text-center transition-all cursor-pointer flex flex-col items-center justify-center min-h-[260px] overflow-hidden ${
                      isDragging
                        ? 'border-emerald-500 bg-emerald-50/50 dark:bg-emerald-950/30'
                        : selectedFile
                        ? 'border-slate-300 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-900/50'
                        : 'border-slate-300 dark:border-slate-700 hover:border-emerald-500 dark:hover:border-emerald-500 hover:bg-slate-50 dark:hover:bg-slate-900'
                    }`}
                  >
                    <input
                      type="file"
                      ref={fileInputRef}
                      onChange={handleFileSelect}
                      accept="image/jpeg,image/png,image/jpg,image/webp"
                      className="hidden"
                    />

                    {previewUrl ? (
                      <div className="relative group w-full space-y-3">
                        <div className="relative inline-block w-full">
                          <img
                            src={showHeatmap && predictionResult?.gradcam_base64 ? predictionResult.gradcam_base64 : previewUrl}
                            alt="Preview"
                            className="h-56 w-full object-contain rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-950 transition-all duration-300"
                          />

                          {/* Bounding Box Overlay Canvas */}
                          {showBoundingBoxes && !showHeatmap && predictionResult?.detected_objects?.map((obj, idx) => (
                            <div
                              key={idx}
                              className="absolute border-2 border-emerald-400 bg-emerald-500/20 rounded-md transition-all pointer-events-none"
                              style={{
                                left: `${obj.box[0]}%`,
                                top: `${obj.box[1]}%`,
                                width: `${Math.max(5, obj.box[2] - obj.box[0])}%`,
                                height: `${Math.max(5, obj.box[3] - obj.box[1])}%`
                              }}
                            >
                              <span className="absolute -top-5 left-0 bg-emerald-600 text-white text-[9px] font-extrabold px-1.5 py-0.5 rounded shadow">
                                {obj.label} ({(obj.confidence * 100).toFixed(0)}%)
                              </span>
                            </div>
                          ))}
                        </div>

                        <div className="flex items-center justify-between text-xs text-slate-600 dark:text-slate-400 px-2">
                          <span className="truncate max-w-[180px] font-medium">{selectedFile.name}</span>
                          <span>{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</span>
                        </div>

                        {/* View Toggles (Grad-CAM & Bounding Boxes) */}
                        {predictionResult && (
                          <div className="grid grid-cols-2 gap-2 pt-1">
                            <button
                              type="button"
                              onClick={(e) => {
                                e.stopPropagation();
                                setShowHeatmap(!showHeatmap);
                              }}
                              className={`py-1.5 px-3 border rounded-xl text-xs font-bold flex items-center justify-center space-x-1.5 transition-all ${
                                showHeatmap
                                  ? 'bg-indigo-600 text-white border-indigo-600'
                                  : 'bg-indigo-50 dark:bg-indigo-950/80 border-indigo-200 dark:border-indigo-800 text-indigo-700 dark:text-indigo-300 hover:bg-indigo-100'
                              }`}
                            >
                              <Eye className="h-3.5 w-3.5" />
                              <span>{showHeatmap ? 'Grad-CAM On' : 'Show Grad-CAM'}</span>
                            </button>

                            <button
                              type="button"
                              onClick={(e) => {
                                e.stopPropagation();
                                setShowBoundingBoxes(!showBoundingBoxes);
                              }}
                              className={`py-1.5 px-3 border rounded-xl text-xs font-bold flex items-center justify-center space-x-1.5 transition-all ${
                                showBoundingBoxes
                                  ? 'bg-emerald-600 text-white border-emerald-600'
                                  : 'bg-emerald-50 dark:bg-emerald-950/80 border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-100'
                              }`}
                            >
                              <Crosshair className="h-3.5 w-3.5" />
                              <span>{showBoundingBoxes ? 'Detection Boxes On' : 'Show Detection Boxes'}</span>
                            </button>
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="space-y-3">
                        <div className="p-4 rounded-full bg-emerald-50 dark:bg-emerald-950/80 text-emerald-600 inline-block">
                          <ImageIcon className="h-8 w-8" />
                        </div>
                        <div>
                          <p className="text-xs font-bold text-slate-700 dark:text-slate-200">
                            Drag & Drop image here or <span className="text-emerald-600 underline">browse</span>
                          </p>
                          <p className="text-[11px] text-slate-400 mt-1">
                            Supported: JPG, JPEG, PNG, WEBP (Max 10MB)
                          </p>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Upload Error Banner */}
                  {uploadError && (
                    <div className="p-3 bg-rose-50 dark:bg-rose-950/60 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 rounded-xl text-xs flex items-center space-x-2">
                      <AlertCircle className="h-4 w-4 shrink-0" />
                      <span>{uploadError}</span>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex space-x-2">
                    {selectedFile && (
                      <button
                        type="button"
                        onClick={handleRemoveImage}
                        disabled={analyzing}
                        className="px-4 py-2.5 border border-slate-200 dark:border-slate-700 hover:bg-rose-50 hover:text-rose-600 hover:border-rose-200 dark:hover:bg-rose-950 rounded-xl text-xs font-bold transition-all flex items-center space-x-1"
                      >
                        <Trash2 className="h-4 w-4" />
                        <span>Remove</span>
                      </button>
                    )}
                    <button
                      type="button"
                      disabled={!selectedFile || analyzing}
                      onClick={handleAnalyzeImage}
                      className={`flex-1 py-2.5 text-white font-bold text-xs rounded-xl shadow-md transition-all flex items-center justify-center space-x-2 ${
                        !selectedFile || analyzing
                          ? 'bg-slate-400 cursor-not-allowed'
                          : 'bg-emerald-600 hover:bg-emerald-700 shadow-emerald-600/20'
                      }`}
                    >
                      {analyzing ? (
                        <>
                          <RefreshCw className="h-4 w-4 animate-spin" />
                          <span>Running 14-Phase Pipeline...</span>
                        </>
                      ) : (
                        <>
                          <Sparkles className="h-4 w-4" />
                          <span>Analyze Image with AI</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>


              </div>

              {/* Results Container (Right Side) */}
              <div className="lg:col-span-7 space-y-4">
                {analyzing ? (
                  <div className="p-8 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 flex flex-col items-center justify-center min-h-[460px] text-center space-y-4">
                    <div className="relative">
                      <div className="w-16 h-16 rounded-full border-4 border-emerald-200 border-t-emerald-600 animate-spin" />
                      <BrainCircuit className="h-8 w-8 text-emerald-600 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
                    </div>
                    <div>
                      <h4 className="text-base font-bold text-slate-900 dark:text-slate-100">
                        Analyzing Item with AI Decision Engine...
                      </h4>
                      <p className="text-xs text-slate-500 mt-1 max-w-md">
                        {analysisStep === 1 && 'Detecting item boundaries and object locations...'}
                        {analysisStep === 2 && 'Classifying material category and confidence levels...'}
                        {analysisStep === 3 && 'Evaluating visual condition, wear, and surface defects...'}
                        {analysisStep === 4 && 'Computing repairability, resale value, and circular recommendations...'}
                      </p>
                    </div>
                  </div>
                ) : predictionResult ? (
                  <div className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-6 shadow-md">
                    {/* Low Confidence Warning Safeguard */}
                    {predictionResult.is_low_confidence && (
                      <div className="p-4 bg-amber-50 dark:bg-amber-950/60 border-2 border-amber-400 dark:border-amber-700 text-amber-900 dark:text-amber-100 rounded-2xl text-xs flex items-center space-x-3 shadow-md">
                        <AlertTriangle className="h-6 w-6 text-amber-600 shrink-0" />
                        <div>
                          <p className="font-extrabold text-sm">Low Confidence Classification Warning</p>
                          <p className="text-xs font-semibold mt-0.5">
                            "{predictionResult.low_confidence_message || 'I am not sufficiently confident to classify this image.'}"
                          </p>
                        </div>
                      </div>
                    )}

                    {/* Header */}
                    <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4">
                      <div>
                        <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
                          Primary Classification Result
                        </span>
                        <h2 className="text-2xl font-extrabold font-heading text-slate-900 dark:text-slate-100 mt-0.5">
                          {predictionResult.predicted_category}
                        </h2>
                      </div>
                      <div className="text-right">
                        <span className={`px-3 py-1.5 rounded-full text-xs font-bold ${
                          predictionResult.is_low_confidence
                            ? 'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200'
                            : 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200'
                        }`}>
                          AI Confidence: {(predictionResult.confidence_score * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>

                    {/* Textual Explainable AI Feature Reasoning */}
                    {predictionResult.explanation_text && (
                      <div className="p-3 bg-indigo-50/80 dark:bg-indigo-950/50 rounded-xl border border-indigo-200 dark:border-indigo-800 text-xs text-indigo-900 dark:text-indigo-200 flex items-start space-x-2">
                        <Info className="h-4 w-4 text-indigo-600 shrink-0 mt-0.5" />
                        <div>
                          <span className="font-bold">Explainable AI Feature Reasoning: </span>
                          <span>{predictionResult.explanation_text}</span>
                        </div>
                      </div>
                    )}

                    {/* Top-5 Predictions Breakdown */}
                    <div className="bg-slate-50 dark:bg-slate-900/60 p-4 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-3">
                      <button
                        type="button"
                        onClick={() => setShowTop5(!showTop5)}
                        className="w-full flex items-center justify-between text-xs font-bold text-slate-700 dark:text-slate-200 hover:text-emerald-600"
                      >
                        <span className="flex items-center space-x-2">
                          <Layers className="h-4 w-4 text-emerald-600" />
                          <span>Category Predictions Breakdown</span>

                        </span>
                        {showTop5 ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                      </button>

                      {showTop5 && predictionResult.top_5_predictions?.length > 0 && (
                        <div className="space-y-2 pt-2 border-t border-slate-200 dark:border-slate-800">
                          {predictionResult.top_5_predictions
                            .filter((pred, idx) => idx === 0 || pred.confidence >= 0.05)
                            .map((pred, i) => (

                            <div key={i} className="space-y-1 text-xs">
                              <div className="flex justify-between font-semibold">
                                <span className={i === 0 ? 'text-emerald-600 dark:text-emerald-400 font-bold' : 'text-slate-600 dark:text-slate-400'}>
                                  {i + 1}. {pred.category}
                                </span>
                                <span>{(pred.confidence * 100).toFixed(1)}%</span>
                              </div>
                              <div className="w-full h-1.5 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                                <div
                                  className={`h-full rounded-full transition-all ${
                                    i === 0 ? 'bg-emerald-500' : 'bg-slate-400 dark:bg-slate-500'
                                  }`}
                                  style={{ width: `${Math.min(100, pred.confidence * 100)}%` }}
                                />
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* Key Metrics Grid */}
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                      {/* Metric 1: Condition */}
                      <div className="p-3 bg-slate-50 dark:bg-slate-900/80 rounded-xl border border-slate-200 dark:border-slate-800">
                        <span className="text-[10px] font-bold text-slate-400 uppercase">Visual Condition</span>
                        <p className={`text-sm font-bold mt-1 ${
                          predictionResult.condition === 'Unknown' ? 'text-amber-600' : 'text-slate-800 dark:text-slate-100'
                        }`}>
                          {predictionResult.condition}
                        </p>
                      </div>

                      {/* Metric 2: Repairability */}
                      <div className="p-3 bg-slate-50 dark:bg-slate-900/80 rounded-xl border border-slate-200 dark:border-slate-800">
                        <span className="text-[10px] font-bold text-slate-400 uppercase">Repairability</span>
                        <p className="text-sm font-bold text-indigo-600 dark:text-indigo-400 mt-1">
                          {predictionResult.repairability_rating} ({predictionResult.repairability_score}/100)
                        </p>
                      </div>

                      {/* Metric 3: Resale Value */}
                      <div className="p-3 bg-slate-50 dark:bg-slate-900/80 rounded-xl border border-slate-200 dark:border-slate-800">
                        <span className="text-[10px] font-bold text-slate-400 uppercase">Resale Value</span>
                        <p className="text-sm font-extrabold text-emerald-600 dark:text-emerald-400 mt-1">
                          {predictionResult.resale_value_display}
                        </p>
                      </div>

                      {/* Metric 4: Recycling Scrap Value */}
                      <div className="p-3 bg-slate-50 dark:bg-slate-900/80 rounded-xl border border-slate-200 dark:border-slate-800">
                        <span className="text-[10px] font-bold text-slate-400 uppercase">Scrap Value</span>
                        <p className="text-sm font-extrabold text-amber-600 dark:text-amber-400 mt-1">
                          {predictionResult.recycling_value_inr} ({predictionResult.recycling_value_usd})
                        </p>
                      </div>
                    </div>

                    {/* Detected Visual Defects */}
                    {predictionResult.visual_defects_detected?.length > 0 && (
                      <div className="p-3 bg-slate-50 dark:bg-slate-900/60 rounded-xl border border-slate-200 dark:border-slate-800 text-xs">
                        <span className="font-bold text-slate-600 dark:text-slate-300">Visual Defects Detected: </span>
                        <span className="text-slate-700 dark:text-slate-300">
                          {predictionResult.visual_defects_detected.join(' • ')}
                        </span>
                      </div>
                    )}

                    {/* Recommendation Card */}
                    <div className="p-4 bg-emerald-50 dark:bg-emerald-950/60 rounded-xl border border-emerald-200 dark:border-emerald-800 space-y-2">
                      <div className="flex items-center space-x-2">
                        <Sparkles className="h-5 w-5 text-emerald-600" />
                        <h4 className="font-bold text-slate-900 dark:text-slate-100 text-sm">
                          AI Circular Recommendation
                        </h4>
                      </div>
                      <p className="text-xs text-slate-700 dark:text-slate-200 font-medium">
                        {predictionResult.recommendation}
                      </p>

                      {predictionResult.co2_saved_kg > 0 && (
                        <div className="flex items-center space-x-4 pt-2 border-t border-emerald-200/60 dark:border-emerald-800/60 text-xs text-emerald-800 dark:text-emerald-200 font-semibold">
                          <span>🌱 CO2 Saved: {predictionResult.co2_saved_kg} kg</span>
                          <span>♻️ Waste Diverted: {predictionResult.waste_diverted_kg} kg</span>
                        </div>
                      )}
                    </div>



                    {/* Integration Actions */}
                    <div className="pt-2 flex flex-wrap gap-3 border-t border-slate-200 dark:border-slate-800">
                      <button
                        type="button"
                        onClick={handleSaveToInventory}
                        disabled={savingInventory || inventorySaved}
                        className={`flex-1 py-2.5 px-4 rounded-xl text-xs font-bold transition-all flex items-center justify-center space-x-2 shadow-sm ${
                          inventorySaved
                            ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-200 border border-emerald-300'
                            : 'bg-emerald-600 hover:bg-emerald-700 text-white'
                        }`}
                      >
                        {inventorySaved ? (
                          <>
                            <CheckCircle2 className="h-4 w-4" />
                            <span>Saved to Inventory!</span>
                          </>
                        ) : (
                          <>
                            <PlusCircle className="h-4 w-4" />
                            <span>{savingInventory ? 'Saving...' : 'Save to Inventory'}</span>
                          </>
                        )}
                      </button>

                      <button
                        type="button"
                        onClick={handleCreateListing}
                        className="flex-1 py-2.5 px-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold transition-all flex items-center justify-center space-x-2 shadow-sm"
                      >
                        <ArrowRight className="h-4 w-4" />
                        <span>Create Listing / Sell</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => navigate('/impact-passports')}
                        className="py-2.5 px-4 bg-teal-600 hover:bg-teal-700 text-white rounded-xl text-xs font-bold transition-all flex items-center justify-center space-x-2 shadow-sm"
                      >
                        <Award className="h-4 w-4" />
                        <span>Impact Passport</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => navigate('/pickup-partners')}
                        className="py-2.5 px-4 bg-purple-600 hover:bg-purple-700 text-white rounded-xl text-xs font-bold transition-all flex items-center justify-center space-x-2 shadow-sm"
                      >
                        <Building2 className="h-4 w-4" />
                        <span>Find Pickup Hubs</span>
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="p-8 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 flex flex-col items-center justify-center min-h-[460px] text-center space-y-3 text-slate-400">
                    <BrainCircuit className="h-12 w-12 text-slate-300 dark:text-slate-600" />
                    <p className="text-sm font-semibold text-slate-600 dark:text-slate-300">
                      No Image Analyzed Yet
                    </p>
                    <p className="text-xs max-w-sm">
                      Upload an item image on the left to instantly analyze category, visual condition, market resale value, and optimal circular pathways.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* TAB: MANUAL INPUT CLASSIFIER */}
        {activeTab === 'manual' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Input Form (Left Side) */}
            <div className="lg:col-span-5 p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4 shadow-sm">
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                <Sliders className="h-5 w-5 text-emerald-600" />
                <span>Manual Item Input Form</span>
              </h3>
              <p className="text-xs text-slate-500">
                Manually specify item attributes to run end-to-end circular economy AI decision calculations.
              </p>

              <form onSubmit={handleManualSubmit} className="space-y-4 text-xs">
                <div>
                  <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">Item Description / Name</label>
                  <input
                    type="text"
                    value={manualForm.item_name}
                    onChange={(e) => setManualForm({ ...manualForm, item_name: e.target.value })}
                    placeholder="e.g. Cardboard Box, Banana Peel, Coca-Cola Can"
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-semibold focus:ring-2 focus:ring-emerald-500"
                    required
                  />
                </div>

                <div>
                  <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">Material Category</label>
                  <select
                    value={manualForm.category}
                    onChange={(e) => setManualForm({ ...manualForm, category: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-semibold focus:ring-2 focus:ring-emerald-500"
                  >
                    {['Cardboard Box', 'Organic Waste', 'Glass Bottle', 'Aluminium Can', 'Paper Sheet', 'Plastic Bottle', 'Trash'].map((cat) => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>


                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">Visual Condition</label>
                    <select
                      value={manualForm.condition}
                      onChange={(e) => setManualForm({ ...manualForm, condition: e.target.value })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-semibold focus:ring-2 focus:ring-emerald-500"
                    >
                      {['Excellent', 'Good', 'Fair', 'Poor', 'Damaged'].map((cond) => (
                        <option key={cond} value={cond}>{cond}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">Weight (kg)</label>
                    <input
                      type="number"
                      step="0.1"
                      min="0.1"
                      value={manualForm.weight_kg}
                      onChange={(e) => setManualForm({ ...manualForm, weight_kg: parseFloat(e.target.value) || 0.1 })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-semibold focus:ring-2 focus:ring-emerald-500"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">Item Age (Years)</label>
                    <input
                      type="number"
                      step="0.5"
                      min="0"
                      value={manualForm.age_years}
                      onChange={(e) => setManualForm({ ...manualForm, age_years: parseFloat(e.target.value) || 0 })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-semibold focus:ring-2 focus:ring-emerald-500"
                    />
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">Original Price ($)</label>
                    <input
                      type="number"
                      step="1"
                      min="0"
                      value={manualForm.original_price}
                      onChange={(e) => setManualForm({ ...manualForm, original_price: parseFloat(e.target.value) || 0 })}
                      className="w-full px-3 py-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-semibold focus:ring-2 focus:ring-emerald-500"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={manualLoading}
                  className="w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl shadow-md transition-all flex items-center justify-center space-x-2"
                >
                  <BrainCircuit className="h-4 w-4" />
                  <span>{manualLoading ? 'Evaluating AI Engine...' : 'Run Manual AI Decision Pipeline'}</span>
                </button>
              </form>
            </div>

            {/* Results Display (Right Side) */}
            <div className="lg:col-span-7 space-y-4">
              {manualLoading ? (
                <div className="p-8 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 flex flex-col items-center justify-center min-h-[400px] text-center space-y-4">
                  <div className="w-12 h-12 rounded-full border-4 border-emerald-200 border-t-emerald-600 animate-spin" />
                  <p className="text-sm font-bold text-slate-700 dark:text-slate-200">Processing Manual Item Decision Pipeline...</p>
                </div>
              ) : manualResult ? (
                <div className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-6 shadow-md">
                  <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4">
                    <div>
                      <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
                        Manual Evaluation Output
                      </span>
                      <h2 className="text-2xl font-extrabold font-heading text-slate-900 dark:text-slate-100 mt-0.5">
                        {manualResult.predicted_category}
                      </h2>
                      <p className="text-xs text-slate-500 mt-0.5 font-semibold">Broad Taxonomy: {manualResult.broad_category}</p>
                    </div>
                    <div className="text-right">
                      <span className="px-3 py-1.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200">
                        AI Confidence: {(manualResult.confidence_score * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>

                  <div className="p-3 bg-indigo-50/80 dark:bg-indigo-950/50 rounded-xl border border-indigo-200 dark:border-indigo-800 text-xs text-indigo-900 dark:text-indigo-200 flex items-start space-x-2">
                    <Info className="h-4 w-4 text-indigo-600 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-bold">Feature Reasoning: </span>
                      <span>{manualResult.explanation_text}</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div className="p-3 bg-slate-50 dark:bg-slate-900/60 rounded-xl border border-slate-200 dark:border-slate-800">
                      <span className="text-[10px] font-bold text-slate-500 uppercase">Visual Condition</span>
                      <p className="text-sm font-bold text-slate-900 dark:text-slate-100 mt-0.5">{manualResult.condition}</p>
                    </div>

                    <div className="p-3 bg-slate-50 dark:bg-slate-900/60 rounded-xl border border-slate-200 dark:border-slate-800">
                      <span className="text-[10px] font-bold text-slate-500 uppercase">Repairability</span>
                      <p className="text-sm font-bold text-emerald-600 dark:text-emerald-400 mt-0.5">
                        {manualResult.repairability_rating} ({manualResult.repairability_score.toFixed(0)}/100)
                      </p>
                    </div>

                    <div className="p-3 bg-slate-50 dark:bg-slate-900/60 rounded-xl border border-slate-200 dark:border-slate-800">
                      <span className="text-[10px] font-bold text-slate-500 uppercase">Resale Value</span>
                      <p className="text-sm font-bold text-indigo-600 dark:text-indigo-400 mt-0.5">{manualResult.resale_value_display}</p>
                    </div>

                    <div className="p-3 bg-slate-50 dark:bg-slate-900/60 rounded-xl border border-slate-200 dark:border-slate-800">
                      <span className="text-[10px] font-bold text-slate-500 uppercase">Scrap Value</span>
                      <p className="text-sm font-bold text-amber-600 dark:text-amber-400 mt-0.5">
                        {manualResult.recycling_value_inr} ({manualResult.recycling_value_usd})
                      </p>
                    </div>
                  </div>

                  <div className="p-5 rounded-2xl bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/40 dark:to-teal-950/40 border border-emerald-200 dark:border-emerald-800/60 space-y-3">
                    <div className="flex items-center justify-between">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-900 dark:text-emerald-300 flex items-center space-x-2">
                        <Sparkles className="h-4 w-4 text-emerald-600" />
                        <span>AI Circular Recommendation</span>
                      </h4>
                      <span className="px-2.5 py-1 rounded-full text-xs font-extrabold bg-emerald-600 text-white">
                        {manualResult.recommendation.recommended_action}
                      </span>
                    </div>

                    <p className="text-xs text-emerald-900 dark:text-emerald-200 font-medium">
                      {manualResult.recommendation.action_reasoning}
                    </p>

                    <div className="flex items-center space-x-4 pt-2 border-t border-emerald-200/60 dark:border-emerald-800/60 text-xs text-emerald-800 dark:text-emerald-200 font-semibold">
                      <span>🌱 CO2 Saved: {manualResult.co2_saved_kg} kg</span>
                      <span>♻️ Waste Diverted: {manualResult.waste_diverted_kg} kg</span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="p-8 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 flex flex-col items-center justify-center min-h-[400px] text-center space-y-3 text-slate-400">
                  <Sliders className="h-12 w-12 text-slate-300 dark:text-slate-600" />
                  <p className="text-sm font-semibold text-slate-600 dark:text-slate-300">
                    No Manual Item Submitted Yet
                  </p>
                  <p className="text-xs max-w-sm">
                    Fill out the form on the left to evaluate custom item parameters in real time.
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB: Impact Passport Generator */}
        {activeTab === 'passport' && (
          <div className="p-6 rounded-3xl glass-card border border-slate-200 dark:border-slate-800 space-y-6 shadow-md">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4 gap-4">
              <div>
                <h3 className="text-xl font-bold font-heading text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                  <Award className="h-6 w-6 text-amber-500" />
                  <span>Digital AI Circular Impact Passport Generator</span>
                </h3>
                <p className="text-xs text-slate-500 mt-1">Generate a verified digital material certificate, QR token badge, and carbon impact report.</p>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setActiveTab('pipeline')}
                  className="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 rounded-xl font-bold text-xs transition-all flex items-center space-x-1.5"
                >
                  <ArrowLeft className="h-4 w-4" />
                  <span>Back to Classifier</span>
                </button>
                <button
                  onClick={() => setPassportOpen(true)}
                  className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs shadow-md transition-all flex items-center space-x-2"
                >
                  <Award className="h-4 w-4" />
                  <span>Open Full Passport Modal</span>
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="p-5 bg-gradient-to-br from-emerald-900 via-teal-900 to-indigo-950 text-white rounded-2xl space-y-4 shadow-xl">
                <span className="px-3 py-1 bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 rounded-full text-[10px] font-extrabold uppercase tracking-wider">
                  Live Passport Certificate Preview
                </span>
                <div className="space-y-1">
                  <h2 className="text-2xl font-extrabold font-heading text-white">
                    {predictionResult?.predicted_category || 'Cotton T-Shirt / Garment'}
                  </h2>
                  <p className="text-xs text-emerald-200">Category: {predictionResult?.predicted_category || 'Clothes'} • Condition: Good</p>
                </div>

                <div className="grid grid-cols-3 gap-2 pt-2 text-center text-xs">
                  <div className="p-2.5 bg-white/10 rounded-xl border border-white/10">
                    <span className="text-[9px] text-emerald-200 block">CO2 Saved</span>
                    <span className="font-extrabold text-emerald-300">2.5 kg</span>
                  </div>
                  <div className="p-2.5 bg-white/10 rounded-xl border border-white/10">
                    <span className="text-[9px] text-teal-200 block">Waste Diverted</span>
                    <span className="font-extrabold text-teal-300">1.2 kg</span>
                  </div>
                  <div className="p-2.5 bg-white/10 rounded-xl border border-white/10">
                    <span className="text-[9px] text-amber-200 block">Tree Equivalent</span>
                    <span className="font-extrabold text-amber-300">0.13 Trees</span>
                  </div>
                </div>

                <div className="pt-2 flex items-center justify-between border-t border-white/10">
                  <div>
                    <span className="text-[10px] text-slate-300 block">Estimated Market Resale</span>
                    <span className="text-lg font-extrabold text-emerald-300">
                      {predictionResult?.resale_value_display || '₹174 ($2.10)'}
                    </span>
                  </div>
                  <button
                    onClick={() => setPassportOpen(true)}
                    className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl text-xs font-bold shadow transition-all"
                  >
                    View QR Passport Card
                  </button>
                </div>
              </div>

              <div className="p-6 bg-slate-50 dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-4">
                <h4 className="font-bold text-sm text-slate-900 dark:text-slate-100">Why Use AI Circular Passports?</h4>
                <ul className="text-xs space-y-2.5 text-slate-600 dark:text-slate-400">
                  <li className="flex items-start space-x-2">
                    <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0 mt-0.5" />
                    <span><strong>Transparent Material Tracking:</strong> Verifies exact material category and visual condition history.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0 mt-0.5" />
                    <span><strong>Higher Resale Trust:</strong> Items with digital certificates sell up to 40% faster on circular marketplaces.</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0 mt-0.5" />
                    <span><strong>Auditable Impact:</strong> Track verified CO2 savings and waste diverted from landfills.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* TAB: NGO & Partner Finder */}
        {activeTab === 'partners' && (
          <div className="p-6 rounded-3xl glass-card border border-slate-200 dark:border-slate-800 space-y-6 shadow-md">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-4 gap-4">
              <div>
                <h3 className="text-xl font-bold font-heading text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                  <Building2 className="h-6 w-6 text-purple-600" />
                  <span>Smart Local NGO & Recycling Pickup Partner Finder</span>
                </h3>
                <p className="text-xs text-slate-500 mt-1">Locate verified municipal recycling hubs, NGO donation shelters, and e-waste pickup centers.</p>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setActiveTab('pipeline')}
                  className="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 rounded-xl font-bold text-xs transition-all flex items-center space-x-1.5"
                >
                  <ArrowLeft className="h-4 w-4" />
                  <span>Back to Classifier</span>
                </button>
                <button
                  onClick={() => setPartnerOpen(true)}
                  className="px-5 py-2.5 bg-purple-600 hover:bg-purple-700 text-white rounded-xl font-bold text-xs shadow-md transition-all flex items-center space-x-2"
                >
                  <Building2 className="h-4 w-4" />
                  <span>Open Full Partner Finder Modal</span>
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                { title: "Goonj Clothes Shelter NGO", category: "Clothes", rate: "Free Pick-up & Donation", phone: "+91 80 2668 0000", rating: "4.9 ★" },
                { title: "EcoRecycle E-Waste Hub", category: "Battery", rate: "Scrap Rate: ₹42 / kg", phone: "+91 80 6789 1234", rating: "4.9 ★" },
                { title: "Metals Scrap Recovery Corp", category: "Metal", rate: "Scrap Rate: ₹50 / kg", phone: "+91 80 2333 4455", rating: "4.8 ★" },
                { title: "Polymer Material Recovery Hub", category: "Plastic", rate: "Scrap Rate: ₹12 / kg", phone: "+91 80 5555 6677", rating: "4.8 ★" },
                { title: "GreenSole Footwear Upcycling", category: "Shoes", rate: "Sole Recovery & Upcycling", phone: "+91 99 2000 4567", rating: "4.9 ★" },
                { title: "Paper & Cardboard Mill Recycler", category: "Cardboard", rate: "Scrap Rate: ₹7 / kg", phone: "+91 80 3333 9988", rating: "4.7 ★" }
              ].map((p, i) => (
                <div key={i} className="p-4 bg-slate-50 dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="px-2 py-0.5 rounded-full font-bold bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-200">
                      {p.category}
                    </span>
                    <span className="font-bold text-amber-500">{p.rating}</span>
                  </div>
                  <h4 className="font-bold text-sm text-slate-900 dark:text-slate-100">{p.title}</h4>
                  <p className="text-xs text-emerald-600 font-semibold">{p.rate}</p>
                  <a
                    href={`tel:${p.phone}`}
                    className="w-full py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-xl text-xs font-bold flex items-center justify-center space-x-1.5 shadow-sm transition-all"
                  >
                    <span>Call {p.phone}</span>
                  </a>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 2: Sustainability Calculator */}

        {activeTab === 'sustainability' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <form onSubmit={handleSusSubmit} className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                <Leaf className="h-5 w-5 text-emerald-600" />
                <span>LCA Sustainability Calculator</span>
              </h3>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Category</label>
                  <select
                    value={susForm.category}
                    onChange={(e) => setSusForm({ ...susForm, category: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  >
                    {['Cardboard Box', 'Organic Waste', 'Glass Bottle', 'Aluminium Can', 'Paper Sheet', 'Plastic Bottle', 'Trash'].map((cat) => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>

                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Material</label>
                  <select
                    value={susForm.material}
                    onChange={(e) => setSusForm({ ...susForm, material: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  >
                    <option value="metal">Metal</option>
                    <option value="glass">Glass</option>
                    <option value="paper">Paper</option>
                    <option value="plastic">Plastic</option>
                    <option value="wood">Wood</option>
                    <option value="electronics">Electronics</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Condition</label>
                  <select
                    value={susForm.condition}
                    onChange={(e) => setSusForm({ ...susForm, condition: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  >
                    <option value="Excellent">Excellent</option>
                    <option value="Good">Good</option>
                    <option value="Fair">Fair</option>
                    <option value="Poor">Poor</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Weight (kg)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={susForm.weight_kg}
                    onChange={(e) => setSusForm({ ...susForm, weight_kg: parseFloat(e.target.value) || 0 })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Reuse Potential</label>
                  <select
                    value={susForm.reuse_potential}
                    onChange={(e) => setSusForm({ ...susForm, reuse_potential: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  >
                    <option value="High">High</option>
                    <option value="Moderate">Moderate</option>
                    <option value="Low">Low</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                disabled={susLoading}
                className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs shadow-md transition-all"
              >
                {susLoading ? 'Computing Score...' : 'Predict Sustainability Score'}
              </button>
            </form>

            <div className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4 flex flex-col justify-center">
              {susResult ? (
                <div className="space-y-4 text-center">
                  <div className="inline-flex items-center justify-center p-6 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border-4 border-emerald-500 shadow-inner">
                    <span className="text-4xl font-extrabold font-heading text-emerald-600 dark:text-emerald-400">
                      {susResult.sustainability_score}
                    </span>
                    <span className="text-xs font-bold text-slate-400">/100</span>
                  </div>
                  <div>
                    <span className="inline-block px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200">
                      {susResult.environmental_impact_category}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-300 max-w-sm mx-auto">
                    {susResult.recommendation}
                  </p>
                </div>
              ) : (
                <div className="text-center py-8 space-y-2 text-slate-400">
                  <Leaf className="h-10 w-10 mx-auto" />
                  <p className="text-xs">Submit item parameters to evaluate sustainability impact score.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 3: Market Price Regressor */}
        {activeTab === 'price' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <form onSubmit={handlePriceSubmit} className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                <DollarSign className="h-5 w-5 text-emerald-600" />
                <span>Market Price Regressor (XGBoost / Random Forest)</span>
              </h3>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Category</label>
                  <select
                    value={priceForm.category}
                    onChange={(e) => setPriceForm({ ...priceForm, category: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  >
                    {['Battery', 'Biological', 'Cardboard', 'Clothes', 'Glass', 'Metal', 'Paper', 'Plastic', 'Shoes', 'Trash'].map((cat) => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>

                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Brand</label>
                  <input
                    type="text"
                    value={priceForm.brand}
                    onChange={(e) => setPriceForm({ ...priceForm, brand: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Age (Years)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    value={priceForm.age_years}
                    onChange={(e) => setPriceForm({ ...priceForm, age_years: parseFloat(e.target.value) || 0 })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Condition</label>
                  <select
                    value={priceForm.condition}
                    onChange={(e) => setPriceForm({ ...priceForm, condition: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  >
                    <option value="Excellent">Excellent</option>
                    <option value="Good">Good</option>
                    <option value="Fair">Fair</option>
                    <option value="Poor">Poor</option>
                    <option value="Unknown">Unknown</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Original Price (₹)</label>
                  <input
                    type="number"
                    step="1"
                    min="0"
                    value={priceForm.original_price}
                    onChange={(e) => setPriceForm({ ...priceForm, original_price: parseFloat(e.target.value) || 0 })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={priceLoading}
                className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs shadow-md transition-all"
              >
                {priceLoading ? 'Predicting Price...' : 'Run Price Inference'}
              </button>
            </form>

            <div className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 flex flex-col justify-center">
              {priceResult ? (
                <div className="space-y-4">
                  <div className="p-4 bg-emerald-50 dark:bg-emerald-950/60 rounded-xl border border-emerald-200 dark:border-emerald-800 text-center">
                    <span className="text-xs font-bold text-slate-500 uppercase">Predicted Resale Price</span>
                    <h2 className="text-3xl font-extrabold font-heading text-emerald-600 dark:text-emerald-400 mt-1">
                      {priceResult.resale_value_display || formatCurrency(priceResult.predicted_resale_price)}
                    </h2>
                  </div>

                  <div className="p-4 bg-slate-100 dark:bg-slate-900 rounded-xl space-y-2 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-500">Scrap Recycling Value:</span>
                      <span className="font-bold text-amber-600">{priceResult.recycling_value_inr || '₹45'} ({priceResult.recycling_value_usd || '$0.50'})</span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8 space-y-2 text-slate-400">
                  <DollarSign className="h-10 w-10 mx-auto" />
                  <p className="text-xs">Run price inference to view estimated resale market value or non-resale scrap value.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 4: Visual Damage Classifier */}
        {activeTab === 'condition' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <form onSubmit={handleCondSubmit} className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                <ShieldCheck className="h-5 w-5 text-emerald-600" />
                <span>Empirical Visual Damage Classifier</span>
              </h3>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Age in Years</label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  value={condForm.age_years}
                  onChange={(e) => setCondForm({ ...condForm, age_years: parseFloat(e.target.value) || 0 })}
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Usage Level</label>
                <select
                  value={condForm.usage_level}
                  onChange={(e) => setCondForm({ ...condForm, usage_level: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                >
                  <option value="Heavy">Heavy Usage</option>
                  <option value="Moderate">Moderate Usage</option>
                  <option value="Light">Light Usage</option>
                  <option value="Mint">Unused / Mint</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={condLoading}
                className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs shadow-md transition-all"
              >
                {condLoading ? 'Classifying...' : 'Classify Condition'}
              </button>
            </form>

            <div className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 flex flex-col justify-center">
              {condResult ? (
                <div className="text-center space-y-3">
                  <span className="text-xs font-bold text-slate-400">Evaluated Condition</span>
                  <h2 className="text-3xl font-extrabold font-heading text-emerald-600 dark:text-emerald-400">
                    {condResult.predicted_condition}
                  </h2>
                  <span className="inline-block px-3 py-1 bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200 rounded-full text-xs font-bold">
                    Confidence: {(condResult.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              ) : (
                <div className="text-center py-8 space-y-2 text-slate-400">
                  <ShieldCheck className="h-10 w-10 mx-auto" />
                  <p className="text-xs">Classify condition rating based on visual damage evidence.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 5: Recommendation Engine */}
        {activeTab === 'recommendation' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <form onSubmit={handleRecSubmit} className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                <Sparkles className="h-5 w-5 text-emerald-600" />
                <span>Circular Engine Routing</span>
              </h3>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Category</label>
                  <select
                    value={recForm.category}
                    onChange={(e) => setRecForm({ ...recForm, category: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  >
                    {['Battery', 'Biological', 'Cardboard', 'Clothes', 'Glass', 'Metal', 'Paper', 'Plastic', 'Shoes', 'Trash'].map((cat) => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>

                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Condition</label>
                  <select
                    value={recForm.condition}
                    onChange={(e) => setRecForm({ ...recForm, condition: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs"
                  >
                    <option value="Excellent">Excellent</option>
                    <option value="Good">Good</option>
                    <option value="Fair">Fair</option>
                    <option value="Poor">Poor</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                disabled={recLoading}
                className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs shadow-md transition-all"
              >
                {recLoading ? 'Generating Recommendations...' : 'Generate Recommendations'}
              </button>
            </form>

            <div className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4">
              {recResult ? (
                <div className="space-y-4 text-xs">
                  <div className="p-3 bg-emerald-50 dark:bg-emerald-950/60 rounded-xl border border-emerald-200 dark:border-emerald-800">
                    <span className="text-slate-400 text-[10px] uppercase font-bold">Recommended Action</span>
                    <h3 className="text-lg font-bold text-emerald-600 dark:text-emerald-400 capitalize">{recResult.recommended_action}</h3>
                    <p className="text-slate-600 dark:text-slate-300 mt-1">{recResult.action_reasoning}</p>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8 space-y-2 text-slate-400">
                  <Sparkles className="h-10 w-10 mx-auto" />
                  <p className="text-xs">Generate circular recommendations for reuse, donation, or recycling.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 6: Model Metrics & Dataset Info */}
        {activeTab === 'metrics' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
                <span className="text-[10px] font-bold uppercase text-slate-400">Total Dataset Images</span>
                <h3 className="text-2xl font-extrabold text-emerald-600 dark:text-emerald-400 mt-1">14,423</h3>
              </div>
              <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
                <span className="text-[10px] font-bold uppercase text-slate-400">Taxonomy Classes</span>
                <h3 className="text-2xl font-extrabold text-indigo-600 dark:text-indigo-400 mt-1">10 Categories</h3>
              </div>
              <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
                <span className="text-[10px] font-bold uppercase text-slate-400">Training Split</span>
                <h3 className="text-2xl font-extrabold text-teal-600 dark:text-teal-400 mt-1">12,362 Images</h3>
              </div>
              <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800">
                <span className="text-[10px] font-bold uppercase text-slate-400">Test Evaluation Split</span>
                <h3 className="text-2xl font-extrabold text-amber-600 dark:text-amber-400 mt-1">2,061 Images</h3>
              </div>
            </div>

            <div className="p-6 rounded-2xl glass-card border border-slate-200 dark:border-slate-800 space-y-4">
              <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 flex items-center space-x-2">
                <BarChart3 className="h-5 w-5 text-emerald-600" />
                <span>Verified Dataset Class Distribution</span>
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400">
                Real multi-class circular waste and item corpus breakdown across 10 categories (14,423 real photographs).
              </p>

              <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-2">
                {[
                  { name: 'Glass', count: '2,237' },
                  { name: 'Plastic', count: '2,079' },
                  { name: 'Paper', count: '1,930' },
                  { name: 'Clothes', count: '1,892' },
                  { name: 'Cardboard', count: '1,814' },
                  { name: 'Shoes', count: '1,449' },
                  { name: 'Metal', count: '930' },
                  { name: 'Battery', count: '756' },
                  { name: 'Biological', count: '699' },
                  { name: 'Trash', count: '637' }
                ].map((item, i) => (
                  <div key={i} className="p-3 bg-slate-100 dark:bg-slate-900 rounded-xl text-center">
                    <span className="text-[10px] font-bold text-slate-400 uppercase">{item.name}</span>
                    <p className="text-sm font-bold text-slate-800 dark:text-slate-100 mt-0.5">{item.count} imgs</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      <ImpactPassportModal
        open={passportOpen}
        onClose={() => setPassportOpen(false)}
        itemData={predictionResult}
      />

      <PartnerFinderModal
        open={partnerOpen}
        onClose={() => setPartnerOpen(false)}
        defaultCategory={predictionResult?.predicted_category || 'Clothes'}
      />
    </DashboardLayout>
  );
};
