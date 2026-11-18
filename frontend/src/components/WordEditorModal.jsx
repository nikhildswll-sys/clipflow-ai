import React, { useState, useEffect } from "react";
import {
  X,
  Check,
  Sparkles,
  Edit3,
  Wand2,
  Languages,
  RotateCcw,
  Save
} from "lucide-react";

export default function WordEditorModal({
  isOpen,
  onClose,
  clip,
  onSaveWords
}) {
  if (!isOpen || !clip) return null;

  const [words, setWords] = useState([]);

  useEffect(() => {
    if (clip?.words) {
      setWords(clip.words.map(w => ({ ...w })));
    }
  }, [clip?.id, isOpen]);

  const handleWordChange = (idx, newText) => {
    setWords(prev => {
      const updated = [...prev];
      updated[idx] = { ...updated[idx], word: newText };
      return updated;
    });
  };

  const autoFixSlang = () => {
    const corrections = {
      "plwn": "Pehlwan",
      "plwno": "Pehlwano",
      "bdmi": "Badmashi",
      "bdmasi": "Badmashi",
      "bdmashi": "Badmashi",
      "rod": "Rude",
      "rood": "Rude",
      "rud": "Rude",
      "atitud": "Attitude",
      "atitood": "Attitude",
      "doremona": "Doraemon",
      "doramon": "Doraemon",
      "nobitaa": "Nobita",
      "indya": "India",
      "gunda": "Gunda",
      "gundagardi": "Gundagardi",
      "kalesh": "Kalesh",
      "lafda": "Lafda",
      "bawa": "Bawa"
    };

    setWords(prev =>
      prev.map(w => {
        const lower = w.word.toLowerCase().replace(/[^\w]/g, "");
        if (corrections[lower]) {
          return { ...w, word: corrections[lower] };
        }
        return w;
      })
    );
  };

  const handleSave = () => {
    onSaveWords(clip.id, words);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-3xl bg-[#121422] border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-[#16192B]">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-purple-600/20 text-purple-400 border border-purple-500/30">
              <Edit3 className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Edit Subtitle Words & Spellings</h2>
              <p className="text-xs text-slate-400">Click any word to fix typos or adjust Hinglish spellings</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 text-slate-400 hover:text-white transition-all cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Toolbar */}
        <div className="flex items-center justify-between px-6 py-3 bg-[#0A0B13] border-b border-slate-800 text-xs">
          <div className="flex items-center gap-2 text-slate-400">
            <span>Total Words: <strong className="text-white font-mono">{words.length}</strong></span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={autoFixSlang}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-purple-600/30 hover:bg-purple-600/50 text-purple-300 border border-purple-500/40 text-xs font-semibold transition-all cursor-pointer"
            >
              <Wand2 className="w-3.5 h-3.5 text-amber-300" />
              <span>Auto-Fix Slang & Typos</span>
            </button>
          </div>
        </div>

        {/* Word Grid / Pills */}
        <div className="p-6 overflow-y-auto space-y-4 max-h-[60vh]">
          <p className="text-xs text-slate-400">
            Har word ke timebox par click karke direct edit karein. Video aur subtitles turant update ho jayenge:
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5">
            {words.map((w, idx) => (
              <div
                key={idx}
                className="flex flex-col p-2 rounded-xl bg-[#0F111D] border border-slate-800 hover:border-purple-500/60 focus-within:border-purple-500 transition-all"
              >
                <div className="flex justify-between items-center text-[10px] text-slate-500 font-mono mb-1">
                  <span>#{idx + 1}</span>
                  <span>{w.start.toFixed(1)}s - {w.end.toFixed(1)}s</span>
                </div>
                <input
                  type="text"
                  value={w.word}
                  onChange={(e) => handleWordChange(idx, e.target.value)}
                  className="w-full bg-slate-900 px-2 py-1 rounded-lg text-white font-bold text-sm focus:outline-none focus:ring-1 focus:ring-purple-400"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-6 py-3.5 border-t border-slate-800 bg-[#16192B]">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium text-xs transition-all cursor-pointer"
          >
            Cancel
          </button>

          <button
            onClick={handleSave}
            className="flex items-center gap-2 px-5 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-purple-600/30 transition-all cursor-pointer"
          >
            <Save className="w-4 h-4" />
            <span>Save & Apply Words</span>
          </button>
        </div>
      </div>
    </div>
  );
}
