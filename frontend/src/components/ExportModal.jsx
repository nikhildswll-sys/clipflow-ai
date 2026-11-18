import React from "react";
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
  X
} from "lucide-react";

export default function ExportModal({
  isOpen,
  onClose,
  clip,
  renderedUrl,
  downloadUrls = {},
  aspectRatio,
  resolution,
  captionStyle
}) {
  if (!isOpen) return null;

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
    }
  }, [isOpen]);

  const videoDownloadUrl = downloadUrls.video || renderedUrl;

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
