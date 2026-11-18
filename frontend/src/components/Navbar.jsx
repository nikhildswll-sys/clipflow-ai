import React from "react";
import {
  Scissors,
  Layers,
  Sparkles,
  Download,
  Plus,
  Video,
  Monitor,
  Moon,
  Sun
} from "lucide-react";

export default function Navbar({
  aspectRatio = "9:16",
  onSelectAspectRatio,
  resolution = "1080p",
  onSelectResolution,
  onOpenIngest,
  onOpenAutoPilot,
  onBatchDownload,
  isBatchRendering,
  totalClipsCount = 0,
  isDark = false,
  onToggleTheme
}) {
  const aspectRatios = [
    { id: "9:16", label: "9:16", badge: "DEFAULT", desc: "Shorts / Reels" },
    { id: "16:9", label: "16:9", badge: "WIDE", desc: "Landscape" },
    { id: "1:1", label: "1:1", badge: "FEED", desc: "Square" },
    { id: "4:5", label: "4:5", badge: "PORTRAIT", desc: "Portrait" },
  ];

  const resolutions = [
    { id: "1080p", label: "1080p FHD" },
    { id: "2k", label: "2K QHD" },
    { id: "4k", label: "4K UHD" },
    { id: "source", label: "Source" },
  ];

  return (
    <header className="sticky top-0 z-40 w-full bg-white/95 backdrop-blur-md border-b border-slate-200 px-6 py-3 shadow-[0_1px_3px_rgba(0,0,0,0.03)]">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
        {/* Brand Logo */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center shadow-md shadow-indigo-600/20 text-white">
            <Scissors className="w-5 h-5 stroke-[2.5]" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg text-slate-900 tracking-tight font-['Plus_Jakarta_Sans',sans-serif]">
                ClipFlow <span className="text-indigo-600">AI</span>
              </span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-600 border border-indigo-100">
                PRO 2.0
              </span>
            </div>
            <p className="text-[11px] text-slate-500 font-medium">AI Podcast & Live Stream Clipper</p>
          </div>
        </div>

        {/* Center: Aspect Ratio & Resolution Selectors */}
        <div className="flex items-center gap-2 bg-slate-100/80 p-1 rounded-xl border border-slate-200/80">
          {/* Aspect Ratio Switcher */}
          <div className="flex items-center gap-1">
            {aspectRatios.map((ar) => {
              const isSelected = aspectRatio === ar.id;
              return (
                <button
                  key={ar.id}
                  onClick={() => onSelectAspectRatio(ar.id)}
                  title={ar.desc}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                    isSelected
                      ? "bg-white text-indigo-700 shadow-sm border border-slate-200"
                      : "text-slate-600 hover:text-slate-900 hover:bg-slate-200/60"
                  }`}
                >
                  <span>{ar.label}</span>
                  {ar.badge === "DEFAULT" && (
                    <span className={`px-1 py-0.2 rounded text-[9px] font-extrabold ${isSelected ? "bg-indigo-100 text-indigo-700" : "bg-slate-200 text-slate-600"}`}>
                      DEF
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          <span className="text-slate-300">|</span>

          {/* Resolution Switcher */}
          <div className="flex items-center gap-1 pr-1">
            {resolutions.map((res) => {
              const isSelected = resolution === res.id;
              return (
                <button
                  key={res.id}
                  onClick={() => onSelectResolution(res.id)}
                  className={`px-2.5 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    isSelected
                      ? "bg-indigo-600 text-white font-bold shadow-sm"
                      : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  {res.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Actions: AutoPilot + Ingest + Batch Export */}
        <div className="flex items-center gap-2.5">
          {/* AutoPilot 30-min Bot Button */}
          <button
            onClick={onOpenAutoPilot}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-gradient-to-r from-red-600 to-indigo-600 hover:opacity-95 text-white text-xs font-bold shadow-md shadow-red-600/20 transition-all cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>AutoPilot Bot ⚡</span>
          </button>

          {/* New Video Ingest Button */}
          <button
            onClick={onOpenIngest}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-800 text-xs font-semibold transition-all cursor-pointer shadow-sm"
          >
            <Plus className="w-4 h-4 text-indigo-600" />
            <span>Import</span>
          </button>

          {/* Download All Clips Batch Zip Button */}
          <button
            onClick={onBatchDownload}
            disabled={isBatchRendering || totalClipsCount === 0}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold shadow-md shadow-indigo-600/20 transition-all cursor-pointer disabled:opacity-50"
          >
            <Download className="w-4 h-4" />
            <span>{isBatchRendering ? "Packaging ZIP..." : `Download All (${totalClipsCount})`}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
