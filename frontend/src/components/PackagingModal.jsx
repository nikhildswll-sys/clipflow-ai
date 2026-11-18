import React, { useState } from "react";
import {
  X,
  Sparkles,
  Copy,
  Check,
  Flame,
  Hash,
  Share2,
  Tv,
  MessageSquare
} from "lucide-react";

export default function PackagingModal({ clip, isOpen, onClose }) {
  if (!isOpen || !clip) return null;

  const [activePlatform, setActivePlatform] = useState("tiktok");
  const [copiedKey, setCopiedKey] = useState(null);

  const packaging = clip.packaging || {};
  const variations = packaging.platform_variations || {};
  const currentVar = variations[activePlatform] || { text: packaging.social_caption || "" };

  const handleCopy = (text, key) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-2xl bg-[#121422] border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-[#16192B]">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-purple-600/20 text-purple-400 border border-purple-500/30">
              <Sparkles className="w-5 h-5 text-amber-300" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">AI Viral Packaging & Hooks</h2>
              <p className="text-xs text-slate-400">High-CTR titles, opening text hooks & platform-ready copy</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 text-slate-400 hover:text-white transition-all cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-5">
          {/* Attention-Grabbing Opening Hook */}
          <div className="p-4 rounded-xl bg-gradient-to-r from-purple-950/40 to-indigo-950/30 border border-purple-500/40">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[11px] font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1">
                <Flame className="w-3.5 h-3.5" />
                Catchy Viral Hook (First 3 Seconds)
              </span>
              <button
                onClick={() => handleCopy(packaging.hook, "hook")}
                className="flex items-center gap-1 text-xs text-purple-300 hover:text-white transition-colors cursor-pointer"
              >
                {copiedKey === "hook" ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedKey === "hook" ? "Copied!" : "Copy"}</span>
              </button>
            </div>
            <p className="text-base font-bold text-white tracking-wide">
              "{packaging.hook}"
            </p>
          </div>

          {/* Engaging Video Title */}
          <div className="p-4 rounded-xl bg-[#171A2C] border border-slate-800">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                Optimized Video Title
              </span>
              <button
                onClick={() => handleCopy(packaging.title, "title")}
                className="flex items-center gap-1 text-xs text-slate-400 hover:text-white transition-colors cursor-pointer"
              >
                {copiedKey === "title" ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedKey === "title" ? "Copied!" : "Copy"}</span>
              </button>
            </div>
            <p className="text-sm font-semibold text-slate-200">
              {packaging.title}
            </p>
          </div>

          {/* Attention Grabbing Opening Overlay Text */}
          <div className="p-4 rounded-xl bg-[#171A2C] border border-slate-800">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[11px] font-bold text-cyan-400 uppercase tracking-wider">
                Video Screen Text Overlay
              </span>
              <button
                onClick={() => handleCopy(packaging.opening_overlay_text, "overlay")}
                className="flex items-center gap-1 text-xs text-slate-400 hover:text-white transition-colors cursor-pointer"
              >
                {copiedKey === "overlay" ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedKey === "overlay" ? "Copied!" : "Copy"}</span>
              </button>
            </div>
            <p className="text-sm font-semibold text-cyan-200">
              {packaging.opening_overlay_text}
            </p>
          </div>

          {/* Platform Variations Tabs */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Multi-Platform Social Captions
              </span>
              <span className="text-[11px] text-slate-500">Auto-tailored length & tags</span>
            </div>

            <div className="flex bg-[#0A0B13] p-1 rounded-xl border border-slate-800 mb-3 overflow-x-auto">
              {[
                { id: "tiktok", label: "TikTok" },
                { id: "instagram_reels", label: "Instagram Reels" },
                { id: "youtube_shorts", label: "YouTube Shorts" },
                { id: "x_twitter", label: "X / Twitter" },
                { id: "linkedin", label: "LinkedIn" }
              ].map((plat) => (
                <button
                  key={plat.id}
                  onClick={() => setActivePlatform(plat.id)}
                  className={`flex-1 min-w-[100px] py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer whitespace-nowrap ${
                    activePlatform === plat.id
                      ? "bg-purple-600 text-white shadow-md shadow-purple-600/30"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  {plat.label}
                </button>
              ))}
            </div>

            {/* Platform Textbox */}
            <div className="relative p-4 rounded-xl bg-[#0F111D] border border-slate-800 text-sm text-slate-200 font-sans whitespace-pre-wrap leading-relaxed">
              {currentVar.text}
              <button
                onClick={() => handleCopy(currentVar.text, "caption")}
                className="absolute top-3 right-3 flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-white transition-all cursor-pointer shadow"
              >
                {copiedKey === "caption" ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedKey === "caption" ? "Copied!" : "Copy Caption"}</span>
              </button>
            </div>
          </div>

          {/* Trending Hashtag Cloud */}
          {packaging.hashtags && packaging.hashtags.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1">
                  <Hash className="w-3.5 h-3.5 text-purple-400" />
                  Relevant Viral Hashtags
                </span>
                <button
                  onClick={() => handleCopy(packaging.hashtags.join(" "), "tags")}
                  className="text-xs text-purple-400 hover:text-white cursor-pointer"
                >
                  {copiedKey === "tags" ? "Copied all tags!" : "Copy all tags"}
                </button>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {packaging.hashtags.map((h, i) => (
                  <span
                    key={i}
                    className="px-2.5 py-1 rounded-lg bg-slate-800/80 border border-slate-700 text-slate-300 text-xs font-mono font-medium hover:border-purple-500 cursor-pointer transition-colors"
                    onClick={() => handleCopy(h, `h_${i}`)}
                  >
                    {h}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end px-6 py-3.5 border-t border-slate-800 bg-[#16192B]">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs transition-all shadow-md shadow-purple-600/30 cursor-pointer"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
