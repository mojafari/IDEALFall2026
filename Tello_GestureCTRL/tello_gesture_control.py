"""
IDEAL Fall 2026 - Tello Gesture Control

Fly the Tello with hand gestures seen by its own camera.

    Open hand (all fingers up)   -> TAKE_OFF
    Fist (all fingers down)      -> LAND and end the program
    Index finger up              -> FORWARD (moves toward you!)
    Index + middle finger up     -> ROTATE_LEFT
    Anything else / no hand      -> HOVER

Safety features:
- A gesture must be held steady for HOLD_TIME seconds before it counts.
- A movement runs ONCE per gesture. Relax your hand (or hide it) before
  repeating the same movement.
- While hovering, the program keeps talking to the drone so it does not
  auto-land after 15 seconds of silence.
- Pressing Q, or any error, lands the drone.

Tip: practice your gestures first with the webcam:  python gesture_controller.py
"""

import threading
import time

import cv2
from djitellopy import Tello

from gesture_controller import GestureController

# --- Settings you can change ---
HOLD_TIME = 0.3           # Seconds a gesture must be held before it counts
COMMAND_COOLDOWN = 0.5    # Seconds to wait after a command finishes
MOVE_DISTANCE_CM = 30     # Distance for FORWARD (Tello allows 20-500 cm)
ROTATE_DEGREES = 45       # Angle for ROTATE_LEFT
KEEPALIVE_INTERVAL = 5.0  # Seconds between "I'm still here" messages while hovering

# --- Shared variables (used by more than one thread) ---
frame_lock = threading.Lock()
latest_frame = None         # Newest camera frame (BGR)
active_gesture = "NO_HAND"  # Gesture that has been held for HOLD_TIME
is_running = True           # Set to False to stop every thread
in_flight = False


def video_read_thread():
    """Keep copying the newest Tello frame into latest_frame."""
    global latest_frame
    frame_read = tello.get_frame_read()
    while is_running:
        frame = frame_read.frame
        if frame is not None:
            # djitellopy gives RGB frames, but OpenCV and our controller expect BGR.
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            with frame_lock:
                latest_frame = frame
        time.sleep(0.01)


def gesture_command_thread():
    """Turn the active gesture into drone commands."""
    global is_running, in_flight

    last_command_time = time.time()
    ready_for_move = True  # Becomes False after a move, True again after HOVER/NO_HAND

    while is_running:
        gesture = active_gesture

        # Relaxing your hand "re-arms" the movement commands.
        if gesture in ("HOVER", "NO_HAND"):
            ready_for_move = True

        if time.time() - last_command_time > COMMAND_COOLDOWN:
            try:
                if gesture == "TAKE_OFF" and not in_flight:
                    print("Command: TAKE_OFF")
                    tello.takeoff()
                    in_flight = True
                    ready_for_move = False
                    last_command_time = time.time()

                elif gesture == "LAND" and in_flight:
                    print("Command: LAND")
                    tello.land()
                    in_flight = False
                    is_running = False  # End the program after landing

                elif gesture == "FORWARD" and in_flight and ready_for_move:
                    print(f"Command: FORWARD {MOVE_DISTANCE_CM} cm")
                    tello.move_forward(MOVE_DISTANCE_CM)
                    ready_for_move = False
                    last_command_time = time.time()

                elif gesture == "ROTATE_LEFT" and in_flight and ready_for_move:
                    print(f"Command: ROTATE_LEFT {ROTATE_DEGREES} degrees")
                    tello.rotate_counter_clockwise(ROTATE_DEGREES)
                    ready_for_move = False
                    last_command_time = time.time()

                elif in_flight and time.time() - last_command_time > KEEPALIVE_INTERVAL:
                    # The Tello lands by itself if it hears nothing for 15 seconds.
                    # A "stay still" RC command keeps it hovering.
                    tello.send_rc_control(0, 0, 0, 0)
                    last_command_time = time.time()

            except Exception as error:
                # For example: "out of range" or a command timeout. Keep going.
                print(f"Command failed: {error}")
                last_command_time = time.time()

        time.sleep(0.05)


# --- Main program ---
if __name__ == "__main__":
    # Load the gesture model BEFORE connecting to the drone
    # (the first run needs internet to download it).
    gesture_controller = GestureController()

    tello = Tello()
    tello.connect()
    print("Battery:", tello.get_battery(), "%")
    tello.streamon()

    video_thread = threading.Thread(target=video_read_thread, daemon=True)
    command_thread = threading.Thread(target=gesture_command_thread, daemon=True)
    video_thread.start()
    command_thread.start()

    seen_gesture = "NO_HAND"   # What the camera sees right now
    seen_since = time.time()   # When we first saw it

    try:
        while is_running:
            with frame_lock:
                frame = None if latest_frame is None else latest_frame.copy()

            if frame is not None:
                gesture, landmarks = gesture_controller.process_frame(frame)

                # Only accept a gesture after it has been steady for HOLD_TIME.
                # This ignores in-between shapes while your hand changes gesture.
                now = time.time()
                if gesture != seen_gesture:
                    seen_gesture = gesture
                    seen_since = now
                if now - seen_since >= HOLD_TIME:
                    active_gesture = seen_gesture

                if landmarks is not None:
                    gesture_controller.draw_landmarks(frame, landmarks)

                status = "FLYING" if in_flight else "ON GROUND"
                cv2.putText(frame, f"Seen: {seen_gesture}", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, f"Active: {active_gesture}  ({status})", (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                cv2.imshow("Tello Gesture Control", cv2.resize(frame, (960, 720)))

            # Press Q to land and quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                is_running = False

    finally:
        print("Stopping...")
        is_running = False
        command_thread.join(timeout=10)  # Let a running command finish first
        video_thread.join(timeout=2)
        try:
            if tello.is_flying:
                tello.land()
        except Exception as error:
            print(f"Landing failed: {error}")
        cv2.destroyAllWindows()
        tello.end()
        print("Program ended safely.")
