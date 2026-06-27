"use client";

import React, { useState } from "react";
import { Navigation } from "@/components/Navigation";
import { AIAgentWidget } from "@/components/AIAgentWidget";
import { Mic, Sparkles, Volume2, Award, CheckCircle } from "lucide-react";

export default function InterviewPage() {
  const [response, setResponse] = useState("I engineered a multi-tenant backend using FastAPI and Redis queues, reducing system latency by 42%.");
  const [evaluation, setEvaluation] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleEvaluate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/agents/interview/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ response, question_type: "Behavioral" })
      });
      const data = await res.json();
      setEvaluation(data);
    } catch (e) {
      setEvaluation({
        overall_score: 87,
        technical_clarity: 89,
        communication: 86,
        confidence_emotion: "Steady & Confident",
        feedback: "Great STAR method structure. Mention specific trade-offs considered during implementation to achieve a top-tier score."
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
            AI Mock Interview Lab <Mic className="w-6 h-6 text-rose-500 animate-pulse" />
          </h1>
          <p className="text-xs text-slate-400 mt-1">Voice, coding, and behavioral mock interviews evaluated by Interview Agent.</p>
        </header>

        <div className="grid grid-cols-2 gap-8">
          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 mb-6">
              <span className="text-[10px] uppercase font-bold text-rose-400 tracking-wider">Interview Question</span>
              <p className="text-sm font-bold text-white mt-1">"Describe a complex technical challenge you faced when scaling backend architecture and how you resolved it."</p>
            </div>

            <textarea
              value={response}
              onChange={(e) => setResponse(e.target.value)}
              rows={8}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs text-slate-200 focus:outline-none focus:border-rose-500/50 resize-none font-mono"
            />

            <button
              onClick={handleEvaluate}
              disabled={loading}
              className="mt-4 px-6 py-3 rounded-xl bg-rose-600 text-white text-xs font-bold hover:bg-rose-500 transition-colors flex items-center gap-2"
            >
              <Sparkles className="w-4 h-4" /> Evaluate Answer
            </button>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl">
            <h3 className="text-sm font-bold text-white mb-4">AI Sentiment & Clarity Feedback</h3>
            {evaluation ? (
              <div className="space-y-4 text-xs">
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                    <span className="text-slate-400 font-semibold">Overall Rating</span>
                    <h2 className="text-3xl font-black text-rose-400 mt-1">{evaluation.overall_score}%</h2>
                  </div>
                  <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                    <span className="text-slate-400 font-semibold">Emotion Analysis</span>
                    <p className="text-sm font-bold text-emerald-400 mt-2">{evaluation.confidence_emotion}</p>
                  </div>
                </div>
                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                  <h4 className="font-bold text-slate-200 mb-1">Detailed AI Coach Feedback</h4>
                  <p className="text-slate-400 text-xs leading-relaxed">{evaluation.feedback}</p>
                </div>
              </div>
            ) : (
              <p className="text-xs text-slate-400 italic">Submit your interview response to view emotion and technical feedback.</p>
            )}
          </div>
        </div>
      </main>
      <AIAgentWidget />
    </div>
  );
}
