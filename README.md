# ClipFlow AI — AI Podcast & Live Stream Clipper 🚀

**ClipFlow AI** is a professional, studio-grade AI video clipping platform designed to transform long-form podcasts, creator interviews, gaming streams, and live broadcasts into viral, high-retention short clips for TikTok, YouTube Shorts, and Instagram Reels.

---

## 🌟 Key Capabilities

### 1. 🤖 AI Automatic Viral Moment Detection
- **Full Video & Audio Analysis**: Analyzes speech transcripts, audio energy, lexical hooks, and emotional inflections.
- **7 Engagement Categories**:
  - 🔥 **Shocking Reveal**: High curiosity secrets, exposed truths, and mind-blowing disclosures.
  - ⚡ **Controversial Debate**: Polarizing opinions, hot debates, and contrarian perspectives.
  - 😂 **Humor & Funny Moments**: Laughter peaks, comedic punchlines, and hilarious reactions.
  - 👑 **Powerful Speech / Motivation**: Discipline, greatness, success mindset, and emotional pep talks.
  - 💡 **Mind-Blowing Facts**: Statistically shocking insights, psychological phenomenons, and science.
  - 🥊 **Heated Argument**: Tension peaks, debates, and clash moments.
  - ❤️ **Emotional Vulnerability**: Deep empathy, heart-to-heart confessions, and raw life lessons.
- **Virality Potential Score (0–100)**: Evaluates Hook Strength, Emotional Intensity, Retention & Pacing, Punchline Delivery, and Shareability.
- **Smart Sentence Boundary Snapping**: Never cuts words, sentences, or reactions mid-thought.

### 2. 🎬 Intelligent Auto-Framing & Video Editing
- **Default Aspect Ratio**: **19:6** (Ultrawide Cinematic Vertical Banner) as requested.
- **Customizable Aspect Ratios**:
  - `19:6` Ultrawide Vertical (Cinematic Banner) — *Default*
  - `9:16` Vertical (TikTok, Shorts, Reels)
  - `16:9` Landscape (Full YouTube, TV, Desktop)
  - `1:1` Square (Instagram Feed, X/Twitter, LinkedIn)
  - `4:5` Portrait (Instagram Portrait Feed)
- **Smart Speaker Tracking**: OpenCV face detection with Exponential Moving Average (EMA) smoothing for cinematic, natural camera pan without jerky motion.
- **Multi-Speaker Diarization**: Detects host vs. guest positioning and frames them appropriately.
- **Studio Quality Export**: Visually lossless encoding (CRF 18) with support for **1080p Full HD**, **2K Quad HD**, **4K Ultra HD**, or **Source** resolution.
- **Smart Silence Removal**: Option to trim awkward silence pauses for hyper-retention pacing.

### 3. ✨ AI Animated Captions Engine
Accurately synchronized word-by-word subtitles with word-level timestamps:
- **Hormozi Style**: Bold Impact uppercase font, crisp white letters with heavy stroke, and electric yellow active keyword pop.
- **MrBeast Style**: Large bouncy vibrant captions, neon green/yellow accents, drop shadows, and animated pops.
- **Minimal Style**: Elegant translucent frosted glass subtitles for aesthetic storytelling.
- **Podcast Style**: Modern bold sans-serif with active cyan karaoke tracking.
- **Cinematic Style**: Classic serif typography with subtle golden amber highlights.
- **Gaming Style**: Electric cyber neon magenta and yellow borders for high-energy streams.
- **Neon Style**: Glowing luminous emerald and cyan light rays.
- **Customization Controls**:
  - Font family and size
  - Highlight and primary text colors
  - Vertical screen position (Top, Center, Bottom)
  - Words per line (2, 3, 4, 5 words)
  - Dynamic contextual emoji integration (🔥, 💀, 🤯, 💰, 🏆, etc.)
  - Uppercase and bold toggles

### 4. ✍️ AI Viral Hooks & Social Packaging Generator
For every generated clip, ClipFlow AI generates:
- **Attention-Grabbing Opening Hook** (First 3 seconds)
- **High-CTR Video Title**
- **On-Screen Opening Text Overlay**
- **Platform-Specific Captions**:
  - 🎵 **TikTok** (with trending #fyp tags)
  - 📸 **Instagram Reels** (formatted with engagement calls-to-action)
  - 🔴 **YouTube Shorts** (punchy title + tags)
  - 🐦 **X (Twitter)** (debate & thread hooks)
  - 💼 **LinkedIn** (professional takeaways)
- **One-Click Clipboard Copying**

### 5. 📥 Multi-Source Ingest
- **Upload Podcast / Video**: Drag & drop MP4, MOV, MKV, WEBM, MP3, WAV.
- **YouTube Link**: Paste any YouTube video or podcast URL (auto-download via `yt-dlp`).
- **Live Stream Buffer**: Real-time HLS (`.m3u8`), RTMP, or YouTube Live stream clipping with customizable rolling buffer (30s–180s).
- **Pre-analyzed Sample Demos**: 1-click exploration with Lex Fridman & Elon Musk or Ranveer Allahbadia (Hindi).

---

## 🚀 Quick Start Guide

### 1. Launch Backend API Server
```powershell
cd D:\ai-stream-clipper\backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Launch Frontend Studio Dashboard
```powershell
cd D:\ai-stream-clipper\frontend
npm run dev
```

Open your browser at:
- **Vite Studio Dashboard**: [http://127.0.0.1:5173](http://127.0.0.1:5173)
- **FastAPI Unified Production Endpoint**: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛠️ Technology Stack
- **Backend**: FastAPI, Uvicorn, Python 3.12
- **Transcription**: Faster-Whisper (CTranslate2) with multilingual support (English & Hindi)
- **Computer Vision**: OpenCV (Haar Cascades, EMA face tracking)
- **Media Engine**: FFmpeg (HW acceleration, ASS subtitle burn-in, audio crossfades)
- **Stream Ingest**: `yt-dlp` & FFmpeg HLS buffer
- **Frontend**: React 19, Vite, Tailwind CSS v4, Lucide Icons, Canvas-Confetti
