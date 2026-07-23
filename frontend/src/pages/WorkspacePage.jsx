import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { LayoutGrid, MessageSquare, FileText, GitCompare, Edit3, Download, Sparkles, Send, Search, CheckCircle2 } from 'lucide-react';

export default function WorkspacePage() {
  const [activeWorkspaceTab, setActiveWorkspaceTab] = useState('notes');
  const [notesContent, setNotesContent] = useState(
    "# Executive Briefing Notes\n\n- Reviewed Leave Policy v2.4 changes\n- Confirmed 100% PTO carryover policy\n- Prepared onboarding checklist for Senior Engineers."
  );

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="px-3 py-1 rounded-lg bg-gradient-to-r from-cyan-500/20 to-blue-500/20 text-cyan-300 font-mono text-xs font-bold border border-cyan-500/30">
              PHASE 3 UNIFIED SUITE
            </span>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight font-heading shimmer-text">
              AI Productivity Workspace
            </h1>
          </div>
          <p className="text-xs md:text-sm text-slate-400 mt-1">
            All-in-one split-screen workspace with document preview, version comparison, and scratchpad notes.
          </p>
        </div>
      </div>

      {/* Split Screen Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 min-h-[600px]">
        {/* Panel 1: Document Version Comparison / Preview */}
        <div className="glass-panel rounded-3xl p-6 flex flex-col justify-between space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2 font-heading">
              <GitCompare className="w-4 h-4 text-cyan-400" /> Side-by-Side Version Delta Comparison
            </h3>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800/50">
              Leave Policy v2.1 vs v2.4
            </span>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs flex-1">
            <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-2">
              <span className="text-[10px] font-bold text-rose-400 uppercase tracking-wider font-mono">v2.1 Baseline</span>
              <p className="text-slate-300 leading-relaxed">
                Employees can carry over a maximum of 5 unused PTO days into the following calendar year. Unused leave beyond 5 days expires automatically.
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-emerald-950/30 border border-emerald-800/50 space-y-2">
              <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider font-mono">v2.4 Revised Draft</span>
              <p className="text-slate-200 leading-relaxed font-semibold">
                Employees can carry over up to 10 unused PTO days with department head approval. Extended parental leave entitlement increased to 16 weeks.
              </p>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-cyan-950/40 border border-cyan-500/20 text-xs text-cyan-300 flex items-center justify-between">
            <span className="flex items-center gap-1.5 font-mono text-[11px]">
              <Sparkles className="w-3.5 h-3.5 text-cyan-400" /> AI Delta Analysis: Entitlement expanded by 100%
            </span>
            <span className="text-[10px] text-cyan-400/80">Approved Revision</span>
          </div>
        </div>

        {/* Panel 2: Persistent Scratchpad Notes */}
        <div className="glass-panel rounded-3xl p-6 flex flex-col justify-between space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2 font-heading">
              <Edit3 className="w-4 h-4 text-purple-400" /> Persistent AI Scratchpad Notes
            </h3>
            <button
              onClick={() => setNotesContent(notesContent + "\n- AI Added: Verified compliance against corporate policy.")}
              className="px-2.5 py-1 rounded-lg bg-cyan-500/10 text-cyan-400 hover:bg-cyan-500 hover:text-slate-950 text-[11px] font-bold transition-all flex items-center gap-1"
            >
              <Sparkles className="w-3 h-3" /> Magic Auto-Summarize
            </button>
          </div>

          <textarea
            value={notesContent}
            onChange={(e) => setNotesContent(e.target.value)}
            className="w-full flex-1 min-h-[350px] p-4 rounded-2xl bg-slate-950 border border-slate-800 text-xs font-mono text-slate-200 leading-relaxed focus:outline-none focus:border-cyan-500/60 shadow-inner resize-none"
          />

          <div className="flex items-center justify-between text-xs pt-2">
            <span className="text-slate-400 font-mono">Auto-saved to User Session Memory</span>
            <button
              onClick={() => alert("Notes saved to workflow memory!")}
              className="px-4 py-2 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs shadow-md"
            >
              Save Notes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
