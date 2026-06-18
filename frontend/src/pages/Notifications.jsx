import React, { useState, useEffect } from 'react';
import { Bell, Trash2, CheckCircle, AlertTriangle, Info, AlertOctagon } from 'lucide-react';
import { notificationsAPI } from '../services/api';

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('ALL');

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const res = await notificationsAPI.list(filter);
      setNotifications(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, [filter]);

  const handleMarkRead = async (id) => {
    try {
      await notificationsAPI.markRead(id);
      setNotifications(notifications.map(n => n.id === id ? { ...n, is_read: 1 } : n));
    } catch (err) {
      console.error(err);
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await notificationsAPI.markAllRead();
      setNotifications(notifications.map(n => ({ ...n, is_read: 1 })));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await notificationsAPI.delete(id);
      setNotifications(notifications.filter(n => n.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const getSeverityIcon = (severity) => {
    if (severity === 'HIGH') return <AlertOctagon className="h-6 w-6 text-red-500" />;
    if (severity === 'MEDIUM') return <AlertTriangle className="h-6 w-6 text-amber-500" />;
    return <Info className="h-6 w-6 text-blue-500" />;
  };

  const getSeverityBadge = (severity) => {
    if (severity === 'HIGH') return 'bg-red-500/10 text-red-400 border-red-500/20';
    if (severity === 'MEDIUM') return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
    return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="flex items-center justify-between mb-8 border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-slate-800 rounded-lg">
            <Bell className="h-6 w-6 text-accentBlue" />
          </div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Notification Center</h1>
        </div>
        
        <div className="flex items-center gap-4">
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-sm rounded-lg focus:ring-accentBlue focus:border-accentBlue p-2.5 text-slate-300"
          >
            <option value="ALL">All Alerts</option>
            <option value="HIGH">High Strain</option>
            <option value="MEDIUM">Medium Strain</option>
            <option value="INFO">Information</option>
          </select>
          
          <button 
            onClick={handleMarkAllRead}
            className="text-sm font-medium text-slate-400 hover:text-white transition-colors"
          >
            Mark all as read
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12 text-slate-500">Loading notifications...</div>
      ) : notifications.length === 0 ? (
        <div className="text-center py-20 bg-slate-900/30 rounded-2xl border border-slate-800/50">
          <CheckCircle className="h-16 w-16 text-emerald-500/20 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-slate-300">You're all caught up</h3>
          <p className="text-sm text-slate-500 mt-1">No notifications matching this filter.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {notifications.map((notification) => (
            <div 
              key={notification.id} 
              className={`flex items-start gap-4 p-5 rounded-xl border transition-all ${
                notification.is_read 
                  ? 'bg-slate-900/30 border-slate-800/50 opacity-70' 
                  : 'bg-slate-800/40 border-slate-700 hover:border-slate-600 shadow-lg'
              }`}
            >
              <div className="mt-1 flex-shrink-0">
                {getSeverityIcon(notification.severity)}
              </div>
              
              <div className="flex-grow">
                <div className="flex items-center justify-between mb-1">
                  <div className="flex items-center gap-2">
                    <h3 className={`font-semibold ${notification.is_read ? 'text-slate-300' : 'text-white'}`}>
                      {notification.title}
                    </h3>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${getSeverityBadge(notification.severity)}`}>
                      {notification.severity}
                    </span>
                  </div>
                  <span className="text-xs text-slate-500">
                    {new Date(notification.created_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                  </span>
                </div>
                <p className="text-sm text-slate-400 leading-relaxed mb-3">
                  {notification.message}
                </p>
                
                <div className="flex items-center gap-3 mt-2 pt-3 border-t border-slate-800/50">
                  {!notification.is_read && (
                    <button 
                      onClick={() => handleMarkRead(notification.id)}
                      className="text-xs font-semibold text-accentBlue hover:text-blue-400 flex items-center gap-1"
                    >
                      <CheckCircle className="h-3.5 w-3.5" /> Mark as Read
                    </button>
                  )}
                  <button 
                    onClick={() => handleDelete(notification.id)}
                    className="text-xs font-semibold text-red-500 hover:text-red-400 flex items-center gap-1 ml-auto"
                  >
                    <Trash2 className="h-3.5 w-3.5" /> Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
