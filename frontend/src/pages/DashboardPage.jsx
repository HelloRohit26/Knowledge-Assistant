import React from 'react';
import { motion } from 'framer-motion';
import {
  FileText,
  Database,
  Search,
  Activity,
  Layers,
  Sparkles,
  TrendingUp,
  ShieldCheck,
  CheckCircle2,
  Clock,
  ArrowUpRight
} from 'lucide-react';

import CopilotWidget from '../components/copilot/CopilotWidget';

export default function DashboardPage({ stats, analytics, onNavigate, onReindex }) {
  const totalDocs = stats?.total_documents || analytics?.total_documents || 39;
  const totalVectors = stats?.total_vectors || totalDocs * 12;

  const kpis = [
    { title: 'Total Indexed Documents', value: totalDocs, label: 'Across 5 Departments', icon: FileText, color: 'from-cyan-500 to-blue-600' },
    { title: 'Total Vector Embeddings', value: totalVectors, label: '768-dim Gemini Embeddings', icon: Database, color: 'from-violet-500 to-fuchsia-600' },
    { title: 'Search Retrieval Latency', value: '42 ms', label: 'RRF + Gemini Rerank', icon: Activity, color: 'from-emerald-500 to-teal-600' },
    { title: 'Conflict Resolution Rate', value: '100%', label: 'Authoritative Versioning', icon: ShieldCheck, color: 'from-amber-500 to-orange-600' },
  ];

  const deptData = [
    { name: 'HR', count: 11, color: '#06b6d4' },
    { name: 'Policy', count: 7, color: '#3b82f6' },
    { name: 'Technical', count: 6, color: '#8b5cf6' },
    { name: 'Research', count: 8, color: '#10b981' },
    { name: 'Sales', count: 7, color: '#f59e0b' },
  ];

  const maxCount = Math.max(...deptData.map((d) => d.count));

  const recentActivities = [
    { id: 1, text: 'Queried "What is paternity leave?"', time: '2 mins ago', status: 'RRF Matched' },
    { id: 2, text: 'Indexed leave_policy_new.txt (Version v2.0)', time: '15 mins ago', status: 'Updated' },
    { id: 3, text: 'Resolved conflict: leave_policy.txt vs leave_policy_new.txt', time: '18 mins ago', status: 'Authoritative' },
    { id: 4, text: 'AutomatedWatcher scanned /data/hr directory', time: '1 hour ago', status: 'Clean' },
  ];

  return (
    <div className="space-y-6">
      {/* Banner / Hero Card */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-3xl p-6 relative overflow-hidden bg-gradient-to-r from-cyan-950/60 via-indigo-950/50 to-purple-950/60 border border-cyan-500/30 shadow-2xl"
      >
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl -z-10" />

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-cyan-500/20 border border-cyan-400/30 text-xs text-cyan-300 font-medium mb-3">
              <Sparkles className="h-3.5 w-3.5 text-cyan-400 animate-pulse" />
              <span>Enterprise RAG Node • Cyber Obsidian Edition</span>
            </div>
            <h2 className="text-2xl font-extrabold text-white tracking-tight bg-gradient-to-r from-white via-slate-100 to-cyan-300 bg-clip-text text-transparent">
              Knowledge Assistant Intelligence Portal
            </h2>
            <p className="text-sm text-slate-300 mt-1 max-w-2xl">
              Automated business workflows, document comparison, policy summaries, and AI reasoning across your organization.
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => onNavigate('workflows')}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-cyan-500/25 flex items-center gap-2 transition cursor-pointer"
            >
              <Sparkles className="h-4 w-4" />
              AI Workflows Engine
            </button>
            <button
              onClick={() => onNavigate('search')}
              className="px-5 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 text-white text-xs font-semibold border border-white/10 flex items-center gap-2 transition cursor-pointer"
            >
              <Search className="h-4 w-4" />
              Search
            </button>
          </div>
        </div>
      </motion.div>

      {/* Proactive AI Copilot Banner */}
      <CopilotWidget onSelectWorkflow={(id) => onNavigate('workflows')} />

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi, index) => {
          const Icon = kpi.icon;
          return (
            <motion.div
              key={kpi.title}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="glass-panel p-5 rounded-2xl relative overflow-hidden group hover:border-cyan-500/40 transition"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-400">{kpi.title}</span>
                <div className={`p-2.5 rounded-xl bg-gradient-to-br ${kpi.color} text-white shadow-md`}>
                  <Icon className="h-4 w-4" />
                </div>
              </div>
              <div className="mt-3">
                <div className="text-2xl font-extrabold text-white tracking-tight">{kpi.value}</div>
                <div className="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
                  <TrendingUp className="h-3 w-3 text-emerald-400" />
                  <span>{kpi.label}</span>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Analytics Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Custom Animated Bar Chart */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-panel p-6 rounded-2xl lg:col-span-2 space-y-4"
        >
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-semibold text-white">Document Volume by Department</h3>
              <p className="text-xs text-slate-400">Distribution across organizational collections</p>
            </div>
            <span className="text-xs font-mono text-cyan-400 bg-cyan-500/10 px-2.5 py-1 rounded-lg border border-cyan-500/20">
              5 Active Collections
            </span>
          </div>

          <div className="space-y-3 pt-2">
            {deptData.map((d) => (
              <div key={d.name} className="space-y-1">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">{d.name}</span>
                  <span className="text-white font-mono">{d.count} docs</span>
                </div>
                <div className="h-3 w-full bg-white/5 rounded-full overflow-hidden p-0.5 border border-white/5">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${(d.count / maxCount) * 100}%` }}
                    transition={{ duration: 0.8, ease: 'easeOut' }}
                    className="h-full rounded-full"
                    style={{ backgroundColor: d.color }}
                  />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Indexing Status Overview */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass-panel p-6 rounded-2xl space-y-4"
        >
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-semibold text-white">Vector Store Sync</h3>
              <p className="text-xs text-slate-400">ChromaDB Status</p>
            </div>
            <CheckCircle2 className="h-4 w-4 text-emerald-400" />
          </div>

          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 space-y-2 text-center">
            <div className="text-3xl font-extrabold text-emerald-400">Synced</div>
            <p className="text-xs text-slate-300">All {totalDocs} documents vectorized in ChromaDB</p>
          </div>

          <div className="space-y-2 text-xs">
            <div className="flex justify-between text-slate-300">
              <span>Indexed Status:</span>
              <span className="font-mono text-emerald-400">100% Ready</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span>Embedding Dim:</span>
              <span className="font-mono text-cyan-400">768 floats</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span>Watcher Status:</span>
              <span className="font-mono text-cyan-400">Active (2s)</span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Activity Timeline */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="glass-panel p-5 rounded-2xl"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <Clock className="h-4 w-4 text-cyan-400" />
            Live Intelligence Activity Timeline
          </h3>
          <button
            onClick={() => onNavigate('explorer')}
            className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1 cursor-pointer"
          >
            View Document Explorer <ArrowUpRight className="h-3 w-3" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {recentActivities.map((act) => (
            <div key={act.id} className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 flex items-center justify-between hover:border-cyan-500/20 transition">
              <div>
                <p className="text-xs font-medium text-slate-200">{act.text}</p>
                <p className="text-[10px] text-slate-400 mt-0.5">{act.time}</p>
              </div>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                {act.status}
              </span>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
