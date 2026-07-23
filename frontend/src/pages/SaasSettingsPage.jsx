import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Key, Building, ShieldCheck, Copy, Plus, RefreshCw, CheckCircle2, Zap } from 'lucide-react';
import { fetchOrganizationInfo, fetchApiKeys, createApiKey } from '../services/api';

export default function SaasSettingsPage() {
  const [org, setOrg] = useState(null);
  const [apiKeys, setApiKeys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newKeyName, setNewKeyName] = useState('');
  const [generatedKey, setGeneratedKey] = useState(null);

  const loadSaaSData = async () => {
    setLoading(true);
    try {
      const [oRes, kRes] = await Promise.all([
        fetchOrganizationInfo().catch(() => ({ data: null })),
        fetchApiKeys().catch(() => ({ data: { keys: [] } }))
      ]);
      if (oRes.data) setOrg(oRes.data);
      if (kRes.data?.keys) setApiKeys(kRes.data.keys);
    } catch (err) {
      console.error('Error loading SaaS data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSaaSData();
  }, []);

  const handleCreateKey = async (e) => {
    e.preventDefault();
    try {
      const res = await createApiKey(newKeyName || 'Developer Key');
      setGeneratedKey(res.data.api_key);
      setNewKeyName('');
      loadSaaSData();
    } catch (err) {
      console.error('Error creating key:', err);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="px-3 py-1 rounded-lg bg-gradient-to-r from-emerald-500/20 to-cyan-500/20 text-emerald-300 font-mono text-xs font-bold border border-emerald-500/30">
              PHASE 10 SAAS ARCHITECTURE
            </span>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-100 tracking-tight font-heading shimmer-text">
              SaaS Multi-Tenancy & API Keys
            </h1>
          </div>
          <p className="text-xs md:text-sm text-slate-400 mt-1">
            Commercial enterprise workspace settings, multi-tenant organization, and REST API Key access.
          </p>
        </div>
      </div>

      {/* Organization Info Card */}
      <div className="glass-panel rounded-3xl p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-2xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <Building className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-100 font-heading">{org?.name || 'Acme Enterprise Org'}</h3>
              <p className="text-xs text-slate-400 font-mono">Org ID: {org?.org_id || 'org-84920'}</p>
            </div>
          </div>

          <span className="px-3.5 py-1.5 rounded-full bg-emerald-950/80 text-emerald-300 border border-emerald-800/50 font-mono text-xs font-bold uppercase">
            {org?.tier || 'Enterprise'} Plan Active
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-3 border-t border-slate-800">
          <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800">
            <span className="text-[10px] font-mono text-slate-400 uppercase">Document Storage Limit</span>
            <p className="text-lg font-bold text-slate-100 font-mono">{org?.max_documents || 5000} Documents</p>
          </div>
          <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800">
            <span className="text-[10px] font-mono text-slate-400 uppercase">API Rate Limit</span>
            <p className="text-lg font-bold text-slate-100 font-mono">10,000 req / min</p>
          </div>
          <div className="p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800">
            <span className="text-[10px] font-mono text-slate-400 uppercase">SLA & Security</span>
            <p className="text-lg font-bold text-emerald-400 font-mono">99.99% SOC 2</p>
          </div>
        </div>
      </div>

      {/* API Key Management */}
      <div className="glass-panel rounded-3xl p-6 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
          <div>
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2 font-heading">
              <Key className="w-5 h-5 text-cyan-400" /> Developer REST API Keys
            </h3>
            <p className="text-xs text-slate-400 mt-1">Authenticate external application integrations using `x-api-key` header.</p>
          </div>
        </div>

        {/* Generate Key Form */}
        <form onSubmit={handleCreateKey} className="flex gap-3">
          <input
            type="text"
            required
            value={newKeyName}
            onChange={(e) => setNewKeyName(e.target.value)}
            placeholder="Key description (e.g. Production Backend Service)..."
            className="flex-1 px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
          />
          <button
            type="submit"
            className="px-5 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs flex items-center gap-2 cursor-pointer shadow-md"
          >
            <Plus className="w-4 h-4 text-slate-950" /> Generate Key
          </button>
        </form>

        {generatedKey && (
          <div className="p-4 rounded-2xl bg-emerald-950/40 border border-emerald-800/60 text-xs space-y-2">
            <span className="font-bold text-emerald-300">New API Key Created (Copy now, will not be shown again):</span>
            <div className="p-3 rounded-xl bg-slate-950 text-cyan-300 font-mono select-all flex items-center justify-between border border-emerald-800/40">
              <span>{generatedKey}</span>
              <button
                onClick={() => navigator.clipboard.writeText(generatedKey)}
                className="px-2.5 py-1 rounded bg-emerald-900 text-emerald-200 hover:bg-emerald-800 text-[10px] font-bold"
              >
                Copy
              </button>
            </div>
          </div>
        )}

        {/* Existing Keys Table */}
        <div className="overflow-x-auto pt-2">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/60 text-slate-400 uppercase font-mono text-[10px] border-b border-slate-800">
              <tr>
                <th className="px-4 py-3">Key Name</th>
                <th className="px-4 py-3">API Key</th>
                <th className="px-4 py-3">Role</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Created At</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {apiKeys.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-slate-500 text-xs">
                    No active API keys found. Generate one above!
                  </td>
                </tr>
              ) : (
                apiKeys.map((k) => (
                  <tr key={k.key_id} className="hover:bg-slate-800/40">
                    <td className="px-4 py-3 font-semibold text-slate-100">{k.name}</td>
                    <td className="px-4 py-3 text-cyan-400">{k.masked_key}</td>
                    <td className="px-4 py-3 text-slate-400">{k.role}</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800/50 text-[10px]">
                        Active
                      </span>
                    </td>
                    <td className="px-4 py-3 text-slate-400">{k.created_at.slice(0, 16)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
