# pose_controller.py
import mediapipe as mp
import cv2


class PoseController:
    """Detects and interprets body poses using MediaPipe."""

    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def process_frame(self, frame):
        """
        Processes a video frame to detect body pose and interpret gestures.
        Returns the recognized pose command, pose landmarks, and the results.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)

        command = "HOVER"
        pose_landmarks_list = []

        if results.pose_landmarks:
            pose_landmarks_list.append(results.pose_landmarks)
            command = self._get_pose_command(results.pose_landmarks)

        return command, pose_landmarks_list, results

    def _get_pose_command(self, pose_landmarks):
        """Analyzes pose landmarks to identify a specific body command."""
        if not pose_landmarks:
            return "HOVER"

        # Landmark indices for key body parts
        left_shoulder = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_wrist = pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]

        # Use the average shoulder position as a reference point
        shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2

        # Define movement based on arm positions relative to shoulders
        # Arms Up for Takeoff
        if (left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y):
            return "TAKE_OFF"

        # Arms Down for Land
        if (left_wrist.y > shoulder_center_y + 0.1 and right_wrist.y > shoulder_center_y + 0.1):
            return "LAND"

        # Left Arm Raised for Turn Left
        if (left_wrist.y < left_shoulder.y and right_wrist.y > right_shoulder.y):
            return "TURN_LEFT"

        # Right Arm Raised for Turn Right
        if (right_wrist.y < right_shoulder.y and left_wrist.y > left_shoulder.y):
            return "TURN_RIGHT"

        # A simple movement: moving arms forward
        if (left_wrist.z < left_shoulder.z - 0.2 and right_wrist.z < right_shoulder.z - 0.2):
             return "FORWARD"

        return "HOVER"

