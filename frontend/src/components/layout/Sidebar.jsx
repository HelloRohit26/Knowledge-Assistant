import React from 'react';
import { motion } from 'framer-motion';
import {
  LayoutDashboard,
  Search,
  MessageSquare,
  FolderKanban,
  BarChart3,
  ShieldAlert,
  Sparkles,
  Command,
  LogOut,
  ChevronRight,
  Database
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, onOpenCommandPalette, user, onLogout }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, badge: null },
    { id: 'search', label: 'AI Search', icon: Search, badge: 'RRF' },
    { id: 'chat', label: 'Intelligence Chat', icon: MessageSquare, badge: 'Agent' },
    { id: 'explorer', label: 'Document Explorer', icon: FolderKanban, badge: null },
    { id: 'analytics', label: 'Analytics', icon: BarChart3, badge: null },
    { id: 'admin', label: 'Admin Console', icon: ShieldAlert, badge: 'RBAC' },
  ];

  return (
    <aside className="w-64 border-r border-white/10 bg-slate-950/80 backdrop-blur-2xl flex flex-col justify-between p-4 h-screen sticky top-0 z-30 select-none">
      <div>
        {/* Brand Header */}
        <div className="flex items-center gap-3 px-3 py-3 mb-6 rounded-2xl bg-white/5 border border-white/10">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-cyan-400 p-[2px] shadow-lg glow-accent">
            <div className="h-full w-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Sparkles className="h-5 w-5 text-cyan-400" />
            </div>
          </div>
          <div>
            <h1 className="text-sm font-bold tracking-wide text-white">Knowledge Base</h1>
            <p className="text-[10px] text-cyan-400 font-mono flex items-center gap-1">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              v2.0 Enterprise
            </p>
          </div>
        </div>

        {/* Command Palette Trigger Pill */}
        <button
          onClick={onOpenCommandPalette}
          className="w-full mb-6 flex items-center justify-between px-3 py-2.5 rounded-xl bg-white/5 border border-white/10 text-xs text-slate-400 hover:bg-white/10 hover:text-white transition group"
        >
          <span className="flex items-center gap-2">
            <Command className="h-3.5 w-3.5 text-blue-400 group-hover:rotate-12 transition-transform" />
            Quick Command
          </span>
          <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300 border border-white/10 font-mono">
            ⌘K
          </kbd>
        </button>

        {/* Navigation Menu */}
        <div className="space-y-1">
          <p className="px-3 text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">
            Core Platform
          </p>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30 shadow-lg shadow-blue-500/10'
                    : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`h-4 w-4 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="px-1.5 py-0.5 rounded-md text-[9px] font-mono bg-white/10 text-slate-300">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Footer User Info */}
      <div className="pt-4 border-t border-white/10">
        <div className="flex items-center justify-between px-3 py-2 rounded-xl bg-white/5">
          <div className="flex items-center gap-2 overflow-hidden">
            <div className="h-8 w-8 rounded-lg bg-blue-500/20 text-blue-400 font-bold flex items-center justify-center text-xs border border-blue-500/30">
              {user?.username ? user.username[0].toUpperCase() : 'A'}
            </div>
            <div className="truncate">
              <p className="text-xs font-medium text-white truncate">{user?.username || 'Admin User'}</p>
              <p className="text-[10px] text-slate-400 capitalize">{user?.role || 'Administrator'}</p>
            </div>
          </div>

          {onLogout && (
            <button
              onClick={onLogout}
              title="Logout"
              className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition"
            >
              <LogOut className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
}
