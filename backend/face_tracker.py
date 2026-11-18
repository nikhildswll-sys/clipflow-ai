import os
import cv2
import numpy as np
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger("FaceTracker")

class SmartFaceTracker:
    """
    OpenCV-powered face detection and speaker tracking for intelligent auto-reframing.
    Tracks face coordinates over time, calculates smoothed pan trajectory,
    and produces crop parameters for 9:16, 16:9, 1:1, 4:5 aspect ratios.
    """

    def __init__(self):
        # Load OpenCV's built-in Haar Cascade for frontal faces
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def analyze_video_framing(self, video_path: str, start_time: float, end_time: float, sample_fps: float = 2.0) -> Dict[str, Any]:
        """
        Samples video between start_time and end_time to track speaker faces.
        Returns:
            {
                "dominant_x_ratio": float (0.0 to 1.0, default 0.5),
                "dominant_y_ratio": float (0.0 to 1.0, default 0.35),
                "speaker_count": int,
                "multi_speaker_detected": bool,
                "speakers_x": [float, float],
                "framing_keyframes": [{"time": float, "crop_x": float}]
            }
        """
        if not os.path.exists(video_path):
            return {"dominant_x_ratio": 0.5, "dominant_y_ratio": 0.35, "speaker_count": 1, "multi_speaker_detected": False}

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {"dominant_x_ratio": 0.5, "dominant_y_ratio": 0.35, "speaker_count": 1, "multi_speaker_detected": False}

        video_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        start_frame = int(start_time * video_fps)
        end_frame = min(total_frames, int(end_time * video_fps))
        frame_step = max(1, int(video_fps / sample_fps))

        detected_centers_x = []
        detected_centers_y = []
        keyframes = []
        smoothed_x = 0.5
        alpha = 0.15  # EMA smoothing factor for cinematic cameraman pan

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        current_frame_idx = start_frame

        while current_frame_idx < end_frame:
            ret, frame = cap.read()
            if not ret:
                break

            if (current_frame_idx - start_frame) % frame_step == 0:
                t = current_frame_idx / video_fps
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Quick scale down for fast CPU face detection
                h, w = gray.shape
                scale = min(1.0, 640.0 / max(w, h))
                if scale < 1.0:
                    small = cv2.resize(gray, (int(w * scale), int(h * scale)))
                else:
                    small = gray

                faces = self.face_cascade.detectMultiScale(
                    small,
                    scaleFactor=1.15,
                    minNeighbors=4,
                    minSize=(30, 30)
                )

                if len(faces) > 0:
                    # Sort faces by area descending (primary speaker closest to camera)
                    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
                    fx, fy, fw, fh = faces[0]
                    # Map back to 0.0 - 1.0 ratio
                    center_x = (fx + fw / 2.0) / (small.shape[1])
                    center_y = (fy + fh / 2.0) / (small.shape[0])

                    detected_centers_x.append(center_x)
                    detected_centers_y.append(center_y)

                    # Smooth tracking
                    smoothed_x = (alpha * center_x) + ((1 - alpha) * smoothed_x)
                    keyframes.append({"time": round(t - start_time, 2), "crop_x": round(smoothed_x, 3)})

            current_frame_idx += 1

        cap.release()

        # Multi-speaker analysis
        multi_speaker = False
        speakers_x = [0.5]
        if len(detected_centers_x) > 4:
            x_arr = np.array(detected_centers_x)
            # Check if there is bimodal distribution (e.g. host on left x<0.4 and guest on right x>0.6)
            left_speaker = x_arr[x_arr < 0.45]
            right_speaker = x_arr[x_arr > 0.55]
            if len(left_speaker) >= 2 and len(right_speaker) >= 2:
                multi_speaker = True
                speakers_x = [round(float(np.mean(left_speaker)), 2), round(float(np.mean(right_speaker)), 2)]

            mean_x = float(np.median(x_arr))
            mean_y = float(np.median(detected_centers_y)) if detected_centers_y else 0.35
        else:
            mean_x = 0.5
            mean_y = 0.35

        return {
            "dominant_x_ratio": round(mean_x, 3),
            "dominant_y_ratio": round(mean_y, 3),
            "speaker_count": 2 if multi_speaker else 1,
            "multi_speaker_detected": multi_speaker,
            "speakers_x": speakers_x,
            "framing_keyframes": keyframes
        }
