import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Search,
  Filter,
  Sparkles,
  ShieldCheck,
  Award,
  Layers,
  ChevronRight,
  SlidersHorizontal,
  X,
  FileText,
  Zap,
  CheckCircle,
  HelpCircle
} from 'lucide-react';
import { searchKnowledgeBase } from '../services/api';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [searchResults, setSearchResults] = useState(null);

  // Filters state
  const [selectedDept, setSelectedDept] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [selectedType, setSelectedType] = useState('');

  const departments = ['HR', 'Policy', 'Technical', 'Sales', 'Research'];
  const statuses = ['Active', 'Draft', 'Archived'];
  const docTypes = ['Policy', 'SOP', 'Handbook', 'Guideline', 'Report'];

  const handleSearch = async (e) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const filters = {};
      if (selectedDept) filters.department = selectedDept;
      if (selectedStatus) filters.status = selectedStatus;
      if (selectedType) filters.document_type = selectedType;

      const filterObj = Object.keys(filters).length > 0 ? filters : null;

      const res = await searchKnowledgeBase(query, 5, filterObj);
      setSearchResults(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setSelectedDept('');
    setSelectedStatus('');
    setSelectedType('');
  };

  return (
    <div className="space-y-6">
      {/* Search Bar Section */}
      <div className="glass-panel p-6 rounded-3xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl -z-10" />

        <form onSubmit={handleSearch} className="space-y-4">
          <div className="relative flex items-center">
            <Search className="absolute left-4 h-5 w-5 text-cyan-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search enterprise policies, technical docs, guidelines..."
              className="w-full pl-12 pr-36 py-4 rounded-2xl bg-white/[0.03] border border-white/10 text-white placeholder:text-slate-500 outline-none focus:border-cyan-500/50 focus:ring-4 focus:ring-cyan-500/10 transition text-sm font-medium"
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-2.5 px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold text-xs transition shadow-lg shadow-cyan-500/25 flex items-center gap-2 cursor-pointer"
            >
              {loading ? (
                <Sparkles className="h-4 w-4 animate-spin text-white" />
              ) : (
                <>
                  <Zap className="h-4 w-4" />
                  <span>Hybrid Search</span>
                </>
              )}
            </button>
          </div>

          {/* Filter Bar Chips */}
          <div className="flex flex-wrap items-center gap-3 pt-2 border-t border-white/5">
            <div className="flex items-center gap-1.5 text-xs text-slate-400 mr-2">
              <SlidersHorizontal className="h-3.5 w-3.5 text-cyan-400" />
              <span>Filters:</span>
            </div>

            {/* Department Selector */}
            <select
              value={selectedDept}
              onChange={(e) => setSelectedDept(e.target.value)}
              className="px-3 py-1.5 rounded-xl bg-white/5 border border-white/10 text-xs text-slate-300 outline-none hover:bg-white/10 transition cursor-pointer"
            >
              <option value="" className="bg-slate-900">All Departments</option>
              {departments.map((d) => (
                <option key={d} value={d} className="bg-slate-900">{d}</option>
              ))}
            </select>

            {/* Status Selector */}
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="px-3 py-1.5 rounded-xl bg-white/5 border border-white/10 text-xs text-slate-300 outline-none hover:bg-white/10 transition cursor-pointer"
            >
              <option value="" className="bg-slate-900">All Statuses</option>
              {statuses.map((s) => (
                <option key={s} value={s} className="bg-slate-900">{s}</option>
              ))}
            </select>

            {/* Doc Type Selector */}
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="px-3 py-1.5 rounded-xl bg-white/5 border border-white/10 text-xs text-slate-300 outline-none hover:bg-white/10 transition cursor-pointer"
            >
              <option value="" className="bg-slate-900">All Document Types</option>
              {docTypes.map((t) => (
                <option key={t} value={t} className="bg-slate-900">{t}</option>
              ))}
            </select>

            {(selectedDept || selectedStatus || selectedType) && (
              <button
                type="button"
                onClick={clearFilters}
                className="text-xs text-rose-400 hover:text-rose-300 flex items-center gap-1 ml-auto cursor-pointer"
              >
                <X className="h-3 w-3" /> Clear Filters
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Query Analysis Header Pill */}
      {searchResults?.query_analysis && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-4 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex flex-wrap items-center justify-between gap-3 text-xs"
        >
          <div className="flex items-center gap-2 text-cyan-300">
            <Sparkles className="h-4 w-4 text-cyan-400" />
            <span className="font-semibold">Parsed Intent:</span>
            <span className="text-white font-mono">"{searchResults.query_analysis.search_text}"</span>
          </div>

          <div className="flex items-center gap-2">
            {searchResults.query_analysis.department && (
              <span className="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 text-[11px]">
                Dept: {searchResults.query_analysis.department}
              </span>
            )}
            {searchResults.query_analysis.status && (
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 text-[11px]">
                Status: {searchResults.query_analysis.status}
              </span>
            )}
            {searchResults.query_analysis.document_type && (
              <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 text-[11px]">
                Type: {searchResults.query_analysis.document_type}
              </span>
            )}
          </div>
        </motion.div>
      )}

      {/* Results List */}
      {searchResults ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400 px-1">
            <span>
              Found <strong className="text-white">{searchResults.results?.length || 0}</strong> relevant results across hybrid BM25 + Vector pipeline
            </span>
          </div>

          {searchResults.results?.map((res, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="glass-panel p-5 rounded-2xl space-y-3 hover:border-cyan-500/30 transition group"
            >
              {/* Header Badges */}
              <div className="flex items-center justify-between gap-2 flex-wrap">
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-cyan-400" />
                  <span className="text-sm font-bold text-white group-hover:text-cyan-300 transition">
                    {res.metadata?.file_name || 'Document Result'}
                  </span>

                  {res.is_authoritative && (
                    <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] font-semibold flex items-center gap-1">
                      <ShieldCheck className="h-3 w-3" /> Authoritative
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-2 text-[11px]">
                  <span className="px-2 py-0.5 rounded bg-white/5 text-slate-300 font-mono">
                    Score: {res.composite_score?.toFixed(1) || '85.0'}
                  </span>
                  <span className="px-2.5 py-0.5 rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">
                    {res.metadata?.department || 'General'}
                  </span>
                </div>
              </div>

              {/* Text Snippet */}
              <p className="text-xs text-slate-300 leading-relaxed font-mono bg-black/40 p-3 rounded-xl border border-white/5">
                {res.document}
              </p>

              {/* Footer Metadata Tag */}
              <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                <span>Path: {res.metadata?.file_path || 'data/...'}</span>
                <span>Version: {res.metadata?.version || 'v1.0'}</span>
              </div>
            </motion.div>
          ))}
        </div>
      ) : (
        <div className="glass-panel p-12 rounded-3xl text-center space-y-3">
          <div className="h-12 w-12 rounded-2xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center mx-auto border border-cyan-500/20">
            <Search className="h-6 w-6" />
          </div>
          <h3 className="text-base font-semibold text-white">Enterprise Hybrid Search</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            Type any query above to run RRF (Reciprocal Rank Fusion) combining ChromaDB semantic vectors with BM25 keyword matching.
          </p>
        </div>
      )}
    </div>
  );
}
