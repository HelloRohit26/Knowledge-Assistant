import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Network, FileText, Sparkles, Layers, RefreshCw, ChevronRight, X, Database, ShieldCheck, Zap } from 'lucide-react';
import { fetchKnowledgeGraph } from '../services/api';

export default function KnowledgeGraphPage() {
  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedNode, setSelectedNode] = useState(null);

  const loadGraph = async () => {
    setLoading(true);
    try {
      const res = await fetchKnowledgeGraph();
      if (res.data) setGraphData(res.data);
    } catch (err) {
      console.error('Error fetching knowledge graph:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadGraph();
  }, []);

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="px-3 py-1 rounded-lg bg-gradient-to-r from-purple-500/20 to-cyan-500/20 text-purple-300 font-mono text-xs font-bold border border-purple-500/30">
              PHASE 4 GRAPH ENGINE
            </span>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight font-heading shimmer-text">
              Interactive Enterprise Knowledge Graph
            </h1>
          </div>
          <p className="text-xs md:text-sm text-slate-400 mt-1">
            Visual entity relations, document connectivity, and cross-department knowledge mapping.
          </p>
        </div>

        <button
          onClick={loadGraph}
          className="px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-cyan-500/50 text-slate-200 text-xs font-semibold flex items-center gap-2 transition-all cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Knowledge Graph</span>
        </button>
      </div>

      {/* Main Canvas Card */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Interactive Graph Canvas */}
        <div className="lg:col-span-2 glass-panel rounded-3xl p-6 relative overflow-hidden min-h-[500px] flex flex-col justify-between">
          <div className="flex items-center justify-between z-10">
            <div className="flex items-center gap-2">
              <Network className="w-5 h-5 text-cyan-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-slate-200 font-mono">
                Visual Graph Topology
              </span>
            </div>
            {graphData && (
              <span className="px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-800/50 text-cyan-300 text-xs font-mono">
                {graphData.nodes_count} Nodes • {graphData.edges_count} Edges
              </span>
            )}
          </div>

          {/* Visual Node Cloud Canvas Representation */}
          <div className="my-8 relative h-[360px] flex items-center justify-center">
            {/* Background Orbital Rings */}
            <div className="absolute w-[320px] h-[320px] rounded-full border border-cyan-500/10 animate-pulse pointer-events-none" />
            <div className="absolute w-[440px] h-[440px] rounded-full border border-purple-500/10 pointer-events-none" />

            {loading ? (
              <div className="text-center space-y-2">
                <RefreshCw className="w-8 h-8 text-cyan-400 animate-spin mx-auto" />
                <p className="text-xs text-slate-400 font-mono">Rendering Entity Topology...</p>
              </div>
            ) : graphData?.nodes ? (
              <div className="relative w-full h-full">
                {graphData.nodes.map((node, i) => {
                  const angle = (i / graphData.nodes.length) * 2 * Math.PI;
                  const radius = node.type === 'category' ? 90 : 160;
                  const x = 50 + (radius / 3.8) * Math.cos(angle);
                  const y = 50 + (radius / 3.8) * Math.sin(angle);

                  return (
                    <motion.div
                      key={node.id}
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: i * 0.04, type: 'spring' }}
                      whileHover={{ scale: 1.25, zIndex: 30 }}
                      onClick={() => setSelectedNode(node)}
                      style={{ left: `${x}%`, top: `${y}%` }}
                      className={`absolute -translate-x-1/2 -translate-y-1/2 p-2.5 rounded-2xl border cursor-pointer shadow-xl backdrop-blur-xl transition-all ${
                        node.type === 'category'
                          ? 'bg-cyan-950/80 border-cyan-500/50 text-cyan-300 shadow-cyan-500/20'
                          : 'bg-slate-900/90 border-slate-700 text-slate-200 hover:border-cyan-400'
                      }`}
                    >
                      <div className="flex items-center gap-1.5 whitespace-nowrap">
                        {node.type === 'category' ? (
                          <Layers className="w-3.5 h-3.5 text-cyan-400" />
                        ) : (
                          <FileText className="w-3.5 h-3.5 text-purple-400" />
                        )}
                        <span className="text-[11px] font-bold font-heading">{node.label}</span>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            ) : null}
          </div>

          <div className="flex items-center justify-between text-[11px] text-slate-400 border-t border-slate-800/80 pt-3 z-10">
            <span>Click any node to inspect entity relationships & AI explanations</span>
            <span className="font-mono text-cyan-400">Interactive Entity Explorer</span>
          </div>
        </div>

        {/* Selected Node Details Drawer */}
        <div className="glass-panel rounded-3xl p-6 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2 mb-4 font-heading">
              <Sparkles className="w-4 h-4 text-cyan-400" /> Entity Inspector
            </h3>

            {selectedNode ? (
              <div className="space-y-4">
                <div className="p-4 rounded-2xl bg-cyan-950/40 border border-cyan-500/30">
                  <span className="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-mono text-[10px] uppercase font-bold">
                    {selectedNode.type} Node
                  </span>
                  <h4 className="text-base font-bold text-slate-100 mt-2 font-heading">{selectedNode.label}</h4>
                  {selectedNode.collection && (
                    <p className="text-xs text-slate-400 mt-1">Collection: {selectedNode.collection}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <h5 className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono">
                    AI Relationship Analysis
                  </h5>
                  <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/60 p-3.5 rounded-xl border border-slate-800">
                    This node links organizational policy directives with departmental execution rules across active knowledge stores.
                  </p>
                </div>
              </div>
            ) : (
              <div className="py-16 text-center text-slate-500 text-xs">
                Select any node on the graph canvas to inspect entity connections.
              </div>
            )}
          </div>

          <div className="pt-4 border-t border-slate-800 text-center">
            <span className="text-[11px] text-slate-400 font-mono">Knowledge Graph Engine v1.0</span>
          </div>
        </div>
      </div>
    </div>
  );
}
