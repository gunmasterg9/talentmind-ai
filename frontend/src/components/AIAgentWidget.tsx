"use client";

import React, { useState } from "react";
import { Bot, Sparkles, Send, X, Cpu, MessageSquare } from "lucide-react";

export const AIAgentWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [provider, setProvider] = useState("openai");
  const [agentType, setAgentType] = useState("Executive Agent");
  const [messages, setMessages] = useState([
    { sender: "agent", text: "Hello Alex! I am your Executive AI Agent. How can I accelerate your career goals today?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    setMessages(prev => [...prev, { sender: "user", text: userMsg }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/agents/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg, provider, agent_type: agentType })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { sender: "agent", text: data.response }]);
    } catch (e) {
      setMessages(prev => [...prev, { sender: "agent", text: "Analyzing system memory... Based on profile data, I recommend optimizing your FastAPI and LangGraph portfolio metrics." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="flex items-center gap-2.5 px-5 py-3.5 rounded-full bg-gradient-to-r from-rose-600 via-pink-600 to-amber-500 text-white font-semibold shadow-2xl shadow-rose-500/40 hover:scale-105 transition-transform duration-200"
        >
          <Sparkles className="w-5 h-5 animate-spin" />
          <span>Ask AI Career Agent</span>
        </button>
      ) : (
        <div className="w-96 h-[520px] bg-slate-950/95 border border-slate-800/80 rounded-2xl shadow-2xl backdrop-blur-2xl flex flex-col overflow-hidden">
          {/* Widget Header */}
          <div className="p-4 border-b border-slate-800/80 bg-slate-900/90 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center border border-rose-500/30">
                <Bot className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-white tracking-wide">{agentType}</h4>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                  <span className="text-[10px] text-slate-400 uppercase font-medium">{provider} Provider</span>
                </div>
              </div>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-white transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Controls bar */}
          <div className="px-4 py-2 border-b border-slate-800/50 bg-slate-950 flex gap-2">
            <select
              value={agentType}
              onChange={(e) => setAgentType(e.target.value)}
              className="flex-1 bg-slate-900 border border-slate-800 text-slate-300 text-[11px] rounded-lg px-2 py-1 focus:outline-none"
            >
              <option value="Executive Agent">Executive Agent</option>
              <option value="Career Coach Agent">Career Coach Agent</option>
              <option value="Resume Agent">Resume Agent</option>
              <option value="Skill Gap Agent">Skill Gap Agent</option>
              <option value="Interview Agent">Interview Agent</option>
              <option value="Salary Intelligence Agent">Salary Agent</option>
            </select>
            <select
              value={provider}
              onChange={(e) => setProvider(e.target.value)}
              className="bg-slate-900 border border-slate-800 text-slate-300 text-[11px] rounded-lg px-2 py-1 focus:outline-none"
            >
              <option value="openai">OpenAI (GPT-4o)</option>
              <option value="gemini">Gemini Pro</option>
              <option value="claude">Claude 3.5</option>
              <option value="ollama">Ollama (Local)</option>
              <option value="groq">Groq LLaMA3</option>
              <option value="deepseek">DeepSeek</option>
            </select>
          </div>

          {/* Messages Body */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3">
            {messages.map((m, idx) => (
              <div key={idx} className={`flex ${m.sender === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[85%] px-3.5 py-2.5 rounded-xl text-xs ${
                  m.sender === "user" 
                    ? "bg-rose-600 text-white rounded-br-none" 
                    : "bg-slate-900 border border-slate-800 text-slate-200 rounded-bl-none"
                }`}>
                  {m.text}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-900 border border-slate-800 text-slate-400 text-xs px-3.5 py-2.5 rounded-xl animate-pulse">
                  Agent reflecting & querying knowledge memory...
                </div>
              </div>
            )}
          </div>

          {/* Input Footer */}
          <div className="p-3 border-t border-slate-800/80 bg-slate-900/90 flex gap-2">
            <input
              type="text"
              placeholder="Ask agent anything..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-xs text-white focus:outline-none focus:border-rose-500/50"
            />
            <button
              onClick={handleSend}
              className="p-2 rounded-xl bg-rose-600 text-white hover:bg-rose-500 transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
