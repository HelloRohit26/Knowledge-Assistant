import React from 'react';
import { Sparkles, Bell, RefreshCw, Cpu, Activity } from 'lucide-react';

export default function Header({ activeTab, onReindex, isReindexing, stats }) {
  const titles = {
    dashboard: 'System Overview & Control Center',
    search: 'Enterprise Hybrid Search Engine',
    chat: 'AI Intelligence Assistant & RAG Hub',
    explorer: 'Document Registry & Vault Explorer',
    analytics: 'Enterprise Intelligence Analytics',
    admin: 'Administration & Role-Based Access Control',
  };

  return (
    <header className="h-16 border-b border-white/10 bg-slate-950/60 backdrop-blur-xl px-6 flex items-center justify-between sticky top-0 z-20">
      <div>
        <h2 className="text-base font-semibold text-white tracking-wide">
          {titles[activeTab] || 'Dashboard'}
        </h2>
        <p className="text-[11px] text-slate-400">
          Knowledge Base Intelligence Node • {stats?.total_documents || 0} Documents Tracked
        </p>
      </div>

      <div className="flex items-center gap-4">
        {/* Model Badge */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-xs text-blue-300">
          <Cpu className="h-3.5 w-3.5 text-blue-400" />
          <span>Gemini 3.5 Flash + BM25</span>
        </div>

        {/* System Health Indicator */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-400 font-mono">
          <Activity className="h-3.5 w-3.5 animate-pulse text-emerald-400" />
          <span>Healthy</span>
        </div>

        {/* Manual Reindex Button */}
        <button
          onClick={onReindex}
          disabled={isReindexing}
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition shadow-lg shadow-blue-600/20 disabled:opacity-50 cursor-pointer"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${isReindexing ? 'animate-spin' : ''}`} />
          <span>{isReindexing ? 'Re-indexing...' : 'Sync & Index'}</span>
        </button>
      </div>
    </header>
  );
}
