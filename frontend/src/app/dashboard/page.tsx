"use client";

import React, { useEffect, useState } from "react";
import { Navigation } from "@/components/Navigation";
import { AIAgentWidget } from "@/components/AIAgentWidget";
import { 
  Activity, Award, Briefcase, TrendingUp, Sparkles, Target, 
  CheckCircle2, ArrowUpRight, ShieldAlert, FileCheck, BrainCircuit
} from "lucide-react";

export default function CandidateDashboard() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/dashboard/candidate")
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(() => {
        setStats({
          career_health_score: 88.5,
          ats_score: 84.0,
          skill_index: 90.0,
          interview_score: 86.5,
          application_success_rate: "38%",
          learning_progress: "65%",
          network_growth: "+14 connections this week",
          salary_growth_projection: "+24% ($165,000 median)",
          active_jobs_count: 14,
          recent_applications: [
            { id: "APP-1", job_title: "Lead AI Autonomous Systems Engineer", company: "ScaleAI Next", status: "Applied", fit_score: 96.2 },
            { id: "APP-2", job_title: "Senior Staff Backend Engineer", company: "DeepMind Partner", status: "Interviewing", fit_score: 92.8 }
          ]
        });
      });
  }, []);

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex">
      <Navigation />
      <main className="flex-1 ml-72 p-8 overflow-y-auto">
        {/* Top Header */}
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
              Autonomous Career Dashboard <Sparkles className="w-5 h-5 text-rose-500 animate-pulse" />
            </h1>
            <p className="text-xs text-slate-400 mt-1">AI Autonomous Ecosystem continuously optimizing your profile and market placement.</p>
          </div>
          <div className="flex gap-3">
            <span className="px-3.5 py-1.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              12 Agents Active
            </span>
          </div>
        </header>

        {/* Career Metrics 4-Grid */}
        <div className="grid grid-cols-4 gap-5 mb-8">
          <div className="p-5 rounded-2xl bg-slate-900/60 border border-rose-500/20 backdrop-blur-xl relative overflow-hidden group hover:border-rose-500/40 transition-all">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Career Health Score</p>
                <h3 className="text-3xl font-black text-white mt-2">{stats?.career_health_score || 88.5}<span className="text-sm text-rose-400">/100</span></h3>
              </div>
              <div className="p-3 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
                <Activity className="w-5 h-5" />
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2 text-[11px] text-emerald-400 font-medium">
              <TrendingUp className="w-3.5 h-3.5" /> +4.2% from last month
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-xl hover:border-slate-700 transition-all">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">ATS Resume Fit Score</p>
                <h3 className="text-3xl font-black text-white mt-2">{stats?.ats_score || 84.0}%</h3>
              </div>
              <div className="p-3 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
                <FileCheck className="w-5 h-5" />
              </div>
            </div>
            <p className="mt-4 text-[11px] text-slate-400">Optimized for Senior AI Roles</p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-xl hover:border-slate-700 transition-all">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Skill Index Score</p>
                <h3 className="text-3xl font-black text-white mt-2">{stats?.skill_index || 90.0}</h3>
              </div>
              <div className="p-3 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
                <BrainCircuit className="w-5 h-5" />
              </div>
            </div>
            <p className="mt-4 text-[11px] text-slate-400">Top 5% in FastAPI & Multi-Agents</p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-xl hover:border-slate-700 transition-all">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Interview Rating</p>
                <h3 className="text-3xl font-black text-white mt-2">{stats?.interview_score || 86.5}%</h3>
              </div>
              <div className="p-3 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
                <Award className="w-5 h-5" />
              </div>
            </div>
            <p className="mt-4 text-[11px] text-slate-400">High Confidence & Tone Clarity</p>
          </div>
        </div>

        {/* Main 2-Column Section */}
        <div className="grid grid-cols-3 gap-8">
          {/* Active Workflows & Opportunities */}
          <div className="col-span-2 space-y-6">
            <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-xl">
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h3 className="text-base font-bold text-white">Active Autonomous AI Applications</h3>
                  <p className="text-xs text-slate-400 mt-0.5">Jobs auto-matched and tracked by Job Discovery Agent.</p>
                </div>
              </div>
              <div className="space-y-3">
                {stats?.recent_applications.map((app: any) => (
                  <div key={app.id} className="p-4 rounded-xl bg-slate-950/80 border border-slate-800/60 flex justify-between items-center hover:border-slate-700 transition-all">
                    <div>
                      <h4 className="text-sm font-bold text-white">{app.job_title}</h4>
                      <p className="text-xs text-slate-400">{app.company} • Auto-Matched</p>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <span className="text-xs font-bold text-emerald-400">{app.fit_score}% Fit</span>
                        <p className="text-[10px] text-slate-400 uppercase">{app.status}</p>
                      </div>
                      <ArrowUpRight className="w-4 h-4 text-slate-500" />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* AI Autonomous Log & Recommendations */}
          <div className="space-y-6">
            <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900/90 to-slate-950 border border-rose-500/20 shadow-xl">
              <h3 className="text-sm font-bold text-white flex items-center gap-2 mb-4">
                <Sparkles className="w-4 h-4 text-rose-400" /> Executive AI Autonomous Log
              </h3>
              <div className="space-y-3 text-xs text-slate-300">
                <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                  <p className="font-semibold text-rose-300">Resume Agent Action</p>
                  <p className="text-[11px] text-slate-400 mt-0.5">Auto-updated profile bullets for high throughput systems.</p>
                </div>
                <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                  <p className="font-semibold text-amber-300">Skill Gap Alert</p>
                  <p className="text-[11px] text-slate-400 mt-0.5">Recommended 2-hour Neo4j Graph Cypher crash course.</p>
                </div>
                <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                  <p className="font-semibold text-emerald-300">Opportunity Monitor</p>
                  <p className="text-[11px] text-slate-400 mt-0.5">Detected $50,000 Global AI Agent Hackathon registration.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      <AIAgentWidget />
    </div>
  );
}
