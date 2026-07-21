import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Folder,
  FolderOpen,
  FileText,
  Upload,
  Trash2,
  Eye,
  RefreshCw,
  Search,
  CheckCircle,
  Clock,
  ShieldCheck,
  X,
  Plus
} from 'lucide-react';
import { fetchDocuments, uploadDocument, deleteDocument } from '../services/api';

export default function ExplorerPage() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFolder, setSelectedFolder] = useState('all');
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadFile, setUploadFile] = useState(null);
  const [uploadCollection, setUploadCollection] = useState('general');
  const [uploading, setUploading] = useState(false);

  const folders = [
    { id: 'all', name: 'All Documents' },
    { id: 'hr', name: 'HR Policies & Forms' },
    { id: 'policy', name: 'Company Policies' },
    { id: 'technical', name: 'Technical & Architecture' },
    { id: 'sales', name: 'Sales & Pricing' },
    { id: 'research', name: 'Research & User Data' },
  ];

  const loadDocs = async () => {
    setLoading(true);
    try {
      const params = selectedFolder !== 'all' ? { collection: selectedFolder } : {};
      const res = await fetchDocuments(params);
      setDocuments(res.data.documents || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocs();
  }, [selectedFolder]);

  const handleDelete = async (filePath) => {
    if (!window.confirm(`Delete document: ${filePath}?`)) return;
    try {
      await deleteDocument(filePath);
      loadDocs();

      if (selectedDoc?.file_path === filePath) {
        setSelectedDoc(null);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    if (!uploadFile) return;

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', uploadFile);
      formData.append('collection', uploadCollection);

      await uploadDocument(formData);
      setShowUploadModal(false);
      setUploadFile(null);
      loadDocs();
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Action Header */}
      <div className="flex items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-bold text-white">Document Registry & Vault Explorer</h3>
          <p className="text-xs text-slate-400">Single source of truth for all tracked enterprise assets</p>
        </div>

        <button
          onClick={() => setShowUploadModal(true)}
          className="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition shadow-lg shadow-blue-600/30 flex items-center gap-2 cursor-pointer"
        >
          <Upload className="h-4 w-4" />
          <span>Upload Document</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar Folder Navigation */}
        <div className="glass-panel p-4 rounded-2xl space-y-1">
          <p className="px-3 text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">
            Collections & Folders
          </p>
          {folders.map((f) => {
            const isSelected = selectedFolder === f.id;
            return (
              <button
                key={f.id}
                onClick={() => setSelectedFolder(f.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs transition ${
                  isSelected
                    ? 'bg-blue-600/20 text-blue-400 font-semibold border border-blue-500/30'
                    : 'text-slate-400 hover:bg-white/5 hover:text-white'
                }`}
              >
                {isSelected ? <FolderOpen className="h-4 w-4 text-blue-400" /> : <Folder className="h-4 w-4 text-slate-400" />}
                <span>{f.name}</span>
              </button>
            );
          })}
        </div>

        {/* File Table */}
        <div className="glass-panel p-5 rounded-2xl lg:col-span-3 space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400 border-b border-white/10 pb-3">
            <span>Showing {documents.length} registered documents</span>
            <button onClick={loadDocs} className="hover:text-white transition">
              <RefreshCw className="h-3.5 w-3.5" />
            </button>
          </div>

          {loading ? (
            <div className="py-12 text-center text-xs text-slate-400">Loading document vault...</div>
          ) : documents.length === 0 ? (
            <div className="py-12 text-center text-xs text-slate-500">No documents found in this folder</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-white/10 text-slate-400 font-medium">
                    <th className="pb-3 px-2">Document Name</th>
                    <th className="pb-3 px-2">Collection</th>
                    <th className="pb-3 px-2">Status</th>
                    <th className="pb-3 px-2">Version</th>
                    <th className="pb-3 px-2 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {documents.map((doc) => (
                    <tr key={doc.file_path} className="hover:bg-white/5 transition">
                      <td className="py-3 px-2 font-medium text-white flex items-center gap-2">
                        <FileText className="h-4 w-4 text-blue-400 shrink-0" />
                        <span className="truncate max-w-xs">{doc.file_name}</span>
                      </td>
                      <td className="py-3 px-2 text-slate-300 capitalize">{doc.collection}</td>
                      <td className="py-3 px-2">
                        <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          {doc.vector_status}
                        </span>
                      </td>
                      <td className="py-3 px-2 font-mono text-slate-300">v{doc.version || 1}.0</td>
                      <td className="py-3 px-2 text-right space-x-2">
                        <button
                          onClick={() => setSelectedDoc(doc)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-blue-400 hover:bg-blue-500/10 transition"
                          title="Inspect Metadata"
                        >
                          <Eye className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(doc.file_path)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition"
                          title="Delete Document"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* Metadata Inspector Drawer */}
      <AnimatePresence>
        {selectedDoc && (
          <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/80 backdrop-blur-md">
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              className="w-full max-w-md h-full bg-slate-900 border-l border-white/10 p-6 overflow-y-auto space-y-6 shadow-2xl"
            >
              <div className="flex items-center justify-between pb-4 border-b border-white/10">
                <h3 className="text-sm font-bold text-white">Metadata Inspector</h3>
                <button onClick={() => setSelectedDoc(null)} className="p-1 rounded text-slate-400 hover:text-white">
                  <X className="h-5 w-5" />
                </button>
              </div>

              <div>
                <h4 className="text-base font-semibold text-white">{selectedDoc.file_name}</h4>
                <p className="text-xs text-slate-400 font-mono mt-1">{selectedDoc.file_path}</p>
              </div>

              {selectedDoc.metadata ? (
                <div className="space-y-4 text-xs">
                  <div className="p-3 rounded-xl bg-white/5 space-y-2">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Department:</span>
                      <span className="text-white font-semibold">{selectedDoc.metadata.department || 'General'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Document Type:</span>
                      <span className="text-white font-semibold">{selectedDoc.metadata.document_type || 'Policy'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Status:</span>
                      <span className="text-emerald-400 font-semibold">{selectedDoc.metadata.status || 'Active'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Authority Score:</span>
                      <span className="text-blue-400 font-semibold">{selectedDoc.metadata.authority_score || 100}/100</span>
                    </div>
                  </div>

                  {selectedDoc.metadata.summary && (
                    <div>
                      <span className="text-slate-400 block mb-1 font-semibold">Summary:</span>
                      <p className="p-3 rounded-xl bg-white/5 text-slate-300 leading-relaxed">
                        {selectedDoc.metadata.summary}
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-xs text-slate-500">No extracted metadata available for this file.</p>
              )}
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* Upload Modal */}
      <AnimatePresence>
        {showUploadModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="w-full max-w-md p-6 rounded-3xl bg-slate-900 border border-white/10 shadow-2xl space-y-5"
            >
              <div className="flex items-center justify-between pb-3 border-b border-white/10">
                <h3 className="text-sm font-bold text-white">Upload New Document</h3>
                <button onClick={() => setShowUploadModal(false)} className="p-1 rounded text-slate-400 hover:text-white">
                  <X className="h-4 w-4" />
                </button>
              </div>

              <form onSubmit={handleUploadSubmit} className="space-y-4 text-xs">
                <div>
                  <label className="text-slate-300 block mb-1.5">Collection Folder:</label>
                  <select
                    value={uploadCollection}
                    onChange={(e) => setUploadCollection(e.target.value)}
                    className="w-full p-2.5 rounded-xl bg-white/5 border border-white/10 text-white outline-none"
                  >
                    <option value="hr" className="bg-slate-900">HR</option>
                    <option value="policy" className="bg-slate-900">Policy</option>
                    <option value="technical" className="bg-slate-900">Technical</option>
                    <option value="sales" className="bg-slate-900">Sales</option>
                    <option value="research" className="bg-slate-900">Research</option>
                    <option value="general" className="bg-slate-900">General</option>
                  </select>
                </div>

                <div>
                  <label className="text-slate-300 block mb-1.5">Select File (.txt, .pdf, .docx, .json):</label>
                  <input
                    type="file"
                    required
                    onChange={(e) => setUploadFile(e.target.files[0])}
                    className="w-full p-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 file:mr-4 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:bg-blue-600 file:text-white"
                  />
                </div>

                <div className="pt-3 flex gap-2">
                  <button
                    type="submit"
                    disabled={uploading}
                    className="flex-1 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold transition cursor-pointer"
                  >
                    {uploading ? 'Uploading & Indexing...' : 'Upload & Trigger Indexing'}
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
