import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

export default function Auth({ onLoginSuccess, initialMode = 'login' }) {
  const [isLogin, setIsLogin] = useState(initialMode === 'login');
  const navigate = useNavigate();

  // Login State
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  
  // Registration State
  const [formData, setFormData] = useState({
    full_name: '', username: '', email: '', password: '', confirmPassword: '',
    age: '', gender: 'Prefer not to say', occupation: 'Student',
    institution: '', department: '', academic_year: '', working_hours: '',
    avg_screen_time: '', avg_sleep_hours: '', preferred_work_time: 'Morning',
    stress_level: 5, privacy_consent: false
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    if (!loginUsername || !loginPassword) {
      setError('Please fill in all fields.');
      return;
    }
    setError('');
    setLoading(true);

    try {
      const response = await axios.post('/api/auth/login', { username: loginUsername, password: loginPassword });
      const { token, user } = response.data;
      // Persist token & user, update parent state, then navigate to dashboard.
      onLoginSuccess(token, user);
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    
    // Validation
    if (!formData.full_name || !formData.username || !formData.email || !formData.password || !formData.confirmPassword) {
      setError('Please fill in all required personal information.');
      return;
    }
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters strong.');
      return;
    }
    if (!formData.privacy_consent) {
      setError('You must accept the privacy policy to register.');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const submitData = { ...formData };
      delete submitData.confirmPassword;
      delete submitData.privacy_consent;

      const response = await axios.post('/api/auth/register', submitData);
      const { token, user } = response.data;
      // Persist token & user, update parent state, then navigate directly to dashboard.
      // This skips the login page entirely — sign-up = auto-login.
      onLoginSuccess(token, user);
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="flex min-h-[85vh] items-center justify-center px-4 py-8">
      <div className="absolute top-1/4 left-1/2 -z-10 h-72 w-72 -translate-x-1/2 rounded-full bg-accentBlue/10 blur-[100px] animate-pulse-slow"></div>
      
      <div className={`w-full ${isLogin ? 'max-w-md' : 'max-w-4xl'} rounded-2xl glass-panel p-8 shadow-2xl transition-all duration-300`}>
        <div className="mb-8 text-center">
          <div className="inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-accentBlue/10 text-3xl text-accentBlue mb-3">
            🧠
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-white">
            Neuro-Behavioral Drift
          </h2>
          <p className="mt-1 text-sm text-slate-400">
            Cognitive Strain Detection Platform
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-xl bg-red-500/10 border border-red-500/20 p-3 text-sm text-red-400 text-center">
            {error}
          </div>
        )}

        {isLogin ? (
          <form onSubmit={handleLoginSubmit} className="space-y-5">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Username</label>
              <input type="text" value={loginUsername} onChange={(e) => setLoginUsername(e.target.value)} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-3 text-slate-200 outline-none focus:border-accentBlue" placeholder="Enter username" />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Password</label>
              <input type="password" value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-3 text-slate-200 outline-none focus:border-accentBlue" placeholder="Enter password" />
            </div>
            <button type="submit" disabled={loading} className="w-full rounded-xl bg-accentBlue py-3.5 font-semibold text-white transition-all hover:bg-blue-600 active:scale-[0.98] disabled:opacity-50">
              {loading ? 'Processing...' : 'Sign In'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleRegisterSubmit} className="space-y-8">
            {/* 1. Personal Information */}
            <div>
              <h3 className="text-lg font-semibold text-white border-b border-slate-700 pb-2 mb-4">Personal Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Full Name *</label>
                  <input type="text" name="full_name" value={formData.full_name} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="John Doe" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Username *</label>
                  <input type="text" name="username" value={formData.username} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="johndoe123" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Email Address *</label>
                  <input type="email" name="email" value={formData.email} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="john@example.com" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Age</label>
                  <input type="number" name="age" value={formData.age} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="25" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Password *</label>
                  <input type="password" name="password" value={formData.password} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="Minimum 8 characters" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Confirm Password *</label>
                  <input type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="Confirm password" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Gender</label>
                  <select name="gender" value={formData.gender} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue">
                    <option>Male</option>
                    <option>Female</option>
                    <option>Non-binary</option>
                    <option>Prefer not to say</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Occupation</label>
                  <select name="occupation" value={formData.occupation} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue">
                    <option>Student</option>
                    <option>Professional</option>
                    <option>Other</option>
                  </select>
                </div>
              </div>
            </div>

            {/* 2. Academic / Work Information */}
            <div>
              <h3 className="text-lg font-semibold text-white border-b border-slate-700 pb-2 mb-4">Academic / Work Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Institution / Company</label>
                  <input type="text" name="institution" value={formData.institution} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="University / Company Name" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Department / Field of Study</label>
                  <input type="text" name="department" value={formData.department} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="e.g. Computer Science" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Academic Year</label>
                  <input type="text" name="academic_year" value={formData.academic_year} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="e.g. Sophomore (if student)" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Working Hours Per Day</label>
                  <input type="number" step="0.5" name="working_hours" value={formData.working_hours} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="e.g. 8" />
                </div>
              </div>
            </div>

            {/* 3. Behavioral Baseline Information */}
            <div>
              <h3 className="text-lg font-semibold text-white border-b border-slate-700 pb-2 mb-4">Behavioral Baseline Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Average Daily Screen Time (hours)</label>
                  <input type="number" step="0.5" name="avg_screen_time" value={formData.avg_screen_time} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="e.g. 6.5" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Average Sleep Hours</label>
                  <input type="number" step="0.5" name="avg_sleep_hours" value={formData.avg_sleep_hours} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue" placeholder="e.g. 7.5" />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Preferred Work/Study Time</label>
                  <select name="preferred_work_time" value={formData.preferred_work_time} onChange={handleInputChange} className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-accentBlue">
                    <option>Morning</option>
                    <option>Afternoon</option>
                    <option>Evening</option>
                    <option>Night</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Stress Level (1-10): {formData.stress_level}</label>
                  <input type="range" min="1" max="10" name="stress_level" value={formData.stress_level} onChange={handleInputChange} className="w-full accent-accentBlue mt-2" />
                </div>
              </div>
            </div>

            {/* Privacy & Consent */}
            <div className="bg-slate-900/50 p-4 rounded-xl border border-slate-700/60">
              <label className="flex items-start gap-3 cursor-pointer">
                <input type="checkbox" name="privacy_consent" checked={formData.privacy_consent} onChange={handleInputChange} className="mt-1 h-4 w-4 rounded border-slate-700 text-accentBlue focus:ring-accentBlue" />
                <span className="text-sm text-slate-300">
                  I consent to the collection and processing of my behavioral data for the purpose of cognitive strain modeling. I understand that this data will be stored securely and will not be shared with third parties without explicit permission.
                </span>
              </label>
            </div>

            <button type="submit" disabled={loading} className="w-full rounded-xl bg-accentBlue py-3.5 font-semibold text-white transition-all hover:bg-blue-600 active:scale-[0.98] disabled:opacity-50">
              {loading ? 'Processing...' : 'Complete Registration'}
            </button>
          </form>
        )}

        <div className="mt-6 text-center text-sm border-t border-slate-800 pt-6">
          <span className="text-slate-400">
            {isLogin ? "Don't have an account?" : "Already have an account?"}
          </span>{' '}
          {isLogin ? (
            <Link
              to="/register"
              className="font-medium text-accentBlue hover:underline ml-1"
            >
              Register now
            </Link>
          ) : (
            <Link
              to="/login"
              className="font-medium text-accentBlue hover:underline ml-1"
            >
              Log in
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
