import React from "react";
import {
  Sparkles,
  Type,
  Palette,
  AlignVerticalJustifyCenter,
  Smile,
  Flame,
  Check,
  Sliders,
  Languages,
  Square,
  Box
} from "lucide-react";

export default function CaptionEditor({
  captionStyle,
  onSelectStyle,
  customCaptions,
  onUpdateCustom,
  onTranslateEnglish,
  onConvertToHinglish,
  isTranslating = false,
  isHinglish = false,
  isConvertingHinglish = false
}) {
  const stylesList = [
    {
      id: "hormozi",
      name: "Hormozi Clean",
      desc: "Anton font with clean yellow keyword punch & heavy black outline",
      previewText: "THE 1 SECRET",
      previewColor: "#FFDE00",
      font: "Anton",
      tag: "🔥 VIRAL #1"
    },
    {
      id: "mrbeast",
      name: "MrBeast Punch",
      desc: "Bouncy vibrant scale pop with neon green/yellow accents",
      previewText: "CRAZIEST MOMENT!",
      previewColor: "#00FF66",
      font: "Anton",
      tag: "⚡ RETENTION"
    },
    {
      id: "minimal",
      name: "Minimalist Pill",
      desc: "Clean, elegant Poppins font with sleek black backdrop pill",
      previewText: "Clean & Aesthetic.",
      previewColor: "#FFFFFF",
      font: "Poppins",
      tag: "✨ AESTHETIC"
    },
    {
      id: "podcast",
      name: "Podcast Karaoke",
      desc: "Montserrat typography with word-by-word active cyan highlight",
      previewText: "Active karaoke flow",
      previewColor: "#06B6D4",
      font: "Montserrat",
      tag: "🎙️ INTERVIEWS"
    },
    {
      id: "cinematic",
      name: "Cinematic Classic",
      desc: "Cinzel luxury serif with golden amber highlights",
      previewText: "Timeless Story.",
      previewColor: "#FBBF24",
      font: "Cinzel",
      tag: "🎬 CINEMATIC"
    },
    {
      id: "gaming",
      name: "Gaming Punch",
      desc: "Cyber Rubik black with electric magenta/yellow pop",
      previewText: "INSANE CLUTCH 💀",
      previewColor: "#FF007A",
      font: "Rubik",
      tag: "🎮 GAMING"
    },
    {
      id: "neon",
      name: "Neon Light Rays",
      desc: "Bebas Neue with luminous glowing emerald light blur aura",
      previewText: "GLOWING VIBES",
      previewColor: "#00FF88",
      font: "Bebas Neue",
      tag: "🌟 NEON TUBE"
    }
  ];

  const fontOptions = [
    { id: "Anton", name: "Anton (Hormozi / MrBeast)" },
    { id: "Montserrat", name: "Montserrat 900 (Black)" },
    { id: "Bebas Neue", name: "Bebas Neue (Punchy Caps)" },
    { id: "Poppins", name: "Poppins 900 (Clean Rounded)" },
    { id: "Outfit", name: "Outfit Heavy (Modern Tech)" },
    { id: "Rubik", name: "Rubik Black (Gaming)" },
    { id: "Permanent Marker", name: "Permanent Marker (Edgy)" }
  ];

  const currentFont = customCaptions.fontname || (captionStyle === "podcast" ? "Montserrat" : captionStyle === "minimal" ? "Poppins" : "Anton");

  return (
    <div className="flex flex-col gap-5 p-5 bg-white border border-slate-200 rounded-2xl shadow-sm">
      {/* Header with Language Translation Switcher */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-200">
        <div className="flex items-center gap-2">
          <Type className="w-5 h-5 text-indigo-600" />
          <h3 className="font-bold text-slate-900 text-base">Animated Caption Engine</h3>
        </div>

        {/* 1-Click Language Convert Action Buttons */}
        <div className="flex items-center gap-2">
          {/* Translate to English Button */}
          <button
            onClick={onTranslateEnglish}
            disabled={isTranslating}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 text-indigo-700 text-xs font-bold transition-all cursor-pointer shadow-sm disabled:opacity-50"
            title="Translate dialogue to clean, fluent English using Whisper AI"
          >
            <Languages className="w-3.5 h-3.5" />
            <span>{isTranslating ? "Translating..." : "🇬🇧 Translate to English"}</span>
          </button>

          {/* Convert to Hinglish Button */}
          <button
            onClick={onConvertToHinglish}
            disabled={isConvertingHinglish}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer shadow-sm ${
              isHinglish
                ? "bg-emerald-600 text-white"
                : "bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-800"
            }`}
            title="Convert Hindi/Urdu to Roman Hinglish script"
          >
            <span>{isConvertingHinglish ? "Converting..." : isHinglish ? "🇮🇳 Hinglish Active" : "🇮🇳 Hinglish"}</span>
          </button>
        </div>
      </div>

      {/* Preset Cards Carousel / Grid */}
      <div>
        <label className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2.5 block">
          Preset Styles
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2.5">
          {stylesList.map((st) => {
            const isSelected = captionStyle === st.id;
            return (
              <button
                key={st.id}
                onClick={() => onSelectStyle(st.id)}
                className={`relative flex flex-col p-3 rounded-xl border text-left transition-all cursor-pointer ${
                  isSelected
                    ? "bg-indigo-50/70 border-indigo-500 shadow-sm ring-1 ring-indigo-500/30"
                    : "bg-slate-50 border-slate-200 hover:border-slate-300 hover:bg-slate-100/60"
                }`}
              >
                {isSelected && (
                  <div className="absolute top-2.5 right-2.5 w-4 h-4 rounded-full bg-indigo-600 flex items-center justify-center">
                    <Check className="w-3 h-3 text-white" />
                  </div>
                )}

                <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-wider mb-1">
                  {st.tag}
                </span>

                <span className="font-bold text-slate-900 text-sm mb-1">{st.name}</span>

                {/* Typography preview */}
                <div className="mt-2 py-2 px-2 bg-slate-900 rounded-lg text-center overflow-hidden">
                  <span
                    className="font-black text-sm tracking-wide"
                    style={{
                      color: st.previewColor,
                      fontFamily: st.font,
                      textShadow: isSelected ? "0 0 10px currentColor" : "0 2px 4px rgba(0,0,0,0.8)"
                    }}
                  >
                    {st.previewText}
                  </span>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Font Family & Background Style */}
      <div className="pt-2 border-t border-slate-200 flex flex-col gap-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Font Family Selector */}
          <div>
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5 block">
              Creator Font Family
            </label>
            <div className="grid grid-cols-2 gap-1.5">
              {fontOptions.map((f) => (
                <button
                  key={f.id}
                  onClick={() => onUpdateCustom("fontname", f.id)}
                  className={`p-2 rounded-xl border text-left text-xs transition-all cursor-pointer truncate ${
                    currentFont === f.id
                      ? "bg-indigo-600 text-white font-bold border-indigo-600 shadow-sm"
                      : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100"
                  }`}
                  style={{ fontFamily: f.id }}
                >
                  {f.name}
                </button>
              ))}
            </div>
          </div>

          {/* Background Box & Highlights */}
          <div>
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5 block">
              Caption Box Styling
            </label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { id: "none", label: "Outline Only", desc: "No box background" },
                { id: "pill", label: "Dark Pill", desc: "Aesthetic backdrop" },
                { id: "highlight", label: "Active Box", desc: "Colored word box" }
              ].map((box) => (
                <button
                  key={box.id}
                  onClick={() => onUpdateCustom("box_style", box.id)}
                  className={`p-2.5 rounded-xl border text-center transition-all cursor-pointer ${
                    (customCaptions.box_style || "none") === box.id
                      ? "bg-indigo-600 text-white font-bold border-indigo-600 shadow-sm"
                      : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  <div className="text-xs font-bold mb-0.5">{box.label}</div>
                  <div className="text-[10px] opacity-75">{box.desc}</div>
                </button>
              ))}
            </div>

            {/* Highlight Color Palette */}
            <div className="mt-3">
              <label className="text-xs text-slate-500 mb-1.5 block font-medium">Highlight Keyword Color</label>
              <div className="flex items-center gap-2 bg-slate-50 p-2 rounded-xl border border-slate-200">
                {["#FFDE00", "#00FF66", "#06B6D4", "#FF007A", "#FF6B00", "#FFFFFF", "#9D00FF"].map((col) => (
                  <button
                    key={col}
                    onClick={() => onUpdateCustom("highlight_color", col)}
                    className={`flex-1 h-7 rounded-lg border-2 transition-transform cursor-pointer ${
                      customCaptions.highlight_color === col ? "scale-115 border-slate-900 shadow-sm" : "border-transparent"
                    }`}
                    style={{ backgroundColor: col }}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Position, Font Size, Words Per Group & Toggles */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-1">
          {/* Subtitle Font Size */}
          <div>
            <label className="text-xs text-slate-500 mb-1.5 block font-medium">Subtitle Font Size</label>
            <div className="flex bg-slate-100 p-1 rounded-xl border border-slate-200">
              {[
                { id: "small", label: "Small" },
                { id: "medium", label: "Medium" },
                { id: "large", label: "Large" }
              ].map((s) => (
                <button
                  key={s.id}
                  onClick={() => onUpdateCustom("font_size", s.id)}
                  className={`flex-1 py-1.5 rounded-lg text-xs font-medium capitalize transition-all cursor-pointer ${
                    (customCaptions.font_size || "medium") === s.id
                      ? "bg-indigo-600 text-white font-bold shadow-sm"
                      : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  {s.label}
                </button>
              ))}
            </div>
          </div>

          {/* Screen Position */}
          <div>
            <label className="text-xs text-slate-500 mb-1.5 block font-medium">Vertical Position</label>
            <div className="flex bg-slate-100 p-1 rounded-xl border border-slate-200">
              {["top", "center", "bottom"].map((pos) => (
                <button
                  key={pos}
                  onClick={() => onUpdateCustom("position", pos)}
                  className={`flex-1 py-1.5 rounded-lg text-xs font-medium capitalize transition-all cursor-pointer ${
                    (customCaptions.position || "bottom") === pos
                      ? "bg-white text-indigo-700 font-bold shadow-sm"
                      : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  {pos}
                </button>
              ))}
            </div>
          </div>

          {/* Words Per Line */}
          <div>
            <label className="text-xs text-slate-500 mb-1.5 block font-medium">
              Words Per Line: <span className="text-indigo-600 font-bold">{customCaptions.words_per_group || 3}</span>
            </label>
            <div className="flex items-center gap-2">
              {[2, 3, 4, 5].map((cnt) => (
                <button
                  key={cnt}
                  onClick={() => onUpdateCustom("words_per_group", cnt)}
                  className={`flex-1 py-1.5 rounded-lg text-xs font-bold border transition-all cursor-pointer ${
                    (customCaptions.words_per_group || 3) === cnt
                      ? "bg-indigo-600 text-white border-indigo-600 shadow-sm"
                      : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  {cnt} {cnt === 2 ? "⚡" : ""}
                </button>
              ))}
            </div>
          </div>

          {/* Emojis & All Caps */}
          <div className="flex items-end gap-2">
            <button
              onClick={() => onUpdateCustom("has_emojis", !(customCaptions.has_emojis ?? true))}
              className={`flex-1 py-2 px-3 rounded-xl border text-xs font-bold flex items-center justify-center gap-1.5 transition-all cursor-pointer ${
                (customCaptions.has_emojis ?? true)
                  ? "bg-indigo-50 border-indigo-200 text-indigo-700 shadow-sm"
                  : "bg-slate-50 border-slate-200 text-slate-500"
              }`}
            >
              <Smile className="w-3.5 h-3.5" />
              <span>Emojis {(customCaptions.has_emojis ?? true) ? "ON" : "OFF"}</span>
            </button>

            <button
              onClick={() => onUpdateCustom("uppercase", !(customCaptions.uppercase ?? true))}
              className={`flex-1 py-2 px-3 rounded-xl border text-xs font-bold flex items-center justify-center gap-1.5 transition-all cursor-pointer ${
                (customCaptions.uppercase ?? true)
                  ? "bg-indigo-50 border-indigo-200 text-indigo-700 shadow-sm"
                  : "bg-slate-50 border-slate-200 text-slate-500"
              }`}
            >
              <Type className="w-3.5 h-3.5" />
              <span>{(customCaptions.uppercase ?? true) ? "ALL CAPS" : "Normal"}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
