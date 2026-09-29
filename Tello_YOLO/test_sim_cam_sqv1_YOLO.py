"""
IDEAL Fall 2026 - Tello + YOLO Object Detection

Learning objectives:
- Run a pre-trained AI model (YOLO) on live drone video
- Use threads so the drone can fly while the video keeps updating
- Fly a square flight path with a loop

The drone takes off, flies a 1 m square, and lands. While it flies, every
video frame is sent to YOLO, which draws boxes and labels around the
objects it recognizes (people, chairs, bottles, laptops, ...).

The YOLO model file (yolov8n.pt, about 6 MB) is downloaded on the first run.
Run this once while connected to normal internet, NOT the Tello Wi-Fi, or
download it ahead of time (see the README).

Press Q in the video window to stop the flight and land.
"""

import threading
import time

import cv2
from djitellopy import Tello
from ultralytics import YOLO

# --- Settings you can change ---
MODEL_NAME = "yolov8n.pt"  # "n" = nano: the smallest and fastest YOLOv8 model
SIDE_LENGTH_CM = 100       # Length of each side of the square
NUMBER_OF_SIDES = 4

# --- Shared variables (used by more than one thread) ---
frame_lock = threading.Lock()
latest_frame = None   # Newest camera frame (BGR)
is_running = True     # Set to False to stop every thread

# --- YOLO setup ---
# Load the model BEFORE connecting to the drone. If the file is missing,
# Ultralytics downloads it, which needs internet.
print("Loading YOLO model...")
model = YOLO(MODEL_NAME)


def video_read_thread():
    """Keep copying the newest Tello frame into latest_frame."""
    global latest_frame
    frame_read = tello.get_frame_read()
    while is_running:
        frame = frame_read.frame
        if frame is not None:
            # djitellopy gives RGB frames, but YOLO and OpenCV expect BGR.
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            with frame_lock:
                latest_frame = frame
        time.sleep(0.01)


def command_thread_function():
    """Take off, fly a square, and land."""
    global is_running
    try:
        tello.takeoff()
        for side in range(NUMBER_OF_SIDES):
            if not is_running:  # Stop early if Q was pressed
                break
            print(f"Side {side + 1} of {NUMBER_OF_SIDES}")
            tello.move_forward(SIDE_LENGTH_CM)
            tello.rotate_counter_clockwise(360 // NUMBER_OF_SIDES)
    except Exception as error:
        print(f"An error occurred in the command thread: {error}")
    finally:
        # Always land, even if something went wrong above.
        try:
            if tello.is_flying:
                tello.land()
        except Exception as error:
            print(f"Landing failed: {error}")
        is_running = False  # Tell the main loop the flight is over


# --- Main program ---
if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    print("Battery:", tello.get_battery(), "%")
    tello.streamon()

    video_thread = threading.Thread(target=video_read_thread, daemon=True)
    command_thread = threading.Thread(target=command_thread_function)

    video_thread.start()
    command_thread.start()

    try:
        while is_running:
            with frame_lock:
                frame = None if latest_frame is None else latest_frame.copy()

            if frame is not None:
                # Detect and track objects in this frame.
                # persist=True lets YOLO remember objects between frames,
                # so each object keeps the same ID number while it is visible.
                results = model.track(frame, persist=True, verbose=False)

                # plot() returns a copy of the frame with boxes and labels drawn on it.
                annotated_frame = results[0].plot()
                annotated_frame = cv2.resize(annotated_frame, (960, 720))
                cv2.imshow("Tello YOLO", annotated_frame)

            # Press Q to stop the flight early (the drone lands after its current move)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Q pressed: landing after the current move...")
                is_running = False

    finally:
        is_running = False
        command_thread.join()  # Wait for the drone to land
        video_thread.join(timeout=1)
        cv2.destroyAllWindows()
        tello.end()
        print("Program ended safely.")
