import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Zap,
  Play,
  FileText,
  Clock,
  CheckCircle2,
  AlertCircle,
  Download,
  Plus,
  Search,
  Sparkles,
  UserPlus,
  GitCompare,
  UserMinus,
  DollarSign,
  BarChart3,
  ShieldCheck,
  FileCode,
  Scale,
  Cpu,
  AlertTriangle,
  Briefcase,
  Layers,
  ChevronRight,
  X,
  FileSpreadsheet,
  Bookmark,
  Share2,
  RefreshCw,
  TrendingUp
} from 'lucide-react';

import {
  fetchWorkflowTemplates,
  executeWorkflow,
  fetchWorkflowHistory,
  exportWorkflowPDF,
  exportWorkflowDOCX,
  createWorkflowTemplate
} from '../services/api';
import CopilotWidget from '../components/copilot/CopilotWidget';

const ICON_MAP = {
  UserPlus: UserPlus,
  GitCompare: GitCompare,
  FileText: FileText,
  UserMinus: UserMinus,
  DollarSign: DollarSign,
  BarChart3: BarChart3,
  ShieldCheck: ShieldCheck,
  FileCode: FileCode,
  Scale: Scale,
  Cpu: Cpu,
  AlertTriangle: AlertTriangle,
  Briefcase: Briefcase,
  Search: Search,
  Zap: Zap
};

const CATEGORIES = ['All', 'HR', 'Finance', 'Legal', 'Engineering', 'Management', 'History'];

// Motion Stagger Variants
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
    },
  },
};

const cardVariants = {
  hidden: { opacity: 0, y: 20, scale: 0.96 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { type: 'spring', stiffness: 300, damping: 24 },
  },
};

export default function WorkflowsPage() {
  const [activeCategory, setActiveCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [templates, setTemplates] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  // Execution Modal & State
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);
  const [inputValues, setInputValues] = useState({});
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionProgress, setExecutionProgress] = useState(0);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [activeRunResult, setActiveRunResult] = useState(null);

  // Detail Drawer for History Items
  const [inspectRun, setInspectRun] = useState(null);

  // Export Loading
  const [isExportingPdf, setIsExportingPdf] = useState(false);
  const [isExportingDocx, setIsExportingDocx] = useState(false);

  // Custom Template Modal
  const [isTemplateModalOpen, setIsTemplateModalOpen] = useState(false);
  const [newTemplateData, setNewTemplateData] = useState({
    title: '',
    description: '',
    category: 'Engineering',
    steps: 'Scan architecture docs\nExtract APIs\nGenerate specification'
  });

  const loadData = async () => {
    setLoading(true);
    try {
      const [tRes, hRes] = await Promise.all([
        fetchWorkflowTemplates().catch(() => ({ data: { templates: [] } })),
        fetchWorkflowHistory().catch(() => ({ data: { history: [] } }))
      ]);

      if (tRes.data?.templates) setTemplates(tRes.data.templates);
      if (hRes.data?.history) setHistory(hRes.data.history);
    } catch (err) {
      console.error('Error loading workflow page data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleOpenWorkflowModal = (template) => {
    setSelectedWorkflow(template);
    const initialInputs = {};
    if (template.inputs_schema) {
      template.inputs_schema.forEach((inp) => {
        initialInputs[inp.key] = inp.default || '';
      });
    }
    setInputValues(initialInputs);
  };

  const handleStartExecution = async () => {
    if (!selectedWorkflow) return;
    setIsExecuting(true);
    setExecutionProgress(10);
    setCurrentStepIndex(0);
    setActiveRunResult(null);

    // Simulate animated step progression
    const stepTimer = setInterval(() => {
      setExecutionProgress((prev) => {
        if (prev >= 85) return prev;
        return prev + 18;
      });
      setCurrentStepIndex((prev) => (prev < 4 ? prev + 1 : prev));
    }, 850);

    try {
      const res = await executeWorkflow(selectedWorkflow.id, inputValues, selectedWorkflow.is_custom ? selectedWorkflow : null);
      clearInterval(stepTimer);
      setExecutionProgress(100);
      setCurrentStepIndex(4);
      setActiveRunResult(res.data);
      loadData();
    } catch (err) {
      clearInterval(stepTimer);
      setIsExecuting(false);
      alert('Execution failed. Please check inputs and try again.');
    }
  };

  const handleExportPDF = async (title, category, markdownContent) => {
    setIsExportingPdf(true);
    try {
      const response = await exportWorkflowPDF(title, category, markdownContent);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${title.toLowerCase().replace(/ /g, '_')}_report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('PDF export error:', err);
      alert('Failed to generate PDF export.');
    } finally {
      setIsExportingPdf(false);
    }
  };

  const handleExportDOCX = async (title, category, markdownContent) => {
    setIsExportingDocx(true);
    try {
      const response = await exportWorkflowDOCX(title, category, markdownContent);
      const blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${title.toLowerCase().replace(/ /g, '_')}_report.docx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('DOCX export error:', err);
      alert('Failed to generate DOCX export.');
    } finally {
      setIsExportingDocx(false);
    }
  };

  const handleCreateCustomTemplate = async (e) => {
    e.preventDefault();
    try {
      const stepArray = newTemplateData.steps.split('\n').filter((s) => s.trim().length > 0);
      await createWorkflowTemplate({
        title: newTemplateData.title,
        description: newTemplateData.description,
        category: newTemplateData.category,
        steps: stepArray
      });
      setIsTemplateModalOpen(false);
      setNewTemplateData({ title: '', description: '', category: 'Engineering', steps: '' });
      loadData();
    } catch (err) {
      console.error('Error creating template:', err);
    }
  };

  const filteredTemplates = templates.filter((t) => {
    const matchesCat = activeCategory === 'All' || t.category === activeCategory;
    const matchesSearch =
      t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesSearch;
  });

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-16">
      {/* Top Banner Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="px-3 py-1 rounded-lg bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 font-mono text-xs font-bold border border-cyan-500/30 shadow-md">
              ENTERPRISE PLATFORM
            </span>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight font-heading shimmer-text">
              AI Workflows Engine
            </h1>
          </div>
          <p className="text-xs md:text-sm text-slate-400 mt-1">
            Automate end-to-end enterprise tasks, generate executive reports, SOPs, and policy audits using AI reasoning.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={() => setIsTemplateModalOpen(true)}
            className="px-4.5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 hover:border-cyan-500/50 text-slate-200 text-xs font-semibold flex items-center gap-2 transition-all shadow-lg hover:shadow-cyan-500/10 cursor-pointer"
          >
            <Plus className="w-4 h-4 text-cyan-400" />
            <span>Create Custom Template</span>
          </motion.button>
        </div>
      </div>

      {/* Proactive Copilot Widget */}
      <CopilotWidget onSelectWorkflow={(id) => {
        const found = templates.find((t) => t.id === id);
        if (found) handleOpenWorkflowModal(found);
      }} />

      {/* Navigation Tabs & Search Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
        {/* Category Tabs */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 sm:pb-0 scrollbar-none">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-4 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition-all duration-200 flex items-center gap-2 cursor-pointer ${
                activeCategory === cat
                  ? 'bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-600 text-white shadow-lg shadow-cyan-500/25 border border-cyan-400/40'
                  : 'bg-slate-900/60 text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 border border-slate-800/80'
              }`}
            >
              {cat === 'History' && <Clock className="w-3.5 h-3.5" />}
              {cat}
              {cat === 'History' && history.length > 0 && (
                <span className="px-1.5 py-0.5 rounded-full text-[10px] bg-slate-950/60 text-cyan-300 font-mono">
                  {history.length}
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Search */}
        {activeCategory !== 'History' && (
          <div className="relative w-full sm:w-72">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search enterprise workflows..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-200 text-xs focus:outline-none focus:border-cyan-500/60 focus:ring-1 focus:ring-cyan-500/30 transition-all placeholder:text-slate-500 shadow-inner"
            />
          </div>
        )}
      </div>

      {/* VIEW 1: WORKFLOW TEMPLATE CARDS GRID */}
      {activeCategory !== 'History' && (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5"
        >
          {filteredTemplates.map((tpl) => {
            const IconComp = ICON_MAP[tpl.icon] || Zap;
            return (
              <motion.div
                key={tpl.id}
                variants={cardVariants}
                whileHover={{ y: -6, scale: 1.015 }}
                className="glass-card-interactive rounded-2xl p-5 flex flex-col justify-between relative group overflow-hidden"
              >
                {/* Radial Beam Background Effect */}
                <div className="absolute -top-24 -right-24 w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl group-hover:bg-cyan-500/20 transition-all duration-500 pointer-events-none" />

                <div>
                  <div className="flex items-center justify-between gap-3 mb-3.5">
                    <div className="p-3 rounded-xl bg-cyan-950/60 text-cyan-400 border border-cyan-800/40 group-hover:bg-gradient-to-r group-hover:from-cyan-500 group-hover:to-blue-600 group-hover:text-slate-950 transition-all duration-300 shadow-md">
                      <IconComp className="w-5 h-5" />
                    </div>
                    <div className="flex items-center gap-2">
                      {tpl.is_custom && (
                        <span className="px-2 py-0.5 rounded bg-purple-950/80 text-purple-300 border border-purple-800/50 text-[10px] font-mono font-semibold">
                          Custom
                        </span>
                      )}
                      <span className="px-2.5 py-1 rounded-full bg-slate-800/90 text-slate-300 border border-slate-700 text-[10px] font-bold tracking-wide uppercase">
                        {tpl.category}
                      </span>
                    </div>
                  </div>

                  <h3 className="text-base font-bold text-slate-100 group-hover:text-cyan-300 transition-colors leading-snug font-heading">
                    {tpl.title}
                  </h3>
                  <p className="text-xs text-slate-400 mt-2 leading-relaxed line-clamp-3">
                    {tpl.description}
                  </p>

                  {/* Steps count & indicator */}
                  <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400 font-mono">
                    <span className="flex items-center gap-1.5 text-slate-300">
                      <Layers className="w-3.5 h-3.5 text-cyan-400" />
                      {tpl.steps ? tpl.steps.length : 3} Pipeline Steps
                    </span>
                    <span className="text-[10px] text-cyan-400/80">
                      ~15s AI Execution
                    </span>
                  </div>
                </div>

                <div className="mt-5">
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleOpenWorkflowModal(tpl)}
                    className="w-full py-2.5 rounded-xl bg-cyan-500/10 hover:bg-gradient-to-r hover:from-cyan-500 hover:to-blue-600 text-cyan-300 hover:text-slate-950 border border-cyan-500/30 hover:border-transparent font-bold text-xs flex items-center justify-center gap-2 transition-all duration-200 shadow-md cursor-pointer"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" />
                    <span>Run Workflow</span>
                  </motion.button>
                </div>
              </motion.div>
            );
          })}
        </motion.div>
      )}

      {/* VIEW 2: WORKFLOW HISTORY TABLE */}
      {activeCategory === 'History' && (
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-panel rounded-2xl overflow-hidden shadow-2xl"
        >
          <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/40">
            <h3 className="text-sm font-bold text-slate-200 flex items-center gap-2 font-heading">
              <Clock className="w-4 h-4 text-cyan-400" /> Recently Executed AI Workflows
            </h3>
            <span className="text-xs text-slate-400 font-mono">{history.length} total runs</span>
          </div>

          {history.length === 0 ? (
            <div className="p-12 text-center text-slate-500 text-xs">
              No workflow executions logged yet. Run a workflow above!
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950/80 text-slate-400 uppercase font-mono text-[10px] border-b border-slate-800">
                  <tr>
                    <th className="px-5 py-3.5">Workflow Title</th>
                    <th className="px-5 py-3.5">Category</th>
                    <th className="px-5 py-3.5">Status</th>
                    <th className="px-5 py-3.5">Execution Time</th>
                    <th className="px-5 py-3.5">Timestamp</th>
                    <th className="px-5 py-3.5 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {history.map((run) => (
                    <tr key={run.run_id} className="hover:bg-slate-800/40 transition-colors">
                      <td className="px-5 py-3.5 font-semibold text-slate-100 flex items-center gap-2">
                        <Zap className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
                        <span>{run.title}</span>
                      </td>
                      <td className="px-5 py-3.5">
                        <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px]">
                          {run.category}
                        </span>
                      </td>
                      <td className="px-5 py-3.5">
                        {run.status === 'completed' ? (
                          <span className="px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-300 border border-emerald-800/50 text-[10px] font-semibold flex items-center gap-1 w-fit">
                            <CheckCircle2 className="w-3 h-3 text-emerald-400" /> Completed
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded bg-rose-950/80 text-rose-300 border border-rose-800/50 text-[10px] font-semibold flex items-center gap-1 w-fit">
                            <AlertCircle className="w-3 h-3 text-rose-400" /> Failed
                          </span>
                        )}
                      </td>
                      <td className="px-5 py-3.5 font-mono text-slate-400">
                        {run.execution_time_ms ? `${(run.execution_time_ms / 1000).toFixed(1)}s` : '0.5s'}
                      </td>
                      <td className="px-5 py-3.5 text-slate-400 font-mono">
                        {run.created_at ? run.created_at.replace('T', ' ').slice(0, 16) : 'Just now'}
                      </td>
                      <td className="px-5 py-3.5 text-right">
                        <button
                          onClick={() => setInspectRun(run)}
                          className="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-cyan-500 hover:text-slate-950 text-slate-200 text-[11px] font-bold transition-all cursor-pointer shadow-md"
                        >
                          View Report
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </motion.div>
      )}

      {/* EXECUTION MODAL & RUNNER VIEW */}
      <AnimatePresence>
        {selectedWorkflow && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-xl">
            <motion.div
              initial={{ opacity: 0, scale: 0.94, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.94, y: 20 }}
              transition={{ type: 'spring', stiffness: 350, damping: 28 }}
              className="bg-slate-900 border border-slate-800 rounded-3xl max-w-3xl w-full overflow-hidden shadow-2xl relative flex flex-col max-h-[90vh]"
            >
              {/* Modal Header */}
              <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/70">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-md">
                    <Zap className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-base font-extrabold text-slate-100 font-heading">{selectedWorkflow.title}</h3>
                    <p className="text-xs text-slate-400 font-mono">{selectedWorkflow.category} Domain Workflow Execution</p>
                  </div>
                </div>

                {!isExecuting && (
                  <button
                    onClick={() => {
                      setSelectedWorkflow(null);
                      setActiveRunResult(null);
                    }}
                    className="p-1.5 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                )}
              </div>

              {/* Modal Body */}
              <div className="p-6 overflow-y-auto flex-1 space-y-6">
                {/* STATE A: PARAMETER INPUT FORM */}
                {!isExecuting && !activeRunResult && (
                  <div className="space-y-5">
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {selectedWorkflow.description}
                    </p>

                    {/* Inputs */}
                    <div className="space-y-3 pt-2">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-400 font-mono">
                        Execution Parameters
                      </h4>

                      {selectedWorkflow.inputs_schema && selectedWorkflow.inputs_schema.length > 0 ? (
                        selectedWorkflow.inputs_schema.map((inp) => (
                          <div key={inp.key} className="space-y-1.5">
                            <label className="text-xs font-semibold text-slate-300 flex items-center gap-1">
                              {inp.label}
                              {inp.required && <span className="text-cyan-400">*</span>}
                            </label>
                            {inp.type === 'select' ? (
                              <select
                                value={inputValues[inp.key] || ''}
                                onChange={(e) => setInputValues({ ...inputValues, [inp.key]: e.target.value })}
                                className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-cyan-500/60 shadow-inner"
                              >
                                {inp.options.map((opt) => (
                                  <option key={opt} value={opt}>
                                    {opt}
                                  </option>
                                ))}
                              </select>
                            ) : (
                              <input
                                type="text"
                                value={inputValues[inp.key] || ''}
                                onChange={(e) => setInputValues({ ...inputValues, [inp.key]: e.target.value })}
                                placeholder={inp.placeholder || ''}
                                className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-cyan-500/60 shadow-inner"
                              />
                            )}
                          </div>
                        ))
                      ) : (
                        <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-400">
                          This workflow executes using active document corpus defaults.
                        </div>
                      )}
                    </div>

                    {/* Pipeline Steps Preview */}
                    <div className="pt-3 border-t border-slate-800">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono mb-2.5">
                        Pipeline Execution Sequence
                      </h4>
                      <div className="space-y-2">
                        {selectedWorkflow.steps.map((st, idx) => (
                          <div key={idx} className="flex items-center gap-3 text-xs text-slate-300">
                            <span className="w-5 h-5 rounded-full bg-slate-800 border border-slate-700 text-[10px] font-mono font-bold flex items-center justify-center text-cyan-400 shrink-0 shadow">
                              {idx + 1}
                            </span>
                            <span>{st}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* STATE B: LIVE PIPELINE EXECUTION ANIMATION */}
                {isExecuting && !activeRunResult && (
                  <div className="py-8 space-y-6 text-center">
                    <div className="relative w-24 h-24 mx-auto">
                      <div className="absolute inset-0 rounded-full border-4 border-slate-800" />
                      <div
                        className="absolute inset-0 rounded-full border-4 border-cyan-400 border-t-transparent animate-spin"
                      />
                      <div className="absolute inset-0 flex items-center justify-center font-mono font-bold text-sm text-cyan-300">
                        {executionProgress}%
                      </div>
                    </div>

                    <div>
                      <h4 className="text-base font-bold text-slate-100 animate-pulse font-heading">
                        Executing AI Reasoning & Hybrid Search Pipeline...
                      </h4>
                      <p className="text-xs text-cyan-400 mt-1 font-mono">
                        {selectedWorkflow.steps[currentStepIndex] || 'Finalizing report artifacts...'}
                      </p>
                    </div>

                    {/* Framer Motion Pipeline Steps Progress */}
                    <div className="max-w-md mx-auto space-y-2 text-left pt-2">
                      {selectedWorkflow.steps.map((st, idx) => {
                        const isDone = idx < currentStepIndex;
                        const isCurrent = idx === currentStepIndex;
                        return (
                          <motion.div
                            key={idx}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.08 }}
                            className={`p-3 rounded-xl border flex items-center justify-between text-xs font-mono transition-all ${
                              isDone
                                ? 'bg-emerald-950/40 border-emerald-800/60 text-emerald-300'
                                : isCurrent
                                ? 'bg-cyan-950/60 border-cyan-500/60 text-cyan-300 shadow-lg shadow-cyan-500/10'
                                : 'bg-slate-950/40 border-slate-800 text-slate-500'
                            }`}
                          >
                            <span className="flex items-center gap-2.5">
                              {isDone ? (
                                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                              ) : isCurrent ? (
                                <RefreshCw className="w-4 h-4 text-cyan-400 animate-spin" />
                              ) : (
                                <span className="w-4 h-4 rounded-full bg-slate-800 text-[10px] flex items-center justify-center text-slate-400">
                                  {idx + 1}
                                </span>
                              )}
                              <span>{st}</span>
                            </span>
                            <span className="text-[10px]">
                              {isDone ? 'COMPLETED' : isCurrent ? 'EXECUTING' : 'PENDING'}
                            </span>
                          </motion.div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* STATE C: REPORT RESULTS & EXPORT OPTIONS */}
                {activeRunResult && (
                  <div className="space-y-6">
                    {/* Key Takeaways */}
                    <div className="p-4.5 rounded-2xl bg-gradient-to-r from-cyan-950/40 via-slate-900/60 to-purple-950/40 border border-cyan-500/30 space-y-2 shadow-lg">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-400 flex items-center gap-2 font-mono">
                        <Sparkles className="w-4 h-4 text-cyan-400" /> Executive Takeaways
                      </h4>
                      <ul className="text-xs text-slate-200 space-y-1.5 list-disc pl-4 leading-relaxed">
                        {activeRunResult.result?.key_takeaways?.map((kt, i) => (
                          <li key={i}>{kt}</li>
                        ))}
                      </ul>
                    </div>

                    {/* Report Content View */}
                    <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800 text-slate-200 text-xs leading-relaxed space-y-3 font-sans whitespace-pre-wrap shadow-inner">
                      {activeRunResult.result?.report_markdown}
                    </div>
                  </div>
                )}
              </div>

              {/* Modal Footer */}
              <div className="p-5 border-t border-slate-800 bg-slate-950/70 flex items-center justify-between gap-3">
                {!activeRunResult && !isExecuting && (
                  <>
                    <button
                      onClick={() => setSelectedWorkflow(null)}
                      className="px-4.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold cursor-pointer"
                    >
                      Cancel
                    </button>
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={handleStartExecution}
                      className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-600 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-500/25 cursor-pointer"
                    >
                      <Play className="w-4 h-4 fill-current text-slate-950" /> Execute Workflow
                    </motion.button>
                  </>
                )}

                {activeRunResult && (
                  <div className="flex items-center justify-between w-full">
                    <button
                      onClick={() => {
                        setSelectedWorkflow(null);
                        setActiveRunResult(null);
                        setIsExecuting(false);
                      }}
                      className="px-4.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold cursor-pointer"
                    >
                      Close Window
                    </button>

                    <div className="flex items-center gap-3">
                      <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() =>
                          handleExportDOCX(
                            selectedWorkflow.title,
                            selectedWorkflow.category,
                            activeRunResult.result?.report_markdown || ''
                          )
                        }
                        disabled={isExportingDocx}
                        className="px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 hover:border-cyan-500/50 text-slate-200 text-xs font-semibold flex items-center gap-2 shadow-md cursor-pointer"
                      >
                        <FileSpreadsheet className="w-4 h-4 text-cyan-400" />
                        <span>{isExportingDocx ? 'Generating DOCX...' : 'Export DOCX'}</span>
                      </motion.button>

                      <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() =>
                          handleExportPDF(
                            selectedWorkflow.title,
                            selectedWorkflow.category,
                            activeRunResult.result?.report_markdown || ''
                          )
                        }
                        disabled={isExportingPdf}
                        className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-600 text-slate-950 font-extrabold text-xs flex items-center gap-2 shadow-lg shadow-cyan-500/25 cursor-pointer"
                      >
                        <Download className="w-4 h-4 text-slate-950" />
                        <span>{isExportingPdf ? 'Generating PDF...' : 'Export PDF'}</span>
                      </motion.button>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* INSPECT HISTORY RUN DRAWER / MODAL */}
      <AnimatePresence>
        {inspectRun && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-xl">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-slate-900 border border-slate-800 rounded-3xl max-w-3xl w-full max-h-[85vh] overflow-hidden flex flex-col shadow-2xl"
            >
              <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/70">
                <div>
                  <h3 className="text-base font-bold text-slate-100 font-heading">{inspectRun.title}</h3>
                  <p className="text-xs text-slate-400 font-mono">Run ID: {inspectRun.run_id} | {inspectRun.created_at}</p>
                </div>
                <button
                  onClick={() => setInspectRun(null)}
                  className="p-1.5 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="p-6 overflow-y-auto flex-1 space-y-4 text-xs text-slate-200 whitespace-pre-wrap font-sans bg-slate-950 shadow-inner">
                {inspectRun.result?.report_markdown || 'No report content recorded for this run.'}
              </div>

              <div className="p-4.5 border-t border-slate-800 bg-slate-950/70 flex items-center justify-between">
                <button
                  onClick={() => setInspectRun(null)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold cursor-pointer"
                >
                  Close
                </button>

                <div className="flex items-center gap-3">
                  <button
                    onClick={() =>
                      handleExportDOCX(inspectRun.title, inspectRun.category, inspectRun.result?.report_markdown || '')
                    }
                    className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 hover:border-cyan-500/50 text-slate-200 text-xs font-semibold flex items-center gap-2 cursor-pointer"
                  >
                    <FileSpreadsheet className="w-4 h-4 text-cyan-400" /> Export DOCX
                  </button>

                  <button
                    onClick={() =>
                      handleExportPDF(inspectRun.title, inspectRun.category, inspectRun.result?.report_markdown || '')
                    }
                    className="px-4.5 py-2 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs flex items-center gap-2 cursor-pointer shadow-md shadow-cyan-500/20"
                  >
                    <Download className="w-4 h-4" /> Export PDF
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* CREATE CUSTOM TEMPLATE MODAL */}
      <AnimatePresence>
        {isTemplateModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-xl">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-slate-900 border border-slate-800 rounded-3xl max-w-lg w-full p-6 shadow-2xl space-y-4"
            >
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <h3 className="text-base font-bold text-slate-100 font-heading">Create Custom AI Workflow</h3>
                <button
                  onClick={() => setIsTemplateModalOpen(false)}
                  className="p-1 rounded text-slate-400 hover:text-white"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <form onSubmit={handleCreateCustomTemplate} className="space-y-3.5 text-xs">
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Workflow Title</label>
                  <input
                    type="text"
                    required
                    value={newTemplateData.title}
                    onChange={(e) => setNewTemplateData({ ...newTemplateData, title: e.target.value })}
                    placeholder="e.g. Contract Renewal Risk Scanner"
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 focus:outline-none focus:border-cyan-500 shadow-inner"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Description</label>
                  <textarea
                    required
                    rows={2}
                    value={newTemplateData.description}
                    onChange={(e) => setNewTemplateData({ ...newTemplateData, description: e.target.value })}
                    placeholder="Briefly describe what this workflow accomplishes..."
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 focus:outline-none focus:border-cyan-500 shadow-inner"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Category</label>
                  <select
                    value={newTemplateData.category}
                    onChange={(e) => setNewTemplateData({ ...newTemplateData, category: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 focus:outline-none focus:border-cyan-500 shadow-inner"
                  >
                    <option value="HR">HR</option>
                    <option value="Finance">Finance</option>
                    <option value="Legal">Legal</option>
                    <option value="Engineering">Engineering</option>
                    <option value="Management">Management</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Pipeline Steps (1 per line)</label>
                  <textarea
                    required
                    rows={3}
                    value={newTemplateData.steps}
                    onChange={(e) => setNewTemplateData({ ...newTemplateData, steps: e.target.value })}
                    placeholder="Step 1: Scan contracts&#10;Step 2: Extract termination clause&#10;Step 3: Generate risk score"
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 font-mono text-[11px] focus:outline-none focus:border-cyan-500 shadow-inner"
                  />
                </div>

                <div className="pt-4 flex items-center justify-end gap-3 border-t border-slate-800">
                  <button
                    type="button"
                    onClick={() => setIsTemplateModalOpen(false)}
                    className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 font-semibold cursor-pointer"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl bg-cyan-500 text-slate-950 font-bold cursor-pointer shadow-md shadow-cyan-500/20"
                  >
                    Save Template
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
