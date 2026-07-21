import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart3, TrendingUp, Search, Layers, ShieldCheck, Activity } from 'lucide-react';
import { fetchAnalytics } from '../services/api';

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics()
      .then((res) => setAnalytics(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const deptData = [
    { name: 'HR', count: 11, color: '#3b82f6' },
    { name: 'Policy', count: 7, color: '#06b6d4' },
    { name: 'Technical', count: 6, color: '#8b5cf6' },
    { name: 'Research', count: 8, color: '#10b981' },
    { name: 'Sales', count: 7, color: '#f59e0b' },
  ];

  const typeData = [
    { name: 'Policy', count: 14, color: '#3b82f6' },
    { name: 'SOP & Guide', count: 8, color: '#06b6d4' },
    { name: 'Manual', count: 5, color: '#8b5cf6' },
    { name: 'Report & Data', count: 12, color: '#10b981' },
  ];

  const maxDept = Math.max(...deptData.map((d) => d.count));
  const maxType = Math.max(...typeData.map((d) => d.count));

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-bold text-white">Enterprise Knowledge Intelligence Analytics</h3>
        <p className="text-xs text-slate-400">Real-time metrics on retrieval performance, document volume, and department usage</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Department Volume Chart */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-panel p-6 rounded-2xl space-y-4"
        >
          <h4 className="text-sm font-semibold text-white">Document Volume by Department</h4>

          <div className="space-y-4 pt-2">
            {deptData.map((d) => (
              <div key={d.name} className="space-y-1">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">{d.name}</span>
                  <span className="text-white font-mono">{d.count} files</span>
                </div>
                <div className="h-3.5 w-full bg-white/5 rounded-full overflow-hidden p-0.5 border border-white/5">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${(d.count / maxDept) * 100}%` }}
                    transition={{ duration: 0.8, ease: 'easeOut' }}
                    className="h-full rounded-full"
                    style={{ backgroundColor: d.color }}
                  />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Document Type Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-panel p-6 rounded-2xl space-y-4"
        >
          <h4 className="text-sm font-semibold text-white">Document Type Breakdown</h4>

          <div className="space-y-4 pt-2">
            {typeData.map((t) => (
              <div key={t.name} className="space-y-1">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-300">{t.name}</span>
                  <span className="text-white font-mono">{t.count} items</span>
                </div>
                <div className="h-3.5 w-full bg-white/5 rounded-full overflow-hidden p-0.5 border border-white/5">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${(t.count / maxType) * 100}%` }}
                    transition={{ duration: 0.8, ease: 'easeOut' }}
                    className="h-full rounded-full"
                    style={{ backgroundColor: t.color }}
                  />
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
