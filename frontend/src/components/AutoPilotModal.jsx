import React, { useState, useEffect } from "react";
import {
  Sparkles,
  Play,
  Square,
  Clock,
  Video,
  ShieldCheck,
  AlertTriangle,
  Flame,
  CheckCircle2,
  ExternalLink,
  Plus,
  RefreshCw,
  X
} from "lucide-react";
import {
  fetchYouTubeStatus,
  fetchYouTubeAuthUrl,
  fetchAutoPilotStatus,
  startAutoPilot,
  stopAutoPilot,
  addAutoPilotTopic
} from "../api";

export default function AutoPilotModal({ isOpen, onClose }) {
  const [ytStatus, setYtStatus] = useState({ authenticated: false, has_client_secret: true });
  const [apStatus, setApStatus] = useState(null);
  const [intervalMin, setIntervalMin] = useState(30);
  const [privacy, setPrivacy] = useState("public");
  const [customTopic, setCustomTopic] = useState("");
  const [customCategory, setCustomCategory] = useState("GTA 6");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const refreshAll = async () => {
    try {
      const [yt, ap] = await Promise.all([
        fetchYouTubeStatus(),
        fetchAutoPilotStatus()
      ]);
      setYtStatus(yt);
      setApStatus(ap);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    if (isOpen) {
      refreshAll();
      const interval = setInterval(refreshAll, 3000);
      return () => clearInterval(interval);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleStart = async () => {
    setLoading(true);
    setMsg("");
    try {
      const res = await startAutoPilot(intervalMin, privacy);
      setMsg("✅ AutoPilot 30-min loop started! Searching GTA 6 & viral topics...");
      refreshAll();
    } catch (e) {
      setMsg("❌ Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async () => {
    setLoading(true);
    try {
      await stopAutoPilot();
      setMsg("⏸️ AutoPilot stopped.");
      refreshAll();
    } catch (e) {
      setMsg("❌ Error: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTopic = async (e) => {
    e.preventDefault();
    if (!customTopic.trim()) return;
    try {
      await addAutoPilotTopic(customTopic, customCategory);
      setCustomTopic("");
      setMsg("🔥 Added topic to front of viral queue!");
      refreshAll();
    } catch (e) {
      setMsg("❌ Error adding topic: " + e.message);
    }
  };

  const handleOpenAuthUrl = async () => {
    try {
      const data = await fetchYouTubeAuthUrl();
      if (data?.auth_url) {
        window.open(data.auth_url, "_blank");
      }
    } catch (e) {
      alert("Please run `python authenticate_youtube.py` in your terminal or check client_secret.json");
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-2xl bg-white border border-slate-200 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-gradient-to-r from-red-600 to-indigo-700 text-white">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-white/20 backdrop-blur-md">
              <Sparkles className="w-5 h-5 text-amber-300" />
            </div>
            <div>
              <h2 className="font-bold text-lg">AutoPilot YouTube Shorts Bot</h2>
              <p className="text-xs text-white/80">Autonomous 30-min Viral Video Clipper & Uploader</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-all cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-5 flex-1">
          {/* YouTube Authorization Status Card */}
          <div className="p-4 rounded-xl border border-slate-200 bg-slate-50 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className={`p-3 rounded-xl ${ytStatus.authenticated ? "bg-emerald-100 text-emerald-700" : "bg-amber-100 text-amber-700"}`}>
                <Video className="w-6 h-6" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="font-bold text-slate-900 text-sm">YouTube Channel Connection</h4>
                  {ytStatus.authenticated ? (
                    <span className="flex items-center gap-1 text-[11px] font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                      <CheckCircle2 className="w-3 h-3" /> Ready
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-[11px] font-bold text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200">
                      <AlertTriangle className="w-3 h-3" /> Auth Required
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-500 mt-0.5">
                  {ytStatus.authenticated
                    ? "OAuth token loaded. Direct background upload is active!"
                    : "Grant Google permission once so AutoPilot can post Shorts automatically."}
                </p>
              </div>
            </div>

            {!ytStatus.authenticated && (
              <button
                onClick={handleOpenAuthUrl}
                className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 transition-all cursor-pointer whitespace-nowrap"
              >
                <ShieldCheck className="w-4 h-4" />
                <span>Authorize Channel</span>
              </button>
            )}
          </div>

          {/* AutoPilot Engine State Card */}
          <div className="p-5 rounded-xl border-2 border-indigo-500/30 bg-indigo-50/50 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-600">Scheduler Status</span>
                <div className="flex items-center gap-2 mt-0.5">
                  <div className={`w-3 h-3 rounded-full ${apStatus?.is_running ? "bg-emerald-500 animate-ping" : "bg-slate-400"}`} />
                  <span className="font-extrabold text-slate-900 text-base">
                    {apStatus?.is_running ? "ACTIVE & RUNNING" : "STOPPED"}
                  </span>
                </div>
              </div>

              {apStatus?.is_running ? (
                <button
                  onClick={handleStop}
                  disabled={loading}
                  className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 cursor-pointer"
                >
                  <Square className="w-4 h-4" /> Stop AutoPilot
                </button>
              ) : (
                <button
                  onClick={handleStart}
                  disabled={loading || !ytStatus.authenticated}
                  className={`px-5 py-2.5 rounded-xl text-white font-bold text-xs shadow-md flex items-center gap-2 cursor-pointer transition-all ${
                    ytStatus.authenticated
                      ? "bg-gradient-to-r from-emerald-600 to-indigo-600 hover:opacity-95 shadow-indigo-600/20"
                      : "bg-slate-400 cursor-not-allowed"
                  }`}
                >
                  <Play className="w-4 h-4 fill-white" /> Start 30-Min Auto-Upload
                </button>
              )}
            </div>

            {/* Interval & Privacy Settings */}
            <div className="grid grid-cols-2 gap-3 pt-2 border-t border-indigo-200/60">
              <div>
                <label className="text-xs font-semibold text-slate-600 mb-1 block">Upload Frequency</label>
                <select
                  value={intervalMin}
                  onChange={(e) => setIntervalMin(Number(e.target.value))}
                  disabled={apStatus?.is_running}
                  className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs font-semibold text-slate-800"
                >
                  <option value={15}>Every 15 Minutes (Turbo)</option>
                  <option value={30}>Every 30 Minutes (Recommended)</option>
                  <option value={60}>Every 1 Hour (Standard)</option>
                  <option value={120}>Every 2 Hours (Relaxed)</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-600 mb-1 block">Video Visibility</label>
                <select
                  value={privacy}
                  onChange={(e) => setPrivacy(e.target.value)}
                  disabled={apStatus?.is_running}
                  className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs font-semibold text-slate-800"
                >
                  <option value="public">🌍 Public (Instant Reach)</option>
                  <option value="unlisted">🔗 Unlisted (Review Link First)</option>
                  <option value="private">🔒 Private (Draft Mode)</option>
                </select>
              </div>
            </div>

            {/* Real-time status tracker */}
            {apStatus?.is_running && (
              <div className="p-3 bg-white rounded-lg border border-indigo-100 flex items-center justify-between text-xs">
                <span className="text-slate-600">Current Action: <b className="text-indigo-600 capitalize">{apStatus.current_status}</b></span>
                <span className="font-mono text-indigo-700 font-bold bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
                  Next in: {Math.floor((apStatus.seconds_remaining || 0) / 60)}m {(apStatus.seconds_remaining || 0) % 60}s
                </span>
              </div>
            )}

            {msg && (
              <p className="text-xs font-semibold text-indigo-900 bg-white/70 p-2 rounded-lg border border-indigo-200">
                {msg}
              </p>
            )}
          </div>

          {/* Viral Topic Queue & GTA 6 Priority */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
                <Flame className="w-4 h-4 text-orange-500" />
                <span>Curated Viral Topics ({apStatus?.total_topics_queued || 14} queued)</span>
              </label>
            </div>

            {/* Add Custom Topic Form */}
            <form onSubmit={handleAddTopic} className="flex gap-2 mb-3">
              <select
                value={customCategory}
                onChange={(e) => setCustomCategory(e.target.value)}
                className="bg-slate-50 border border-slate-200 rounded-xl px-2.5 py-1.5 text-xs font-medium text-slate-700"
              >
                <option value="GTA 6">GTA 6</option>
                <option value="Sci-Fi">Sci-Fi</option>
                <option value="AI & Tech">AI & Tech</option>
                <option value="Gaming">Gaming</option>
                <option value="Mystery">Mystery</option>
              </select>
              <input
                type="text"
                placeholder="Enter custom viral topic (e.g. GTA 6 secret cheat codes)..."
                value={customTopic}
                onChange={(e) => setCustomTopic(e.target.value)}
                className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-indigo-500"
              />
              <button
                type="submit"
                className="px-3.5 py-1.5 rounded-xl bg-slate-900 hover:bg-black text-white text-xs font-bold flex items-center gap-1 transition-all cursor-pointer"
              >
                <Plus className="w-3.5 h-3.5" /> Add
              </button>
            </form>

            {/* Topics sample list */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-40 overflow-y-auto pr-1">
              {[
                { cat: "GTA 6", title: "GTA 6 leaked physics and graphics realism breakdown", tag: "🔥 TRENDING" },
                { cat: "GTA 6", title: "Vice City map comparison size vs GTA 5", tag: "🗺️ 3X MAP" },
                { cat: "GTA 6", title: "Lucia and Jason secret storyline details", tag: "💀 STORY" },
                { cat: "Sci-Fi", title: "James Webb telescope impossible deep space structure", tag: "🔭 SPACE" },
                { cat: "Sci-Fi", title: "Black hole time dilation paradox explained", tag: "⏳ TIME" },
                { cat: "AI & Tech", title: "Humanoid robots agility and AI consciousness", tag: "🤖 ROBOTICS" },
              ].map((t, idx) => (
                <div key={idx} className="p-2.5 rounded-lg border border-slate-200 bg-white flex items-center justify-between text-xs">
                  <div className="truncate pr-2">
                    <span className="font-bold text-slate-800 block truncate">{t.title}</span>
                    <span className="text-[10px] text-slate-500 font-semibold">{t.cat}</span>
                  </div>
                  <span className="text-[10px] font-bold text-red-600 bg-red-50 border border-red-200 px-1.5 py-0.5 rounded whitespace-nowrap">
                    {t.tag}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Upload History */}
          {apStatus?.history && apStatus.history.length > 0 && (
            <div>
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2 block">
                Recent Automated Uploads
              </label>
              <div className="space-y-1.5 max-h-36 overflow-y-auto">
                {apStatus.history.map((h, i) => (
                  <div key={i} className="p-2.5 rounded-lg border border-slate-200 bg-slate-50 flex items-center justify-between text-xs">
                    <div>
                      <span className="font-bold text-slate-900 block">{h.title}</span>
                      <span className="text-[10px] text-slate-500">{h.time} • {h.category}</span>
                    </div>
                    {h.youtube_url ? (
                      <a
                        href={h.youtube_url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-red-600 hover:text-red-700 font-bold flex items-center gap-1 text-[11px]"
                      >
                        <span>Watch Short</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    ) : (
                      <span className="text-[10px] text-slate-400 font-mono">{h.status}</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-between">
          <span className="text-xs text-slate-500">
            Automated via ClipFlow AI • 9:16 Shorts • Hormozi Clean
          </span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-xl bg-slate-200 hover:bg-slate-300 text-slate-800 text-xs font-bold cursor-pointer"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
