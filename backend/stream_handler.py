import os
import subprocess
import json
import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("StreamHandler")

import os
import subprocess
import json
import time
import re
import logging
from typing import Dict, Any, Optional, Callable

logger = logging.getLogger("StreamHandler")

class StreamHandler:
    """
    Handles YouTube video download and live stream capture using yt-dlp & FFmpeg.
    Supports YouTube URLs, Twitch, Kick, HLS (.m3u8), and RTMP live streams.
    Extracts YouTube Replay Heatmaps (Most Replayed peaks) and Chapters for high-retention clipping.
    """

    @classmethod
    def get_youtube_metadata(cls, url: str) -> Dict[str, Any]:
        """Fetches metadata, title, duration, author, thumbnail, heatmap, and chapters without downloading"""
        cmd = [
            "yt-dlp",
            "--dump-json",
            "--no-playlist",
            url
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            info = json.loads(res.stdout)
            
            heatmap_raw = info.get("heatmap") or []
            chapters_raw = info.get("chapters") or []

            logger.info(f"Fetched metadata for '{info.get('title')}': Duration={info.get('duration')}s, Heatmap points={len(heatmap_raw)}, Chapters={len(chapters_raw)}")

            return {
                "title": info.get("title", "YouTube Video"),
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "Creator"),
                "thumbnail": info.get("thumbnail", ""),
                "description": info.get("description", "")[:300],
                "is_live": info.get("is_live", False),
                "view_count": info.get("view_count", 0),
                "heatmap": heatmap_raw,
                "chapters": chapters_raw
            }
        except Exception as e:
            logger.error(f"Failed to fetch metadata with yt-dlp: {e}")
            return {
                "title": "Stream / Video",
                "duration": 300,
                "uploader": "Online Video",
                "thumbnail": "",
                "description": "Video stream content",
                "is_live": False,
                "heatmap": [],
                "chapters": []
            }

    @classmethod
    def download_youtube_video(
        cls,
        url: str,
        output_path: str,
        max_height: int = 720,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> bool:
        """
        Downloads YouTube video with fast multi-fragment streaming and non-blocking progress parsing.
        Default 720p enables ultra-fast downloads (150-250MB for 50-minute podcasts vs 1.5GB for 1080p).
        Never deadlocks on pipe buffers.
        """
        cmd = [
            "yt-dlp",
            "-f", f"bv*[height<={max_height}]+ba/b[height<={max_height}]/b",
            "--merge-output-format", "mp4",
            "--concurrent-fragments", "4",
            "--socket-timeout", "20",
            "--retries", "5",
            "--no-playlist",
            "--newline",
            "-o", output_path,
            url
        ]
        logger.info(f"Downloading YouTube video ({max_height}p max): {url} -> {output_path}")

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            last_pct = 0.0
            for line in proc.stdout:
                line_str = line.strip()
                if "[download]" in line_str and "%" in line_str:
                    match = re.search(r"(\d+(?:\.\d+)?)%", line_str)
                    if match:
                        pct = float(match.group(1))
                        if abs(pct - last_pct) >= 2.0 or pct >= 100.0:
                            last_pct = pct
                            if progress_callback:
                                progress_callback(pct, line_str)
                            logger.info(f"yt-dlp progress: {line_str}")

            proc.wait()

            if proc.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                logger.info(f"Download successful: {output_path} ({os.path.getsize(output_path) // (1024*1024)} MB)")
                return True

            # Fallback format if specific format failed
            logger.warning(f"Initial yt-dlp download exited with code {proc.returncode}, trying fallback format...")
            fallback_cmd = [
                "yt-dlp",
                "-f", "b/ba+bv/best",
                "--merge-output-format", "mp4",
                "--no-playlist",
                "-o", output_path,
                url
            ]
            res = subprocess.run(fallback_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
            return os.path.exists(output_path) and os.path.getsize(output_path) > 1000

        except Exception as e:
            logger.error(f"yt-dlp download failed: {e}")
            return False

    @classmethod
    def capture_live_stream_segment(cls, stream_url: str, output_path: str, duration_sec: int = 120) -> bool:
        """
        Captures real-time live stream chunks (e.g. 60-120 seconds rolling buffer)
        from HLS / m3u8 / RTMP / YouTube Live / Twitch for instantaneous clipping!
        Fixes all buffering, timestamp desync, and audio beeping/stutter issues.
        """
        resolved_stream_url = stream_url.strip()
        audio_stream_url = None

        # 1. If it's a YouTube / Twitch / Web stream URL, resolve direct media manifests via yt-dlp
        is_web_url = any(domain in resolved_stream_url.lower() for domain in ["youtube.com", "youtu.be", "twitch.tv", "kick.com"])
        if is_web_url:
            logger.info(f"Resolving live stream manifest with yt-dlp for {stream_url}...")
            try:
                g_cmd = [
                    "yt-dlp",
                    "-g",
                    "-f", "bv*[height<=720]+ba/b[height<=720]/b",
                    "--no-playlist",
                    "--no-warnings",
                    stream_url
                ]
                res = subprocess.run(g_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=25)
                if res.returncode == 0 and res.stdout.strip():
                    urls = [u.strip() for u in res.stdout.strip().splitlines() if u.strip().startswith("http")]
                    if len(urls) == 1:
                        resolved_stream_url = urls[0]
                    elif len(urls) >= 2:
                        resolved_stream_url = urls[0]
                        audio_stream_url = urls[1]
                    logger.info(f"Resolved direct stream manifest successfully.")
            except Exception as e:
                logger.warning(f"Could not resolve via yt-dlp -g: {e}")

        # 2. Build robust FFmpeg capture command with audio re-encode to eliminate beeps & buffering
        if audio_stream_url:
            cmd = [
                "ffmpeg", "-y",
                "-reconnect", "1", "-reconnect_at_eof", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
                "-i", resolved_stream_url,
                "-reconnect", "1", "-reconnect_at_eof", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
                "-i", audio_stream_url,
                "-t", str(duration_sec),
                "-avoid_negative_ts", "make_zero",
                "-fflags", "+genpts+discardcorrupt",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                output_path
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-reconnect", "1", "-reconnect_at_eof", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
                "-i", resolved_stream_url,
                "-t", str(duration_sec),
                "-avoid_negative_ts", "make_zero",
                "-fflags", "+genpts+discardcorrupt",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                output_path
            ]

        logger.info(f"Recording live stream segment ({duration_sec}s): {stream_url}")
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=duration_sec + 45)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
                logger.info(f"Live stream captured cleanly: {output_path} ({os.path.getsize(output_path)//1024} KB)")
                return True
        except Exception as e:
            logger.error(f"FFmpeg live capture failed: {e}")

        # 3. Fallback: yt-dlp direct section download if FFmpeg live capture hit timeout
        if is_web_url:
            logger.info("Attempting direct yt-dlp clip buffer fallback...")
            try:
                ytdlp_cmd = [
                    "yt-dlp",
                    "-f", "bv*[height<=720]+ba/b[height<=720]/b",
                    "--download-sections", f"*00:00:00-00:01:{min(59, duration_sec):02d}",
                    "--no-playlist",
                    "-o", output_path,
                    stream_url
                ]
                subprocess.run(ytdlp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=duration_sec + 30)
                if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
                    return True
            except Exception as e:
                logger.error(f"yt-dlp buffer fallback failed: {e}")

        return False
