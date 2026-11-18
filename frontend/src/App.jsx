import React, { useState, useEffect } from "react";
import confetti from "canvas-confetti";
import {
  fetchProjects,
  fetchProject,
  fetchPresets,
  uploadVideoFile,
  importYouTube,
  importLiveStream,
  renderClip,
  batchRender
} from "./api";

import Navbar from "./components/Navbar";
import StudioPlayer from "./components/StudioPlayer";
import ClipsList from "./components/ClipsList";
import CaptionEditor from "./components/CaptionEditor";
import PackagingModal from "./components/PackagingModal";
import ExportModal from "./components/ExportModal";
import IngestModal from "./components/IngestModal";
import WordEditorModal from "./components/WordEditorModal";

import {
  Sparkles,
  Layers,
  Scissors,
  Download,
  AlertCircle,
  FileVideo,
  Radio,
  Tv,
  CheckCircle2,
  TrendingUp,
  Cpu
} from "lucide-react";

export default function App() {
  const [projects, setProjects] = useState([]);
  const [currentProject, setCurrentProject] = useState(null);
  const [activeClipId, setActiveClipId] = useState(null);

  // Settings
  const [aspectRatio, setAspectRatio] = useState("19:6"); // Default 19:6 as requested
  const [resolution, setResolution] = useState("1080p");
  const [captionStyle, setCaptionStyle] = useState("hormozi");
  const [customCaptions, setCustomCaptions] = useState({
    position: "bottom",
    font_size: "medium",
    words_per_group: 3,
    highlight_color: "#FFDE00",
    has_emojis: true,
    uppercase: true
  });

  // Modals & Drawers
  const [isIngestOpen, setIsIngestOpen] = useState(false);
  const [isPackagingOpen, setIsPackagingOpen] = useState(false);
  const [isExportOpen, setIsExportOpen] = useState(false);
  const [isWordEditorOpen, setIsWordEditorOpen] = useState(false);
  const [selectedPackagingClip, setSelectedPackagingClip] = useState(null);

  const handleSaveWords = async (clipId, newWords) => {
    if (!currentProject) return;
    try {
      const updatedClips = currentProject.clips.map(c => {
        if (c.id === clipId) {
          return {
            ...c,
            words: newWords,
            text: newWords.map(w => w.word).join(" ")
          };
        }
        return c;
      });
      setCurrentProject({ ...currentProject, clips: updatedClips });

      await fetch("/api/update-clip-words", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_id: currentProject.id,
          clip_id: clipId,
          words: newWords
        })
      });
      confetti({ particleCount: 30, spread: 50 });
    } catch (e) {
      console.error("Save words error", e);
    }
  };

  // Loading States
  const [isProcessing, setIsProcessing] = useState(false);
  const [jobProgress, setJobProgress] = useState(null);
  const [isRendering, setIsRendering] = useState(false);
  const [isBatchRendering, setIsBatchRendering] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [isConvertingHinglish, setIsConvertingHinglish] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  const handleTranslateEnglish = async () => {
    if (!currentProject) return;
    setIsTranslating(true);
    setErrorMessage(null);
    try {
      const res = await fetch(`/api/translate-english/${currentProject.id}`, { method: "POST" });
      if (!res.ok) throw new Error("Failed to translate to English");
      const data = await res.json();
      setCurrentProject(data.project);
      if (data.project.clips && data.project.clips.length > 0) {
        setActiveClipId(data.project.clips[0].id);
      }
      confetti({ particleCount: 60, spread: 70 });
    } catch (err) {
      setErrorMessage(err.message || "English translation failed");
    } finally {
      setIsTranslating(false);
    }
  };

  const handleConvertToHinglish = async () => {
    if (!currentProject) return;
    setIsConvertingHinglish(true);
    setErrorMessage(null);
    try {
      const res = await fetch(`/api/convert-hinglish/${currentProject.id}`, { method: "POST" });
      if (!res.ok) throw new Error("Failed to convert project to Hinglish");
      const data = await res.json();
      setCurrentProject(data.project);
      confetti({ particleCount: 60, spread: 70 });
    } catch (err) {
      setErrorMessage(err.message || "Hinglish conversion failed");
    } finally {
      setIsConvertingHinglish(false);
    }
  };

  // Polling real-time engine progress during processing
  useEffect(() => {
    let interval = null;
    if (isProcessing) {
      interval = setInterval(async () => {
        try {
          const res = await fetch("/api/progress");
          if (res.ok) {
            const data = await res.json();
            setJobProgress(data);
          }
        } catch (e) {
          // Ignore transient poll error
        }
      }, 600);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isProcessing]);

  // Last rendered data
  const [lastRendered, setLastRendered] = useState(null);

  // Load projects on start
  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await fetchProjects();
      setProjects(data);
      if (data && data.length > 0) {
        const active = data[0];
        setCurrentProject(active);
        if (active.clips && active.clips.length > 0) {
          setActiveClipId(active.clips[0].id);
        }
      }
    } catch (err) {
      console.error("Failed to load projects", err);
    }
  };

  const handleSelectClip = (id) => {
    setActiveClipId(id);
  };

  const handleUpdateCustomCaptions = (key, val) => {
    setCustomCaptions(prev => ({ ...prev, [key]: val }));
  };

  const handleUpdateClipBounds = (clipId, newStart, newEnd) => {
    if (!currentProject) return;
    const updatedClips = currentProject.clips.map(c => {
      if (c.id === clipId) {
        return {
          ...c,
          start: newStart,
          end: newEnd,
          duration: Math.max(1, newEnd - newStart)
        };
      }
      return c;
    });
    setCurrentProject({ ...currentProject, clips: updatedClips });
  };

  const handleOpenPackaging = (clip) => {
    const targetClip = clip || currentProject?.clips?.find(c => c.id === activeClipId);
    if (targetClip) {
      setSelectedPackagingClip(targetClip);
      setIsPackagingOpen(true);
    }
  };

  // Render & Export Single Clip
  const handleExportCurrent = async (clipToExport) => {
    const targetClip = clipToExport || currentProject?.clips?.find(c => c.id === activeClipId);
    if (!targetClip || !currentProject) return;

    setIsRendering(true);
    setErrorMessage(null);
    try {
      const payload = {
        project_id: currentProject.id,
        clip_id: targetClip.id,
        start_time: targetClip.start,
        end_time: targetClip.end,
        aspect_ratio: aspectRatio,
        resolution: resolution,
        caption_style: captionStyle,
        custom_captions: customCaptions,
        remove_silence: false,
        quality_crf: 18
      };
      const res = await renderClip(payload);
      setLastRendered({
        clip: targetClip,
        video_url: res.video_url,
        download_urls: res.download_urls
      });
      setIsExportOpen(true);

      // Update clip in local project state
      const updatedClips = currentProject.clips.map(c => {
        if (c.id === targetClip.id) {
          return {
            ...c,
            rendered_video: res.video_url,
            download_urls: res.download_urls
          };
        }
        return c;
      });
      setCurrentProject({ ...currentProject, clips: updatedClips });
    } catch (err) {
      setErrorMessage(err.message || "Rendering failed");
    } finally {
      setIsRendering(false);
    }
  };

  // Batch Export All Clips in ZIP
  const handleBatchDownload = async () => {
    if (!currentProject || !currentProject.clips?.length) return;
    setIsBatchRendering(true);
    try {
      const payload = {
        project_id: currentProject.id,
        aspect_ratio: aspectRatio,
        resolution: resolution,
        caption_style: captionStyle,
        remove_silence: false
      };
      const res = await batchRender(payload);
      if (res.zip_url) {
        confetti({
          particleCount: 100,
          spread: 80,
          origin: { y: 0.5 }
        });
        window.open(res.zip_url, "_blank");
      }
    } catch (err) {
      setErrorMessage("Batch packaging failed");
    } finally {
      setIsBatchRendering(false);
    }
  };

  // Ingest Handlers
  const handleUploadFile = async (file) => {
    setIsProcessing(true);
    setErrorMessage(null);
    try {
      const res = await uploadVideoFile(file);
      setProjects(prev => [res, ...prev]);
      setCurrentProject(res);
      if (res.clips && res.clips.length > 0) {
        setActiveClipId(res.clips[0].id);
      }
      setIsIngestOpen(false);
      confetti({ particleCount: 70, spread: 70 });
    } catch (err) {
      setErrorMessage(err.message || "Upload and analysis failed");
      setIsIngestOpen(false);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleImportYouTube = async (url) => {
    setIsProcessing(true);
    setErrorMessage(null);
    try {
      const res = await importYouTube(url);
      setProjects(prev => [res, ...prev]);
      setCurrentProject(res);
      if (res.clips && res.clips.length > 0) {
        setActiveClipId(res.clips[0].id);
      }
      setIsIngestOpen(false);
      confetti({ particleCount: 70, spread: 70 });
    } catch (err) {
      setErrorMessage(err.message || "YouTube import failed");
      setIsIngestOpen(false);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleImportStream = async (streamUrl, duration) => {
    setIsProcessing(true);
    setErrorMessage(null);
    try {
      const res = await importLiveStream(streamUrl, duration);
      setProjects(prev => [res, ...prev]);
      setCurrentProject(res);
      if (res.clips && res.clips.length > 0) {
        setActiveClipId(res.clips[0].id);
      }
      setIsIngestOpen(false);
      confetti({ particleCount: 70, spread: 70 });
    } catch (err) {
      setErrorMessage(err.message || "Live stream capture failed");
      setIsIngestOpen(false);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleLoadDemo = async (demoId) => {
    setIsIngestOpen(false);
    try {
      const p = await fetchProject(demoId);
      setCurrentProject(p);
      if (p.clips && p.clips.length > 0) {
        setActiveClipId(p.clips[0].id);
      }
    } catch (err) {
      setErrorMessage("Demo load failed");
    }
  };

  const activeClip = currentProject?.clips?.find(c => c.id === activeClipId) || currentProject?.clips?.[0];

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900 flex flex-col font-sans">
      {/* Top Navbar */}
      <Navbar
        aspectRatio={aspectRatio}
        onSelectAspectRatio={setAspectRatio}
        resolution={resolution}
        onSelectResolution={setResolution}
        onOpenIngest={() => setIsIngestOpen(true)}
        onBatchDownload={handleBatchDownload}
        isBatchRendering={isBatchRendering}
        totalClipsCount={currentProject?.clips?.length || 0}
      />

      {/* Global Status Banner if processing */}
      {isProcessing && (
        <div className="w-full bg-indigo-600 px-5 py-3 text-white text-center flex items-center justify-between gap-4 text-xs font-semibold shadow-md">
          <div className="flex items-center gap-3">
            <Cpu className="w-4 h-4 text-amber-300 animate-spin" />
            <span className="font-bold">{jobProgress?.step_title || "AI Clipping Engine Active..."}</span>
          </div>

          <div className="flex items-center gap-3">
            <div className="w-32 h-2 bg-indigo-900/40 rounded-full overflow-hidden">
              <div
                className="h-full bg-white rounded-full transition-all duration-300"
                style={{ width: `${jobProgress?.progress || 15}%` }}
              />
            </div>
            <span className="font-mono text-white font-bold">{jobProgress?.progress || 15}%</span>
            <button
              onClick={() => setIsIngestOpen(true)}
              className="px-2.5 py-1 rounded-md bg-white/20 hover:bg-white/30 text-white text-[11px] font-bold cursor-pointer"
            >
              Open Console
            </button>
          </div>
        </div>
      )}

      {/* Error alert toast */}
      {errorMessage && (
        <div className="w-full bg-rose-50 border-b border-rose-200 px-4 py-2 text-center flex items-center justify-center gap-2 text-xs font-semibold text-rose-700">
          <AlertCircle className="w-4 h-4 text-rose-500" />
          <span>{errorMessage}</span>
          <button onClick={() => setErrorMessage(null)} className="ml-2 underline cursor-pointer">
            Dismiss
          </button>
        </div>
      )}

      {/* Main Workspace Layout */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Viral Clips Library & Ranking (5 Cols) */}
        <div className="lg:col-span-5 flex flex-col gap-4">
          {/* Active Video Overview Card */}
          {currentProject && (
            <div className="p-4 rounded-2xl bg-white border border-slate-200 flex items-center justify-between gap-3 shadow-sm">
              <div className="flex items-center gap-3 overflow-hidden">
                <div className="w-12 h-12 rounded-xl overflow-hidden bg-slate-100 flex-shrink-0 border border-slate-200">
                  <img
                    src={currentProject.thumbnail}
                    alt="Thumbnail"
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="overflow-hidden">
                  <h3 className="font-bold text-slate-900 text-sm truncate">
                    {currentProject.title}
                  </h3>
                  <div className="flex items-center gap-2 text-xs text-slate-500 mt-0.5">
                    <span className="capitalize">{currentProject.source_type}</span>
                    <span>•</span>
                    <span className="uppercase font-mono font-bold text-indigo-600">{currentProject.language_mode === "english" ? "ENGLISH" : currentProject.language}</span>
                    <span>•</span>
                    <span>{currentProject.speaker_count} Speaker(s)</span>
                  </div>
                </div>
              </div>

              <button
                onClick={() => setIsIngestOpen(true)}
                className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-700 text-xs font-bold whitespace-nowrap cursor-pointer transition-colors shadow-sm"
              >
                Change
              </button>
            </div>
          )}

          {/* Clips List */}
          <ClipsList
            clips={currentProject?.clips || []}
            activeClipId={activeClipId}
            onSelectClip={handleSelectClip}
            onOpenPackaging={handleOpenPackaging}
            onExportClip={handleExportCurrent}
            isRendering={isRendering}
          />
        </div>

        {/* Right Column: Studio Video Preview, Timeline & Caption Engine (7 Cols) */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          {/* Studio Video Player Frame */}
          <StudioPlayer
            project={currentProject}
            clip={activeClip}
            aspectRatio={aspectRatio}
            resolution={resolution}
            captionStyle={captionStyle}
            customCaptions={customCaptions}
            onUpdateClipBounds={handleUpdateClipBounds}
            onOpenPackaging={() => handleOpenPackaging(activeClip)}
            onOpenWordEditor={() => setIsWordEditorOpen(true)}
            onTranslateEnglish={handleTranslateEnglish}
            onConvertToHinglish={handleConvertToHinglish}
            isTranslating={isTranslating}
            isConvertingHinglish={isConvertingHinglish}
            onExportCurrent={() => handleExportCurrent(activeClip)}
            isRendering={isRendering}
          />

          {/* AI Animated Caption Style Customizer */}
          <CaptionEditor
            captionStyle={captionStyle}
            onSelectStyle={setCaptionStyle}
            customCaptions={customCaptions}
            onUpdateCustom={handleUpdateCustomCaptions}
            onTranslateEnglish={handleTranslateEnglish}
            onConvertToHinglish={handleConvertToHinglish}
            isTranslating={isTranslating}
            isHinglish={Boolean(currentProject?.is_hinglish || currentProject?.language_mode === "hinglish")}
            isConvertingHinglish={isConvertingHinglish}
          />
        </div>
      </main>

      {/* Modals */}
      <IngestModal
        isOpen={isIngestOpen}
        onClose={() => setIsIngestOpen(false)}
        onUploadFile={handleUploadFile}
        onImportYouTube={handleImportYouTube}
        onImportStream={handleImportStream}
        onLoadDemo={handleLoadDemo}
        isProcessing={isProcessing}
        jobProgress={jobProgress}
      />

      <PackagingModal
        isOpen={isPackagingOpen}
        onClose={() => setIsPackagingOpen(false)}
        clip={selectedPackagingClip}
      />

      <ExportModal
        isOpen={isExportOpen}
        onClose={() => setIsExportOpen(false)}
        clip={lastRendered?.clip}
        renderedUrl={lastRendered?.video_url}
        downloadUrls={lastRendered?.download_urls}
        aspectRatio={aspectRatio}
        resolution={resolution}
        captionStyle={captionStyle}
      />

      <WordEditorModal
        isOpen={isWordEditorOpen}
        onClose={() => setIsWordEditorOpen(false)}
        clip={activeClip}
        onSaveWords={handleSaveWords}
      />
    </div>
  );
}
