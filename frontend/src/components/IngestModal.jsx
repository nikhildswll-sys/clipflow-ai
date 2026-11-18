import React, { useState, useEffect, useRef } from "react";
import {
  X,
  Upload,
  Radio,
  FileVideo,
  Sparkles,
  Link2,
  CheckCircle2,
  AlertCircle,
  Clock,
  Layers,
  Video,
  Cpu,
  Terminal,
  Activity,
  ArrowRight
} from "lucide-react";

export default function IngestModal({
  isOpen,
  onClose,
  onUploadFile,
  onImportYouTube,
  onImportStream,
  onLoadDemo,
  isProcessing = false,
  jobProgress = {}
}) {
  if (!isOpen) return null;

  const [activeTab, setActiveTab] = useState("youtube");
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [streamUrl, setStreamUrl] = useState("");
  const [streamDuration, setStreamDuration] = useState(60);
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const logsEndRef = useRef(null);

  // Auto-scroll live logs
  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [jobProgress?.logs?.length]);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const submitUpload = () => {
    if (selectedFile) {
      onUploadFile(selectedFile);
    }
  };

  const submitYouTube = (e) => {
    e.preventDefault();
    if (youtubeUrl.trim()) {
      onImportYouTube(youtubeUrl.trim());
    }
  };

  const submitStream = (e) => {
    e.preventDefault();
    if (streamUrl.trim()) {
      onImportStream(streamUrl.trim(), streamDuration);
    }
  };

  const currentStep = jobProgress?.step || 1;
  const progressPercent = jobProgress?.progress || 10;
  const stepTitle = jobProgress?.step_title || "Initializing AI Pipeline...";
  const logs = jobProgress?.logs || [];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-2xl bg-white border border-slate-200/90 rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh]">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4.5 border-b border-slate-100 bg-slate-50/70">
          <div className="flex items-center gap-3">
            <div className={`p-2.5 rounded-2xl ${isProcessing ? "bg-indigo-600 text-white animate-pulse" : "bg-indigo-50 text-indigo-600"} border border-indigo-100`}>
              {isProcessing ? <Activity className="w-5 h-5" /> : <Upload className="w-5 h-5" />}
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                {isProcessing ? "AI Clipping Pipeline Active" : "Import Podcast or Live Stream"}
              </h2>
              <p className="text-xs text-slate-500">
                {isProcessing ? "Live progress & terminal output" : "Automatic speech transcription, face tracking & viral cuts"}
              </p>
            </div>
          </div>
          {!isProcessing && (
            <button
              onClick={onClose}
              className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-500 hover:text-slate-800 transition-all cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* IF PROCESSING: LIVE MISSION CONTROL STEPPER & TERMINAL FEED */}
        {isProcessing ? (
          <div className="p-6 flex flex-col gap-5 overflow-y-auto bg-white">
            {/* Giant Progress Bar */}
            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 shadow-sm flex flex-col gap-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-sm font-bold text-slate-900">
                  <Cpu className="w-4 h-4 text-indigo-600 animate-spin" />
                  <span>{stepTitle}</span>
                </div>
                <span className="font-mono text-2xl font-black text-indigo-600">
                  {progressPercent}%
                </span>
              </div>

              {/* Progress track */}
              <div className="w-full h-3 bg-slate-200 rounded-full overflow-hidden p-0.5">
                <div
                  className="h-full bg-gradient-to-r from-indigo-600 via-indigo-500 to-emerald-500 rounded-full transition-all duration-300 relative shadow-sm"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>

              <div className="flex justify-between text-[11px] text-slate-500 font-medium">
                <span>Step {currentStep} of 5</span>
                <span>Aspect Ratio: 9:16 Shorts Default • Lossless Quality</span>
              </div>
            </div>

            {/* Step-by-Step Checklist */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              {[
                { step: 1, label: "1. Download / Media Ingest", done: currentStep > 1, active: currentStep === 1 },
                { step: 2, label: "2. Audio Stream Extraction (PCM)", done: currentStep > 2, active: currentStep === 2 },
                { step: 3, label: "3. Faster-Whisper Transcription", done: currentStep > 3, active: currentStep === 3 },
                { step: 4, label: "4. Viral Moment & Hook AI Scan", done: currentStep > 4, active: currentStep === 4 },
                { step: 5, label: "5. Face Tracking & 9:16 Framing", done: currentStep >= 5 && progressPercent === 100, active: currentStep === 5 && progressPercent < 100 },
              ].map((st) => (
                <div
                  key={st.step}
                  className={`p-3 rounded-xl border flex items-center justify-between transition-all ${
                    st.done
                      ? "bg-emerald-50 border-emerald-200 text-emerald-800 font-semibold"
                      : st.active
                      ? "bg-indigo-50 border-indigo-300 text-indigo-900 font-bold shadow-sm"
                      : "bg-slate-50/60 border-slate-200 text-slate-400"
                  }`}
                >
                  <span>{st.label}</span>
                  {st.done ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  ) : st.active ? (
                    <span className="w-2.5 h-2.5 rounded-full bg-indigo-600 animate-ping" />
                  ) : null}
                </div>
              ))}
            </div>

            {/* Live Terminal Log Feed */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5 uppercase tracking-wider">
                  <Terminal className="w-3.5 h-3.5 text-indigo-600" />
                  Live Activity Terminal Output
                </span>
                <span className="text-[10px] text-emerald-600 font-mono font-semibold flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                  Real-time engine feed
                </span>
              </div>

              <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 font-mono text-[11px] text-emerald-300 h-40 overflow-y-auto space-y-1 select-text shadow-inner">
                {logs.length > 0 ? (
                  logs.map((line, idx) => (
                    <div key={idx} className="leading-relaxed">
                      {line}
                    </div>
                  ))
                ) : (
                  <div className="text-slate-500 italic">Initializing engine streams...</div>
                )}
                <div ref={logsEndRef} />
              </div>
            </div>
          </div>
        ) : (
          /* STANDARD INPUT TABS */
          <div className="bg-white">
            {/* Ingest Tabs */}
            <div className="flex bg-slate-100 p-1.5 border-b border-slate-200 gap-1">
              {[
                { id: "youtube", label: "YouTube URL", icon: Video },
                { id: "upload", label: "Upload File", icon: Upload },
                { id: "stream", label: "Live Stream Buffer", icon: Radio },
                { id: "demo", label: "Sample Projects", icon: Sparkles },
              ].map((tab) => {
                const Icon = tab.icon;
                const isTabActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                      isTabActive
                        ? "bg-white text-indigo-700 shadow-sm border border-slate-200/80"
                        : "text-slate-600 hover:text-slate-900 hover:bg-slate-200/50"
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </div>

            {/* Tab Content */}
            <div className="p-6">
              {/* TAB 1: YOUTUBE */}
              {activeTab === "youtube" && (
                <form onSubmit={submitYouTube} className="space-y-4">
                  <div>
                    <label className="text-xs font-bold text-slate-700 mb-2 block">
                      Paste YouTube Podcast or Interview Link
                    </label>
                    <div className="relative">
                      <Video className="absolute left-3.5 top-3.5 w-5 h-5 text-red-500" />
                      <input
                        type="url"
                        value={youtubeUrl}
                        onChange={(e) => setYoutubeUrl(e.target.value)}
                        placeholder="https://www.youtube.com/watch?v=..."
                        className="w-full pl-11 pr-4 py-3 rounded-2xl bg-white border border-slate-300 text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 placeholder-slate-400 transition-all shadow-sm"
                        required
                      />
                    </div>
                    <p className="text-[11px] text-slate-500 mt-2 font-medium">
                      Works with long podcasts (50+ min), interviews, and live streams. Auto-detects top 2–3 audience replay peaks.
                    </p>
                  </div>

                  <div className="p-4 rounded-2xl bg-indigo-50/70 border border-indigo-100 text-xs text-indigo-900 space-y-1">
                    <div className="font-bold text-indigo-700 flex items-center gap-1.5">
                      <Sparkles className="w-4 h-4" />
                      Audience Retention & Replay AI
                    </div>
                    <p className="text-slate-600 leading-relaxed">
                      Fetches YouTube's actual Most Replayed heatmap to pinpoint the most engaging viral moment across the full episode, with automatic 9:16 Shorts reframing and animated captions.
                    </p>
                  </div>

                  <button
                    type="submit"
                    disabled={!youtubeUrl}
                    className="w-full py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-md shadow-indigo-600/20 transition-all cursor-pointer disabled:opacity-50"
                  >
                    Fetch & Generate Top Viral Moments
                  </button>
                </form>
              )}

              {/* TAB 2: FILE UPLOAD */}
              {activeTab === "upload" && (
                <div className="space-y-4">
                  <div
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    className={`relative flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-3xl transition-all cursor-pointer ${
                      dragActive
                        ? "border-indigo-500 bg-indigo-50/40"
                        : selectedFile
                        ? "border-emerald-500 bg-emerald-50/30"
                        : "border-slate-300 hover:border-slate-400 bg-slate-50/60"
                    }`}
                  >
                    <input
                      type="file"
                      accept="video/*,audio/*"
                      onChange={handleFileChange}
                      className="absolute inset-0 opacity-0 cursor-pointer"
                    />

                    {selectedFile ? (
                      <div className="flex flex-col items-center text-center">
                        <CheckCircle2 className="w-12 h-12 text-emerald-600 mb-2" />
                        <span className="font-bold text-slate-900 text-sm mb-1">{selectedFile.name}</span>
                        <span className="text-xs text-slate-500 font-mono">
                          {(selectedFile.size / (1024 * 1024)).toFixed(1)} MB • Click or drag to replace
                        </span>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center text-center">
                        <div className="w-12 h-12 rounded-2xl bg-indigo-50 flex items-center justify-center text-indigo-600 mb-3 border border-indigo-100">
                          <FileVideo className="w-6 h-6" />
                        </div>
                        <span className="font-bold text-slate-900 text-sm mb-1">
                          Drag & Drop podcast video or audio here
                        </span>
                        <span className="text-xs text-slate-500 mb-3">
                          Supports MP4, MOV, MKV, WEBM, MP3, WAV (Up to 4K)
                        </span>
                        <span className="px-3.5 py-1.5 rounded-xl bg-white border border-slate-200 text-slate-700 text-xs font-bold shadow-sm">
                          Browse Files
                        </span>
                      </div>
                    )}
                  </div>

                  <button
                    onClick={submitUpload}
                    disabled={!selectedFile}
                    className="w-full py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-md shadow-indigo-600/20 transition-all cursor-pointer disabled:opacity-50"
                  >
                    Generate Viral Clips with AI
                  </button>
                </div>
              )}

              {/* TAB 3: LIVE STREAM BUFFER */}
              {activeTab === "stream" && (
                <form onSubmit={submitStream} className="space-y-4">
                  <div>
                    <label className="text-xs font-bold text-slate-700 mb-2 block">
                      Live Stream URL (HLS / m3u8 / RTMP / YouTube Live)
                    </label>
                    <div className="relative">
                      <Radio className="absolute left-3.5 top-3.5 w-5 h-5 text-emerald-500 animate-pulse" />
                      <input
                        type="text"
                        value={streamUrl}
                        onChange={(e) => setStreamUrl(e.target.value)}
                        placeholder="https://example.com/live/stream.m3u8"
                        className="w-full pl-11 pr-4 py-3 rounded-2xl bg-white border border-slate-300 text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 placeholder-slate-400"
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-xs font-semibold text-slate-700 mb-2">
                      <span>Live Buffer Window:</span>
                      <span className="font-mono text-indigo-600 font-bold">{streamDuration} Seconds</span>
                    </div>
                    <div className="flex items-center gap-2">
                      {[30, 60, 90, 120].map((dur) => (
                        <button
                          type="button"
                          key={dur}
                          onClick={() => setStreamDuration(dur)}
                          className={`flex-1 py-2 rounded-xl text-xs font-bold border transition-all cursor-pointer ${
                            streamDuration === dur
                              ? "bg-indigo-600 text-white border-indigo-600 shadow-sm"
                              : "bg-white border-slate-200 text-slate-600 hover:bg-slate-50"
                          }`}
                        >
                          {dur}s
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-100 text-xs text-emerald-900">
                    <span className="font-bold block mb-1">⚡ Instant Stream Clipping</span>
                    Records the live stream buffer in memory and cuts viral moments with minimal processing delay.
                  </div>

                  <button
                    type="submit"
                    disabled={!streamUrl}
                    className="w-full py-3.5 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm shadow-md shadow-emerald-600/20 transition-all cursor-pointer disabled:opacity-50"
                  >
                    Capture & Clip Live Stream
                  </button>
                </form>
              )}

              {/* TAB 4: DEMO SAMPLES */}
              {activeTab === "demo" && (
                <div className="space-y-3">
                  <span className="text-xs text-slate-500 block mb-1 font-medium">
                    Select a pre-analyzed long-form studio podcast to explore all features instantly:
                  </span>

                  <div
                    onClick={() => onLoadDemo("demo_podcast_01")}
                    className="p-4 rounded-2xl bg-slate-50 hover:bg-indigo-50/50 border border-slate-200 hover:border-indigo-300 transition-all cursor-pointer flex items-center justify-between group shadow-sm"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-indigo-100 border border-indigo-200 flex items-center justify-center text-indigo-700 font-black">
                        AI
                      </div>
                      <div>
                        <h4 className="font-bold text-slate-900 text-sm group-hover:text-indigo-600 transition-colors">
                          Lex Fridman & Elon Musk: The AI Revolution
                        </h4>
                        <p className="text-xs text-slate-500">English • 2 Speakers • Shocking & Controversial</p>
                      </div>
                    </div>
                    <span className="px-3 py-1.5 rounded-xl bg-white border border-slate-200 text-indigo-600 text-xs font-bold shadow-sm">
                      Load Project
                    </span>
                  </div>

                  <div
                    onClick={() => onLoadDemo("demo_podcast_hindi_02")}
                    className="p-4 rounded-2xl bg-slate-50 hover:bg-amber-50/50 border border-slate-200 hover:border-amber-300 transition-all cursor-pointer flex items-center justify-between group shadow-sm"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-amber-100 border border-amber-200 flex items-center justify-center text-amber-700 font-black">
                        HI
                      </div>
                      <div>
                        <h4 className="font-bold text-slate-900 text-sm group-hover:text-amber-600 transition-colors">
                          Ranveer Allahbadia: Success Mindset (Hinglish)
                        </h4>
                        <p className="text-xs text-slate-500">Hindi / Hinglish • Motivation & Discipline</p>
                      </div>
                    </div>
                    <span className="px-3 py-1.5 rounded-xl bg-white border border-slate-200 text-amber-600 text-xs font-bold shadow-sm">
                      Load Project
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
