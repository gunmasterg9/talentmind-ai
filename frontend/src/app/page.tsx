"use client";

import React from "react";
import Link from "next/link";
import { Sparkles, ArrowRight, Bot, Shield, Briefcase, Users, FileText, Compass, Activity } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#070a12] text-slate-100 selection:bg-rose-900 selection:text-rose-200">
      {/* Navigation */}
      <header className="max-w-7xl mx-auto px-6 py-6 flex justify-between items-center border-b border-slate-800/60">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 to-amber-400 p-0.5 shadow-lg shadow-rose-500/20">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-rose-500 animate-pulse" />
            </div>
          </div>
          <span className="font-extrabold text-xl tracking-tight text-white">REDROB <span className="text-rose-500">AI OS</span></span>
        </div>
        <div className="flex gap-4 items-center">
          <Link href="/dashboard" className="px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-bold text-slate-200 transition-colors">
            Candidate HQ
          </Link>
          <Link href="/recruiter" className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-rose-600 to-pink-600 hover:from-rose-500 hover:to-pink-500 text-xs font-bold text-white shadow-lg shadow-rose-500/25 transition-all">
            Recruiter Portal
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-5xl mx-auto px-6 py-24 text-center relative">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-semibold mb-8">
          <Sparkles className="w-4 h-4" /> The Autonomous AI Career Operating System
        </div>
        <h1 className="text-5xl sm:text-6xl font-black text-white tracking-tight leading-tight">
          Don't Search Jobs. <br />
          <span className="bg-gradient-to-r from-rose-400 via-pink-400 to-amber-400 bg-clip-text text-transparent">Let Autonomous AI Work 24x7 For You.</span>
        </h1>
        <p className="max-w-2xl mx-auto text-slate-400 text-base mt-6 leading-relaxed">
          Redrob orchestrates 12 specialized autonomous AI agents continuously monitoring jobs, optimizing ATS resumes, predicting salary growth, and preparing mock interviews.
        </p>

        <div className="mt-10 flex justify-center gap-4">
          <Link href="/dashboard" className="px-8 py-4 rounded-2xl bg-gradient-to-r from-rose-600 via-pink-600 to-amber-500 text-white font-bold text-sm shadow-2xl shadow-rose-500/30 hover:scale-105 transition-transform flex items-center gap-3">
            Launch Autonomous Agents <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* 12 Autonomous Agents Grid Preview */}
      <section className="max-w-7xl mx-auto px-6 py-16">
        <h2 className="text-center text-2xl font-bold text-white mb-12">Powered By 12 Autonomous AI Agents</h2>
        <div className="grid grid-cols-4 gap-6">
          {[
            { title: "Executive Agent", desc: "Coordinates global workflow & long-term career memory.", icon: Bot },
            { title: "Career Coach Agent", desc: "Predicts trajectory & generates 12-month roadmaps.", icon: Compass },
            { title: "Resume Agent", desc: "Deep ATS analysis & real-time bullet rewriting.", icon: FileText },
            { title: "Job Discovery Agent", desc: "Scans thousands of jobs & predicts acceptance odds.", icon: Briefcase },
            { title: "Skill Gap Agent", desc: "Detects missing skills & recommends target projects.", icon: Activity },
            { title: "Interview Agent", desc: "Simulates voice & behavioral mock interviews.", icon: Sparkles },
            { title: "Recruiter Agent", desc: "AI candidate ranking & resume scoring engine.", icon: Users },
            { title: "Opportunity Monitor", desc: "Runs 24x7 scanning hackathons & contracts.", icon: Shield }
          ].map((agent, idx) => {
            const Icon = agent.icon;
            return (
              <div key={idx} className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800/80 backdrop-blur-xl hover:border-rose-500/30 transition-all">
                <Icon className="w-8 h-8 text-rose-500 mb-4" />
                <h3 className="text-sm font-bold text-white">{agent.title}</h3>
                <p className="text-xs text-slate-400 mt-2 leading-relaxed">{agent.desc}</p>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
}
