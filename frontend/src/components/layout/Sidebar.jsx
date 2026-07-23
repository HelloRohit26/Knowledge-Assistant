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
  Zap,
  Network,
  LayoutGrid,
  Building
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, onOpenCommandPalette, user, onLogout }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, badge: null },
    { id: 'workflows', label: 'AI Workflows', icon: Zap, badge: 'Work Assistant' },
    { id: 'workspace', label: 'AI Workspace', icon: LayoutGrid, badge: 'Unified' },
    { id: 'knowledge-graph', label: 'Knowledge Graph', icon: Network, badge: 'Topology' },
    { id: 'search', label: 'AI Search', icon: Search, badge: 'RRF' },
    { id: 'chat', label: 'Intelligence Chat', icon: MessageSquare, badge: 'Agent' },
    { id: 'explorer', label: 'Document Explorer', icon: FolderKanban, badge: null },
    { id: 'analytics', label: 'Analytics', icon: BarChart3, badge: null },
    { id: 'saas-settings', label: 'SaaS & API Keys', icon: Building, badge: 'API' },
    { id: 'admin', label: 'Admin Console', icon: ShieldAlert, badge: 'RBAC' },
  ];

  return (
    <aside className="w-64 border-r border-slate-800/80 bg-slate-950/80 backdrop-blur-2xl flex flex-col justify-between p-4 h-screen sticky top-0 z-30 select-none">
      <div>
        {/* Brand Header with Glowing Halo */}
        <div className="relative group mb-6">
          <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-cyan-500 via-indigo-500 to-fuchsia-500 opacity-30 group-hover:opacity-60 blur-md transition duration-500" />
          <div className="relative flex items-center gap-3 px-3.5 py-3 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl backdrop-blur-xl">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-fuchsia-500 p-[2px] shadow-lg shadow-cyan-500/20">
              <div className="h-full w-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <Sparkles className="h-5 w-5 text-cyan-400 animate-pulse" />
              </div>
            </div>
            <div>
              <h1 className="text-sm font-extrabold tracking-wide text-white shimmer-text font-heading">
                Knowledge Platform
              </h1>
              <p className="text-[10px] text-cyan-400 font-mono flex items-center gap-1">
                <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-ping" />
                v2.5 AI Assistant
              </p>
            </div>
          </div>
        </div>

        {/* Command Palette Trigger Pill */}
        <button
          onClick={onOpenCommandPalette}
          className="w-full mb-6 flex items-center justify-between px-3.5 py-2.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 hover:bg-slate-800/80 hover:text-slate-200 hover:border-cyan-500/40 transition-all duration-200 group cursor-pointer shadow-md"
        >
          <span className="flex items-center gap-2 font-medium">
            <Command className="h-3.5 w-3.5 text-cyan-400 group-hover:rotate-12 transition-transform" />
            Quick Command
          </span>
          <kbd className="px-2 py-0.5 rounded-lg bg-slate-950 text-[10px] text-cyan-300 border border-cyan-500/30 font-mono shadow-inner">
            ⌘K
          </kbd>
        </button>

        {/* Navigation Menu */}
        <div className="space-y-1 relative">
          <p className="px-3 text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2 font-mono">
            Platform Capabilities
          </p>

          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full relative flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200 cursor-pointer ${
                  isActive
                    ? 'text-cyan-300 font-bold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/50'
                }`}
              >
                {/* Active Glowing Background Motion Pill */}
                {isActive && (
                  <motion.div
                    layoutId="sidebar-active-indicator"
                    className="absolute inset-0 rounded-xl bg-gradient-to-r from-cyan-500/20 via-blue-500/15 to-purple-500/20 border border-cyan-500/40 shadow-lg shadow-cyan-500/10"
                    transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                  />
                )}

                <div className="flex items-center gap-3 relative z-10">
                  <Icon className={`h-4 w-4 transition-colors ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>

                {item.badge && (
                  <span className={`relative z-10 px-2 py-0.5 rounded-md text-[9px] font-mono font-medium border ${
                    isActive
                      ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40'
                      : 'bg-slate-900 text-slate-400 border-slate-800'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Footer User Profile */}
      <div className="pt-4 border-t border-slate-800/80">
        <div className="flex items-center justify-between px-3 py-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center gap-2.5 overflow-hidden">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-cyan-500 to-purple-600 text-slate-950 font-extrabold flex items-center justify-center text-xs shadow-md shadow-cyan-500/20">
              {user?.username ? user.username[0].toUpperCase() : 'A'}
            </div>
            <div className="truncate">
              <p className="text-xs font-bold text-slate-200 truncate font-heading">{user?.username || 'Admin User'}</p>
              <p className="text-[10px] text-cyan-400 font-mono capitalize">{user?.role || 'Administrator'}</p>
            </div>
          </div>

          {onLogout && (
            <button
              onClick={onLogout}
              title="Logout"
              className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors cursor-pointer"
            >
              <LogOut className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
}
