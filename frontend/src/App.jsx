import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import Auth from './pages/Auth';
import Dashboard from './pages/Dashboard';
import ModelSettings from './pages/ModelSettings';
import Profile from './pages/Profile';
import NotificationsPage from './pages/Notifications';
import { Brain, LayoutDashboard, Database, User, Settings, Bell } from 'lucide-react';
import axios from 'axios';
import { notificationsAPI } from './services/api';
import { registerServiceWorker, requestNotificationPermission } from './utils/pushNotifications';

export default function App() {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [checkingAuth, setCheckingAuth] = useState(true);
  const [unreadCount, setUnreadCount] = useState(0);

  // Run ONCE on mount — restore session from localStorage and validate token with backend.
  // We do NOT re-run this when token changes (no [token] dependency) because
  // handleLoginSuccess already sets both token and user directly from the API response,
  // so there is no need for a second round-trip validation after login/register.
  useEffect(() => {
    registerServiceWorker();

    const restoreSession = async () => {
      const storedToken = localStorage.getItem('token');
      const storedUser = (() => {
        try { return JSON.parse(localStorage.getItem('user')); }
        catch { return null; }
      })();

      if (storedToken) {
        // Optimistically restore from localStorage so the UI is instant on reload.
        setToken(storedToken);
        setUser(storedUser);

        try {
          // Silently re-validate the token with the backend.
          const res = await axios.get('/api/auth/me', {
            headers: { Authorization: `Bearer ${storedToken}` }
          });
          // Update user with fresh data from server.
          setUser(res.data);
          localStorage.setItem('user', JSON.stringify(res.data));
        } catch (err) {
          console.error('Stored token is invalid, clearing session:', err);
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          setToken(null);
          setUser(null);
        }
      }

      setCheckingAuth(false);
    };

    restoreSession();
  }, []); // ← empty deps: run once on mount only

  // Fetch unread notification count whenever the user is authenticated.
  useEffect(() => {
    if (!token) return;
    const fetchCount = async () => {
      try {
        const res = await notificationsAPI.unreadCount();
        setUnreadCount(res.data.unread_count);
      } catch (e) {}
    };
    fetchCount();
    const interval = setInterval(fetchCount, 30000);
    return () => clearInterval(interval);
  }, [token]);

  /**
   * Called immediately after a successful login OR registration API response.
   * The token and user come directly from the API response body — no extra
   * round-trip is needed, so navigation to /dashboard happens instantly.
   */
  const handleLoginSuccess = (newToken, newUser) => {
    // Persist to localStorage first so protected routes don't flash /login.
    localStorage.setItem('token', newToken);
    localStorage.setItem('user', JSON.stringify(newUser));
    // Update React state — the router will now render Dashboard.
    setToken(newToken);
    setUser(newUser);
    setTimeout(() => requestNotificationPermission(), 1000);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
  };

  if (checkingAuth) {
    return (
      <div className="flex h-screen items-center justify-center bg-darkBg text-slate-100">
        <div className="text-center">
          <Brain className="mx-auto h-12 w-12 text-accentBlue animate-bounce mb-4" />
          <h3 className="text-lg font-medium text-slate-300">Calibrating diagnostics interface...</h3>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-darkBg text-slate-100 flex flex-col justify-between">
        
        {/* Navigation Bar */}
        {token && user && (
          <header className="border-b border-slate-800 bg-darkCard/80 backdrop-blur-md sticky top-0 z-50 px-4 py-3">
            <div className="container mx-auto flex items-center justify-between">
              
              <Link to="/dashboard" className="flex items-center gap-2.5 group select-none">
                <div className="h-9 w-9 rounded-xl bg-accentBlue/10 text-accentBlue flex items-center justify-center font-bold text-xl group-hover:scale-105 transition-transform">
                  🧠
                </div>
                <div>
                  <span className="font-extrabold text-sm text-white block tracking-wide">NEURO-DRIFT</span>
                  <span className="text-[10px] text-slate-400 block -mt-1 uppercase font-semibold">Cognitive Strain Monitor</span>
                </div>
              </Link>

              <nav className="flex items-center gap-6">
                <Link 
                  to="/dashboard" 
                  className="flex items-center gap-1.5 text-sm font-semibold text-slate-400 hover:text-white transition-colors"
                >
                  <LayoutDashboard className="h-4 w-4" />
                  Dashboard
                </Link>

                <Link 
                  to="/model-telemetry" 
                  className="flex items-center gap-1.5 text-sm font-semibold text-slate-400 hover:text-white transition-colors"
                >
                  <Database className="h-4 w-4" />
                  Model Telemetry
                </Link>
              </nav>

              <div className="flex items-center gap-4">
                <Link to="/notifications" className="relative text-slate-400 hover:text-white transition-colors">
                  <Bell className="h-5 w-5" />
                  {unreadCount > 0 && (
                    <span className="absolute -top-1.5 -right-1.5 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[9px] font-bold text-white border-2 border-darkCard">
                      {unreadCount}
                    </span>
                  )}
                </Link>

                <Link to="/profile" className="flex items-center gap-2 bg-slate-900 border border-slate-800/80 rounded-xl px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white hover:border-slate-700 transition-colors">
                  <User className="h-3.5 w-3.5 text-accentBlue" />
                  <span>{user.full_name || user.username}</span>
                </Link>
              </div>

            </div>
          </header>
        )}

        {/* Main Content Area */}
        <main className="flex-grow w-full">
          <Routes>
            {/* Auth routes — redirect to dashboard if already authenticated */}
            <Route
              path="/login"
              element={token && user ? <Navigate to="/dashboard" replace /> : <Auth key="login" onLoginSuccess={handleLoginSuccess} initialMode="login" />}
            />
            <Route
              path="/register"
              element={token && user ? <Navigate to="/dashboard" replace /> : <Auth key="register" onLoginSuccess={handleLoginSuccess} initialMode="register" />}
            />

            {/* Protected routes — redirect to login if not authenticated */}
            <Route
              path="/dashboard"
              element={token && user ? <Dashboard token={token} user={user} onLogout={handleLogout} /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/model-telemetry"
              element={token && user ? <ModelSettings token={token} /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/profile"
              element={token && user ? <Profile token={token} onLogout={handleLogout} /> : <Navigate to="/login" replace />}
            />
            <Route
              path="/notifications"
              element={token && user ? <NotificationsPage /> : <Navigate to="/login" replace />}
            />

            {/* Catch-all */}
            <Route
              path="*"
              element={<Navigate to={token && user ? "/dashboard" : "/login"} replace />}
            />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-900 bg-slate-950/20 py-4 text-center text-xs text-slate-600">
          <div className="container mx-auto">
            &copy; {new Date().getFullYear()} Neuro-Behavioral Drift Modeling Platform. Local secure processing sandbox active.
          </div>
        </footer>

      </div>
    </Router>
  );
}
