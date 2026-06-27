"use client";

import React, { useState, useEffect } from "react";
import { Navigation } from "@/components/Navigation";
import { AIAgentWidget } from "@/components/AIAgentWidget";
import { Users, Search, Sparkles, Award, ArrowUpRight, CheckCircle2 } from "lucide-react";

export default function RecruiterPage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/dashboard/recruiter")
      .then(res => res.json())
      .then(d => setData(d))
      .catch(() => {
        setData({
          total_applicants: 12,
          top_matches_count: 3,
          avg_match_score: "91.4%",
          interviews_scheduled: 4,
          ranked_candidates: [
            { candidate_id: "CAND-1", name: "Rohan Sharma", composite_score: 95.0, semantic_fit: 97.0, recommendation: "Strong Hire", summary: "Demonstrates exceptional proficiency in backend AI systems and scalable architecture." },
            { candidate_id: "CAND-2", name: "Priya Patel", composite_score: 90.5, semantic_fit: 92.5, recommendation: "Strong Hire", summary: "Solid full stack experience with React and Python APIs." }
          ]
        });
      });
  }, []);

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex">
      <Navigation />
      <main className="flex-1 ml-72 p-8 overflow-y-auto">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
              Recruiter Candidate AI Suite <Users className="w-6 h-6 text-rose-500" />
            </h1>
            <p className="text-xs text-slate-400 mt-1">Semantic candidate matching, automated resume scoring, and AI hiring analytics.</p>
          </div>
        </header>

        <div className="grid grid-cols-4 gap-5 mb-8">
          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <p className="text-xs font-semibold uppercase text-slate-400">Total Applicants</p>
            <h3 className="text-3xl font-black text-white mt-2">{data?.total_applicants || 12}</h3>
          </div>
          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <p className="text-xs font-semibold uppercase text-slate-400">Top Matches (&gt;90%)</p>
            <h3 className="text-3xl font-black text-rose-400 mt-2">{data?.top_matches_count || 3}</h3>
          </div>
          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <p className="text-xs font-semibold uppercase text-slate-400">Average Match Score</p>
            <h3 className="text-3xl font-black text-emerald-400 mt-2">{data?.avg_match_score || "91.4%"}</h3>
          </div>
          <div className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <p className="text-xs font-semibold uppercase text-slate-400">Interviews Scheduled</p>
            <h3 className="text-3xl font-black text-purple-400 mt-2">{data?.interviews_scheduled || 4}</h3>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800">
          <h3 className="text-base font-bold text-white mb-6">AI Ranked Candidates for Job: JOB-101</h3>
          <div className="space-y-4">
            {data?.ranked_candidates?.map((cand: any, idx: number) => (
              <div key={cand.candidate_id} className="p-5 rounded-xl bg-slate-950 border border-slate-800 flex justify-between items-center hover:border-slate-700 transition-all">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-rose-500/20 text-rose-400 font-black flex items-center justify-center text-sm border border-rose-500/30">
                    #{idx + 1}
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-white">{cand.name}</h4>
                    <p className="text-xs text-slate-400">{cand.summary}</p>
                  </div>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-right">
                    <span className="text-sm font-black text-emerald-400">{cand.composite_score}% Score</span>
                    <p className="text-[10px] text-slate-400 uppercase font-bold">{cand.recommendation}</p>
                  </div>
                  <button className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-xs font-bold text-white border border-slate-700 transition-colors">
                    View Profile
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
      <AIAgentWidget />
    </div>
  );
}
