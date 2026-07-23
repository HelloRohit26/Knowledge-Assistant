import React from 'react';
import { Sparkles, Bell, RefreshCw, Cpu, Activity } from 'lucide-react';

export default function Header({ activeTab, onReindex, isReindexing, stats }) {
  const titles = {
    dashboard: 'System Overview & Control Center',
    workflows: 'AI Workflows & Enterprise Work Assistant',
    workspace: 'Unified AI Productivity Workspace',
    'knowledge-graph': 'Interactive Enterprise Knowledge Graph',
    search: 'Enterprise Hybrid Search Engine',
    chat: 'AI Intelligence Assistant & RAG Hub',
    explorer: 'Document Registry & Vault Explorer',
    analytics: 'Enterprise Intelligence Analytics',
    'saas-settings': 'SaaS Multi-Tenancy & Developer API Keys',
    admin: 'Administration & Role-Based Access Control',
  };

  return (
    <header className="h-16 border-b border-white/10 bg-slate-950/70 backdrop-blur-xl px-6 flex items-center justify-between sticky top-0 z-20">
      <div>
        <h2 className="text-base font-bold text-white tracking-wide bg-gradient-to-r from-white via-slate-200 to-cyan-300 bg-clip-text text-transparent">
          {titles[activeTab] || 'Dashboard'}
        </h2>
        <p className="text-[11px] text-slate-400 font-mono">
          Node: <span className="text-cyan-400 font-semibold">active-prod-1</span> • <span className="text-emerald-400">{stats?.total_documents || 39} Files Tracked</span>
        </p>
      </div>

      <div className="flex items-center gap-3">
        {/* Model Badge */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-xs text-cyan-300 font-mono">
          <Cpu className="h-3.5 w-3.5 text-cyan-400" />
          <span>Gemini 3.5 Flash + BM25</span>
        </div>

        {/* System Health Indicator */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-400 font-mono">
          <Activity className="h-3.5 w-3.5 animate-pulse text-emerald-400" />
          <span>Node Healthy</span>
        </div>

        {/* Manual Reindex Button */}
        <button
          onClick={onReindex}
          disabled={isReindexing}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-600 via-blue-600 to-indigo-600 hover:from-cyan-500 hover:to-indigo-500 text-white text-xs font-semibold transition shadow-lg shadow-cyan-600/30 disabled:opacity-50 cursor-pointer"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${isReindexing ? 'animate-spin' : ''}`} />
          <span>{isReindexing ? 'Indexing...' : 'Sync & Index'}</span>
        </button>
      </div>
    </header>
  );
}
