# gesture_controller.py
import mediapipe as mp
import cv2


class GestureController:
    """Detects and interprets hand gestures using MediaPipe."""

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def process_frame(self, frame):
        """
        Processes a video frame to detect hands and gestures.
        Returns the recognized gesture, hand landmarks, and the processing results.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        gesture = "No Hand"
        hand_landmarks_list = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_landmarks_list.append(hand_landmarks)
                gesture = self._get_gesture(hand_landmarks)

        return gesture, hand_landmarks_list, results

    def _get_gesture(self, hand_landmarks):
        """Analyzes hand landmarks to identify a specific gesture."""
        # Check if the hand is upright
        if not hand_landmarks:
            return "No Hand"

        # Simple logic based on finger positions relative to each other
        fingers_up = [False] * 5  # Thumb, Index, Middle, Ring, Pinky

        # Tip and base landmark indices
        finger_tips = [4, 8, 12, 16, 20]
        finger_bases = [2, 5, 9, 13, 17]

        # Check for thumb up (approximate, based on x-coordinate)
        fingers_up[0] = hand_landmarks.landmark[finger_tips[0]].x > hand_landmarks.landmark[finger_bases[0]].x

        # Check for other fingers up (based on y-coordinate)
        for i in range(1, 5):
            fingers_up[i] = hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_bases[i]].y

        # Interpret gestures
        if all(fingers_up):
            return "TAKE_OFF"
        if all(not f for f in fingers_up):
            return "LAND"
        if fingers_up[1] and not any(fingers_up[2:]):
            return "FORWARD"
        if fingers_up[1] and fingers_up[2] and not any(fingers_up[3:]):
            return "ROTATE_LEFT"  # Example gesture for turning

        return "HOVER"

