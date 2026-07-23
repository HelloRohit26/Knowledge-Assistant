import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Search,
  LayoutDashboard,
  MessageSquare,
  FolderKanban,
  BarChart3,
  ShieldAlert,
  RefreshCw,
  X,
  ArrowRight,
  Zap,
  Network,
  LayoutGrid,
  Building
} from 'lucide-react';

export default function CommandPalette({ isOpen, onClose, setActiveTab, onReindex }) {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
        else openPalette();
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  const openPalette = () => {
    setQuery('');
  };

  if (!isOpen) return null;

  const actions = [
    { id: 'nav-dash', title: 'Go to Dashboard', category: 'Navigation', icon: LayoutDashboard, action: () => { setActiveTab('dashboard'); onClose(); } },
    { id: 'nav-workflows', title: 'Go to AI Workflows', category: 'Navigation', icon: Zap, action: () => { setActiveTab('workflows'); onClose(); } },
    { id: 'nav-workspace', title: 'Go to AI Workspace', category: 'Navigation', icon: LayoutGrid, action: () => { setActiveTab('workspace'); onClose(); } },
    { id: 'nav-graph', title: 'Go to Knowledge Graph', category: 'Navigation', icon: Network, action: () => { setActiveTab('knowledge-graph'); onClose(); } },
    { id: 'nav-saas', title: 'Go to SaaS & API Keys', category: 'Navigation', icon: Building, action: () => { setActiveTab('saas-settings'); onClose(); } },
    { id: 'nav-search', title: 'Go to AI Search', category: 'Navigation', icon: Search, action: () => { setActiveTab('search'); onClose(); } },
    { id: 'nav-chat', title: 'Go to Intelligence Chat', category: 'Navigation', icon: MessageSquare, action: () => { setActiveTab('chat'); onClose(); } },
    { id: 'nav-explorer', title: 'Go to Document Explorer', category: 'Navigation', icon: FolderKanban, action: () => { setActiveTab('explorer'); onClose(); } },
    { id: 'nav-analytics', title: 'Go to Analytics', category: 'Navigation', icon: BarChart3, action: () => { setActiveTab('analytics'); onClose(); } },
    { id: 'nav-admin', title: 'Go to Admin Console', category: 'Navigation', icon: ShieldAlert, action: () => { setActiveTab('admin'); onClose(); } },
    { id: 'act-reindex', title: 'Trigger Incremental Re-index', category: 'Actions', icon: RefreshCw, action: () => { onReindex(); onClose(); } },
  ];

  const filtered = actions.filter(
    (a) => a.title.toLowerCase().includes(query.toLowerCase()) || a.category.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-start justify-center pt-24 px-4 bg-slate-950/80 backdrop-blur-md">
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: -20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: -20 }}
          transition={{ duration: 0.15 }}
          className="w-full max-w-xl rounded-2xl bg-slate-900 border border-white/10 shadow-2xl overflow-hidden glass-panel"
        >
          {/* Input Header */}
          <div className="flex items-center px-4 py-3.5 border-b border-white/10">
            <Search className="h-4 w-4 text-blue-400 mr-3" />
            <input
              type="text"
              autoFocus
              placeholder="Type a command or search workspace..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500"
            />
            <button
              onClick={onClose}
              className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          {/* Action List */}
          <div className="max-h-80 overflow-y-auto p-2 space-y-1">
            {filtered.length === 0 ? (
              <div className="px-4 py-8 text-center text-xs text-slate-500">
                No matching commands found
              </div>
            ) : (
              filtered.map((item) => {
                const Icon = item.icon;
                return (
                  <button
                    key={item.id}
                    onClick={item.action}
                    className="w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs text-slate-300 hover:bg-blue-600/20 hover:text-white transition group"
                  >
                    <div className="flex items-center gap-3">
                      <div className="p-1.5 rounded-lg bg-white/5 group-hover:bg-blue-500/20 text-slate-400 group-hover:text-blue-400 transition">
                        <Icon className="h-4 w-4" />
                      </div>
                      <span>{item.title}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] text-slate-500 font-mono">{item.category}</span>
                      <ArrowRight className="h-3.5 w-3.5 opacity-0 group-hover:opacity-100 text-blue-400 transition" />
                    </div>
                  </button>
                );
              })
            )}
          </div>

          {/* Footer Tip */}
          <div className="px-4 py-2 border-t border-white/10 bg-slate-950/40 flex items-center justify-between text-[11px] text-slate-500">
            <span>Use ↑ ↓ to navigate</span>
            <span>ESC to close</span>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
