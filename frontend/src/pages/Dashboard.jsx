import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';
import { 
  Brain, AlertTriangle, Play, RefreshCw, LogOut, CheckCircle, ShieldAlert, Clock, Keyboard, MousePointer, AppWindow
} from 'lucide-react';

const DEFAULT_BASELINE = {
  screen_time: 180.0,
  typing_speed: 250.0,
  typing_error_rate: 0.03,
  session_duration: 30.0,
  click_frequency: 30.0,
  break_frequency: 2.0,
  mouse_speed: 450.0
};

export default function Dashboard({ token, user, onLogout }) {
  // Application Data States
  const [dashboardData, setDashboardData] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Real-time tracking states
  const [isTracking, setIsTracking] = useState(true);
  const [typedChars, setTypedChars] = useState(0);
  const [backspaceCount, setBackspaceCount] = useState(0);
  const [clickCount, setClickCount] = useState(0);
  const [mouseDistance, setMouseDistance] = useState(0);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [sandboxText, setSandboxText] = useState('');
  
  // Computed live metrics
  const [liveCpm, setLiveCpm] = useState(250);
  const [liveErrorRate, setLiveErrorRate] = useState(0.02);
  const [liveMouseSpeed, setLiveMouseSpeed] = useState(400);
  const [liveClicks, setLiveClicks] = useState(20);
  const [sessionMinutes, setSessionMinutes] = useState(15.0);
  const [breaksPerHour, setBreaksPerHour] = useState(2.0);
  const [screenTimeMinutes, setScreenTimeMinutes] = useState(120.0);
  
  // Simulation and Action States
  const [isFatigueSimulated, setIsFatigueSimulated] = useState(false);
  const [submittingMetrics, setSubmittingMetrics] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [retrainingModel, setRetrainingModel] = useState(false);
  
  // Tracking references
  const lastMousePos = useRef({ x: 0, y: 0 });
  const timerRef = useRef(null);
  const activeTimeRef = useRef(null);

  // Axios config
  const api = axios.create({
    headers: { Authorization: `Bearer ${token}` }
  });

  // Fetch Dashboard Stats and Alerts
  const fetchDashboardData = async () => {
    try {
      setError('');
      const [dashRes, alertRes] = await Promise.all([
        api.get('/api/dashboard'),
        api.get('/api/alerts')
      ]);
      setDashboardData(dashRes.data);
      setAlerts(alertRes.data);
      
      // Update screen time / session durations from database latest values if present
      if (dashRes.data.latest_metrics) {
        setScreenTimeMinutes(dashRes.data.latest_metrics.screen_time);
        setSessionMinutes(dashRes.data.latest_metrics.session_duration);
      }
    } catch (err) {
      console.error(err);
      setError('Could not load dashboard data from backend APIs.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    
    // Live tracking timers
    activeTimeRef.current = setInterval(() => {
      if (isTracking) {
        setElapsedSeconds(prev => prev + 1);
        // Slowly increment screen time and session duration for realism
        setScreenTimeMinutes(prev => prev + (1 / 60));
        setSessionMinutes(prev => prev + (1 / 60));
      }
    }, 1000);

    return () => {
      clearInterval(activeTimeRef.current);
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isTracking]);

  // Recalculate Live Metrics when raw tracker values update
  useEffect(() => {
    if (elapsedSeconds > 2) {
      const minutes = elapsedSeconds / 60;
      // Calculate CPM (limit bounds for clean displays)
      const computedCpm = minutes > 0 ? Math.round(typedChars / minutes) : 250;
      setLiveCpm(Math.min(450, Math.max(50, computedCpm)));
      
      // Calculate backspace error rate
      const totalKeystrokes = typedChars + backspaceCount;
      const rate = totalKeystrokes > 0 ? (backspaceCount / totalKeystrokes) : 0.02;
      setLiveErrorRate(Math.min(0.40, rate));
      
      // Mouse speed (px/sec)
      const speed = Math.round(mouseDistance / elapsedSeconds);
      setLiveMouseSpeed(Math.min(1000, Math.max(10, speed)));
      
      // Click frequency (clicks per min)
      const clicksPerMin = Math.round(clickCount / minutes);
      setLiveClicks(Math.min(120, clicksPerMin));
    }
  }, [typedChars, backspaceCount, mouseDistance, clickCount, elapsedSeconds]);

  // Track Mouse Movements over the sandbox panel
  const handleMouseMove = (e) => {
    if (!isTracking) return;
    const { clientX, clientY } = e;
    if (lastMousePos.current.x !== 0) {
      const dx = clientX - lastMousePos.current.x;
      const dy = clientY - lastMousePos.current.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      setMouseDistance(prev => prev + dist);
    }
    lastMousePos.current = { x: clientX, y: clientY };
  };

  // Keyboard character typing tracker
  const handleTextAreaChange = (e) => {
    if (!isTracking) return;
    const val = e.target.value;
    setSandboxText(val);
    setTypedChars(prev => prev + 1);
  };

  // Track Backspaces separately
  const handleKeyDown = (e) => {
    if (!isTracking) return;
    if (e.key === 'Backspace' || e.key === 'Delete') {
      setBackspaceCount(prev => prev + 1);
    }
  };

  // Click tracker
  const handleSandboxClick = () => {
    if (!isTracking) return;
    setClickCount(prev => prev + 1);
  };

  // Reset Sandbox Trackers
  const resetTrackers = () => {
    setTypedChars(0);
    setBackspaceCount(0);
    setClickCount(0);
    setMouseDistance(0);
    setElapsedSeconds(0);
    setSandboxText('');
    lastMousePos.current = { x: 0, y: 0 };
  };

  // Submit Current Metrics (Simulated or Live tracked)
  const submitMetrics = async () => {
    setSubmittingMetrics(true);
    setSubmitSuccess(false);
    
    // Package metrics: if simulation checked, send heavy drift values
    const payload = isFatigueSimulated ? {
      screen_time: screenTimeMinutes + 240, // push it high
      typing_speed: 90.0,       // sluggish typing
      typing_error_rate: 0.22,  // high error/backspaces
      session_duration: sessionMinutes + 120, // long duration
      click_frequency: 7.0,     // low click activity
      break_frequency: 0.2,     // lack of breaks
      mouse_speed: 85.0         // slow mouse speed
    } : {
      screen_time: Math.round(screenTimeMinutes),
      typing_speed: liveCpm,
      typing_error_rate: parseFloat(liveErrorRate.toFixed(4)),
      session_duration: Math.round(sessionMinutes),
      click_frequency: liveClicks,
      break_frequency: breaksPerHour,
      mouse_speed: liveMouseSpeed
    };

    try {
      await api.post('/api/metrics', payload);
      setSubmitSuccess(true);
      setTimeout(() => setSubmitSuccess(false), 3000);
      fetchDashboardData(); // reload charts/predictions
      resetTrackers();
    } catch (err) {
      console.error(err);
      setError('Metrics transmission failed.');
    } finally {
      setSubmittingMetrics(false);
    }
  };

  // Clear Alerts
  const clearAlerts = async () => {
    try {
      await api.post('/api/alerts/read');
      fetchDashboardData();
    } catch (err) {
      console.error(err);
    }
  };

  // Force model retrain
  const retrainModel = async () => {
    setRetrainingModel(true);
    try {
      await api.post('/api/model/retrain');
      alert('Model successfully retrained with user baseline!');
      fetchDashboardData();
    } catch (err) {
      console.error(err);
      alert('Retraining failed.');
    } finally {
      setRetrainingModel(false);
    }
  };

  // Render variables
  const latestPred = dashboardData?.latest_prediction;
  const currentStrain = latestPred?.strain_label || 'Low';
  const currentDrift = latestPred?.drift_score || 0.0;
  const confidence = latestPred?.strain_probability ? Math.round(latestPred.strain_probability * 100) : 100;
  
  // Custom Gauge styling
  const getDriftColor = (score) => {
    if (score < 30) return 'text-strainLow border-strainLow/30';
    if (score < 65) return 'text-strainMedium border-strainMedium/30';
    return 'text-strainHigh border-strainHigh/30';
  };

  const getStrainColor = (level) => {
    if (level === 'Low') return 'bg-strainLow/10 border-strainLow/20 text-strainLow shadow-strainLow/10';
    if (level === 'Medium') return 'bg-strainMedium/10 border-strainMedium/20 text-strainMedium shadow-strainMedium/10';
    return 'bg-strainHigh/10 border-strainHigh/20 text-strainHigh shadow-strainHigh/10';
  };

  // Prepare Radar Data comparison
  const getRadarData = () => {
    if (!dashboardData) return [];
    const baseline = dashboardData.baseline;
    const latest = dashboardData.latest_metrics || DEFAULT_BASELINE;

    // Features mapped to relative scale (0-100)
    return [
      { subject: 'Typing Speed', baseline: 100, current: Math.round((latest.typing_speed / baseline.typing_speed) * 100) },
      { subject: 'Focus (1/Err)', baseline: 100, current: Math.round((baseline.typing_error_rate / Math.max(0.005, latest.typing_error_rate)) * 100) },
      { subject: 'Stamina (1/Dur)', baseline: 100, current: Math.round((baseline.session_duration / Math.max(1, latest.session_duration)) * 100) },
      { subject: 'Click Rate', baseline: 100, current: Math.round((latest.click_frequency / baseline.click_frequency) * 100) },
      { subject: 'Rest (Breaks)', baseline: 100, current: Math.round((latest.break_frequency / baseline.break_frequency) * 100) },
      { subject: 'Precision (Mouse)', baseline: 100, current: Math.round((latest.mouse_speed / baseline.mouse_speed) * 100) }
    ];
  };

  if (loading) {
    return (
      <div className="flex h-[80vh] items-center justify-center">
        <div className="text-center">
          <RefreshCw className="mx-auto h-12 w-12 text-accentBlue animate-spin mb-4" />
          <h3 className="text-lg font-medium text-slate-300">Synchronizing neural models...</h3>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-6 space-y-6">
      
      {/* 1. Dashboard Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 animate-ping"></span>
            <p className="text-sm font-semibold tracking-wider text-accentBlue uppercase">
              Operational Live State
            </p>
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight mt-1">
            Cognitive Diagnostics Workspace
          </h1>
          <p className="text-slate-400 text-sm mt-0.5">
            Subject ID: <span className="font-semibold text-slate-300">{user.username}</span> | Monitoring cognitive loads.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={retrainModel}
            disabled={retrainingModel}
            className="inline-flex items-center gap-2 rounded-xl bg-slate-900 border border-slate-700/60 px-4 py-2.5 text-sm font-medium text-slate-300 hover:text-white transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`h-4 w-4 ${retrainingModel ? 'animate-spin' : ''}`} />
            Retrain Model
          </button>
          
          <button
            onClick={onLogout}
            className="inline-flex items-center gap-2 rounded-xl bg-red-950/20 border border-red-900/30 px-4 py-2.5 text-sm font-medium text-red-400 hover:bg-red-900/10 hover:text-red-300 transition-all"
          >
            <LogOut className="h-4 w-4" />
            Disconnect
          </button>
        </div>
      </div>

      {error && (
        <div className="rounded-xl bg-red-500/10 border border-red-500/20 p-4 text-sm text-red-400">
          {error}
        </div>
      )}

      {/* 2. Top Metrics Widget Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        
        {/* Metric 1: Cognitive Strain Status */}
        <div className="rounded-2xl glass-panel p-5 relative overflow-hidden flex flex-col justify-between min-h-[140px]">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Cognitive Strain</span>
            <div className="flex items-baseline gap-2 mt-2">
              <span className={`inline-flex items-center gap-1.5 px-3 py-1 text-sm font-bold rounded-lg border ${getStrainColor(currentStrain)}`}>
                <span className={`h-2 w-2 rounded-full ${currentStrain === 'Low' ? 'bg-strainLow' : currentStrain === 'Medium' ? 'bg-strainMedium' : 'bg-strainHigh'} animate-pulse`}></span>
                {currentStrain}
              </span>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-2">
            ML classifier confidence: <span className="font-semibold text-slate-200">{confidence}%</span>
          </p>
        </div>

        {/* Metric 2: Drift Score Gauge */}
        <div className="rounded-2xl glass-panel p-5 relative overflow-hidden flex flex-col justify-between min-h-[140px]">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Behavioral Drift Score</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-3xl font-extrabold text-white">
                {currentDrift}%
              </span>
              <span className={`text-xs px-2 py-0.5 rounded border font-semibold ${getDriftColor(currentDrift)}`}>
                {currentDrift < 30 ? 'Normal' : currentDrift < 65 ? 'Warning' : 'Critical'}
              </span>
            </div>
          </div>
          <div className="w-full bg-slate-800 h-1.5 rounded-full mt-2">
            <div 
              className={`h-full rounded-full transition-all duration-500 ${currentDrift < 30 ? 'bg-strainLow' : currentDrift < 65 ? 'bg-strainMedium' : 'bg-strainHigh'}`} 
              style={{ width: `${currentDrift}%` }}
            ></div>
          </div>
        </div>

        {/* Metric 3: Daily Screen Time */}
        <div className="rounded-2xl glass-panel p-5 relative overflow-hidden flex flex-col justify-between min-h-[140px]">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Daily Screen Time</span>
            <div className="flex items-baseline gap-1 mt-2">
              <span className="text-3xl font-extrabold text-white">
                {Math.round(screenTimeMinutes)}
              </span>
              <span className="text-sm font-medium text-slate-400">min</span>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-2">
            Avg target: &lt; 480 min/day
          </p>
        </div>

        {/* Metric 4: Active Session Duration */}
        <div className="rounded-2xl glass-panel p-5 relative overflow-hidden flex flex-col justify-between min-h-[140px]">
          <div>
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Active Session</span>
            <div className="flex items-baseline gap-1 mt-2">
              <span className="text-3xl font-extrabold text-white">
                {Math.round(sessionMinutes)}
              </span>
              <span className="text-sm font-medium text-slate-400">min</span>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-2">
            Break recommended in <span className="font-semibold text-slate-200">{Math.max(0, 90 - Math.round(sessionMinutes))} min</span>
          </p>
        </div>

      </div>

      {/* 3. Middle Section: Live Sandbox & Simulation Panel & Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Interactive Metrics Sandbox Panel */}
        <div className="lg:col-span-2 rounded-2xl glass-panel p-6 flex flex-col gap-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <div className="p-1.5 rounded-lg bg-accentBlue/10 text-accentBlue">
                <Brain className="h-5 w-5" />
              </div>
              <h2 className="text-lg font-bold text-white">Interactive Behavioral Sandbox</h2>
            </div>
            
            <div className="flex items-center gap-2">
              <button 
                onClick={() => setIsTracking(!isTracking)}
                className={`text-xs px-3 py-1.5 rounded-lg font-semibold border ${isTracking ? 'bg-accentBlue/10 border-accentBlue/30 text-accentBlue' : 'bg-slate-900 border-slate-800 text-slate-400'}`}
              >
                {isTracking ? 'Tracking Live' : 'Paused'}
              </button>
              <button 
                onClick={resetTrackers}
                className="p-1.5 rounded-lg border border-slate-800 text-slate-400 hover:text-white"
                title="Reset trackers"
              >
                <RefreshCw className="h-4 w-4" />
              </button>
            </div>
          </div>

          <p className="text-xs text-slate-400 leading-relaxed">
            Move your cursor inside this sandbox, click, and type text to simulate work. The frontend dynamically measures keyboard velocity (CPM), delete ratios, mouse velocities, and click rates.
          </p>

          {/* Core Sandbox Interactive Area */}
          <div 
            onMouseMove={handleMouseMove}
            onClick={handleSandboxClick}
            className="relative border border-slate-800 bg-slate-950/40 rounded-xl p-4 focus-within:border-accentBlue/50 transition-colors cursor-crosshair min-h-[140px] flex flex-col"
          >
            <textarea
              value={sandboxText}
              onChange={handleTextAreaChange}
              onKeyDown={handleKeyDown}
              disabled={!isTracking}
              placeholder="Start typing text here... The system will record your inputs and calculate typing metrics dynamically. Use Backspaces to simulate error corrections."
              className="w-full flex-grow bg-transparent text-slate-100 text-sm outline-none resize-none placeholder:text-slate-700"
            ></textarea>
            
            {/* Live Sandbox Counters HUD */}
            <div className="flex flex-wrap gap-4 mt-3 pt-3 border-t border-slate-900 text-[11px] text-slate-400 uppercase tracking-wide">
              <div className="flex items-center gap-1">
                <Keyboard className="h-3 w-3 text-accentBlue" />
                <span>Chars: <span className="text-slate-200 font-bold">{typedChars}</span></span>
              </div>
              <div className="flex items-center gap-1">
                <AlertTriangle className="h-3 w-3 text-red-500" />
                <span>Backspaces: <span className="text-slate-200 font-bold">{backspaceCount}</span></span>
              </div>
              <div className="flex items-center gap-1">
                <MousePointer className="h-3 w-3 text-emerald-500" />
                <span>Clicks: <span className="text-slate-200 font-bold">{clickCount}</span></span>
              </div>
              <div className="flex items-center gap-1">
                <Clock className="h-3 w-3 text-amber-500" />
                <span>Active Seconds: <span className="text-slate-200 font-bold">{elapsedSeconds}s</span></span>
              </div>
            </div>
          </div>

          {/* Simulated HUD gauges */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-900/30 p-3.5 rounded-xl border border-slate-900">
            <div className="text-center">
              <div className="text-xs text-slate-500">Typing CPM</div>
              <div className="text-lg font-bold text-slate-200 mt-0.5">{liveCpm}</div>
            </div>
            <div className="text-center border-l border-slate-800">
              <div className="text-xs text-slate-500">Error Rate</div>
              <div className="text-lg font-bold text-slate-200 mt-0.5">{(liveErrorRate * 100).toFixed(1)}%</div>
            </div>
            <div className="text-center border-l border-slate-800">
              <div className="text-xs text-slate-500">Mouse Speed</div>
              <div className="text-lg font-bold text-slate-200 mt-0.5">{liveMouseSpeed} <span className="text-[10px] text-slate-500">px/s</span></div>
            </div>
            <div className="text-center border-l border-slate-800">
              <div className="text-xs text-slate-500">Click Rate</div>
              <div className="text-lg font-bold text-slate-200 mt-0.5">{liveClicks} <span className="text-[10px] text-slate-500">/m</span></div>
            </div>
          </div>

          {/* Action Trigger Panels */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mt-2">
            {/* Fatigue Simulator Toggle */}
            <label className="flex items-center gap-3 cursor-pointer group bg-slate-950/30 border border-slate-800/80 px-4 py-2.5 rounded-xl select-none w-full sm:w-auto">
              <input 
                type="checkbox"
                checked={isFatigueSimulated}
                onChange={(e) => setIsFatigueSimulated(e.target.checked)}
                className="h-4.5 w-4.5 text-accentBlue bg-slate-900 border-slate-700 rounded focus:ring-accentBlue cursor-pointer"
              />
              <div>
                <span className="text-xs font-bold text-slate-300 group-hover:text-white transition-colors flex items-center gap-1.5">
                  <ShieldAlert className={`h-4.5 w-4.5 ${isFatigueSimulated ? 'text-strainHigh animate-bounce' : 'text-slate-500'}`} />
                  Force Cognitive Fatigue Simulation
                </span>
                <p className="text-[10px] text-slate-500 mt-0.5">Injects degraded behavioral patterns to test high-strain warnings.</p>
              </div>
            </label>

            <button
              onClick={submitMetrics}
              disabled={submittingMetrics}
              className={`inline-flex items-center justify-center gap-2 rounded-xl px-5 py-3 font-semibold text-sm transition-all active:scale-[0.98] w-full sm:w-auto ${
                submitSuccess 
                  ? 'bg-emerald-500 text-white shadow-emerald-500/10' 
                  : 'bg-accentBlue text-white hover:bg-blue-600 shadow-lg shadow-accentBlue/10'
              }`}
            >
              {submittingMetrics ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" /> Ingesting...
                </>
              ) : submitSuccess ? (
                <>
                  <CheckCircle className="h-4 w-4" /> Ingested Successfully!
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" /> Transmit Metrics to Model
                </>
              )}
            </button>
          </div>

        </div>

        {/* Live System Alerts Panel */}
        <div className="rounded-2xl glass-panel p-6 flex flex-col gap-4 max-h-[480px]">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <div className="p-1.5 rounded-lg bg-strainHigh/10 text-strainHigh">
                <AlertTriangle className="h-5 w-5" />
              </div>
              <h2 className="text-lg font-bold text-white">Recommendations</h2>
            </div>
            
            {alerts.length > 0 && (
              <button 
                onClick={clearAlerts}
                className="text-xs text-slate-500 hover:text-slate-300 font-semibold"
              >
                Clear All
              </button>
            )}
          </div>

          <div className="flex-grow overflow-y-auto pr-1 space-y-3.5">
            {alerts.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center py-12">
                <CheckCircle className="h-10 w-10 text-emerald-500/30 mb-3" />
                <h4 className="text-sm font-semibold text-slate-400">Behavioral Baseline Stable</h4>
                <p className="text-xs text-slate-600 mt-1">No deviations or strain warnings generated. Keep maintaining regular pacing.</p>
              </div>
            ) : (
              alerts.map((alert) => (
                <div 
                  key={alert.id}
                  className={`rounded-xl border p-3.5 space-y-1 bg-slate-900/50 ${
                    alert.alert_type === 'HIGH_STRAIN' 
                      ? 'border-red-500/20 hover:border-red-500/40 text-red-400' 
                      : alert.alert_type === 'LONG_SESSION'
                      ? 'border-amber-500/20 hover:border-amber-500/40 text-amber-400'
                      : 'border-blue-500/20 hover:border-blue-500/40 text-blue-400'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase tracking-wider bg-slate-950 px-2 py-0.5 rounded">
                      {alert.alert_type.replace('_', ' ')}
                    </span>
                    <span className="text-[9px] text-slate-500">
                      {new Date(alert.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed mt-1">{alert.message}</p>
                </div>
              ))
            )}
          </div>
        </div>

      </div>

      {/* 4. Bottom Section: Recharts Visualizations */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Graph 1: Line Chart (Weekly Drift Trend) */}
        <div className="md:col-span-2 rounded-2xl glass-panel p-5">
          <h3 className="text-sm font-bold text-slate-300 mb-4 uppercase tracking-wider flex items-center gap-1.5">
            <AppWindow className="h-4 w-4 text-accentBlue" />
            Behavioral Drift & Cognitive Load History
          </h3>
          
          <div className="h-[280px]">
            {dashboardData?.timeseries && dashboardData.timeseries.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={dashboardData.timeseries} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="time_label" stroke="#64748b" tick={{ fontSize: 10 }} />
                  <YAxis domain={[0, 100]} stroke="#64748b" tick={{ fontSize: 10 }} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#151c2c', borderColor: '#222f47', borderRadius: '12px' }}
                    labelStyle={{ color: '#94a3b8', fontSize: '11px', fontWeight: 'bold' }}
                    itemStyle={{ fontSize: '12px' }}
                  />
                  <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                  <Line 
                    name="Drift Score (%)" 
                    type="monotone" 
                    dataKey="drift_score" 
                    stroke="#3b82f6" 
                    strokeWidth={2.5} 
                    activeDot={{ r: 6 }} 
                  />
                  <Line 
                    name="Error Rate (x100)" 
                    type="monotone" 
                    dataKey="typing_error_rate" 
                    stroke="#ef4444" 
                    strokeWidth={1.5}
                    // Scale up error rate to fit on percentage scale
                    data={dashboardData.timeseries.map(d => ({ ...d, typing_error_rate: Math.min(100, Math.round(d.typing_error_rate * 400)) }))} 
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-slate-600 text-xs">
                Log metrics to visualize longitudinal drift patterns.
              </div>
            )}
          </div>
        </div>

        {/* Graph 2: Radar Comparison Profile */}
        <div className="rounded-2xl glass-panel p-5">
          <h3 className="text-sm font-bold text-slate-300 mb-4 uppercase tracking-wider flex items-center gap-1.5">
            <Brain className="h-4 w-4 text-emerald-500" />
            Active vs Baseline Profile
          </h3>
          
          <div className="h-[280px]">
            {dashboardData ? (
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" r="75%" data={getRadarData()}>
                  <PolarGrid stroke="#1e293b" />
                  <PolarAngleAxis dataKey="subject" stroke="#94a3b8" tick={{ fontSize: 9 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 150]} stroke="#475569" tick={{ fontSize: 8 }} />
                  <Radar name="Baseline (Healthy)" dataKey="baseline" stroke="#10b981" fill="#10b981" fillOpacity={0.1} />
                  <Radar name="Current Session" dataKey="current" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.25} />
                  <Legend wrapperStyle={{ fontSize: '10px', paddingTop: '5px' }} />
                </RadarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-slate-600 text-xs">
                Insufficient baseline calibration.
              </div>
            )}
          </div>
        </div>

      </div>

    </div>
  );
}
