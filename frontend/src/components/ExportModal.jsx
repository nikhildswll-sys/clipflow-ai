import React, { useState } from "react";
import confetti from "canvas-confetti";
import {
  Download,
  FileVideo,
  FileText,
  Archive,
  CheckCircle,
  ExternalLink,
  Layers,
  Sparkles,
  X,
  Upload,
  Loader2,
  AlertCircle
} from "lucide-react";

export default function ExportModal({
  isOpen,
  onClose,
  project,
  clip,
  renderedUrl,
  downloadUrls = {},
  aspectRatio,
  resolution,
  captionStyle
}) {
  if (!isOpen) return null;

  const [privacyStatus, setPrivacyStatus] = useState("private");
  const [isUploading, setIsUploading] = useState(false);
  const [youtubeResult, setYoutubeResult] = useState(null);
  const [uploadError, setUploadError] = useState(null);

  const triggerConfetti = () => {
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 }
    });
  };

  React.useEffect(() => {
    if (isOpen) {
      triggerConfetti();
      setYoutubeResult(null);
      setUploadError(null);
    }
  }, [isOpen]);

  const videoDownloadUrl = downloadUrls.video || renderedUrl;

  const handleUploadYouTube = async () => {
    if (!project?.id || !clip?.id) {
      setUploadError("Missing project or clip information.");
      return;
    }
    setIsUploading(true);
    setUploadError(null);
    try {
      const res = await fetch("/api/youtube/upload", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_id: project.id,
          clip_id: clip.id,
          privacy_status: privacyStatus,
          title: clip?.packaging?.title,
          description: clip?.packaging?.description,
          tags: clip?.packaging?.tags
        })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to upload to YouTube");
      }
      setYoutubeResult(data);
      confetti({ particleCount: 100, spread: 80 });
    } catch (err) {
      setUploadError(err.message || "Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-lg bg-white border border-slate-200 rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh]">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4.5 border-b border-slate-100 bg-slate-50/70">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-2xl bg-emerald-50 text-emerald-600 border border-emerald-100">
              <CheckCircle className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Clip Render Ready</h2>
              <p className="text-xs text-slate-500">High-bitrate studio quality export</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-500 hover:text-slate-800 transition-all cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4 overflow-y-auto">
          {/* Rendered Video Preview Player */}
          {videoDownloadUrl && (
            <div className="relative rounded-2xl overflow-hidden bg-black shadow-lg border border-slate-200 max-h-[280px] flex items-center justify-center">
              <video
                controls
                autoPlay
                src={videoDownloadUrl}
                className="max-h-[280px] w-auto object-contain mx-auto"
                playsInline
              />
            </div>
          )}

          {/* Metadata pill */}
          <div className="flex items-center justify-between p-3.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs">
            <div className="flex items-center gap-2">
              <span className="font-bold text-indigo-600">{aspectRatio}</span>
              <span className="text-slate-400">•</span>
              <span className="font-bold text-slate-800 uppercase">{resolution}</span>
              <span className="text-slate-400">•</span>
              <span className="text-slate-600 capitalize font-medium">{captionStyle} Captions</span>
            </div>
            <span className="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-bold text-[10px]">
              CRF 18 LOSSLESS
            </span>
          </div>

          {/* Download Formats */}
          <div className="space-y-3">
            {/* Main Video MP4 */}
            <a
              href={videoDownloadUrl}
              download
              className="flex items-center justify-between p-4 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white shadow-md shadow-indigo-600/25 transition-all group cursor-pointer"
            >
              <div className="flex items-center gap-3">
                <FileVideo className="w-5 h-5 text-white" />
                <div>
                  <div className="font-bold text-sm">Download High-Res MP4 Video</div>
                  <div className="text-xs text-indigo-100">Burned animated captions + smart auto-framing</div>
                </div>
              </div>
              <Download className="w-5 h-5 group-hover:translate-y-0.5 transition-transform" />
            </a>

            {/* Separate Subtitle Files */}
            <div className="grid grid-cols-3 gap-2 pt-1">
              <a
                href={downloadUrls.srt}
                download
                className="flex items-center justify-center gap-1.5 p-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-xs font-semibold transition-all shadow-sm"
              >
                <FileText className="w-4 h-4 text-cyan-600" />
                <span>SRT Subtitles</span>
              </a>

              <a
                href={downloadUrls.vtt}
                download
                className="flex items-center justify-center gap-1.5 p-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-xs font-semibold transition-all shadow-sm"
              >
                <FileText className="w-4 h-4 text-indigo-600" />
                <span>VTT Captions</span>
              </a>

              <a
                href={downloadUrls.ass}
                download
                className="flex items-center justify-center gap-1.5 p-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-700 text-xs font-semibold transition-all shadow-sm"
              >
                <Sparkles className="w-4 h-4 text-amber-500" />
                <span>ASS Styled</span>
              </a>
            </div>

            {/* YouTube Shorts Auto-Uploader Card */}
            <div className="mt-4 p-4 rounded-2xl bg-gradient-to-br from-red-50 to-orange-50 border border-red-200 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 rounded-lg bg-red-600 text-white flex items-center justify-center font-black text-xs shadow-sm">
                    ▶
                  </div>
                  <div>
                    <h4 className="font-bold text-xs text-slate-900">Upload to YouTube Shorts</h4>
                    <p className="text-[10px] text-slate-500">Official YouTube Data API v3 integration</p>
                  </div>
                </div>

                {/* Privacy Status Dropdown */}
                <select
                  value={privacyStatus}
                  onChange={(e) => setPrivacyStatus(e.target.value)}
                  disabled={isUploading}
                  className="px-2.5 py-1 text-xs font-semibold bg-white border border-red-200 text-slate-700 rounded-lg shadow-sm focus:outline-none focus:ring-1 focus:ring-red-500"
                >
                  <option value="private">🔒 Private</option>
                  <option value="unlisted">🔗 Unlisted</option>
                  <option value="public">🌐 Public</option>
                </select>
              </div>

              {/* Upload Button */}
              {!youtubeResult ? (
                <button
                  onClick={handleUploadYouTube}
                  disabled={isUploading}
                  className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white font-bold text-xs shadow-md shadow-red-600/25 transition-all cursor-pointer"
                >
                  {isUploading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Authenticating & Uploading to YouTube...</span>
                    </>
                  ) : (
                    <>
                      <Upload className="w-4 h-4" />
                      <span>1-Click Upload Short ({privacyStatus.toUpperCase()})</span>
                    </>
                  )}
                </button>
              ) : (
                <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-emerald-600" />
                    <div>
                      <div className="text-xs font-bold text-emerald-900">Uploaded Successfully!</div>
                      <div className="text-[10px] text-emerald-700">Video ID: {youtubeResult.video_id}</div>
                    </div>
                  </div>
                  <a
                    href={youtubeResult.video_url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-1 px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold shadow-sm transition-all"
                  >
                    <span>Watch Short</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              )}

              {/* Error Message */}
              {uploadError && (
                <div className="p-2.5 bg-red-100/80 border border-red-200 rounded-xl flex items-start gap-2 text-xs text-red-800">
                  <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
                  <div>{uploadError}</div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end px-6 py-4 border-t border-slate-100 bg-slate-50/70">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold text-xs transition-all cursor-pointer"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
