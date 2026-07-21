import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, UserCheck, UserX, Trash2, Key, Users, Lock } from 'lucide-react';
import { fetchUsers, toggleUserStatus, removeUser } from '../services/api';

export default function AdminPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadUsersList = async () => {
    setLoading(true);
    try {
      const res = await fetchUsers();
      setUsers(res.data || []);
    } catch (err) {
      console.error(err);
      // Fallback demo user list if unauthenticated
      setUsers([
        { id: 1, username: 'admin', email: 'admin@knowledge.local', role: 'admin', department: 'Executive', is_active: true },
        { id: 2, username: 'hr_manager', email: 'hr@knowledge.local', role: 'user', department: 'HR', is_active: true },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsersList();
  }, []);

  const handleToggle = async (userId, currentStatus) => {
    try {
      await toggleUserStatus(userId, !currentStatus);
      loadUsersList();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (userId) => {
    if (!window.confirm('Delete user account?')) return;
    try {
      await removeUser(userId);
      loadUsersList();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-bold text-white">Admin Console & Role-Based Access Control</h3>
        <p className="text-xs text-slate-400">Manage user accounts, departmental permissions, and system access policies</p>
      </div>

      {/* Users Table */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel p-5 rounded-2xl space-y-4"
      >
        <div className="flex items-center justify-between">
          <h4 className="text-sm font-semibold text-white flex items-center gap-2">
            <Users className="h-4 w-4 text-blue-400" />
            Registered User Accounts ({users.length})
          </h4>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-white/10 text-slate-400">
                <th className="pb-3 px-2">Username</th>
                <th className="pb-3 px-2">Email</th>
                <th className="pb-3 px-2">Role</th>
                <th className="pb-3 px-2">Department</th>
                <th className="pb-3 px-2">Status</th>
                <th className="pb-3 px-2 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-white/5 transition">
                  <td className="py-3 px-2 font-medium text-white">{u.username}</td>
                  <td className="py-3 px-2 text-slate-300">{u.email}</td>
                  <td className="py-3 px-2">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${u.role === 'admin' ? 'bg-purple-500/20 text-purple-300' : 'bg-blue-500/20 text-blue-300'}`}>
                      {u.role}
                    </span>
                  </td>
                  <td className="py-3 px-2 text-slate-300">{u.department || 'All'}</td>
                  <td className="py-3 px-2">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${u.is_active ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}`}>
                      {u.is_active ? 'Active' : 'Disabled'}
                    </span>
                  </td>
                  <td className="py-3 px-2 text-right space-x-2">
                    <button
                      onClick={() => handleToggle(u.id, u.is_active)}
                      className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition"
                      title="Toggle Status"
                    >
                      {u.is_active ? <UserX className="h-4 w-4 text-amber-400" /> : <UserCheck className="h-4 w-4 text-emerald-400" />}
                    </button>
                    <button
                      onClick={() => handleDelete(u.id)}
                      className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition"
                      title="Delete User"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
}
