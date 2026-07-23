import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

import { AuthProvider, useAuth } from './context/AuthContext';
import Sidebar from './components/layout/Sidebar';
import Header from './components/layout/Header';
import CommandPalette from './components/layout/CommandPalette';

import AmbientBackground from './components/layout/AmbientBackground';

import DashboardPage from './pages/DashboardPage';
import WorkflowsPage from './pages/WorkflowsPage';
import WorkspacePage from './pages/WorkspacePage';
import KnowledgeGraphPage from './pages/KnowledgeGraphPage';
import SaasSettingsPage from './pages/SaasSettingsPage';
import SearchPage from './pages/SearchPage';
import ChatPage from './pages/ChatPage';
import ExplorerPage from './pages/ExplorerPage';
import AnalyticsPage from './pages/AnalyticsPage';
import AdminPage from './pages/AdminPage';
import LoginPage from './pages/LoginPage';

import { fetchRegistryStats, fetchAnalytics, triggerReindex } from './services/api';

function MainApp() {
  const { user, logout, loading: authLoading } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);
  const [stats, setStats] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [isReindexing, setIsReindexing] = useState(false);
  const [toastMessage, setToastMessage] = useState(null);

  const loadStats = async () => {
    try {
      const [sRes, aRes] = await Promise.all([
        fetchRegistryStats().catch(() => ({ data: null })),
        fetchAnalytics().catch(() => ({ data: null })),
      ]);
      if (sRes.data) setStats(sRes.data);
      if (aRes.data) setAnalytics(aRes.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  const handleReindex = async () => {
    setIsReindexing(true);
    showToast('Triggered incremental indexing...');
    try {
      const res = await triggerReindex();
      const { new_files, modified_files, vectors_inserted } = res.data.result || {};
      showToast(`Re-indexing complete: ${new_files || 0} new, ${modified_files || 0} updated.`);
      loadStats();
    } catch (err) {
      showToast('Error during re-indexing.');
    } finally {
      setIsReindexing(false);
    }
  };

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 4000);
  };

  if (authLoading) {
    return (
      <div className="min-h-screen bg-[#030712] flex items-center justify-center text-cyan-400 text-sm font-mono">
        Initializing Knowledge Intelligence Node...
      </div>
    );
  }

  const renderPage = () => {
    switch (activeTab) {
      case 'dashboard':
        return (
          <DashboardPage
            stats={stats}
            analytics={analytics}
            onNavigate={setActiveTab}
            onReindex={handleReindex}
          />
        );
      case 'workflows':
        return <WorkflowsPage />;
      case 'workspace':
        return <WorkspacePage />;
      case 'knowledge-graph':
        return <KnowledgeGraphPage />;
      case 'saas-settings':
        return <SaasSettingsPage />;
      case 'search':
        return <SearchPage />;
      case 'chat':
        return <ChatPage />;
      case 'explorer':
        return <ExplorerPage />;
      case 'analytics':
        return <AnalyticsPage />;
      case 'admin':
        return <AdminPage />;
      default:
        return <DashboardPage stats={stats} analytics={analytics} onNavigate={setActiveTab} />;
    }
  };

  return (
    <div className="flex min-h-screen bg-[#030712] text-slate-100 font-sans relative overflow-hidden">
      {/* Dynamic Ambient Background Mesh */}
      <AmbientBackground />

      {/* Floating Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenCommandPalette={() => setIsCommandPaletteOpen(true)}
        user={user}
        onLogout={logout}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 z-10">
        <Header
          activeTab={activeTab}
          onReindex={handleReindex}
          isReindexing={isReindexing}
          stats={stats}
        />

        <main className="flex-1 p-6 md:p-8 overflow-y-auto">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 15, scale: 0.99 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -15, scale: 0.99 }}
              transition={{ type: 'spring', stiffness: 350, damping: 28 }}
            >
              {renderPage()}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>

      {/* Command Palette (Ctrl+K) */}
      <CommandPalette
        isOpen={isCommandPaletteOpen}
        onClose={() => setIsCommandPaletteOpen(false)}
        setActiveTab={setActiveTab}
        onReindex={handleReindex}
      />

      {/* Toast Notification */}
      <AnimatePresence>
        {toastMessage && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            className="fixed bottom-6 right-6 z-50 px-4 py-3 rounded-2xl bg-slate-900 border border-cyan-500/30 text-xs text-white shadow-2xl flex items-center gap-3 backdrop-blur-xl"
          >
            <span className="h-2 w-2 rounded-full bg-cyan-400 animate-ping" />
            <span>{toastMessage}</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
}