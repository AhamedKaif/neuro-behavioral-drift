import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { User, Briefcase, Brain, Activity, Clock, LogOut, Save, Settings, AlertTriangle } from 'lucide-react';

export default function Profile({ token, onLogout }) {
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({});
  const [saveStatus, setSaveStatus] = useState('');

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await axios.get('/api/profile', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setProfileData(res.data);
        setEditForm({
          full_name: res.data.account.full_name || '',
          ...res.data.profile
        });
      } catch (err) {
        setError('Failed to load profile data.');
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [token]);

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSaveProfile = async () => {
    setSaveStatus('Saving...');
    try {
      await axios.put('/api/profile', editForm, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSaveStatus('Saved successfully!');
      
      // Update local state
      setProfileData(prev => ({
        ...prev,
        account: { ...prev.account, full_name: editForm.full_name },
        profile: { ...editForm, full_name: undefined }
      }));
      
      setTimeout(() => {
        setIsEditing(false);
        setSaveStatus('');
      }, 1500);
    } catch (err) {
      const errMsg = err.response && err.response.data && err.response.data.error 
        ? err.response.data.error 
        : 'Failed to save.';
      setSaveStatus(errMsg);
    }
  };

  const handleDeleteAccount = async () => {
    try {
      await axios.delete('/api/profile/account', {
        headers: { Authorization: `Bearer ${token}` }
      });
      onLogout(); // Disconnect and navigate away
    } catch (err) {
      setError('Failed to delete account.');
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64 text-slate-400">Loading Profile...</div>;
  }
  if (error) {
    return <div className="text-red-400 p-8 text-center">{error}</div>;
  }

  const { account, profile, analytics } = profileData;

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
          <User className="h-8 w-8 text-accentBlue" /> 
          Profile Management
        </h1>
        <div className="flex gap-3">
          {!isEditing ? (
            <button 
              onClick={() => setIsEditing(true)} 
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg flex items-center gap-2 transition-colors border border-slate-700"
            >
              <Settings className="h-4 w-4" /> Edit Profile
            </button>
          ) : (
            <div className="flex gap-3 items-center">
              <span className="text-sm text-green-400">{saveStatus}</span>
              <button 
                onClick={() => setIsEditing(false)} 
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={handleSaveProfile} 
                className="px-4 py-2 bg-accentBlue hover:bg-blue-600 text-white rounded-lg flex items-center gap-2 transition-colors"
              >
                <Save className="h-4 w-4" /> Save Changes
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column */}
        <div className="space-y-6 lg:col-span-1">
          {/* Account Summary Card */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800">
            <div className="flex items-center gap-4 mb-6">
              <div className="h-16 w-16 rounded-full bg-slate-800 border-2 border-accentBlue/30 flex items-center justify-center text-2xl font-bold text-white">
                {account.full_name ? account.full_name.charAt(0).toUpperCase() : 'U'}
              </div>
              <div>
                {isEditing ? (
                  <input 
                    type="text" name="full_name" value={editForm.full_name} onChange={handleEditChange}
                    className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-white mb-1"
                  />
                ) : (
                  <h2 className="text-xl font-bold text-white">{account.full_name}</h2>
                )}
                <p className="text-sm text-slate-400">@{account.username}</p>
              </div>
            </div>
            
            <div className="space-y-3 text-sm border-t border-slate-800 pt-4">
              <div className="flex justify-between">
                <span className="text-slate-500">Email</span>
                <span className="text-slate-300 font-medium">{account.email}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Member Since</span>
                <span className="text-slate-300 font-medium">{new Date(account.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          </div>

          {/* Analytics Summary Card */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-900/50">
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400 mb-4 flex items-center gap-2">
              <Activity className="h-4 w-4" /> Analytics Summary
            </h3>
            
            {analytics.drift_score !== null ? (
              <div className="space-y-4">
                <div>
                  <p className="text-slate-500 text-xs mb-1">Current Cognitive Strain</p>
                  <p className={`text-xl font-bold ${
                    analytics.strain_label === 'High' ? 'text-red-400' : 
                    analytics.strain_label === 'Medium' ? 'text-amber-400' : 'text-green-400'
                  }`}>
                    {analytics.strain_label}
                  </p>
                </div>
                <div>
                  <p className="text-slate-500 text-xs mb-1">Behavioral Drift Score</p>
                  <p className="text-lg font-bold text-white">{analytics.drift_score.toFixed(1)} / 100</p>
                </div>
                <div>
                  <p className="text-slate-500 text-xs mb-1">Last Analysis</p>
                  <p className="text-sm text-slate-300">{new Date(analytics.last_prediction).toLocaleString()}</p>
                </div>
              </div>
            ) : (
              <div className="text-slate-500 text-sm italic py-4">No prediction data available yet. Please complete a diagnostic session.</div>
            )}
          </div>
          
          {/* Danger Zone */}
          <div className="glass-panel p-6 rounded-2xl border border-red-900/30">
            <h3 className="text-sm font-semibold uppercase tracking-wider text-red-500 mb-4 flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" /> Danger Zone
            </h3>
            {showDeleteConfirm ? (
              <div className="space-y-3">
                <p className="text-xs text-slate-400">This action cannot be undone. All data will be permanently deleted.</p>
                <div className="flex gap-2">
                  <button onClick={handleDeleteAccount} className="flex-1 bg-red-600 hover:bg-red-700 text-white text-xs py-2 rounded transition-colors">Confirm Delete</button>
                  <button onClick={() => setShowDeleteConfirm(false)} className="flex-1 bg-slate-800 text-white text-xs py-2 rounded">Cancel</button>
                </div>
              </div>
            ) : (
              <button 
                onClick={() => setShowDeleteConfirm(true)}
                className="w-full flex items-center justify-center gap-2 text-sm text-red-400 border border-red-900/50 hover:bg-red-950/30 py-2 rounded-lg transition-colors"
              >
                Delete Account
              </button>
            )}
          </div>
        </div>

        {/* Right Column - Profile Details */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Personal Info */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800">
            <h3 className="text-lg font-semibold text-white mb-4 border-b border-slate-800 pb-3">Personal Details</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <DetailField label="Age" name="age" value={profile.age} isEditing={isEditing} editForm={editForm} onChange={handleEditChange} type="number" />
              <DetailField label="Gender" name="gender" value={profile.gender} isEditing={isEditing} editForm={editForm} onChange={handleEditChange} type="select" options={['Male', 'Female', 'Non-binary', 'Prefer not to say']} />
              <DetailField label="Occupation" name="occupation" value={profile.occupation} isEditing={isEditing} editForm={editForm} onChange={handleEditChange} type="select" options={['Student', 'Professional', 'Other']} />
            </div>
          </div>

          {/* Academic/Work Info */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800">
            <h3 className="text-lg font-semibold text-white mb-4 border-b border-slate-800 pb-3 flex items-center gap-2">
              <Briefcase className="h-5 w-5 text-accentBlue" /> Academic & Work Profile
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <DetailField label="Institution / Company" name="institution" value={profile.institution} isEditing={isEditing} editForm={editForm} onChange={handleEditChange} />
              <DetailField label="Department" name="department" value={profile.department} isEditing={isEditing} editForm={editForm} onChange={handleEditChange} />
              <DetailField label="Academic Year" name="academic_year" value={profile.academic_year} isEditing={isEditing} editForm={editForm} onChange={handleEditChange} />
              <DetailField label="Working Hours / Day" name="working_hours" value={profile.working_hours} isEditing={isEditing} editForm={editForm} onChange={handleEditChange} type="number" />
            </div>
          </div>

          {/* Behavioral Baseline */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800">
            <h3 className="text-lg font-semibold text-white mb-4 border-b border-slate-800 pb-3 flex items-center gap-2">
              <Brain className="h-5 w-5 text-accentBlue" /> Behavioral Baseline
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <DetailField label="Avg Screen Time (hrs)" name="avg_screen_time" value={profile.avg_screen_time} isEditing={isEditing} editForm={editForm} onChange={handleEditChange} type="number" />
              <DetailField label="Avg Sleep Hours" name="avg_sleep_hours" value={profile.avg_sleep_hours} isEditing={isEditing} editForm={editForm} onChange={handleEditChange} type="number" />
              <DetailField label="Preferred Work Time" name="preferred_work_time" value={profile.preferred_work_time} isEditing={isEditing} editForm={editForm} onChange={handleEditChange} type="select" options={['Morning', 'Afternoon', 'Evening', 'Night']} />
              
              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-500 mb-2">Baseline Stress Level (1-10)</label>
                {isEditing ? (
                  <div className="flex items-center gap-4">
                    <input type="range" min="1" max="10" name="stress_level" value={editForm.stress_level || 5} onChange={handleEditChange} className="w-full accent-accentBlue" />
                    <span className="text-white font-bold">{editForm.stress_level}</span>
                  </div>
                ) : (
                  <div className="w-full bg-slate-800 rounded-full h-2.5 mt-2">
                    <div className={`h-2.5 rounded-full ${profile.stress_level > 7 ? 'bg-red-500' : profile.stress_level > 4 ? 'bg-amber-500' : 'bg-green-500'}`} style={{ width: `${(profile.stress_level / 10) * 100}%` }}></div>
                    <div className="mt-1 text-right text-xs text-slate-400">{profile.stress_level} / 10</div>
                  </div>
                )}
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

// Helper component for rendering fields
function DetailField({ label, name, value, isEditing, editForm, onChange, type = "text", options = [] }) {
  return (
    <div>
      <label className="block text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">{label}</label>
      {isEditing ? (
        type === 'select' ? (
          <select name={name} value={editForm[name] || ''} onChange={onChange} className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:border-accentBlue outline-none">
            {options.map(opt => <option key={opt} value={opt}>{opt}</option>)}
          </select>
        ) : (
          <input type={type} name={name} value={editForm[name] || ''} onChange={onChange} className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:border-accentBlue outline-none" />
        )
      ) : (
        <p className="text-slate-200 font-medium text-sm bg-slate-900/30 px-3 py-2 rounded border border-transparent">{value || '-'}</p>
      )}
    </div>
  );
}
