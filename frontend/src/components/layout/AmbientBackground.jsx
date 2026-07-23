import React from 'react';
import { motion } from 'framer-motion';

export default function AmbientBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden select-none">
      {/* Radial Mesh Gradient Nodes */}
      <motion.div
        animate={{
          scale: [1, 1.15, 1],
          x: [0, 30, 0],
          y: [0, -20, 0],
        }}
        transition={{ duration: 15, repeat: Infinity, ease: 'easeInOut' }}
        className="absolute top-[-10%] left-[15%] w-[700px] h-[700px] bg-gradient-to-br from-cyan-500/15 via-blue-600/10 to-transparent rounded-full blur-[180px]"
      />

      <motion.div
        animate={{
          scale: [1, 1.2, 1],
          x: [0, -40, 0],
          y: [0, 30, 0],
        }}
        transition={{ duration: 18, repeat: Infinity, ease: 'easeInOut', delay: 2 }}
        className="absolute bottom-[-15%] right-[10%] w-[750px] h-[750px] bg-gradient-to-tl from-fuchsia-600/15 via-purple-600/10 to-transparent rounded-full blur-[180px]"
      />

      <motion.div
        animate={{
          scale: [1, 1.1, 1],
          x: [0, 25, 0],
          y: [0, 25, 0],
        }}
        transition={{ duration: 20, repeat: Infinity, ease: 'easeInOut', delay: 4 }}
        className="absolute top-[35%] right-[30%] w-[500px] h-[500px] bg-gradient-to-r from-violet-600/10 to-indigo-600/10 rounded-full blur-[150px]"
      />

      {/* Cyber Grid Lines Texture overlay */}
      <div className="absolute inset-0 bg-[radial-gradient(#38bdf8_1px,transparent_1px)] [background-size:32px_32px] opacity-[0.03]" />
    </div>
  );
}
