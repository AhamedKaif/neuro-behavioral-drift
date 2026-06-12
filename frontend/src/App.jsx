import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import Auth from './pages/Auth';
import Dashboard from './pages/Dashboard';
import ModelSettings from './pages/ModelSettings';
import Profile from './pages/Profile';
import { Brain, LayoutDashboard, Database, User, Settings } from 'lucide-react';
import axios from 'axios';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        try {
          // Verify token against backend
          const res = await axios.get('/api/auth/me', {
            headers: { Authorization: `Bearer ${storedToken}` }
          });
          setToken(storedToken);
          setUser(res.data);
        } catch (err) {
          console.error("Token validation failed", err);
          // Clear invalid token
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          setToken(null);
          setUser(null);
        }
      }
      setCheckingAuth(false);
    };

    checkAuth();
  }, [token]);

  const handleLoginSuccess = (newToken, newUser) => {
    setToken(newToken);
    setUser(newUser);
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

              <Link to="/profile" className="flex items-center gap-2 bg-slate-900 border border-slate-800/80 rounded-xl px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white hover:border-slate-700 transition-colors">
                <User className="h-3.5 w-3.5 text-accentBlue" />
                <span>{user.full_name || user.username}</span>
              </Link>

            </div>
          </header>
        )}

        {/* Main Content Area */}
        <main className="flex-grow w-full">
          <Routes>
            <Route 
              path="/login" 
              element={!token ? <Auth onLoginSuccess={handleLoginSuccess} /> : <Navigate to="/dashboard" />} 
            />
            
            <Route 
              path="/dashboard" 
              element={token ? <Dashboard token={token} user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
            />
            
            <Route 
              path="/model-telemetry" 
              element={token ? <ModelSettings token={token} /> : <Navigate to="/login" />} 
            />

            <Route 
              path="/profile" 
              element={token ? <Profile token={token} onLogout={handleLogout} /> : <Navigate to="/login" />} 
            />

            <Route 
              path="*" 
              element={<Navigate to={token ? "/dashboard" : "/login"} />} 
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
