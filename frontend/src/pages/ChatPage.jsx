import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Send,
  Sparkles,
  Bot,
  User,
  FileText,
  Copy,
  Check,
  ChevronRight,
  HelpCircle,
  Download,
  Share2,
  Sliders
} from 'lucide-react';
import { sendChatMessage } from '../services/api';

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'ai',
      text: 'Hello! I am your Enterprise Knowledge Assistant. Ask me anything about HR policies, remote work, technical standards, or sales guidelines.',
      sources: [],
      citations: [],
    },
  ]);
  const [input, setInput] = useState('');
  const [mode, setMode] = useState('standard'); // standard | agent
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);

  const handleSend = async (e) => {
    if (e) e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setLoading(true);

    try {
      const res = await sendChatMessage(currentInput, mode);
      const aiMessage = {
        id: Date.now() + 1,
        sender: 'ai',
        text: res.data.answer,
        sources: res.data.sources || [],
        citations: res.data.citations || [],
        subQueries: res.data.sub_queries || [],
        isMultiStep: res.data.is_multi_step || false,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'ai',
          text: 'Sorry, I encountered an error connecting to the intelligence backend.',
          sources: [],
          citations: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (id, text) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)]">
      {/* Header Mode Switcher */}
      <div className="flex items-center justify-between pb-4 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400">
            <Bot className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">AI Intelligence Hub</h3>
            <p className="text-xs text-slate-400">Contextual RAG & Multi-Step Reasoning Engine</p>
          </div>
        </div>

        {/* Mode Selector */}
        <div className="flex items-center gap-2 p-1 rounded-xl bg-white/5 border border-white/10 text-xs">
          <button
            onClick={() => setMode('standard')}
            className={`px-3 py-1.5 rounded-lg font-medium transition ${
              mode === 'standard'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Standard RAG
          </button>
          <button
            onClick={() => setMode('agent')}
            className={`px-3 py-1.5 rounded-lg font-medium transition flex items-center gap-1.5 ${
              mode === 'agent'
                ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Sparkles className="h-3.5 w-3.5 text-yellow-400" />
            Agentic Reasoning
          </button>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto py-6 space-y-6 pr-2">
        {messages.map((msg) => (
          <motion.div
            key={msg.id}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex gap-4 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.sender === 'ai' && (
              <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-500 text-white flex items-center justify-center shadow-lg shrink-0 mt-1">
                <Bot className="h-5 w-5" />
              </div>
            )}

            <div
              className={`max-w-3xl rounded-3xl p-5 space-y-3 ${
                msg.sender === 'user'
                  ? 'bg-blue-600 text-white rounded-tr-none'
                  : 'glass-panel text-slate-200 rounded-tl-none'
              }`}
            >
              <div className="flex items-center justify-between gap-4 text-xs opacity-75">
                <span className="font-semibold">{msg.sender === 'user' ? 'You' : 'Knowledge AI'}</span>
                {msg.sender === 'ai' && (
                  <button
                    onClick={() => handleCopy(msg.id, msg.text)}
                    className="p-1 rounded hover:bg-white/10 transition"
                    title="Copy Answer"
                  >
                    {copiedId === msg.id ? (
                      <Check className="h-3.5 w-3.5 text-emerald-400" />
                    ) : (
                      <Copy className="h-3.5 w-3.5 text-slate-400" />
                    )}
                  </button>
                )}
              </div>

              {/* Sub-queries badge if Agent mode */}
              {msg.isMultiStep && (
                <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20 text-xs text-purple-300 space-y-1">
                  <div className="flex items-center gap-1.5 font-semibold">
                    <Sparkles className="h-3.5 w-3.5 text-yellow-400" />
                    <span>Agentic Sub-Queries Executed:</span>
                  </div>
                  <ul className="list-disc list-inside space-y-0.5 text-[11px] text-slate-300">
                    {msg.subQueries?.map((sq, idx) => (
                      <li key={idx}>{sq}</li>
                    ))}
                  </ul>
                </div>
              )}

              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.text}</p>

              {/* Citations / Sources */}
              {msg.citations?.length > 0 && (
                <div className="pt-3 border-t border-white/10 space-y-2">
                  <span className="text-xs font-semibold text-blue-400 block">Verified Sources:</span>
                  <div className="flex flex-wrap gap-2">
                    {msg.citations.map((c, i) => (
                      <div
                        key={i}
                        className="px-3 py-1.5 rounded-xl bg-white/5 border border-white/10 text-xs text-slate-300 flex items-center gap-2"
                      >
                        <FileText className="h-3.5 w-3.5 text-blue-400" />
                        <span>{c.source}</span>
                        {c.is_authoritative && (
                          <span className="px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-300 text-[10px]">
                            Authoritative
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {msg.sender === 'user' && (
              <div className="h-9 w-9 rounded-xl bg-slate-800 text-white flex items-center justify-center shrink-0 mt-1 border border-white/10">
                <User className="h-5 w-5 text-blue-400" />
              </div>
            )}
          </motion.div>
        ))}

        {loading && (
          <div className="flex gap-4 items-center">
            <div className="h-9 w-9 rounded-xl bg-blue-600/20 text-blue-400 flex items-center justify-center animate-pulse">
              <Bot className="h-5 w-5" />
            </div>
            <div className="glass-panel px-4 py-3 rounded-2xl text-xs text-slate-400 flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-blue-400 animate-spin" />
              <span>Analyzing knowledge graph & synthesizing response...</span>
            </div>
          </div>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSend} className="pt-4 border-t border-white/10 flex gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={
            mode === 'agent'
              ? 'Ask a complex multi-step question (e.g. Compare HR leave policy vs WFH policy)...'
              : 'Ask anything about company knowledge...'
          }
          className="flex-1 px-5 py-3.5 rounded-2xl bg-white/5 border border-white/10 text-white placeholder:text-slate-500 outline-none focus:border-blue-500/50 transition text-sm"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="px-6 py-3.5 rounded-2xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition shadow-lg shadow-blue-600/30 flex items-center gap-2 disabled:opacity-50 cursor-pointer"
        >
          <Send className="h-4 w-4" />
          <span>Send</span>
        </button>
      </form>
    </div>
  );
}
