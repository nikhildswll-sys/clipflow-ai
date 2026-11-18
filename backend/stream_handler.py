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
        Captures real-time live stream chunks (e.g. 120 seconds rolling buffer)
        from HLS / m3u8 / RTMP / YouTube Live for instantaneous clipping!
        """
        cmd = [
            "ffmpeg", "-y",
            "-i", stream_url,
            "-t", str(duration_sec),
            "-c:v", "copy",
            "-c:a", "copy",
            output_path
        ]
        logger.info(f"Recording live stream segment ({duration_sec}s): {stream_url}")
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=duration_sec + 30)
            return os.path.exists(output_path)
        except Exception as e:
            logger.error(f"Live stream capture failed: {e}")
            return False
