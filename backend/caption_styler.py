import os
import re
from typing import List, Dict, Any

class CaptionStyler:
    """
    Generates ASS (Advanced SubStation Alpha) subtitle files and styling
    for viral short-form video styles:
    - Hormozi
    - MrBeast
    - Minimal
    - Podcast
    - Cinematic
    - Gaming
    - Neon
    """

    STYLE_PRESETS = {
        "hormozi": {
            "name": "Hormozi Style",
            "fontname": "Anton",
            "fontsize": 34,
            "primary_color": "&H00FFFFFF",     # Crisp White
            "highlight_color": "&H0000E6FF",   # Ultra Bright Gold/Yellow (&H00BBGGRR)
            "secondary_color": "&H00FFFFFF",
            "outline_color": "&H00000000",     # Deep Solid Black
            "back_color": "&H80000000",
            "bold": -1,
            "italic": 0,
            "uppercase": True,
            "outline": 3.0,
            "shadow": 1.5,
            "alignment": 2, # Bottom Center
            "margin_v": 360,
            "words_per_group": 3,
            "animation": "pop",
            "has_emojis": True,
            "glow": False
        },
        "mrbeast": {
            "name": "MrBeast Style",
            "fontname": "Anton",
            "fontsize": 36,
            "primary_color": "&H0000FFFF",     # Vibrant Electric Yellow
            "highlight_color": "&H0055FF00",   # Neon Toxic Green
            "secondary_color": "&H00FFFFFF",
            "outline_color": "&H00000000",
            "back_color": "&H00000000",
            "bold": -1,
            "italic": 0,
            "uppercase": True,
            "outline": 3.5,
            "shadow": 2.0,
            "alignment": 2,
            "margin_v": 360,
            "words_per_group": 2,
            "animation": "bounce",
            "has_emojis": True,
            "glow": False
        },
        "minimal": {
            "name": "Minimal Style",
            "fontname": "Poppins",
            "fontsize": 26,
            "primary_color": "&H00FFFFFF",
            "highlight_color": "&H00E0E0E0",
            "secondary_color": "&H00AAAAAA",
            "outline_color": "&H90000000",
            "back_color": "&HA0000000",
            "bold": 0,
            "italic": 0,
            "uppercase": False,
            "outline": 1.5,
            "shadow": 1.0,
            "alignment": 2,
            "margin_v": 330,
            "words_per_group": 4,
            "animation": "fade",
            "has_emojis": False,
            "glow": False
        },
        "podcast": {
            "name": "Podcast Style",
            "fontname": "Montserrat",
            "fontsize": 32,
            "primary_color": "&H00FFFFFF",
            "highlight_color": "&H00FFAA00",   # Azure / Vibrant Cyan
            "secondary_color": "&H00707070",
            "outline_color": "&H00101010",
            "back_color": "&H90000000",
            "bold": -1,
            "italic": 0,
            "uppercase": False,
            "outline": 2.5,
            "shadow": 1.5,
            "alignment": 2,
            "margin_v": 350,
            "words_per_group": 3,
            "animation": "karaoke",
            "has_emojis": True,
            "glow": False
        },
        "cinematic": {
            "name": "Cinematic Style",
            "fontname": "Cinzel",
            "fontsize": 28,
            "primary_color": "&H00EAEAEA",
            "highlight_color": "&H004ED2FF",   # Warm Amber
            "secondary_color": "&H00808080",
            "outline_color": "&H00080808",
            "back_color": "&H00000000",
            "bold": 0,
            "italic": -1,
            "uppercase": False,
            "outline": 1.8,
            "shadow": 1.5,
            "alignment": 2,
            "margin_v": 330,
            "words_per_group": 4,
            "animation": "fade",
            "has_emojis": False,
            "glow": False
        },
        "gaming": {
            "name": "Gaming Style",
            "fontname": "Rubik",
            "fontsize": 36,
            "primary_color": "&H00FFFFFF",
            "highlight_color": "&H00FF00EA",   # Electric Magenta
            "secondary_color": "&H0000FFFF",   # Cyber Yellow
            "outline_color": "&H002E004B",     # Deep Cyber Purple
            "back_color": "&H00000000",
            "bold": -1,
            "italic": -1,
            "uppercase": True,
            "outline": 3.5,
            "shadow": 2.0,
            "alignment": 2,
            "margin_v": 360,
            "words_per_group": 2,
            "animation": "shake",
            "has_emojis": True,
            "glow": True
        },
        "neon": {
            "name": "Neon Style",
            "fontname": "Bebas Neue",
            "fontsize": 36,
            "primary_color": "&H00FFFFFF",
            "highlight_color": "&H0000FF00",   # Neon Lime
            "secondary_color": "&H00FFFF00",   # Cyan
            "outline_color": "&H0000FF00",     # Neon glow outline
            "back_color": "&H00000000",
            "bold": -1,
            "italic": 0,
            "uppercase": True,
            "outline": 2.5,
            "shadow": 4.0,
            "alignment": 2,
            "margin_v": 360,
            "words_per_group": 3,
            "animation": "glow",
            "has_emojis": True,
            "glow": True
        }
    }

    EMOJI_KEYWORDS = {
        "money": "💸", "cash": "💰", "rich": "🤑", "dollar": "💵", "million": "💰", "billion": "💎",
        "fire": "🔥", "crazy": "🤯", "insane": "🤯", "shock": "😱", "shocking": "😱",
        "dead": "💀", "die": "💀", "killed": "💀", "grave": "🪦",
        "growth": "📈", "viral": "🚀", "secret": "🤫", "truth": "👁️", "lie": "🤥",
        "win": "🏆", "winner": "🥇", "king": "👑", "boss": "💼", "power": "⚡",
        "strong": "💪", "gym": "🏋️", "fight": "🥊", "target": "🎯",
        "brain": "🧠", "mind": "🤯", "think": "🤔", "idea": "💡", "learn": "📚",
        "love": "❤️", "danger": "⚠️", "warning": "🚨", "fake": "❌", "stop": "🛑",
        "india": "🇮🇳", "game": "🎮", "stream": "🔴", "laugh": "😂", "lol": "🤣"
    }

    @staticmethod
    def format_ass_time(seconds: float) -> str:
        """Converts seconds float to ASS timestamp format: H:MM:SS.cs"""
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        csecs = int(round((seconds - int(seconds)) * 100))
        if csecs >= 100:
            csecs = 99
        return f"{hrs:d}:{mins:02d}:{secs:02d}.{csecs:02d}"

    @staticmethod
    def hex_to_ass_color(hex_color: str, alpha: str = "00") -> str:
        """Converts '#RRGGBB' to ASS color '&H[AA][BB][GG][RR]'"""
        if not hex_color:
            return "&H00FFFFFF"
        cleaned = hex_color.lstrip("#")
        if len(cleaned) == 6:
            r = cleaned[0:2]
            g = cleaned[2:4]
            b = cleaned[4:6]
            return f"&H{alpha}{b}{g}{r}".upper()
        return hex_color

    @classmethod
    def inject_emojis(cls, text: str) -> str:
        """Injects contextual emojis into captions for maximum engagement"""
        words = text.split()
        annotated = []
        for w in words:
            clean = re.sub(r'[^\w]', '', w.lower())
            annotated.append(w)
            if clean in cls.EMOJI_KEYWORDS:
                annotated.append(cls.EMOJI_KEYWORDS[clean])
        return " ".join(annotated)

    @classmethod
    def generate_ass(cls, words_data: List[Dict[str, Any]], style_name: str = "hormozi", custom_options: Dict[str, Any] = None, video_width: int = 1080, video_height: int = 1920) -> str:
        """
        Generates full ASS file content from word-level transcript tokens.
        Each word dict expected: {'word': str, 'start': float, 'end': float, 'speaker': int (opt)}
        """
        style = dict(cls.STYLE_PRESETS.get(style_name.lower(), cls.STYLE_PRESETS["hormozi"]))
        if custom_options:
            for k, v in custom_options.items():
                if v is not None:
                    if k in ["primary_color", "highlight_color", "outline_color", "back_color"] and str(v).startswith("#"):
                        style[k] = cls.hex_to_ass_color(str(v))
                    else:
                        style[k] = v

        fontname = style.get("fontname", "Impact")
        
        # Calculate dynamic proportional font size
        base_fontsize = int(style.get("fontsize", 40))
        font_size_pref = custom_options.get("font_size") if custom_options else None
        if font_size_pref == "small":
            base_fontsize = int(base_fontsize * 0.8)
        elif font_size_pref == "large":
            base_fontsize = int(base_fontsize * 1.25)
        elif isinstance(font_size_pref, (int, float)):
            base_fontsize = int(font_size_pref)

        # Scale by target video width relative to standard 1080p width
        # Ensures captions look balanced across 19:6, 9:16, 1:1, etc.
        width_ratio = max(0.70, min(1.0, video_width / 1080.0))
        fontsize = max(26, int(round(base_fontsize * width_ratio)))

        primary_color = style.get("primary_color", "&H00FFFFFF")
        highlight_color = style.get("highlight_color", "&H0000E6FF")
        secondary_color = style.get("secondary_color", "&H00CCCCCC")
        outline_color = style.get("outline_color", "&H00000000")
        back_color = style.get("back_color", "&H80000000")
        bold = -1 if style.get("bold") else 0
        italic = -1 if style.get("italic") else 0
        outline = round(float(style.get("outline", 3.0)) * width_ratio, 1)
        shadow = round(float(style.get("shadow", 1.5)) * width_ratio, 1)
        alignment = int(style.get("alignment", 2))
        
        # Calculate margin_v: position in lower third (above YouTube Shorts / TikTok UI)
        base_margin_v = int(style.get("margin_v", 320))
        margin_v = int(round(base_margin_v * (video_height / 1920.0)))
        
        uppercase = bool(style.get("uppercase", True))
        has_emojis = bool(style.get("has_emojis", True))
        
        # Short punchy phrases (2 to 3 words)
        words_per_group = int(custom_options.get("words_per_group", 2 if width_ratio < 0.75 else style.get("words_per_group", 3))) if custom_options else (2 if width_ratio < 0.75 else int(style.get("words_per_group", 3)))

        ass_header = f"""[Script Info]
Title: AI Stream Clipper Subtitles
ScriptType: v4.00+
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: {video_width}
PlayResY: {video_height}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{fontname},{fontsize},{primary_color},{secondary_color},{outline_color},{back_color},{bold},{italic},0,0,100,100,1,0,1,{outline},{shadow},{alignment},30,30,{margin_v},1
Style: Highlight,{fontname},{int(fontsize * 1.05)},{highlight_color},{secondary_color},{outline_color},{back_color},{bold},{italic},0,0,105,105,1,0,1,{outline + 0.8},{shadow + 0.8},{alignment},30,30,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        events = []
        if not words_data:
            return ass_header

        # 1. Clean, sort, and ensure strictly monotonic non-overlapping word timings
        valid_words = []
        for w in words_data:
            txt = str(w.get("word", "")).strip()
            if not txt:
                continue
            st = float(w.get("start", 0.0))
            en = float(w.get("end", st + 0.3))
            valid_words.append({
                "word": txt,
                "start": max(0.0, st),
                "end": max(st + 0.05, en)
            })

        valid_words.sort(key=lambda x: x["start"])
        if not valid_words:
            return ass_header

        # Enforce non-overlapping words sequence
        prev_en = 0.0
        for w in valid_words:
            if w["start"] < prev_en:
                w["start"] = prev_en
            if w["end"] <= w["start"]:
                w["end"] = w["start"] + 0.15
            prev_en = w["end"]

        # 2. Group words into short punchy phrases (2 to 3 words)
        grouped = []
        current_chunk = []
        for w in valid_words:
            current_chunk.append(w)
            txt = w["word"]
            # Split on punctuation, word count, or natural silence
            silence_gap = (current_chunk and len(current_chunk) > 1 and (w["start"] - current_chunk[-2]["end"] > 0.5))
            if len(current_chunk) >= words_per_group or (txt and txt[-1] in ".?!,") or silence_gap:
                grouped.append(current_chunk)
                current_chunk = []
        if current_chunk:
            grouped.append(current_chunk)

        # 3. Generate strictly non-overlapping sequential dialogue events
        prev_event_end = 0.0
        for chunk_idx, chunk in enumerate(grouped):
            chunk_start = max(chunk[0]["start"], prev_event_end)
            next_start = grouped[chunk_idx + 1][0]["start"] if chunk_idx + 1 < len(grouped) else None
            chunk_end = chunk[-1]["end"]

            if next_start is not None:
                if next_start <= chunk_start:
                    next_start = chunk_start + 0.25 * len(chunk)
                    grouped[chunk_idx + 1][0]["start"] = next_start
                if chunk_end > next_start:
                    chunk_end = next_start
                elif (next_start - chunk_end) > 0.6:
                    chunk_end = min(chunk_end + 0.2, next_start)
                else:
                    chunk_end = next_start
            else:
                chunk_end = max(chunk_start + 0.5, chunk_end)

            if chunk_end <= chunk_start:
                chunk_end = chunk_start + 0.3

            n_words = len(chunk)
            step = (chunk_end - chunk_start) / max(1, n_words)

            for active_idx in range(n_words):
                w_start = chunk_start + active_idx * step
                w_end = (chunk_start + (active_idx + 1) * step) if active_idx + 1 < n_words else chunk_end
                
                # Update boundary tracker
                prev_event_end = w_end

                time_start = cls.format_ass_time(w_start)
                time_end = cls.format_ass_time(w_end)

                # Assemble line with active word highlighted
                parts = []
                for i, cw in enumerate(chunk):
                    raw_text = cw["word"].strip()
                    if uppercase:
                        raw_text = raw_text.upper()

                    if has_emojis:
                        clean = re.sub(r'[^\w]', '', raw_text.lower())
                        if clean in cls.EMOJI_KEYWORDS:
                            raw_text = f"{raw_text} {cls.EMOJI_KEYWORDS[clean]}"

                    if i == active_idx:
                        # Hormozi / Beast active word pop: clean scale up + highlight color
                        anim_tag = r"{\c" + highlight_color + r"\fscx108\fscy108\t(0,60,\fscx100\fscy100)}"
                        parts.append(f"{anim_tag}{raw_text}" + r"{\r}")
                    else:
                        parts.append(raw_text)

                line_text = " ".join(parts)
                events.append(f"Dialogue: 0,{time_start},{time_end},Default,,0,0,0,,{line_text}")

        return ass_header + "\n".join(events) + "\n"

    @classmethod
    def get_style_options(cls):
        """Returns preset details for UI customization"""
        return [
            {"id": k, **v} for k, v in cls.STYLE_PRESETS.items()
        ]
