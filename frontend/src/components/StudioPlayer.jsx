import React, { useRef, useState, useEffect } from "react";
import {
  Play,
  Pause,
  RotateCcw,
  Volume2,
  VolumeX,
  Maximize2,
  Sliders,
  Scissors,
  UserCheck,
  Zap,
  Sparkles,
  Download,
  Share2,
  Clock,
  Layers,
  Edit3
} from "lucide-react";

export default function StudioPlayer({
  project,
  clip,
  aspectRatio = "9:16",
  resolution = "1080p",
  captionStyle = "hormozi",
  customCaptions = {},
  onUpdateClipBounds,
  onOpenPackaging,
  onOpenWordEditor,
  onTranslateEnglish,
  onConvertToHinglish,
  isTranslating = false,
  isConvertingHinglish = false,
  onExportCurrent,
  isRendering = false
}) {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const [showFaceTrackerOverlay, setShowFaceTrackerOverlay] = useState(false);
  const [silenceSkip, setSilenceSkip] = useState(false);

  // Active word calculation for real-time live captions
  const [activeWordsGroup, setActiveWordsGroup] = useState([]);
  const [currentWordIdx, setCurrentWordIdx] = useState(-1);

  const clipStart = clip ? clip.start : 0;
  const clipEnd = clip ? clip.end : duration || 30;

  // Sync video time to clip boundaries
  useEffect(() => {
    if (videoRef.current && clip) {
      videoRef.current.currentTime = clip.start;
      setCurrentTime(clip.start);
      setIsPlaying(false);
    }
  }, [clip?.id]);

  const handleTimeUpdate = () => {
    if (!videoRef.current || !clip) return;
    const t = videoRef.current.currentTime;
    setCurrentTime(t);

    // Loop within clip boundary
    if (t >= clipEnd) {
      videoRef.current.currentTime = clipStart;
      videoRef.current.play();
      return;
    }

    // Determine current caption words group and active word
    if (clip.words && clip.words.length > 0) {
      // Find words in active 2-second or 3-word window
      const wordsPerGroup = customCaptions.words_per_group || (captionStyle === "mrbeast" ? 2 : captionStyle === "minimal" ? 5 : 3);
      
      // Find active word
      const foundIdx = clip.words.findIndex(w => t >= w.start && t <= w.end);
      
      if (foundIdx !== -1) {
        // Group chunk around found index
        const groupStart = Math.floor(foundIdx / wordsPerGroup) * wordsPerGroup;
        const chunk = clip.words.slice(groupStart, groupStart + wordsPerGroup);
        setActiveWordsGroup(chunk);
        setCurrentWordIdx(foundIdx - groupStart);
      } else {
        // Check if between words within the same phrase
        const currentGroup = clip.words.filter(w => t >= w.start - 0.2 && t <= w.end + 0.4);
        if (currentGroup.length > 0) {
          setActiveWordsGroup(currentGroup.slice(0, wordsPerGroup));
          setCurrentWordIdx(0);
        } else {
          setActiveWordsGroup([]);
          setCurrentWordIdx(-1);
        }
      }
    }
  };

  const togglePlay = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
      setIsPlaying(false);
    } else {
      if (videoRef.current.currentTime < clipStart || videoRef.current.currentTime >= clipEnd) {
        videoRef.current.currentTime = clipStart;
      }
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  const restartClip = () => {
    if (!videoRef.current) return;
    videoRef.current.currentTime = clipStart;
    videoRef.current.play();
    setIsPlaying(true);
  };

  // Calculate container aspect ratio dimensions for preview frame
  const getAspectRatioClasses = () => {
    switch (aspectRatio) {
      case "9:16":
        return "aspect-[9/16] max-h-[580px] w-auto";
      case "16:9":
        return "aspect-[16/9] w-full max-w-[720px]";
      case "1:1":
        return "aspect-square max-h-[520px] w-auto";
      case "4:5":
        return "aspect-[4/5] max-h-[560px] w-auto";
      default:
        return "aspect-[9/16] max-h-[580px] w-auto";
    }
  };

  // Calculate crop center offset from face tracking
  const cropCenterX = clip?.crop_center_x ? clip.crop_center_x * 100 : 50;

  // Format seconds to mm:ss
  const formatTime = (sec) => {
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s < 10 ? "0" : ""}${s}`;
  };

  // Caption style classes
  const getCaptionContainerStyle = () => {
    const pos = customCaptions.position || "bottom";
    if (pos === "top") return "top-10";
    if (pos === "center") return "top-1/2 -translate-y-1/2";
    return "bottom-14";
  };

  const getFontSizeClass = () => {
    const size = customCaptions.font_size || "medium";
    if (size === "small") return "text-[11px] sm:text-xs md:text-sm";
    if (size === "large") return "text-sm sm:text-base md:text-lg";
    return "text-xs sm:text-sm md:text-base";
  };

  const renderCaptionWords = () => {
    if (!activeWordsGroup || activeWordsGroup.length === 0) return null;

    const uppercase = customCaptions.uppercase ?? (captionStyle !== "minimal" && captionStyle !== "cinematic");
    const font = customCaptions.fontname || (captionStyle === "podcast" ? "Montserrat" : captionStyle === "minimal" ? "Poppins" : "Anton");
    const boxStyle = customCaptions.box_style || "none";
    const highlightColor = customCaptions.highlight_color || (captionStyle === "mrbeast" ? "#00FF66" : "#FFDE00");
    const fontSizeClass = getFontSizeClass();

    const boxContainerClasses = boxStyle === "none"
      ? ""
      : "bg-black/65 px-3 py-1.5 rounded-xl backdrop-blur-md border border-white/10 shadow-xl shadow-black/80";

    return (
      <div className={`absolute ${getCaptionContainerStyle()} left-0 right-0 px-3 text-center z-20 pointer-events-none select-none flex flex-wrap justify-center items-center gap-1.5`}>
        <div className={`inline-flex flex-wrap justify-center items-center gap-2 max-w-[92%] ${boxContainerClasses}`}>
          {activeWordsGroup.map((w, idx) => {
            const isActive = idx === currentWordIdx;
            let wordText = w.word;
            if (uppercase) wordText = wordText.toUpperCase();

            // Active box background if selected
            const activeWordBg = (boxStyle === "highlight" && isActive)
              ? "bg-indigo-600 text-white px-2 py-0.5 rounded-lg shadow-md ring-1 ring-white/40"
              : "";

            // Hormozi Style
            if (captionStyle === "hormozi") {
              return (
                <span
                  key={idx}
                  className={`font-black tracking-wide ${fontSizeClass} transition-all duration-75 ${activeWordBg} ${
                    isActive
                      ? "scale-106 drop-shadow-[0_2px_8px_rgba(0,0,0,1)]"
                      : "text-white drop-shadow-[0_1px_4px_rgba(0,0,0,0.9)] opacity-95"
                  }`}
                  style={{
                    fontFamily: `${font}, Impact, "Arial Black", sans-serif`,
                    color: isActive ? highlightColor : "#FFFFFF",
                    WebkitTextStroke: "1px #000000",
                    paintOrder: "stroke fill",
                    filter: isActive ? "drop-shadow(0 0 6px rgba(255,222,0,0.8))" : "none"
                  }}
                >
                  {wordText}
                </span>
              );
            }

            // MrBeast Style
            if (captionStyle === "mrbeast") {
              return (
                <span
                  key={idx}
                  className={`font-black tracking-wide ${fontSizeClass} transition-all duration-100 ${activeWordBg} ${
                    isActive
                      ? "-rotate-1 scale-108 drop-shadow-[0_2px_8px_rgba(0,0,0,1)]"
                      : "text-[#FFE600] drop-shadow-[0_1px_4px_rgba(0,0,0,0.9)]"
                  }`}
                  style={{
                    fontFamily: `${font}, Impact, "Arial Black", sans-serif`,
                    color: isActive ? highlightColor : "#FFE600",
                    WebkitTextStroke: "1.2px #000000",
                    paintOrder: "stroke fill",
                    filter: isActive ? "drop-shadow(0 0 6px rgba(0,255,102,0.85))" : "none"
                  }}
                >
                  {wordText}
                </span>
              );
            }

            // Minimal Style
            if (captionStyle === "minimal") {
              return (
                <span
                  key={idx}
                  className={`font-bold tracking-normal ${fontSizeClass} px-2 py-0.5 rounded-lg transition-all duration-150 ${
                    isActive
                      ? "bg-white text-slate-900 shadow-md ring-1 ring-indigo-500/30 scale-105"
                      : "bg-black/60 text-slate-200"
                  }`}
                  style={{ fontFamily: `${font}, sans-serif` }}
                >
                  {wordText}
                </span>
              );
            }

            // Podcast Style
            if (captionStyle === "podcast") {
              return (
                <span
                  key={idx}
                  className={`font-extrabold ${fontSizeClass} transition-all duration-100 ${
                    isActive
                      ? "scale-105 bg-cyan-500/30 px-1.5 py-0.5 rounded-md border border-cyan-400"
                      : "text-white"
                  }`}
                  style={{
                    fontFamily: `${font}, Montserrat, sans-serif`,
                    color: isActive ? (highlightColor || "#06B6D4") : "#FFFFFF",
                    WebkitTextStroke: "1px #000000",
                    paintOrder: "stroke fill",
                    textShadow: isActive ? "0 0 8px rgba(6,182,212,0.85)" : "0 1px 3px rgba(0,0,0,0.8)"
                  }}
                >
                  {wordText}
                </span>
              );
            }

            // Cinematic Style
            if (captionStyle === "cinematic") {
              return (
                <span
                  key={idx}
                  className={`font-bold tracking-widest ${fontSizeClass} transition-colors duration-200 ${
                    isActive ? "scale-105" : "text-neutral-200"
                  }`}
                  style={{
                    fontFamily: font,
                    color: isActive ? (highlightColor || "#FBBF24") : "#EAEAEA",
                    textShadow: "0 2px 8px rgba(0,0,0,0.9)"
                  }}
                >
                  {wordText}
                </span>
              );
            }

            // Gaming Style
            if (captionStyle === "gaming") {
              return (
                <span
                  key={idx}
                  className={`font-black tracking-wider ${fontSizeClass} transition-all duration-100 ${
                    isActive
                      ? "scale-108 drop-shadow-[0_0_12px_rgba(255,0,122,0.85)]"
                      : "text-[#FFE600] drop-shadow-[0_1px_3px_rgba(0,0,0,0.9)]"
                  }`}
                  style={{
                    fontFamily: font,
                    color: isActive ? (highlightColor || "#FF007A") : "#FFE600",
                    WebkitTextStroke: "1.2px #2E004B"
                  }}
                >
                  {wordText}
                </span>
              );
            }

            // Neon Style
            return (
              <span
                key={idx}
                className={`font-black tracking-wide ${fontSizeClass} transition-all duration-150 ${
                  isActive
                    ? "scale-108 drop-shadow-[0_0_14px_#00FF88]"
                    : "text-white drop-shadow-[0_0_6px_rgba(0,255,136,0.35)]"
                }`}
                style={{
                  fontFamily: font,
                  color: isActive ? (highlightColor || "#00FF88") : "#FFFFFF",
                  WebkitTextStroke: "0.8px #003311"
                }}
              >
                {wordText}
              </span>
            );
          })}
        </div>
      </div>
    );
  };

  const clipProgress = clip
    ? Math.max(0, Math.min(100, ((currentTime - clipStart) / Math.max(0.1, clipEnd - clipStart)) * 100))
    : 0;

  return (
    <div className="flex flex-col bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
      {/* Top Bar with Language Switcher & Aspect Ratio Badge */}
      <div className="flex flex-wrap items-center justify-between gap-3 px-5 py-3.5 bg-slate-50 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-indigo-50 border border-indigo-100 text-indigo-700 text-xs font-semibold">
            <Layers className="w-3.5 h-3.5 text-indigo-600" />
            <span>Ratio: {aspectRatio}</span>
            {aspectRatio === "9:16" && (
              <span className="px-1.5 py-0.2 rounded text-[9px] bg-indigo-600 text-white font-bold">
                SHORTS DEFAULT
              </span>
            )}
          </div>

          {/* Language Switcher Buttons */}
          <div className="flex items-center bg-white p-0.5 rounded-lg border border-slate-200 text-xs shadow-sm">
            <button
              onClick={onTranslateEnglish}
              disabled={isTranslating}
              className={`px-2.5 py-1 rounded-md font-semibold transition-all cursor-pointer ${
                project?.language_mode === "english"
                  ? "bg-indigo-600 text-white font-bold shadow-sm"
                  : "text-slate-600 hover:text-slate-900"
              }`}
              title="Translate Hindi / Urdu directly into fluent English using Whisper AI"
            >
              {isTranslating ? "Translating..." : "🇬🇧 English"}
            </button>
            <button
              onClick={onConvertToHinglish}
              disabled={isConvertingHinglish}
              className={`px-2.5 py-1 rounded-md font-semibold transition-all cursor-pointer ${
                project?.language_mode === "hinglish" || project?.is_hinglish
                  ? "bg-indigo-600 text-white font-bold shadow-sm"
                  : "text-slate-600 hover:text-slate-900"
              }`}
              title="Convert Hindi/Devanagari to clean Roman Hinglish"
            >
              {isConvertingHinglish ? "Converting..." : "🇮🇳 Hinglish"}
            </button>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Edit Words Button */}
          <button
            onClick={onOpenWordEditor}
            title="Edit Subtitle Words & Fix Spellings"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white hover:bg-slate-100 text-slate-700 text-xs font-semibold border border-slate-200 transition-all cursor-pointer shadow-sm"
          >
            <Edit3 className="w-3.5 h-3.5 text-indigo-600" />
            <span>Edit Words</span>
          </button>

          {/* Face Tracking Visualizer Toggle */}
          <button
            onClick={() => setShowFaceTrackerOverlay(!showFaceTrackerOverlay)}
            title="Toggle Smart Face Tracking overlay"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              showFaceTrackerOverlay
                ? "bg-indigo-600 text-white shadow-sm"
                : "bg-white hover:bg-slate-100 text-slate-700 border border-slate-200"
            }`}
          >
            <UserCheck className="w-3.5 h-3.5" />
            <span>Face Track {showFaceTrackerOverlay ? "ON" : "OFF"}</span>
          </button>

          {/* Social Packaging Hook Generator Button */}
          <button
            onClick={onOpenPackaging}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold shadow-sm shadow-indigo-600/20 transition-all cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>AI Hooks</span>
          </button>
        </div>
      </div>

      {/* Main Video Stage */}
      <div className="relative flex items-center justify-center p-6 bg-radial from-[#181B2E] to-[#0A0B12] min-h-[500px]">
        {/* Aspect Ratio Canvas Frame */}
        <div
          className={`relative rounded-2xl overflow-hidden bg-black shadow-2xl border-2 border-slate-700/60 flex items-center justify-center ${getAspectRatioClasses()}`}
        >
          {/* HTML5 Video */}
          <video
            ref={videoRef}
            src={project?.video_url}
            className="w-full h-full object-cover transition-all duration-300"
            style={{
              objectPosition: `${cropCenterX}% 35%`,
            }}
            onTimeUpdate={handleTimeUpdate}
            onLoadedMetadata={() => setDuration(videoRef.current?.duration || 0)}
            muted={isMuted}
            playsInline
          />

          {/* Smart Face Tracking Overlay (if enabled) */}
          {showFaceTrackerOverlay && (
            <div
              className="absolute pointer-events-none transition-all duration-300 border-2 border-dashed border-cyan-400 bg-cyan-400/10 rounded-xl"
              style={{
                left: `calc(${cropCenterX}% - 60px)`,
                top: "22%",
                width: "120px",
                height: "140px",
              }}
            >
              <div className="absolute -top-6 left-1/2 -translate-x-1/2 bg-cyan-500 text-black px-2 py-0.5 rounded text-[10px] font-bold whitespace-nowrap shadow">
                SPEAKER 1 (Tracked {Math.round(cropCenterX)}%)
              </div>
            </div>
          )}

          {/* Live Synchronized Animated Subtitle Overlay */}
          {renderCaptionWords()}

          {/* Top Hook Preview Tag on Video */}
          {clip?.packaging?.opening_overlay_text && (
            <div className="absolute top-5 left-3 right-3 text-center pointer-events-none">
              <span className="inline-block bg-red-600/90 text-white text-[11px] font-black uppercase tracking-wider px-3 py-1 rounded-md shadow-lg border border-red-400/40">
                {clip.packaging.opening_overlay_text}
              </span>
            </div>
          )}

          {/* Play / Pause Big Center Overlay when paused */}
          {!isPlaying && (
            <button
              onClick={togglePlay}
              className="absolute inset-0 m-auto w-16 h-16 rounded-full bg-purple-600/80 hover:bg-purple-600 text-white flex items-center justify-center backdrop-blur-md shadow-2xl transition-transform hover:scale-110 cursor-pointer"
            >
              <Play className="w-7 h-7 fill-white translate-x-0.5" />
            </button>
          )}
        </div>
      </div>

      {/* Timeline Controls & Clip Scrub Area */}
      <div className="p-4 bg-white border-t border-slate-200 flex flex-col gap-3">
        {/* Clip Progress Bar */}
        <div className="flex items-center gap-3">
          <span className="text-xs font-mono text-slate-500 min-w-[45px]">
            {formatTime(currentTime)}
          </span>
          <div className="relative flex-1 h-2.5 bg-slate-100 rounded-full overflow-hidden cursor-pointer border border-slate-200">
            {/* Range highlight of the clip */}
            <div
              className="absolute top-0 bottom-0 bg-indigo-100 rounded-full"
              style={{
                left: `${(clipStart / (duration || 60)) * 100}%`,
                width: `${((clipEnd - clipStart) / (duration || 60)) * 100}%`,
              }}
            />
            {/* Playhead */}
            <div
              className="absolute top-0 bottom-0 bg-indigo-600 rounded-full transition-all duration-75"
              style={{ width: `${clipProgress}%` }}
            />
          </div>
          <span className="text-xs font-mono text-slate-500 min-w-[45px]">
            {formatTime(clipEnd)}
          </span>
        </div>

        {/* Trim Boundaries & Fine Adjust Buttons */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-1 text-xs">
          <div className="flex items-center gap-2">
            <button
              onClick={togglePlay}
              className="p-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white transition-all shadow-sm cursor-pointer"
            >
              {isPlaying ? <Pause className="w-4 h-4 fill-white" /> : <Play className="w-4 h-4 fill-white" />}
            </button>
            <button
              onClick={restartClip}
              title="Restart Clip"
              className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition-all cursor-pointer border border-slate-200"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
            <button
              onClick={() => setIsMuted(!isMuted)}
              className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition-all cursor-pointer border border-slate-200"
            >
              {isMuted ? <VolumeX className="w-4 h-4 text-rose-500" /> : <Volume2 className="w-4 h-4" />}
            </button>
          </div>

          {/* In/Out Trim Markers */}
          <div className="flex items-center gap-3 bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-200">
            <div className="flex items-center gap-1.5">
              <Scissors className="w-3.5 h-3.5 text-indigo-600" />
              <span className="text-slate-500 font-medium">In:</span>
              <span className="font-mono text-slate-900 font-bold">{formatTime(clipStart)}</span>
              <button
                onClick={() => onUpdateClipBounds && onUpdateClipBounds(clip.id, Math.max(0, clipStart - 0.5), clipEnd)}
                className="px-1.5 py-0.5 rounded bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 text-[10px]"
              >
                -0.5s
              </button>
              <button
                onClick={() => onUpdateClipBounds && onUpdateClipBounds(clip.id, Math.min(clipEnd - 5, clipStart + 0.5), clipEnd)}
                className="px-1.5 py-0.5 rounded bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 text-[10px]"
              >
                +0.5s
              </button>
            </div>

            <span className="text-slate-300">|</span>

            <div className="flex items-center gap-1.5">
              <span className="text-slate-500 font-medium">Out:</span>
              <span className="font-mono text-slate-900 font-bold">{formatTime(clipEnd)}</span>
              <button
                onClick={() => onUpdateClipBounds && onUpdateClipBounds(clip.id, clipStart, Math.max(clipStart + 5, clipEnd - 0.5))}
                className="px-1.5 py-0.5 rounded bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 text-[10px]"
              >
                -0.5s
              </button>
              <button
                onClick={() => onUpdateClipBounds && onUpdateClipBounds(clip.id, clipStart, clipEnd + 0.5)}
                className="px-1.5 py-0.5 rounded bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 text-[10px]"
              >
                +0.5s
              </button>
            </div>
          </div>

          {/* Export Individual Clip Button */}
          <div className="flex items-center gap-2">
            <button
              onClick={onExportCurrent}
              disabled={isRendering}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-sm transition-all cursor-pointer disabled:opacity-50"
            >
              <Download className="w-4 h-4" />
              <span>{isRendering ? "Rendering Clip..." : "Export This Clip"}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
