import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, ArrowRight, Lightbulb, Zap, RefreshCw, ChevronRight } from 'lucide-react';
import { fetchCopilotSuggestions } from '../../services/api';

export default function CopilotWidget({ onSelectWorkflow }) {
  const [copilotData, setCopilotData] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadCopilotData = async () => {
    setLoading(true);
    try {
      const res = await fetchCopilotSuggestions();
      if (res.data) setCopilotData(res.data);
    } catch (err) {
      console.error('Copilot suggestions load error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCopilotData();
  }, []);

  if (loading) {
    return (
      <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 backdrop-blur-xl animate-pulse">
        <div className="h-4 bg-slate-800 rounded w-1/3 mb-3" />
        <div className="h-3 bg-slate-800/60 rounded w-2/3" />
      </div>
    );
  }

  if (!copilotData || !copilotData.suggestions || copilotData.suggestions.length === 0) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gradient-to-r from-cyan-950/40 via-slate-900/80 to-purple-950/40 border border-cyan-500/20 rounded-2xl p-5 md:p-6 backdrop-blur-2xl shadow-xl relative overflow-hidden group"
    >
      {/* Background Accent Glow */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none group-hover:bg-cyan-500/20 transition-all duration-500" />

      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4 relative z-10">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400">AI Copilot Proactive Assistant</span>
              <span className="px-2 py-0.5 text-[10px] font-mono bg-cyan-500/10 text-cyan-300 rounded-full border border-cyan-500/30">
                {copilotData.total_documents} Documents Indexed
              </span>
            </div>
            <h3 className="text-sm md:text-base font-semibold text-slate-100">
              {copilotData.summary_text}
            </h3>
          </div>
        </div>

        <button
          onClick={loadCopilotData}
          className="text-xs text-slate-400 hover:text-cyan-400 flex items-center gap-1.5 self-start md:self-center transition-colors"
          title="Refresh suggestions"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Insights</span>
        </button>
      </div>

      {/* Suggested Actions Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 relative z-10">
        {copilotData.suggestions.slice(0, 4).map((sug) => (
          <motion.div
            key={sug.id}
            whileHover={{ y: -3, scale: 1.01 }}
            onClick={() => onSelectWorkflow && onSelectWorkflow(sug.workflow_id)}
            className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-cyan-500/40 cursor-pointer group/card transition-all shadow-md flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                  {sug.category}
                </span>
                <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-cyan-950/60 text-cyan-300 border border-cyan-800/50">
                  {sug.badge}
                </span>
              </div>
              <h4 className="text-xs font-semibold text-slate-200 group-hover/card:text-cyan-300 transition-colors line-clamp-2">
                {sug.title}
              </h4>
              <p className="text-[11px] text-slate-400 mt-1 line-clamp-2 leading-relaxed">
                {sug.description}
              </p>
            </div>

            <div className="mt-3 pt-2.5 border-t border-slate-800/60 flex items-center justify-between text-xs text-cyan-400 group-hover/card:text-cyan-300 font-medium">
              <span className="flex items-center gap-1 text-[11px]">
                <Zap className="w-3 h-3 text-cyan-400" /> Run Workflow
              </span>
              <ChevronRight className="w-4 h-4 group-hover/card:translate-x-1 transition-transform" />
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
