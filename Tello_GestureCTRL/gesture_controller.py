"""
IDEAL Fall 2026 - Gesture Controller (hand gesture recognition)

This module finds a hand in an image with MediaPipe and decides which
gesture it is showing. It does not talk to the drone; tello_gesture_control.py
does that.

Run this file by itself to practice gestures with your laptop webcam
(no drone needed):

    python gesture_controller.py

The first run downloads the MediaPipe hand model (about 8 MB), so do it
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
MODEL_PATH = Path(__file__).parent / "hand_landmarker.task"
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
             "hand_landmarker/float16/latest/hand_landmarker.task")

# Pairs of landmark numbers to connect with lines when drawing the hand.
# MediaPipe numbers the 21 hand landmarks like this:
#   0 = wrist
#   1-4 = thumb, 5-8 = index, 9-12 = middle, 13-16 = ring, 17-20 = pinky
#   (for each finger, the first number is the knuckle and the last is the tip)
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),           # thumb
    (0, 5), (5, 6), (6, 7), (7, 8),           # index finger
    (5, 9), (9, 10), (10, 11), (11, 12),      # middle finger
    (9, 13), (13, 14), (14, 15), (15, 16),    # ring finger
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20),  # pinky and palm
]


def download_model():
    """Download the hand model the first time it is needed."""
    if MODEL_PATH.exists():
        return
    print(f"Downloading hand model to {MODEL_PATH} ...")
    temp_path = MODEL_PATH.with_suffix(".part")  # so a failed download never looks finished
    try:
        urllib.request.urlretrieve(MODEL_URL, temp_path)
        temp_path.replace(MODEL_PATH)
    except Exception as error:
        raise RuntimeError(
            "Could not download the hand model. Connect to normal internet "
            "(not the Tello Wi-Fi) and run this again, or download it manually from\n"
            f"  {MODEL_URL}\nand save it as\n  {MODEL_PATH}"
        ) from error
    print("Download complete.")


class GestureController:
    """Detects a hand with MediaPipe and turns it into a gesture name."""

    def __init__(self):
        download_model()
        options = vision.HandLandmarkerOptions(
            base_options=mp_tasks.BaseOptions(model_asset_path=str(MODEL_PATH)),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,  # Only one hand, so two hands cannot give two commands
            min_hand_detection_confidence=0.75,
            min_hand_presence_confidence=0.75,
            min_tracking_confidence=0.75,
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)
        self.start_time = time.monotonic()

    def process_frame(self, frame_bgr):
        """
        Find a hand in a BGR frame and return (gesture, landmarks).

        gesture   -- "TAKE_OFF", "LAND", "FORWARD", "ROTATE_LEFT", "HOVER", or "NO_HAND"
        landmarks -- list of 21 points (each has .x and .y between 0 and 1), or None
        """
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        # VIDEO mode needs a timestamp that always increases (in milliseconds).
        timestamp_ms = int((time.monotonic() - self.start_time) * 1000)
        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        if not result.hand_landmarks:
            return "NO_HAND", None

        landmarks = result.hand_landmarks[0]
        return self.get_gesture(landmarks), landmarks

    @staticmethod
    def get_gesture(landmarks):
        """Decide which gesture the hand is making from its 21 landmarks."""
        # Image coordinates: x grows to the right, y grows DOWNWARD.
        # So a smaller y value means "higher up in the picture".

        # Index, middle, ring, pinky: the finger is "up" if its tip (8, 12, 16, 20)
        # is higher in the picture than its middle joint (6, 10, 14, 18).
        index_up = landmarks[8].y < landmarks[6].y
        middle_up = landmarks[12].y < landmarks[10].y
        ring_up = landmarks[16].y < landmarks[14].y
        pinky_up = landmarks[20].y < landmarks[18].y

        # Thumb: it sticks out sideways, so we compare x instead of y.
        # "Outward" means away from the pinky side of the hand. We figure out
        # which way is outward from the knuckles (index knuckle 5 vs pinky
        # knuckle 17), so this works for left AND right hands.
        outward = 1 if landmarks[5].x > landmarks[17].x else -1
        thumb_up = (landmarks[4].x - landmarks[2].x) * outward > 0

        fingers = [thumb_up, index_up, middle_up, ring_up, pinky_up]

        if all(fingers):
            return "TAKE_OFF"      # open hand
        if not any(fingers):
            return "LAND"          # fist
        if index_up and not middle_up and not ring_up and not pinky_up:
            return "FORWARD"       # index finger only
        if index_up and middle_up and not ring_up and not pinky_up:
            return "ROTATE_LEFT"   # "peace sign"
        return "HOVER"             # anything else

    @staticmethod
    def draw_landmarks(frame, landmarks):
        """Draw the hand skeleton on the frame."""
        height, width = frame.shape[:2]
        points = [(int(p.x * width), int(p.y * height)) for p in landmarks]
        for start, end in HAND_CONNECTIONS:
            cv2.line(frame, points[start], points[end], (255, 255, 255), 2)
        for point in points:
            cv2.circle(frame, point, 4, (0, 0, 255), -1)


# Webcam practice mode: run this file by itself to test gestures without a drone.
if __name__ == "__main__":
    controller = GestureController()
    camera = cv2.VideoCapture(0)
    print("Show gestures to your webcam. Press Q to quit.")

    while True:
        ok, frame = camera.read()   # webcam frames are already BGR
        if not ok:
            print("Could not read from the webcam.")
            break

        gesture, landmarks = controller.process_frame(frame)
        if landmarks is not None:
            controller.draw_landmarks(frame, landmarks)
        cv2.putText(frame, f"Gesture: {gesture}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Gesture Practice (webcam)", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
