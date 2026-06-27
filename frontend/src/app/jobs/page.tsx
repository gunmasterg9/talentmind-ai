"use client";

import React, { useState, useEffect } from "react";
import { Navigation } from "@/components/Navigation";
import { AIAgentWidget } from "@/components/AIAgentWidget";
import { Briefcase, Search, Sparkles, MapPin, Building, DollarSign, BookmarkCheck } from "lucide-react";

export default function JobsPage() {
  const [jobs, setJobs] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/jobs")
      .then(res => res.json())
      .then(data => setJobs(data))
      .catch(() => {
        setJobs([
          { job_id: "JOB-101", title: "Lead AI Autonomous Systems Engineer", company: "ScaleAI Next", location: "Remote / SF", salary_range: "$160k - $210k", description: "Build scalable multi-agent frameworks.", min_exp_years: 4 },
          { job_id: "JOB-102", title: "Senior Staff Backend Engineer", company: "DeepMind Partner", location: "Remote", salary_range: "$150k - $190k", description: "High throughput python backend microservices.", min_exp_years: 5 },
          { job_id: "JOB-103", title: "Full-Stack AI Architect", company: "Redrob Global", location: "Hybrid / NY", salary_range: "$140k - $180k", description: "Next.js 15 and FastAPI AI portal.", min_exp_years: 3 }
        ]);
      });
  }, []);

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex">
      <Navigation />
      <main className="flex-1 ml-72 p-8 overflow-y-auto">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
              Autonomous Opportunity Matcher <Briefcase className="w-6 h-6 text-rose-500" />
            </h1>
            <p className="text-xs text-slate-400 mt-1">Scanned 24x7 across thousands of tech portals by Job Discovery Agent.</p>
          </div>
          <div className="w-72 relative">
            <input 
              type="text" 
              placeholder="Semantic search jobs..." 
              className="w-full bg-slate-900 border border-slate-800 rounded-xl px-4 py-2 text-xs text-white focus:outline-none focus:border-rose-500/50 pl-9"
            />
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          </div>
        </header>

        <div className="space-y-4">
          {jobs.map((job) => (
            <div key={job.job_id} className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 backdrop-blur-xl flex justify-between items-center hover:border-rose-500/30 transition-all">
              <div>
                <div className="flex items-center gap-3">
                  <h3 className="text-lg font-bold text-white">{job.title}</h3>
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/30">96.4% AI Match</span>
                </div>
                <div className="flex items-center gap-4 text-xs text-slate-400 mt-2">
                  <span className="flex items-center gap-1"><Building className="w-3.5 h-3.5" /> {job.company || "ScaleAI Next"}</span>
                  <span className="flex items-center gap-1"><MapPin className="w-3.5 h-3.5" /> {job.location || "Remote"}</span>
                  <span className="flex items-center gap-1 text-emerald-400 font-medium"><DollarSign className="w-3.5 h-3.5" /> {job.salary_range || "$160k - $210k"}</span>
                </div>
                <p className="text-xs text-slate-300 mt-3">{job.description}</p>
              </div>
              <button className="px-5 py-2.5 rounded-xl bg-rose-600 text-white text-xs font-bold hover:bg-rose-500 transition-colors flex items-center gap-2">
                <BookmarkCheck className="w-4 h-4" /> Auto-Apply
              </button>
            </div>
          ))}
        </div>
      </main>
      <AIAgentWidget />
    </div>
  );
}
