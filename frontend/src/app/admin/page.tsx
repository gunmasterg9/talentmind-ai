"use client";

import React from "react";
import { Navigation } from "@/components/Navigation";
import { AIAgentWidget } from "@/components/AIAgentWidget";
import { Shield, Activity, Cpu, Database, Server, Zap } from "lucide-react";

export default function AdminPage() {
  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex">
      <Navigation />
      <main className="flex-1 ml-72 p-8 overflow-y-auto">
        <header className="mb-8">
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            System Admin & AI Monitoring Panel <Shield className="w-6 h-6 text-rose-500" />
          </h1>
          <p className="text-xs text-slate-400 mt-1">Real-time telemetry, multi-provider LLM token usage, database connections, and system health.</p>
        </header>

        <div className="grid grid-cols-4 gap-5 mb-8">
          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <div className="flex justify-between items-center">
              <span className="text-xs font-semibold text-slate-400 uppercase">System Status</span>
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping" />
            </div>
            <h3 className="text-2xl font-black text-emerald-400 mt-2">100% Operational</h3>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <span className="text-xs font-semibold text-slate-400 uppercase">Active LLM Tokens (24h)</span>
            <h3 className="text-2xl font-black text-rose-400 mt-2">1,248,900</h3>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <span className="text-xs font-semibold text-slate-400 uppercase">Vector Indices</span>
            <h3 className="text-2xl font-black text-blue-400 mt-2">Qdrant Active</h3>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <span className="text-xs font-semibold text-slate-400 uppercase">Knowledge Graph Nodes</span>
            <h3 className="text-2xl font-black text-purple-400 mt-2">14,850 Nodes</h3>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800">
          <h3 className="text-base font-bold text-white mb-4">Connected Infrastructure Services</h3>
          <div className="grid grid-cols-3 gap-4 text-xs">
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center gap-3">
              <Server className="w-5 h-5 text-rose-500" />
              <div>
                <p className="font-bold text-white">FastAPI Microservices</p>
                <p className="text-slate-400">Port 8000 • Healthy</p>
              </div>
            </div>
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center gap-3">
              <Database className="w-5 h-5 text-blue-500" />
              <div>
                <p className="font-bold text-white">PostgreSQL & Redis</p>
                <p className="text-slate-400">Connected</p>
              </div>
            </div>
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center gap-3">
              <Zap className="w-5 h-5 text-amber-500" />
              <div>
                <p className="font-bold text-white">LangGraph Multi-Agent Runtime</p>
                <p className="text-slate-400">12 Agents Online</p>
              </div>
            </div>
          </div>
        </div>
      </main>
      <AIAgentWidget />
    </div>
  );
}
