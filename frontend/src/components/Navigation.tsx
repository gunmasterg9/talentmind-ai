"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  Sparkles, LayoutDashboard, Briefcase, FileText, Bot, 
  Target, Award, Users, Shield, Settings, Activity, Compass, Mic
} from "lucide-react";

export const Navigation = () => {
  const pathname = usePathname();

  const navItems = [
    { name: "Candidate HQ", path: "/dashboard", icon: LayoutDashboard },
    { name: "AI Career Coach", path: "/career", icon: Compass },
    { name: "Jobs & Opportunities", path: "/jobs", icon: Briefcase },
    { name: "Resume Optimizer Studio", path: "/resume", icon: FileText },
    { name: "AI Mock Interview Lab", path: "/interview", icon: Mic },
    { name: "Recruiter Suite", path: "/recruiter", icon: Users },
    { name: "Admin Control Panel", path: "/admin", icon: Shield }
  ];

  return (
    <aside className="w-72 border-r border-slate-800/80 bg-slate-950/90 backdrop-blur-2xl flex flex-col h-screen fixed left-0 top-0 z-50">
      {/* Brand Header */}
      <div className="p-6 border-b border-slate-800/60 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 via-pink-500 to-amber-400 p-0.5 shadow-lg shadow-rose-500/20">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-rose-500 animate-pulse" />
            </div>
          </div>
          <div>
            <span className="font-bold text-lg tracking-tight text-white flex items-center gap-1.5">
              REDROB <span className="text-xs px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 font-medium border border-rose-500/30">AI OS</span>
            </span>
            <p className="text-[10px] text-slate-400 font-medium tracking-wide uppercase">Autonomous Career Ecosystem</p>
          </div>
        </Link>
      </div>

      {/* Active AI Agent Monitor Badge */}
      <div className="mx-4 my-4 p-3 rounded-xl bg-slate-900/90 border border-slate-800 flex items-center justify-between shadow-inner">
        <div className="flex items-center gap-2.5">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping" />
          <div>
            <p className="text-xs font-semibold text-slate-200">Executive Agent 24x7</p>
            <p className="text-[10px] text-emerald-400">Monitoring Market Opportunities</p>
          </div>
        </div>
        <Activity className="w-4 h-4 text-slate-500" />
      </div>

      {/* Nav Menu */}
      <nav className="flex-1 px-4 py-2 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.path;
          return (
            <Link
              key={item.path}
              href={item.path}
              className={`flex items-center gap-3 px-3.5 py-3 rounded-xl text-sm font-medium transition-all duration-200 group ${
                isActive 
                  ? "bg-gradient-to-r from-rose-500/20 to-pink-500/10 text-rose-300 border border-rose-500/30 shadow-lg shadow-rose-500/10" 
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/60"
              }`}
            >
              <Icon className={`w-4 h-4 transition-transform group-hover:scale-110 ${isActive ? "text-rose-400" : "text-slate-400"}`} />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* User Profile Footer */}
      <div className="p-4 border-t border-slate-800/60 bg-slate-950">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-purple-500 to-rose-500 flex items-center justify-center font-bold text-xs text-white shadow-md">
              AM
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-200">Alex Mercer</p>
              <p className="text-[10px] text-slate-400">Pro Executive Plan</p>
            </div>
          </div>
          <span className="w-2 h-2 rounded-full bg-emerald-400" />
        </div>
      </div>
    </aside>
  );
};
