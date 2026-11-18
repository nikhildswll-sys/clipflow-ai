import React, { useState } from "react";
import {
  Flame,
  Clock,
  Sparkles,
  ChevronDown,
  ChevronUp,
  Download,
  Share2,
  CheckCircle2,
  UserCheck,
  TrendingUp,
  Zap,
  Tag
} from "lucide-react";

export default function ClipsList({
  clips = [],
  activeClipId,
  onSelectClip,
  onOpenPackaging,
  onExportClip,
  isRendering = false
}) {
  const [expandedScoreId, setExpandedScoreId] = useState(null);

  const toggleScoreBreakdown = (e, id) => {
    e.stopPropagation();
    setExpandedScoreId(expandedScoreId === id ? null : id);
  };

  const formatTime = (sec) => {
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s < 10 ? "0" : ""}${s}`;
  };

  return (
    <div className="flex flex-col gap-3">
      {/* Title & Stats */}
      <div className="flex items-center justify-between px-1">
        <div className="flex items-center gap-2">
          <Flame className="w-5 h-5 text-indigo-600" />
          <h2 className="font-bold text-slate-900 text-base">Viral Moments ({clips.length})</h2>
        </div>
        <span className="text-xs text-indigo-700 font-semibold bg-indigo-50 px-2.5 py-0.5 rounded-full border border-indigo-100">
          Ranked by Virality AI
        </span>
      </div>

      {/* Clips Cards List */}
      <div className="space-y-3">
        {clips.map((clip) => {
          const isSelected = clip.id === activeClipId;
          const breakdown = clip.breakdown || {};
          const isExpanded = expandedScoreId === clip.id;

          let scoreBadgeColor = "text-emerald-700 bg-emerald-50 border-emerald-200";
          if (clip.viral_score < 75) {
            scoreBadgeColor = "text-amber-700 bg-amber-50 border-amber-200";
          }

          return (
            <div
              key={clip.id}
              onClick={() => onSelectClip(clip.id)}
              className={`relative rounded-2xl p-4.5 border transition-all cursor-pointer ${
                isSelected
                  ? "bg-white border-indigo-500 shadow-md shadow-indigo-500/10 ring-2 ring-indigo-500/20"
                  : "bg-white border-slate-200/90 hover:border-slate-300 hover:shadow-sm"
              }`}
            >
              {/* Top Row: Category Badge + Viral Score */}
              <div className="flex items-center justify-between gap-2 mb-2">
                <div className="flex items-center gap-2">
                  <span
                    className="px-2.5 py-0.5 rounded-full text-xs font-bold border"
                    style={{
                      backgroundColor: `${clip.category_color}10`,
                      borderColor: `${clip.category_color}30`,
                      color: clip.category_color,
                    }}
                  >
                    {clip.category_badge || clip.category_label}
                  </span>

                  <div className="flex items-center gap-1 text-[11px] text-slate-500 font-medium">
                    <Clock className="w-3.5 h-3.5" />
                    <span className="font-mono">
                      {formatTime(clip.start)} - {formatTime(clip.end)}
                    </span>
                    <span className="text-slate-400">({Math.round(clip.duration)}s)</span>
                  </div>
                </div>

                {/* Viral Potential Score Badge */}
                <button
                  onClick={(e) => toggleScoreBreakdown(e, clip.id)}
                  title="Click to view Virality Breakdown"
                  className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-bold border transition-transform hover:scale-105 cursor-pointer ${scoreBadgeColor}`}
                >
                  <TrendingUp className="w-3.5 h-3.5" />
                  <span>{clip.viral_score}</span>
                  <span className="text-[10px] opacity-75">/100</span>
                  {isExpanded ? <ChevronUp className="w-3 h-3 ml-0.5" /> : <ChevronDown className="w-3 h-3 ml-0.5" />}
                </button>
              </div>

              {/* Title / Hook Preview */}
              <h3 className="font-bold text-slate-900 text-sm line-clamp-2 leading-snug mb-1.5">
                {clip.packaging?.title || clip.suggested_title || clip.text.slice(0, 70)}
              </h3>

              {/* Opening hook quote */}
              <p className="text-xs text-slate-500 line-clamp-2 italic mb-3">
                "{clip.packaging?.hook || clip.text.slice(0, 100)}..."
              </p>

              {/* Score breakdown drawer */}
              {isExpanded && (
                <div className="mb-3 p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-1.5 animate-fade-in">
                  <div className="flex justify-between items-center text-slate-700">
                    <span>Hook Strength (Curiosity Gap):</span>
                    <span className="font-mono font-bold text-amber-600">{breakdown.hook_strength || 22}/25</span>
                  </div>
                  <div className="flex justify-between items-center text-slate-700">
                    <span>Emotional Intensity:</span>
                    <span className="font-mono font-bold text-rose-600">{breakdown.emotional_intensity || 23}/25</span>
                  </div>
                  <div className="flex justify-between items-center text-slate-700">
                    <span>Retention & Pacing:</span>
                    <span className="font-mono font-bold text-indigo-600">{breakdown.retention_pacing || 18}/20</span>
                  </div>
                  <div className="flex justify-between items-center text-slate-700">
                    <span>Punchline Quality:</span>
                    <span className="font-mono font-bold text-emerald-600">{breakdown.punchline_delivery || 14}/15</span>
                  </div>
                </div>
              )}

              {/* Bottom Actions Row */}
              <div className="flex items-center justify-between pt-2 border-t border-slate-100 text-xs">
                <div className="flex items-center gap-2 text-slate-500">
                  {clip.multi_speaker && (
                    <span className="flex items-center gap-1 text-[11px] text-emerald-600 font-semibold bg-emerald-50 px-2 py-0.5 rounded-md">
                      <UserCheck className="w-3 h-3" />
                      2 Speakers
                    </span>
                  )}
                  {clip.rendered_video && (
                    <span className="flex items-center gap-1 text-[11px] text-indigo-600 font-semibold bg-indigo-50 px-2 py-0.5 rounded-md">
                      <CheckCircle2 className="w-3 h-3" />
                      Rendered
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {/* AI Packaging / Copy Button */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onOpenPackaging(clip);
                    }}
                    className="p-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition-all cursor-pointer border border-slate-200"
                    title="Generate viral hooks, titles & social copy"
                  >
                    <Share2 className="w-3.5 h-3.5" />
                  </button>

                  {/* Render / Export Quick Button */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onExportClip(clip);
                    }}
                    disabled={isRendering}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-semibold transition-all cursor-pointer shadow-sm"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Export</span>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
