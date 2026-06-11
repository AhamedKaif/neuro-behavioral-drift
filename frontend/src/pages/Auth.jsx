import React, { useState } from 'react';
import axios from 'axios';

export default function Auth({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError('Please fill in all fields.');
      return;
    }
    setError('');
    setLoading(true);

    const url = isLogin ? '/api/auth/login' : '/api/auth/register';
    try {
      const response = await axios.post(url, { username, password });
      const { token, user } = response.data;
      
      // Save details to localStorage
      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(user));
      
      onLoginSuccess(token, user);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.error || 
        'An error occurred. Please check if backend is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[85vh] items-center justify-center px-4">
      {/* Background Glow */}
      <div className="absolute top-1/4 left-1/2 -z-10 h-72 w-72 -translate-x-1/2 rounded-full bg-accentBlue/10 blur-[100px] animate-pulse-slow"></div>
      
      <div className="w-full max-w-md rounded-2xl glass-panel p-8 shadow-2xl transition-all duration-300 hover:border-slate-800">
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

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-3 text-slate-200 outline-none transition-colors placeholder:text-slate-600 focus:border-accentBlue focus:bg-slate-900/80"
              placeholder="Enter username"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-xl bg-slate-900/50 border border-slate-700/60 px-4 py-3 text-slate-200 outline-none transition-colors placeholder:text-slate-600 focus:border-accentBlue focus:bg-slate-900/80"
              placeholder="Enter password"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-accentBlue py-3.5 font-semibold text-white shadow-lg shadow-accentBlue/20 transition-all duration-200 hover:bg-blue-600 hover:shadow-blue-500/30 active:scale-[0.98] disabled:opacity-50"
          >
            {loading ? 'Processing...' : isLogin ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        <div className="mt-6 text-center text-sm">
          <span className="text-slate-400">
            {isLogin ? "Don't have an account?" : "Already have an account?"}
          </span>{' '}
          <button
            onClick={() => {
              setIsLogin(!isLogin);
              setError('');
            }}
            className="font-medium text-accentBlue hover:underline"
          >
            {isLogin ? 'Register now' : 'Log in'}
          </button>
        </div>
      </div>
    </div>
  );
}
