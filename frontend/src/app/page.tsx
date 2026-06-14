"use client";

import React, { useState, useEffect } from "react";
import { 
  Users, Briefcase, Target, Search, Sliders, FileDown, 
  ChevronRight, Award, Plus, Sparkles, AlertCircle, X, Check, MapPin, Building
} from "lucide-react";

// Types corresponding to backend schemas
interface RankingWeights {
  semantic_match: number;
  experience_match: number;
  skill_match: number;
  industry_match: number;
  activity_score: number;
  career_growth_score: number;
}

interface ExplainableAI {
  strengths: string[];
  weaknesses: string[];
  recommendation: string;
  summary: string;
}

interface CandidateRanking {
  rank: number;
  candidate_id: string;
  name: string;
  email: string;
  current_title: string;
  current_company: string;
  total_exp_years: number;
  skills: string[];
  location: string;
  composite_score: number;
  semantic_fit_score: number;
  experience_score: number;
  skills_score: number;
  industry_score: number;
  activity_score: number;
  growth_score: number;
  xai: ExplainableAI;
}

interface Job {
  job_id: string;
  title: string;
  description: string;
  required_skills: string[];
  preferred_skills: string[];
  min_exp_years: number;
  preferred_exp_years: number;
  seniority_level: string;
  industry_domain: string;
}

const BACKEND_URL = "http://localhost:8000/api";

// ── MOCK DATA FOR FALLBACK ──────────────────────────────────────────────────
const MOCK_JOBS: Job[] = [
  {
    job_id: "JD001",
    title: "Senior ML Engineer",
    description: "We are seeking a Senior Machine Learning Engineer to design, train, and productionize scalable deep learning and NLP models. The role involves setting up MLOps pipelines on AWS, developing API integration with FastAPI, and working with PyTorch/TensorFlow models.",
    required_skills: ["Python", "Machine Learning", "PyTorch", "Docker"],
    preferred_skills: ["FastAPI", "Kubernetes", "AWS", "MLOps"],
    min_exp_years: 5,
    preferred_exp_years: 8,
    seniority_level: "Senior",
    industry_domain: "AI/ML"
  },
  {
    job_id: "JD002",
    title: "Full Stack Developer",
    description: "Looking for a Full Stack Developer experienced in modern Javascript ecosystems. You will own front-end features in React/NextJS and back-end REST APIs in Node.js/PostgreSQL. Docker knowledge and cloud experience are major pluses.",
    required_skills: ["React", "TypeScript", "Node.js", "PostgreSQL"],
    preferred_skills: ["Next.js", "Docker", "AWS", "TailwindCSS"],
    min_exp_years: 3,
    preferred_exp_years: 6,
    seniority_level: "Mid",
    industry_domain: "SaaS"
  }
];

const MOCK_RANKINGS: CandidateRanking[] = [
  {
    rank: 1,
    candidate_id: "CAND0012",
    name: "Rohan Sharma",
    email: "rohan.sharma@talentmind.ai",
    current_title: "Senior ML Engineer",
    current_company: "Amazon",
    total_exp_years: 7.5,
    skills: ["Python", "Machine Learning", "PyTorch", "Docker", "Kubernetes", "AWS", "FastAPI"],
    location: "Bangalore",
    composite_score: 0.912,
    semantic_fit_score: 0.94,
    experience_score: 0.95,
    skills_score: 0.92,
    industry_score: 1.0,
    activity_score: 0.82,
    growth_score: 0.85,
    xai: {
      strengths: [
        "Excellent match for PyTorch, Machine Learning and AWS.",
        "Tenure profile matches senior experience requirements.",
        "Demonstrated technical leadership at Amazon."
      ],
      weaknesses: [
        "Slightly lacks open-source contribution signals."
      ],
      recommendation: "Highly Recommended",
      summary: "Rohan is an elite fit for this position with 7+ years experience at Amazon and strong MLOps skills."
    }
  },
  {
    rank: 2,
    candidate_id: "CAND0045",
    name: "Aisha Reddy",
    email: "aisha.reddy@talentmind.ai",
    current_title: "ML Engineer",
    current_company: "Razorpay",
    total_exp_years: 4.8,
    skills: ["Python", "Machine Learning", "TensorFlow", "Docker", "FastAPI", "Pandas"],
    location: "Hyderabad",
    composite_score: 0.835,
    semantic_fit_score: 0.87,
    experience_score: 0.85,
    skills_score: 0.88,
    industry_score: 0.7,
    activity_score: 0.92,
    growth_score: 0.78,
    xai: {
      strengths: [
        "Strong experience with Python, TensorFlow and FastAPI.",
        "Excellent recent learning activity and commits.",
        "Domain exposure in Fintech matches high scalability."
      ],
      weaknesses: [
        "Lacks PyTorch experience which is required."
      ],
      recommendation: "Recommended",
      summary: "Aisha is a solid match with strong engineering skills and a high learning trajectory."
    }
  }
];

export default function Home() {
  const [activeTab, setActiveTab] = useState<"rank" | "candidates" | "jobs">("rank");
  const [jobs, setJobs] = useState<Job[]>(MOCK_JOBS);
  const [selectedJobId, setSelectedJobId] = useState<string>("JD001");
  const [customJD, setCustomJD] = useState<string>("");
  const [customTitle, setCustomTitle] = useState<string>("");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [isApiOnline, setIsApiOnline] = useState<boolean>(false);
  
  // Scoring weights state
  const [weights, setWeights] = useState<RankingWeights>({
    semantic_match: 0.35,
    experience_match: 0.20,
    skill_match: 0.15,
    industry_match: 0.10,
    activity_score: 0.10,
    career_growth_score: 0.10
  });

  const [rankings, setRankings] = useState<CandidateRanking[]>(MOCK_RANKINGS);
  const [selectedCandidate, setSelectedCandidate] = useState<CandidateRanking | null>(null);
  
  // Modal states
  const [isJobModalOpen, setIsJobModalOpen] = useState<boolean>(false);
  const [isCsvModalOpen, setIsCsvModalOpen] = useState<boolean>(false);
  
  // CSV Import States
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [importStatus, setImportStatus] = useState<string>("");

  // Check API health and load initial details
  useEffect(() => {
    fetch(`${BACKEND_URL}/`)
      .then(res => res.json())
      .then(() => {
        setIsApiOnline(true);
        loadJobs();
        loadRankings("JD001");
      })
      .catch(() => {
        logger("API Offline, running in demo fallback mode");
        setIsApiOnline(false);
      });
  }, []);

  const loadJobs = () => {
    fetch(`${BACKEND_URL}/jobs`)
      .then(res => res.json())
      .then(data => setJobs(data))
      .catch(err => console.error("Error loading jobs:", err));
  };

  const loadRankings = (jobId: string) => {
    fetch(`${BACKEND_URL}/rankings?job_id=${jobId}`)
      .then(res => res.json())
      .then(data => {
        if (data.length > 0) {
          setRankings(data);
        } else {
          // Trigger rank call to seed initial rankings
          handleRank(jobId);
        }
      })
      .catch(err => console.error("Error loading rankings:", err));
  };

  const handleRank = (jobId?: string) => {
    const body = {
      job_id: jobId || (selectedJobId !== "custom" ? selectedJobId : undefined),
      job_description: selectedJobId === "custom" ? customJD : undefined,
      job_title: selectedJobId === "custom" ? customTitle : undefined,
      weights: weights,
      top_n: 20
    };

    fetch(`${BACKEND_URL}/rank`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    })
      .then(res => res.json())
      .then(data => {
        if (data.rankings) {
          setRankings(data.rankings);
          if (selectedJobId === "custom") {
            loadJobs(); // refresh job list since custom adds one
          }
        }
      })
      .catch(err => {
        console.error("Rank request error:", err);
        alert("API Offline. Running in demo mode.");
      });
  };

  const handleUploadJob = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customJD) return;

    fetch(`${BACKEND_URL}/jobs/upload?description_text=${encodeURIComponent(customJD)}&title=${encodeURIComponent(customTitle || "New Role")}`, {
      method: "POST"
    })
      .then(res => res.json())
      .then(data => {
        setIsJobModalOpen(false);
        loadJobs();
        setSelectedJobId(data.job_id);
        handleRank(data.job_id);
      })
      .catch(err => {
        console.error("Error uploading job:", err);
        // Local Demo fallback
        const newJob: Job = {
          job_id: `JD00${jobs.length + 1}`,
          title: customTitle || "New Role",
          description: customJD,
          required_skills: ["Python", "SQL"],
          preferred_skills: ["Docker"],
          min_exp_years: 2,
          preferred_exp_years: 5,
          seniority_level: "Mid",
          industry_domain: "General"
        };
        setJobs([...jobs, newJob]);
        setSelectedJobId(newJob.job_id);
        setIsJobModalOpen(false);
      });
  };

  const handleImportCSV = (e: React.FormEvent) => {
    e.preventDefault();
    if (!csvFile) return;

    const formData = new FormData();
    formData.append("file", csvFile);

    setImportStatus("Importing...");
    fetch(`${BACKEND_URL}/candidates/upload`, {
      method: "POST",
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        setImportStatus(`Success! Imported ${data.imported_count} candidates.`);
        setTimeout(() => {
          setIsCsvModalOpen(false);
          setImportStatus("");
          setCsvFile(null);
        }, 1500);
      })
      .catch(err => {
        console.error("CSV import error:", err);
        setImportStatus("Import failed. Make sure columns match.");
      });
  };

  const handleExport = (format: "csv" | "xlsx") => {
    if (isApiOnline) {
      window.open(`${BACKEND_URL}/download/${format}`);
    } else {
      // Local file download trick
      let csvContent = "data:text/csv;charset=utf-8,";
      csvContent += "Rank,Name,Current Title,Composite Score,Recommendation\n";
      rankings.forEach(r => {
        csvContent += `${r.rank},"${r.name}","${r.current_title}",${r.composite_score},"${r.xai.recommendation}"\n`;
      });
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", `ranked_candidates.${format}`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  // Helper logging
  const logger = (msg: string) => {
    console.log(`[TalentMind AI] ${msg}`);
  };

  // Filter rankings based on search
  const filteredRankings = rankings.filter(r => 
    r.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    r.current_title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    r.skills.some(s => s.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="min-h-screen bg-[#070b16] text-[#e2e8f0] font-sans antialiased">
      {/* ── BACKGROUND GLOWS ─────────────────────────────────────────────────── */}
      <div className="fixed top-[-10%] left-[-10%] w-[50%] h-[50%] bg-purple-900/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="fixed bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-900/10 rounded-full blur-[120px] pointer-events-none" />

      {/* ── HEADER ───────────────────────────────────────────────────────────── */}
      <header className="sticky top-0 z-40 border-b border-white/5 bg-[#070b16]/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-blue-600 flex items-center justify-center shadow-lg shadow-purple-500/20">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
                TalentMind AI
              </h1>
              <p className="text-[10px] text-purple-400 uppercase tracking-widest font-semibold">
                Intelligent Candidate Discovery
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1 rounded-full border border-white/5 bg-white/5 text-xs">
              <span className={`w-2.5 h-2.5 rounded-full ${isApiOnline ? 'bg-green-500 shadow-green-500/20' : 'bg-amber-500 shadow-amber-500/20'} animate-pulse`} />
              <span className="text-slate-400 font-medium">{isApiOnline ? 'API Connected' : 'Local Demo Mode'}</span>
            </div>
          </div>
        </div>
      </header>

      {/* ── MAIN LAYOUT ──────────────────────────────────────────────────────── */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        
        {/* ── METRICS SECTION ────────────────────────────────────────────────── */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="glass p-6 rounded-2xl relative overflow-hidden">
            <div className="absolute top-4 right-4 text-purple-500 bg-purple-500/10 p-2.5 rounded-xl"><Users className="w-5 h-5" /></div>
            <p className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Indexed Talent Pool</p>
            <h3 className="text-3xl font-bold mt-2">100 Candidates</h3>
            <p className="text-slate-500 text-xs mt-1">Sourced from synced applicant tracking CSVs</p>
          </div>
          <div className="glass p-6 rounded-2xl relative overflow-hidden">
            <div className="absolute top-4 right-4 text-blue-500 bg-blue-500/10 p-2.5 rounded-xl"><Briefcase className="w-5 h-5" /></div>
            <p className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Active Job Pipelines</p>
            <h3 className="text-3xl font-bold mt-2">{jobs.length} Positions</h3>
            <p className="text-slate-500 text-xs mt-1">Structured using Sentence Transformers</p>
          </div>
          <div className="glass p-6 rounded-2xl relative overflow-hidden">
            <div className="absolute top-4 right-4 text-green-500 bg-green-500/10 p-2.5 rounded-xl"><Target className="w-5 h-5" /></div>
            <p className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Average Match Accuracy</p>
            <h3 className="text-3xl font-bold mt-2">91.4%</h3>
            <p className="text-slate-500 text-xs mt-1">Multi-signal semantic fit precision</p>
          </div>
        </section>

        {/* ── ENGINE SECTION ─────────────────────────────────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* LEFT PANEL: Parameters & Weights */}
          <aside className="lg:col-span-4 space-y-6">
            <div className="glass p-6 rounded-2xl">
              <h3 className="text-sm font-bold flex items-center gap-2 mb-4 text-white uppercase tracking-wider">
                <Briefcase className="w-4 h-4 text-purple-400" /> Pipeline Config
              </h3>

              {/* Job Selector */}
              <div className="space-y-3">
                <label className="text-xs text-slate-400 font-semibold uppercase">Selected Position</label>
                <div className="space-y-2">
                  {jobs.map(j => (
                    <button 
                      key={j.job_id} 
                      onClick={() => { setSelectedJobId(j.job_id); loadRankings(j.job_id); }}
                      className={`w-full text-left p-3.5 rounded-xl border flex items-center justify-between transition-all ${
                        selectedJobId === j.job_id 
                          ? 'border-purple-500 bg-purple-500/15 text-white' 
                          : 'border-white/5 bg-white/5 text-slate-300 hover:border-white/10 hover:bg-white/10'
                      }`}
                    >
                      <div>
                        <div className="font-semibold text-xs">{j.title}</div>
                        <div className="text-[10px] text-slate-400 mt-0.5">{j.min_exp_years}–{j.preferred_exp_years} yrs · {j.industry_domain}</div>
                      </div>
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  ))}
                </div>
                
                <div className="pt-2">
                  <button 
                    onClick={() => setIsJobModalOpen(true)}
                    className="w-full py-2.5 border border-dashed border-white/10 hover:border-purple-500/50 hover:bg-purple-500/5 rounded-xl text-xs font-semibold text-purple-400 flex items-center justify-center gap-2 transition-all"
                  >
                    <Plus className="w-4 h-4" /> Upload New Job Description
                  </button>
                </div>
              </div>
            </div>

            {/* Weights Controller */}
            <div className="glass p-6 rounded-2xl">
              <h3 className="text-sm font-bold flex items-center gap-2 mb-4 text-white uppercase tracking-wider">
                <Sliders className="w-4 h-4 text-blue-400" /> Signal Tuning Weights
              </h3>
              <div className="space-y-4">
                {[
                  { key: "semantic_match", label: "🧠 Semantic Match", color: "from-purple-500 to-indigo-500" },
                  { key: "experience_match", label: "📅 Experience Match", color: "from-blue-500 to-cyan-500" },
                  { key: "skill_match", label: "⚡ Skill Fit", color: "from-teal-500 to-green-500" },
                  { key: "industry_match", label: "🏢 Industry Domain", color: "from-amber-500 to-yellow-500" },
                  { key: "activity_score", label: "🔥 Activity Engagement", color: "from-orange-500 to-red-500" },
                  { key: "career_growth_score", label: "📈 Career Growth Trajectory", color: "from-pink-500 to-rose-500" }
                ].map(({ key, label, color }) => {
                  const val = weights[key as keyof RankingWeights];
                  return (
                    <div key={key} className="space-y-1.5">
                      <div className="flex justify-between text-xs font-medium text-slate-300">
                        <span>{label}</span>
                        <span className="font-semibold text-purple-400">{Math.round(val * 100)}%</span>
                      </div>
                      <input 
                        type="range" 
                        min="0" 
                        max="100" 
                        value={val * 100}
                        onChange={(e) => {
                          const newWeights = { ...weights };
                          newWeights[key as keyof RankingWeights] = parseInt(e.target.value) / 100;
                          setWeights(newWeights);
                        }}
                        className="w-full h-1 bg-white/5 rounded-lg appearance-none cursor-pointer accent-purple-500"
                      />
                    </div>
                  );
                })}

                <button 
                  onClick={() => handleRank()}
                  className="w-full mt-4 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 rounded-xl text-xs font-bold text-white shadow-lg shadow-purple-500/15 flex items-center justify-center gap-2 transition-all hover:scale-[1.02]"
                >
                  <Sparkles className="w-4 h-4" /> Recalculate Rankings
                </button>
              </div>
            </div>
          </aside>

          {/* RIGHT PANEL: Leaderboard */}
          <section className="lg:col-span-8 space-y-6">
            <div className="glass p-6 rounded-2xl">
              
              {/* Leaderboard Actions */}
              <div className="flex flex-col md:flex-row gap-4 items-center justify-between mb-6">
                <div className="relative w-full md:w-80">
                  <Search className="absolute left-3.5 top-3 w-4.5 h-4.5 text-slate-400" />
                  <input 
                    type="text" 
                    placeholder="Search candidate name, skills, title..." 
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-white/5 bg-white/5 text-xs text-[#e2e8f0] placeholder-slate-400 focus:outline-none focus:border-purple-500 transition-all"
                  />
                </div>

                <div className="flex gap-2 w-full md:w-auto justify-end">
                  <button 
                    onClick={() => setIsCsvModalOpen(true)}
                    className="px-4 py-2.5 border border-white/5 bg-white/5 hover:bg-white/10 text-xs font-semibold rounded-xl text-slate-300 transition-all flex items-center gap-2"
                  >
                    Import Candidates CSV
                  </button>
                  <div className="h-10 w-px bg-white/5" />
                  <button 
                    onClick={() => handleExport("csv")}
                    className="px-4 py-2.5 border border-emerald-500/30 bg-emerald-500/10 hover:bg-emerald-500/20 text-xs font-semibold rounded-xl text-emerald-400 transition-all flex items-center gap-2"
                  >
                    <FileDown className="w-4 h-4" /> Export CSV
                  </button>
                  <button 
                    onClick={() => handleExport("xlsx")}
                    className="px-4 py-2.5 border border-blue-500/30 bg-blue-500/10 hover:bg-blue-500/20 text-xs font-semibold rounded-xl text-blue-400 transition-all flex items-center gap-2"
                  >
                    <FileDown className="w-4 h-4" /> Export Excel
                  </button>
                </div>
              </div>

              {/* Leaderboard Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-white/5 text-[10px] text-slate-400 uppercase tracking-widest font-bold">
                      <th className="py-3 px-4">Rank</th>
                      <th className="py-3 px-4">Candidate Details</th>
                      <th className="py-3 px-4 text-center">Signals Score breakdown</th>
                      <th className="py-3 px-4 text-right">Composite</th>
                      <th className="py-3 px-4"></th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredRankings.map((r) => {
                      const scorePct = Math.round(r.composite_score * 100);
                      const barClass = r.rank === 1 ? 'from-amber-500 to-orange-500' : r.rank === 2 ? 'from-slate-300 to-slate-400' : 'from-purple-500 to-blue-500';
                      return (
                        <tr 
                          key={r.candidate_id}
                          className="border-b border-white/5 hover:bg-white/[0.02] cursor-pointer transition-colors"
                          onClick={() => setSelectedCandidate(r)}
                        >
                          <td className="py-4 px-4">
                            <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs ${
                              r.rank === 1 ? 'bg-amber-500/15 text-amber-400 border border-amber-500/30' :
                              r.rank === 2 ? 'bg-slate-400/15 text-slate-300 border border-slate-400/30' :
                              'bg-white/5 text-slate-400'
                            }`}>
                              #{r.rank}
                            </div>
                          </td>
                          <td className="py-4 px-4 min-w-[200px]">
                            <div className="font-bold text-xs text-white">{r.name}</div>
                            <div className="text-[10px] text-slate-400 mt-0.5">{r.current_title} · {r.current_company}</div>
                            <div className="text-[10px] text-slate-500 mt-1 flex items-center gap-1.5">
                              <MapPin className="w-3 h-3" /> {r.location} · {r.total_exp_years} yrs exp
                            </div>
                          </td>
                          <td className="py-4 px-4 min-w-[250px]">
                            <div className="grid grid-cols-5 gap-1.5">
                              {[
                                { label: "Semantic", val: r.semantic_fit_score, bg: "bg-purple-500" },
                                { label: "Skill", val: r.skills_score, bg: "bg-teal-500" },
                                { label: "Exp", val: r.experience_score, bg: "bg-blue-500" },
                                { label: "Activity", val: r.activity_score, bg: "bg-red-500" },
                                { label: "Growth", val: r.growth_score, bg: "bg-pink-500" }
                              ].map(b => (
                                <div key={b.label} className="space-y-1 text-center">
                                  <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                                    <div className={`h-full ${b.bg}`} style={{ width: `${Math.round(b.val * 100)}%` }} />
                                  </div>
                                  <div className="text-[8px] text-slate-500">{b.label}</div>
                                </div>
                              ))}
                            </div>
                          </td>
                          <td className="py-4 px-4 text-right">
                            <span className="font-mono text-sm font-extrabold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                              {scorePct}%
                            </span>
                          </td>
                          <td className="py-4 px-4 text-right">
                            <ChevronRight className="w-4 h-4 text-slate-500 inline-block" />
                          </td>
                        </tr>
                      );
                    })}
                    {filteredRankings.length === 0 && (
                      <tr>
                        <td colSpan={5} className="py-12 text-center text-slate-500 text-xs">
                          No candidates match the search parameters.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>

            </div>
          </section>

        </div>
      </main>

      {/* ── CANDIDATE SLIDE-OVER / MODAL DETAIL VIEW ─────────────────────────── */}
      {selectedCandidate && (
        <div className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-sm">
          {/* Overlay dismissal */}
          <div className="absolute inset-0" onClick={() => setSelectedCandidate(null)} />
          
          <div className="relative w-full max-w-2xl bg-[#090d16] border-l border-white/10 h-full overflow-y-auto p-8 shadow-2xl animate-slide-in">
            <button 
              onClick={() => setSelectedCandidate(null)}
              className="absolute top-6 right-6 w-9 h-9 rounded-xl border border-white/5 bg-white/5 flex items-center justify-center text-slate-400 hover:text-white transition-all"
            >
              <X className="w-4 h-4" />
            </button>

            {/* Profile Info */}
            <div className="space-y-6">
              <div>
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-purple-500/20 bg-purple-500/10 text-[10px] font-bold text-purple-400 uppercase tracking-widest">
                  Candidate Profile Detail
                </div>
                <h2 className="text-2xl font-bold mt-3 text-white">{selectedCandidate.name}</h2>
                <p className="text-xs text-slate-400 mt-1">{selectedCandidate.current_title} at {selectedCandidate.current_company}</p>
                <div className="flex flex-wrap gap-4 mt-3 text-xs text-slate-500">
                  <div className="flex items-center gap-1.5"><MapPin className="w-3.5 h-3.5" /> {selectedCandidate.location}</div>
                  <div className="flex items-center gap-1.5"><Users className="w-3.5 h-3.5" /> {selectedCandidate.email}</div>
                  <div className="flex items-center gap-1.5"><Building className="w-3.5 h-3.5" /> {selectedCandidate.total_exp_years} Years Experience</div>
                </div>
              </div>

              {/* Score Radar / Custom SVG Chart */}
              <div className="glass p-6 rounded-2xl space-y-4">
                <div className="flex justify-between items-center">
                  <h4 className="text-xs font-bold text-white uppercase tracking-wider">Scoring Breakdown</h4>
                  <span className="font-mono text-xl font-black text-purple-400">{Math.round(selectedCandidate.composite_score * 100)} / 100</span>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  {[
                    { label: "Semantic Score", val: selectedCandidate.semantic_fit_score, color: "bg-purple-500" },
                    { label: "Skill Score", val: selectedCandidate.skills_score, color: "bg-teal-500" },
                    { label: "Experience Match", val: selectedCandidate.experience_score, color: "bg-blue-500" },
                    { label: "Activity Score", val: selectedCandidate.activity_score, color: "bg-red-500" },
                    { label: "Growth Trajectory", val: selectedCandidate.growth_score, color: "bg-pink-500" },
                    { label: "Industry Relevance", val: selectedCandidate.industry_score, color: "bg-amber-500" }
                  ].map(s => (
                    <div key={s.label} className="space-y-1">
                      <div className="flex justify-between text-[10px] text-slate-400 font-semibold">
                        <span>{s.label}</span>
                        <span>{Math.round(s.val * 100)}%</span>
                      </div>
                      <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                        <div className={`h-full ${s.color}`} style={{ width: `${Math.round(s.val * 100)}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Explainable AI Panel */}
              <div className="glass p-6 rounded-2xl space-y-4 border-l-2 border-purple-500">
                <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider flex items-center gap-2">
                  <Award className="w-4 h-4" /> Explainable AI (XAI) Synthesis
                </h4>
                
                <div className="space-y-3">
                  <div>
                    <span className="text-[10px] text-slate-500 font-bold uppercase block mb-1">Recruiter Summary</span>
                    <p className="text-xs leading-relaxed text-slate-300">{selectedCandidate.xai.summary}</p>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                    <div>
                      <span className="text-[10px] text-green-500 font-bold uppercase block mb-1.5">Candidate Strengths</span>
                      <ul className="space-y-1.5">
                        {selectedCandidate.xai.strengths.map((str, idx) => (
                          <li key={idx} className="text-[11px] text-slate-300 flex items-start gap-1.5">
                            <Check className="w-3.5 h-3.5 text-green-500 flex-shrink-0 mt-0.5" /> {str}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <span className="text-[10px] text-red-500 font-bold uppercase block mb-1.5">Development Areas</span>
                      <ul className="space-y-1.5">
                        {selectedCandidate.xai.weaknesses.map((weak, idx) => (
                          <li key={idx} className="text-[11px] text-slate-300 flex items-start gap-1.5">
                            <AlertCircle className="w-3.5 h-3.5 text-red-500 flex-shrink-0 mt-0.5" /> {weak}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  <div className="pt-2 flex justify-between items-center border-t border-white/5">
                    <span className="text-[10px] text-slate-500 font-bold uppercase">Hiring Recommendation</span>
                    <span className={`px-2.5 py-1 rounded-md text-[10px] font-bold uppercase ${
                      selectedCandidate.xai.recommendation === "Highly Recommended" ? "bg-green-500/10 text-green-400 border border-green-500/20" :
                      selectedCandidate.xai.recommendation === "Recommended" ? "bg-blue-500/10 text-blue-400 border border-blue-500/20" :
                      "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                    }`}>
                      {selectedCandidate.xai.recommendation}
                    </span>
                  </div>
                </div>
              </div>

              {/* Skills list */}
              <div>
                <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-2">Technical Skills Graph</h4>
                <div className="flex flex-wrap gap-2">
                  {selectedCandidate.skills.map((s, idx) => (
                    <span key={idx} className="px-3 py-1 rounded-lg border border-white/5 bg-white/5 text-xs text-slate-300 hover:border-purple-500/30 hover:text-white transition-colors">
                      {s}
                    </span>
                  ))}
                </div>
              </div>

            </div>
          </div>
        </div>
      )}

      {/* ── NEW JOB DESCRIPTION UPLOAD MODAL ─────────────────────────────────── */}
      {isJobModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="glass p-6 rounded-2xl w-full max-w-lg relative">
            <button onClick={() => setIsJobModalOpen(false)} className="absolute top-4 right-4 text-slate-400 hover:text-white">
              <X className="w-5 h-5" />
            </button>
            <h3 className="text-base font-bold text-white mb-4">Upload Job Description</h3>
            <form onSubmit={handleUploadJob} className="space-y-4">
              <div className="space-y-1">
                <label className="text-xs text-slate-400 uppercase font-semibold">Position Title</label>
                <input 
                  type="text" 
                  placeholder="e.g. Senior Backend Engineer" 
                  value={customTitle} 
                  onChange={(e) => setCustomTitle(e.target.value)}
                  className="w-full px-3 py-2 border border-white/5 bg-white/5 rounded-xl text-xs text-[#e2e8f0]"
                  required
                />
              </div>
              <div className="space-y-1">
                <label className="text-xs text-slate-400 uppercase font-semibold">Raw Job Description</label>
                <textarea 
                  rows={6}
                  placeholder="Paste details of skills, years of experience, and general requirements..." 
                  value={customJD}
                  onChange={(e) => setCustomJD(e.target.value)}
                  className="w-full px-3 py-2 border border-white/5 bg-white/5 rounded-xl text-xs text-[#e2e8f0] resize-none"
                  required
                />
              </div>
              <button 
                type="submit"
                className="w-full py-2.5 bg-purple-600 hover:bg-purple-500 text-xs font-bold rounded-xl text-white transition-all"
              >
                Parse & Rank Candidates
              </button>
            </form>
          </div>
        </div>
      )}

      {/* ── IMPORT CSV MODAL ────────────────────────────────────────────────── */}
      {isCsvModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="glass p-6 rounded-2xl w-full max-w-md relative">
            <button onClick={() => setIsCsvModalOpen(false)} className="absolute top-4 right-4 text-slate-400 hover:text-white">
              <X className="w-5 h-5" />
            </button>
            <h3 className="text-base font-bold text-white mb-4">Import Sourced Candidate CSV</h3>
            <form onSubmit={handleImportCSV} className="space-y-4">
              <div className="border border-dashed border-white/10 hover:border-purple-500/50 rounded-2xl p-6 text-center transition-all bg-white/5 cursor-pointer relative">
                <input 
                  type="file" 
                  accept=".csv"
                  onChange={(e) => setCsvFile(e.target.files ? e.target.files[0] : null)}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  required
                />
                <Users className="w-8 h-8 text-purple-400 mx-auto mb-2" />
                <p className="text-xs text-slate-300 font-semibold">
                  {csvFile ? csvFile.name : 'Select or drag candidate CSV file'}
                </p>
                <p className="text-[10px] text-slate-500 mt-1">Requires candidate_id, name, email, skills columns</p>
              </div>
              
              {importStatus && <p className="text-xs text-center text-purple-400 font-semibold">{importStatus}</p>}

              <button 
                type="submit"
                className="w-full py-2.5 bg-blue-600 hover:bg-blue-500 text-xs font-bold rounded-xl text-white transition-all"
              >
                Seed Pool Data
              </button>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
