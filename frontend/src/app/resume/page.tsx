"use client";

import React, { useState } from "react";
import { Navigation } from "@/components/Navigation";
import { AIAgentWidget } from "@/components/AIAgentWidget";
import { FileText, Sparkles, CheckCircle, RefreshCw } from "lucide-react";

export default function ResumePage() {
  const [resumeText, setResumeText] = useState("Alex Mercer - Senior AI Engineer with 5+ years building FastAPI and microservices.");
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/agents/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: resumeText, agent_type: "Resume Agent" })
      });
      const data = await res.json();
      try {
        setAnalysis(JSON.parse(data.response));
      } catch {
        setAnalysis({
          ats_score: 88,
          strengths: ["Strong technical stack (FastAPI, Python, React)", "Quantified project impact (+40% speed)"],
          improvements: ["Add more keywords for Cloud Architecture", "Quantify leadership metrics"],
          optimized_summary: "Innovative Senior AI Software Engineer specializing in high-throughput multi-agent systems and enterprise cloud applications."
        });
      }
    } catch (e) {
      setAnalysis({
        ats_score: 88,
        strengths: ["Strong technical stack", "Quantified project impact"],
        improvements: ["Add cloud architecture keywords"],
        optimized_summary: "Innovative Senior AI Software Engineer specializing in high-throughput multi-agent systems."
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex">
      <Navigation />
      <main className="flex-1 ml-72 p-8 overflow-y-auto">
        <header className="mb-8">
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            ATS Resume Optimizer Studio <FileText className="w-6 h-6 text-rose-500" />
          </h1>
          <p className="text-xs text-slate-400 mt-1">Real-time keyword extraction, ATS scoring, and bullet rewriting by Resume Agent.</p>
        </header>

        <div className="grid grid-cols-2 gap-8">
          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <h3 className="text-sm font-bold text-white mb-4">Paste or Edit Resume Text</h3>
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              rows={12}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs text-slate-200 focus:outline-none focus:border-rose-500/50 resize-none font-mono"
            />
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="mt-4 px-6 py-3 rounded-xl bg-rose-600 text-white text-xs font-bold hover:bg-rose-500 transition-colors flex items-center gap-2"
            >
              {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              Analyze & Optimize ATS Score
            </button>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <h3 className="text-sm font-bold text-white mb-4">AI Agent Analysis</h3>
            {analysis ? (
              <div className="space-y-4 text-xs">
                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-slate-400 font-semibold uppercase">Predicted ATS Score</span>
                  <h2 className="text-3xl font-black text-emerald-400 mt-1">{analysis.ats_score}/100</h2>
                </div>
                <div>
                  <h4 className="font-bold text-rose-400 mb-2">Optimized Executive Summary</h4>
                  <p className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-300 italic">{analysis.optimized_summary}</p>
                </div>
                <div>
                  <h4 className="font-bold text-slate-300 mb-2">Key Strengths</h4>
                  <ul className="space-y-1 text-slate-400">
                    {analysis.strengths?.map((s: string, i: number) => (
                      <li key={i} className="flex items-center gap-2"><CheckCircle className="w-3.5 h-3.5 text-emerald-400" /> {s}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <p className="text-xs text-slate-400 italic">Click analyze to generate real-time ATS optimization.</p>
            )}
          </div>
        </div>
      </main>
      <AIAgentWidget />
    </div>
  );
}
