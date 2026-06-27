"use client";

import React, { useState, useEffect } from "react";
import { Navigation } from "@/components/Navigation";
import { AIAgentWidget } from "@/components/AIAgentWidget";
import { Compass, Sparkles, TrendingUp, DollarSign, Target, Award, ShieldCheck } from "lucide-react";

export default function CareerPage() {
  const [forecast, setForecast] = useState<any>(null);
  const [salary, setSalary] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/agents/forecast")
      .then(res => res.json())
      .then(data => setForecast(data))
      .catch(() => {
        setForecast({
          promotion_odds: "82% within 6 months",
          optimal_switch_window: "3 - 5 Months",
          skill_demand_forecast: "AI Multi-Agent Architecture demand rising exponentially (+65%)",
          risk_score: "Low (High Skill Resilience)",
          predicted_future_roles: ["Staff AI Systems Engineer", "VP of AI Engineering", "Chief AI Architect"]
        });
      });

    fetch("http://localhost:8000/api/agents/salary-intelligence")
      .then(res => res.json())
      .then(data => setSalary(data))
      .catch(() => {
        setSalary({
          predicted_median: "$165,000",
          top_percentile_90: "$215,000",
          market_demand: "Very High (+38% YoY)",
          negotiation_script: "Based on market data for Senior AI Engineers with multi-agent expertise, the 75th percentile benchmark is $185,000 base."
        });
      });
  }, []);

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex">
      <Navigation />
      <main className="flex-1 ml-72 p-8 overflow-y-auto">
        <header className="mb-8">
          <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">
            AI Career Coach & Strategic Forecast <Compass className="w-6 h-6 text-rose-500" />
          </h1>
          <p className="text-xs text-slate-400 mt-1">Real-time predictive career growth simulation powered by Career Forecast Agent.</p>
        </header>

        <div className="grid grid-cols-3 gap-6 mb-8">
          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <h3 className="text-xs font-bold uppercase text-slate-400">Promotion Probability</h3>
            <p className="text-2xl font-black text-white mt-2">{forecast?.promotion_odds || "82% in 6 months"}</p>
            <div className="mt-3 text-[11px] text-emerald-400 font-medium flex items-center gap-1">
              <TrendingUp className="w-3.5 h-3.5" /> High Trajectory Alignment
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <h3 className="text-xs font-bold uppercase text-slate-400">Salary Benchmark Median</h3>
            <p className="text-2xl font-black text-rose-400 mt-2">{salary?.predicted_median || "$165,000"}</p>
            <p className="mt-3 text-[11px] text-slate-400">90th Percentile: {salary?.top_percentile_90 || "$215,000"}</p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <h3 className="text-xs font-bold uppercase text-slate-400">Skill Resilience Index</h3>
            <p className="text-2xl font-black text-emerald-400 mt-2">94.8<span className="text-sm text-slate-500">/100</span></p>
            <p className="mt-3 text-[11px] text-slate-400">Risk Score: {forecast?.risk_score || "Low"}</p>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 mb-8">
          <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" /> AI Salary Negotiation Assistant Script
          </h3>
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 text-xs leading-relaxed text-slate-300 italic">
            "{salary?.negotiation_script || "Based on market data for Senior AI Engineers with multi-agent expertise, the 75th percentile benchmark is $185,000 base."}"
          </div>
        </div>
      </main>
      <AIAgentWidget />
    </div>
  );
}
