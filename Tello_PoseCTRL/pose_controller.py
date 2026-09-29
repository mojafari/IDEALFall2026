"""
IDEAL Fall 2026 - Pose Controller (full-body pose recognition)

This module finds a person's body in an image with MediaPipe and decides
which arm pose they are making. It does not talk to the drone;
tello_pose_control.py does that.

Run this file by itself to practice poses with your laptop webcam
(no drone needed):

    python pose_controller.py

The first run downloads the MediaPipe pose model (about 6 MB), so do it
while you are connected to normal internet, NOT the Tello Wi-Fi.
"""

import time
import urllib.request
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_tasks
from mediapipe.tasks.python import vision

# The model file is stored next to this script.
MODEL_PATH = Path(__file__).parent / "pose_landmarker_lite.task"
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
             "pose_landmarker_lite/float16/latest/pose_landmarker_lite.task")

# MediaPipe numbers 33 body landmarks. These are the ones we use.
# "Left" and "right" mean the PERSON's left and right, not the image's.
LEFT_SHOULDER, RIGHT_SHOULDER = 11, 12
LEFT_ELBOW, RIGHT_ELBOW = 13, 14
LEFT_WRIST, RIGHT_WRIST = 15, 16
LEFT_HIP, RIGHT_HIP = 23, 24

# Lines to draw for the upper body (arms, shoulders, and torso).
BODY_CONNECTIONS = [
    (LEFT_SHOULDER, RIGHT_SHOULDER),
    (LEFT_SHOULDER, LEFT_ELBOW), (LEFT_ELBOW, LEFT_WRIST),
    (RIGHT_SHOULDER, RIGHT_ELBOW), (RIGHT_ELBOW, RIGHT_WRIST),
    (LEFT_SHOULDER, LEFT_HIP), (RIGHT_SHOULDER, RIGHT_HIP),
    (LEFT_HIP, RIGHT_HIP),
]

# Landmarks with visibility below this are probably hidden or off-screen.
MIN_VISIBILITY = 0.5


def download_model():
    """Download the pose model the first time it is needed."""
    if MODEL_PATH.exists():
        return
    print(f"Downloading pose model to {MODEL_PATH} ...")
    temp_path = MODEL_PATH.with_suffix(".part")  # so a failed download never looks finished
    try:
        urllib.request.urlretrieve(MODEL_URL, temp_path)
        temp_path.replace(MODEL_PATH)
    except Exception as error:
        raise RuntimeError(
            "Could not download the pose model. Connect to normal internet "
            "(not the Tello Wi-Fi) and run this again, or download it manually from\n"
            f"  {MODEL_URL}\nand save it as\n  {MODEL_PATH}"
        ) from error
    print("Download complete.")


class PoseController:
    """Detects a body with MediaPipe and turns arm positions into a command name."""

    def __init__(self):
        download_model()
        options = vision.PoseLandmarkerOptions(
            base_options=mp_tasks.BaseOptions(model_asset_path=str(MODEL_PATH)),
            running_mode=vision.RunningMode.VIDEO,
            num_poses=1,  # Only one person controls the drone
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.landmarker = vision.PoseLandmarker.create_from_options(options)
        self.start_time = time.monotonic()

    def process_frame(self, frame_bgr):
        """
        Find a person in a BGR frame and return (command, landmarks).

        command   -- "TAKE_OFF", "LAND", "FORWARD", "TURN_LEFT", "TURN_RIGHT",
                     "HOVER", or "NO_PERSON"
        landmarks -- list of 33 points (each has .x, .y, .z, .visibility), or None
        """
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        # VIDEO mode needs a timestamp that always increases (in milliseconds).
        timestamp_ms = int((time.monotonic() - self.start_time) * 1000)
        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        if not result.pose_landmarks:
            return "NO_PERSON", None

        landmarks = result.pose_landmarks[0]
        return self.get_pose_command(landmarks), landmarks

    @staticmethod
    def get_pose_command(landmarks):
        """Decide which command the arms are showing."""
        left_shoulder = landmarks[LEFT_SHOULDER]
        right_shoulder = landmarks[RIGHT_SHOULDER]
        left_wrist = landmarks[LEFT_WRIST]
        right_wrist = landmarks[RIGHT_WRIST]

        # If the shoulders or wrists are hidden or off-screen, MediaPipe still
        # guesses where they are. Do not fly the drone based on a guess.
        for point in (left_shoulder, right_shoulder, left_wrist, right_wrist):
            if point.visibility is not None and point.visibility < MIN_VISIBILITY:
                return "HOVER"

        # Image coordinates: y grows DOWNWARD, so a smaller y is higher up.
        left_up = left_wrist.y < left_shoulder.y
        right_up = right_wrist.y < right_shoulder.y

        # Both arms raised
        if left_up and right_up:
            return "TAKE_OFF"

        # Only your left arm raised
        if left_up and not right_up:
            return "TURN_LEFT"

        # Only your right arm raised
        if right_up and not left_up:
            return "TURN_RIGHT"

        # Arms crossed in an "X" in front of your chest.
        # The drone camera faces you, so normally your LEFT wrist appears on the
        # RIGHT side of the image (larger x). When your arms cross, they swap sides.
        if left_wrist.x < right_wrist.x:
            return "LAND"

        # Both arms pushed straight toward the camera.
        # z is depth: more negative means closer to the camera.
        if left_wrist.z < left_shoulder.z - 0.2 and right_wrist.z < right_shoulder.z - 0.2:
            return "FORWARD"

        # Arms relaxed at your sides, or anything else
        return "HOVER"

    @staticmethod
    def draw_landmarks(frame, landmarks):
        """Draw the upper-body skeleton on the frame."""
        height, width = frame.shape[:2]
        points = {i: (int(landmarks[i].x * width), int(landmarks[i].y * height))
                  for start_end in BODY_CONNECTIONS for i in start_end}
        for start, end in BODY_CONNECTIONS:
            cv2.line(frame, points[start], points[end], (255, 255, 255), 2)
        for point in points.values():
            cv2.circle(frame, point, 5, (0, 0, 255), -1)


# Webcam practice mode: run this file by itself to test poses without a drone.
if __name__ == "__main__":
    controller = PoseController()
    camera = cv2.VideoCapture(0)
    print("Stand back so your upper body is visible. Press Q to quit.")

    while True:
        ok, frame = camera.read()   # webcam frames are already BGR
        if not ok:
            print("Could not read from the webcam.")
            break

        # Note: we do NOT mirror the webcam image. The Tello camera is not
        # mirrored either, so left/right behave the same way in both.
        command, landmarks = controller.process_frame(frame)
        if landmarks is not None:
            controller.draw_landmarks(frame, landmarks)
        cv2.putText(frame, f"Command: {command}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Pose Practice (webcam)", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
