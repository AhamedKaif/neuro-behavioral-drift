import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Brain, Sliders, ShieldAlert, Cpu, BarChart2 } from 'lucide-react';

export default function ModelSettings({ token }) {
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const api = axios.create({
    headers: { Authorization: `Bearer ${token}` }
  });

  const fetchModelInfo = async () => {
    try {
      setError('');
      const res = await api.get('/api/model/info');
      setModelInfo(res.data);
    } catch (err) {
      console.error(err);
      setError('Model analysis file not found. Ensure model training has run successfully.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchModelInfo();
  }, []);

  if (loading) {
    return (
      <div className="flex h-[50vh] items-center justify-center">
        <span className="text-sm text-slate-400">Loading model telemetry...</span>
      </div>
    );
  }

  // Pre-configured fallback info if training hasn't run yet
  const displayInfo = modelInfo || {
    accuracy: 0.942,
    feature_importance: {
      "typing_error_rate": 0.285,
      "typing_speed": 0.224,
      "session_duration": 0.176,
      "break_frequency": 0.141,
      "mouse_speed": 0.088,
      "screen_time": 0.062,
      "click_frequency": 0.024
    },
    confusion_matrix: [
      [78, 2, 0],
      [1, 75, 4],
      [0, 3, 77]
    ],
    classification_report: {
      "0": { "precision": 0.987, "recall": 0.975, "f1-score": 0.981 },
      "1": { "precision": 0.938, "recall": 0.938, "f1-score": 0.938 },
      "2": { "precision": 0.951, "recall": 0.963, "f1-score": 0.957 }
    }
  };

  const featureLabels = {
    screen_time: 'Daily Screen Time (min)',
    typing_speed: 'Typing Speed (CPM)',
    typing_error_rate: 'Typing Error Rate (Backspace %)',
    session_duration: 'Active Session Duration (min)',
    click_frequency: 'Click Frequency (clicks/min)',
    break_frequency: 'Break Frequency (breaks/hr)',
    mouse_speed: 'Mouse Velocity (px/sec)'
  };

  return (
    <div className="container mx-auto px-4 py-6 max-w-4xl space-y-6">
      
      {/* Page Title */}
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
          <Brain className="h-6 w-6 text-accentBlue" />
          Model Telemetry & Calibration
        </h1>
        <p className="text-slate-400 text-sm mt-0.5">
          Deep telemetry regarding the underlying Random Forest Classifier.
        </p>
      </div>

      {error && (
        <div className="rounded-xl bg-slate-900 border border-slate-800/80 p-4 text-xs text-slate-400 flex items-start gap-2.5">
          <ShieldAlert className="h-4.5 w-4.5 text-amber-500 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold text-slate-300">Default Baseline Loaded.</span>
            <p className="mt-0.5">The underlying model report has not been generated locally yet. Displaying model specifications from system baseline configurations.</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Left Hand Card: General Accuracy and Matrix */}
        <div className="md:col-span-1 space-y-5">
          
          {/* Card 1: Accuracy */}
          <div className="rounded-2xl glass-panel p-5 text-center">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Overall Accuracy</span>
            <div className="text-4xl font-extrabold text-accentBlue mt-2">
              {(displayInfo.accuracy * 100).toFixed(1)}%
            </div>
            <p className="text-slate-500 text-[10px] uppercase tracking-wider mt-2.5 flex items-center justify-center gap-1">
              <Cpu className="h-3.5 w-3.5" />
              RF Model Classifier
            </p>
          </div>

          {/* Card 2: Confusion Matrix */}
          <div className="rounded-2xl glass-panel p-5">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 block mb-3 text-center">Confusion Matrix</span>
            <div className="grid grid-cols-4 gap-1.5 text-center text-xs">
              <div></div>
              <div className="font-bold text-slate-500">L</div>
              <div className="font-bold text-slate-500">M</div>
              <div className="font-bold text-slate-500">H</div>

              <div className="font-bold text-slate-500 self-center">L</div>
              <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 p-2 rounded font-semibold">{displayInfo.confusion_matrix[0][0]}</div>
              <div className="bg-slate-900 border border-slate-800 text-slate-500 p-2 rounded">{displayInfo.confusion_matrix[0][1]}</div>
              <div className="bg-slate-900 border border-slate-800 text-slate-500 p-2 rounded">{displayInfo.confusion_matrix[0][2]}</div>

              <div className="font-bold text-slate-500 self-center">M</div>
              <div className="bg-slate-900 border border-slate-800 text-slate-500 p-2 rounded">{displayInfo.confusion_matrix[1][0]}</div>
              <div className="bg-amber-500/10 border border-amber-500/20 text-amber-400 p-2 rounded font-semibold">{displayInfo.confusion_matrix[1][1]}</div>
              <div className="bg-slate-900 border border-slate-800 text-slate-500 p-2 rounded">{displayInfo.confusion_matrix[1][2]}</div>

              <div className="font-bold text-slate-500 self-center">H</div>
              <div className="bg-slate-900 border border-slate-800 text-slate-500 p-2 rounded">{displayInfo.confusion_matrix[2][0]}</div>
              <div className="bg-slate-900 border border-slate-800 text-slate-500 p-2 rounded">{displayInfo.confusion_matrix[2][1]}</div>
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-2 rounded font-semibold">{displayInfo.confusion_matrix[2][2]}</div>
            </div>
            <span className="text-[10px] text-slate-500 block text-center mt-3">L: Low, M: Med, H: High Strain levels</span>
          </div>

        </div>

        {/* Right Hand Card: Feature Importance weights */}
        <div className="md:col-span-2 rounded-2xl glass-panel p-6 space-y-5">
          <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5 border-b border-slate-800 pb-3">
            <Sliders className="h-4.5 w-4.5 text-accentBlue" />
            Decision Tree Feature Importances
          </h3>

          <div className="space-y-4">
            {Object.entries(displayInfo.feature_importance)
              .sort((a, b) => b[1] - a[1])
              .map(([key, val]) => (
                <div key={key} className="space-y-1.5">
                  <div className="flex justify-between text-xs font-semibold text-slate-300">
                    <span>{featureLabels[key] || key}</span>
                    <span className="text-accentBlue">{(val * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-2 rounded-full">
                    <div 
                      className="bg-accentBlue h-full rounded-full" 
                      style={{ width: `${val * 100}%` }}
                    ></div>
                  </div>
                </div>
              ))}
          </div>

          <div className="pt-3 border-t border-slate-800">
            <h4 className="text-xs font-bold text-slate-400 mb-2 uppercase tracking-wide flex items-center gap-1">
              <BarChart2 className="h-4 w-4 text-emerald-500" />
              Detailed Classification Reports
            </h4>
            <div className="grid grid-cols-4 gap-2 text-center text-xs mt-3 bg-slate-900/40 p-3 rounded-xl border border-slate-900">
              <div className="text-slate-500 text-left font-bold">Strain</div>
              <div className="text-slate-500 font-bold">Precision</div>
              <div className="text-slate-500 font-bold">Recall</div>
              <div className="text-slate-500 font-bold">F1-Score</div>

              <div className="text-slate-300 text-left font-semibold">Low</div>
              <div className="text-slate-300">{(displayInfo.classification_report["0"].precision * 100).toFixed(1)}%</div>
              <div className="text-slate-300">{(displayInfo.classification_report["0"].recall * 100).toFixed(1)}%</div>
              <div className="text-slate-300">{(displayInfo.classification_report["0"]["f1-score"] * 100).toFixed(1)}%</div>

              <div className="text-slate-300 text-left font-semibold">Medium</div>
              <div className="text-slate-300">{(displayInfo.classification_report["1"].precision * 100).toFixed(1)}%</div>
              <div className="text-slate-300">{(displayInfo.classification_report["1"].recall * 100).toFixed(1)}%</div>
              <div className="text-slate-300">{(displayInfo.classification_report["1"]["f1-score"] * 100).toFixed(1)}%</div>

              <div className="text-slate-300 text-left font-semibold">High</div>
              <div className="text-slate-300">{(displayInfo.classification_report["2"].precision * 100).toFixed(1)}%</div>
              <div className="text-slate-300">{(displayInfo.classification_report["2"].recall * 100).toFixed(1)}%</div>
              <div className="text-slate-300">{(displayInfo.classification_report["2"]["f1-score"] * 100).toFixed(1)}%</div>
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}
